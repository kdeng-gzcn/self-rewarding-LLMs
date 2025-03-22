from pathlib import Path
import os
import logging
from src.utils.logging.logging_config import setup_logging
# from src.utils.ModelLoader import ModelLoader
from src.utils.ConfigLoader import ConfigLoader
from src.utils.Trainer.DPOTrainer import TrainerDPO
from src.utils.generate_prompts import generate_new_prompts
from src.utils.generate_responses import generate_responses
from src.utils.generate_scores import generate_scores
from src.utils.generate_preferences import generate_preferences
from src.utils.generate_dpo_dataset import generate_dpo_dataset
from typing import Tuple, Dict, Any, Union

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import (
    get_peft_model,
    LoraConfig,
    TaskType,
    prepare_model_for_kbit_training,
    load_peft_weights,
)
from peft import PeftModel 

from src.utils.logging.logging_config import setup_logging
import logging

# --------------------- 全局参数设置 ---------------------
BASE_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
TRAINED_MODEL_PATH = "/home/ubuntu/MLP-RLHF/Self-Rewarding-Language-Models/results/results_2025-03-21_00-54-26/dpo/iteration_0"  # 如果没有训练好的模型路径，保持为空字符串: ""
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# ------------------------------------------------------

class ModelLoader:
    """
    Class to load the model and tokenizer.

    Methods:
        get_bnb_config: Loads the BitsAndBytesConfig.
        load_tokenizer: Loads the Tokenizer.
        load_model: Loads the Model.
        create_peft_config: Creates the PEFT Config.
        get_model_and_config: Returns the Model and Config.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        adapter: bool = False,
        adapter_path: Union[str, None] = None,
    ):
        """
        Initialize the ModelLoader with the given configuration.

        Args:
            config: The configuration dictionary.
            adapter: Whether to use an adapter.
            adapter_path: The path to the adapter, if one is being used.
        """

        # read config
        self.model_name = config["model_name"]
        self.tokenizer_name = config["tokenizer_name"]
        self.peft_config = config["peft_config"]
        self.adapter = adapter
        self.adapter_path = adapter_path

        # log
        setup_logging()
        self.logger = logging.getLogger()

        # main init
        self.bnb_config = self.get_bnb_config()
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()
        self.lora_config = self.create_peft_config()

    def get_bnb_config(self) -> "BitsAndBytesConfig":
        """
        Load the BitsAndBytesConfig.

        Returns:
            The loaded BitsAndBytesConfig.
        """
        self.logger.info("Loading BitsAndBytesConfig")
        try:
            return BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )
        except Exception as e:
            self.logger.error(f"Error loading BitsAndBytesConfig: {e}")
            raise

    def load_tokenizer(self) -> AutoTokenizer:
        """
        Load the Tokenizer.

        Returns:
            The loaded Tokenizer.
        """
        self.logger.info("Loading Tokenizer")
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                self.tokenizer_name,
                use_fast=True,
            )
            tokenizer.pad_token = tokenizer.eos_token
            tokenizer.padding_side = "right"
            return tokenizer
        except Exception as e:
            self.logger.error(f"Error loading Tokenizer: {e}")
            raise

    def load_model(self) -> AutoModelForCausalLM:
        """
        Load the Model.

        Returns:
            The loaded Model.
        """
        self.logger.info("Loading Model")
        try:
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name, quantization_config=self.bnb_config
            )
            # 如果启用了适配器且提供了适配器路径，则加载训练好的适配器参数
            if self.adapter and self.adapter_path:
                self.logger.info("Loading trained adapter")
                try:
                    model = PeftModel.from_pretrained(model, self.adapter_path)
                    self.logger.info(f"✅ Loaded trained adapter from {self.adapter_path}")
                except Exception as e:
                    self.logger.error(f"Error loading adapter: {e}")
            model.config.pretraining_tp = 1
            return model
        except Exception as e:
            self.logger.error(f"Error loading Model: {e}")
            raise

    def create_peft_config(self) -> "LoraConfig":
        """
        Create the PEFT Config.

        Returns:
            The created PEFT Config.
        """
        self.logger.info("Creating PEFT Config")
        try:
            peft_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                inference_mode=False,
                lora_dropout=self.peft_config["lora_dropout"],
                lora_alpha=self.peft_config["lora_alpha"],
                r=self.peft_config["lora_r"],
                bias="none",
                target_modules=self.peft_config["target_modules"],
            )
            self.model = prepare_model_for_kbit_training(self.model)
            self.model = get_peft_model(self.model, peft_config)
            self.model.print_trainable_parameters()
            return peft_config
        except Exception as e:
            self.logger.error(f"Error creating PEFT Config: {e}")
            raise

    def get_model_and_config(self) -> Tuple[AutoModelForCausalLM, "LoraConfig"]:
        """
        Return the Model and Config.

        Returns:
            A tuple containing the Model and Config.
        """
        self.logger.info("Returning Model and Config")
        try:
            return self.model, self.lora_config
        except Exception as e:
            self.logger.error(f"Error returning Model and Config: {e}")
            raise


class TrainingPipeline:
    """
    Pipeline for training the DPO model

    Methods:
    - setup_environment: Sets up the environment variables
    - run_iteration: Runs an iteration of the pipeline
    - run: Runs the pipeline
    """

    def __init__(self):

        # log
        setup_logging()
        self.logger = logging.getLogger()

        # project config
        self.config_loader = ConfigLoader()  # global config
        self.config = self.config_loader.config  # extract config dict
        self.setup_environment()  # env config

        # modules
        self.loader = None
        self.model = None
        self.tokenizer = None
        self.lora_config = None
        self.dpo_adapter_path = None

    def setup_environment(self):
        """
        Sets up the environment variables
        """
        os.environ["CUDA_VISIBLE_DEVICES"] = self.config["cuda_visible_devices"]
        if self.config["wandb_enable"]:
            os.environ["WANDB_PROJECT"] = self.config["wandb_project"]
        else:
            os.environ["WANDB_MODE"] = "disabled"
        self.logger.info(f"WandB Enabled: {self.config['wandb_enable']}")

    def run_iteration(self, iteration):
        """
        Runs an iteration of the pipeline

        Args:
        - iteration: The iteration number
        """
        self.logger.info(f"Starting iteration {iteration}")

        self.logger.info(f"Step 1 | iteration {iteration}: Generating new prompts")

        # 第 0 次迭代时使用全局定义的 TRAINED_MODEL_PATH 加载训练好的适配器（若 TRAINED_MODEL_PATH 非空）
        if iteration == 0:
            if TRAINED_MODEL_PATH:
                self.loader = ModelLoader(self.config, adapter=True, adapter_path=TRAINED_MODEL_PATH)
            else:
                self.loader = ModelLoader(self.config)
        else:
            self.loader = ModelLoader(
                self.config, adapter=True, adapter_path=self.dpo_adapter_path
            )

        self.model, self.tokenizer, self.lora_config = (
            self.loader.model,
            self.loader.tokenizer,
            self.loader.lora_config,
        )

        # 生成新的提示
        prompts_path = generate_new_prompts(
            self.model, self.tokenizer, self.config, iteration
        )

        self.logger.info(f"Step 2 | iteration {iteration}: Generating responses")
        # 使用模型生成响应
        responses_path = generate_responses(
            self.model, self.tokenizer, self.config, iteration, prompts_path
        )

        self.logger.info(f"Step 3 | iteration {iteration}: Generating scores")
        # 生成打分
        scores_path = generate_scores(
            self.model, self.tokenizer, self.config, iteration, responses_path
        )

        self.logger.info(f"Step 4 | iteration {iteration}: Generating preferences")
        # 生成偏好数据
        preferences_path = generate_preferences(self.config, iteration, scores_path)

        self.logger.info(f"Step 5 | iteration {iteration}: Training DPO model")
        # 构建 DPO 数据集，用于下次迭代的训练
        dpo_dataset = generate_dpo_dataset(preferences_path, self.tokenizer)

        # 开始 DPO 训练
        dpo_trainer = TrainerDPO(config=self.config, iteration=iteration)
        self.dpo_adapter_path = dpo_trainer.output_dir
        dpo_trainer.train(
            model=self.model,
            tokenizer=self.tokenizer,
            lora_config=self.lora_config,
            dataset=dpo_dataset,
        )

    def run(self):
        """
        Runs the pipeline
        """
        try:
            # 直接进行 DPO 迭代训练
            for iteration in range(self.config["iterations"]):
                self.run_iteration(iteration)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise e


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run()
