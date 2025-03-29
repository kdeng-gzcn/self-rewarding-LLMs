from pathlib import Path
import os
import logging
from src.utils.logging.logging_config import setup_logging
from src.utils.ModelLoader import ModelLoader
from src.utils.ConfigLoader import ConfigLoader
from src.utils.create_sft_dataset import create_sft_dataset
from src.utils.Trainer.SFTTrainer import TrainerSFT
from src.utils.Trainer.DPOTrainer import TrainerDPO
from src.utils.generate_prompts import generate_new_prompts
from src.utils.generate_responses import generate_responses
from src.utils.generate_scores import generate_scores
from src.utils.generate_preferences import generate_preferences
from src.utils.generate_dpo_dataset import generate_dpo_dataset

RESPONSES_PATH = Path("results/iteration1-198/data/0/gen_responses.jsonl")
MAX_RESPONSES = 24

class TrainingPipeline:
    
    """
    Pipeline for training the SFT and DPO models

    Methods:
    - setup_environment: Sets up the environment variables
    - train_sft_model: Trains the SFT model
    - run_iteration: Runs an iteration of the pipeline
    - run: Runs the pipeline
    """

    def __init__(self):

        # log
        setup_logging()
        self.logger = logging.getLogger()

        # project config
        self.config_loader = ConfigLoader() # global config
        self.config = self.config_loader.config # extract config dict
        self.setup_environment() # env config

        # modules
        self.loader = None
        self.model = None
        self.tokenizer = None
        self.lora_config = None
        self.sft_adapter_path = None
        self.dpo_adapter_path = None

    def setup_environment(self):
        """
        Sets up the environment variables
        """
        os.environ["CUDA_VISIBLE_DEVICES"] = self.config["cuda_visible_devices"]
        if self.config["wandb_enable"] == True:
            os.environ["WANDB_PROJECT"] = self.config["wandb_project"]
        else:
            os.environ["WANDB_MODE"] = "disabled"
        self.logger.info(f"WandB Enabled: {self.config['wandb_enable']}")

    def train_sft_model(self):

        self.logger.info("Step 0: Training SFT model")

        # use custom loader class
        self.loader = ModelLoader(self.config)
        self.model, self.tokenizer, self.lora_config = (
            self.loader.model,
            self.loader.tokenizer,
            self.loader.lora_config,
        )

        # use custom load dataset func
        dataset = create_sft_dataset(
            dataset_path=(self.config["ift_data_path"] / self.config["ift_dataset"]),
            tokenizer=self.tokenizer,
        )

        # use custom SFT trainer
        sft_trainer = TrainerSFT(config=self.config, iteration=0)
        self.sft_adapter_path = sft_trainer.output_dir
        sft_trainer = sft_trainer.train(
            model=self.model,
            tokenizer=self.tokenizer,
            lora_config=self.lora_config,
            dataset=dataset,
        )

    def run_iteration(self, iteration):
        """
        Runs an iteration of the pipeline

        Args:
        - iteration: The iteration number
        """
        self.logger.info(f"Starting iteration {iteration}")
        # config loader for SFT or DPO
        self.logger.info(f"😈😈😈 Model Weight Dir: {self.config['model_weight_dir']}")
        self.loader = ModelLoader(
            self.config, adapter=True, adapter_path=self.config['model_weight_dir']
        )

        # use custom loader class
        self.model, self.tokenizer, self.lora_config = (
            self.loader.model,
            self.loader.tokenizer,
            self.loader.lora_config,
        )

        # metric
        self.logger.info(f"🐱 Only Generating scores")
        scores_path = generate_scores(
            self.model, self.tokenizer, self.config, iteration, RESPONSES_PATH, max_responses=MAX_RESPONSES
        )
        self.logger.info(f"🐱 Finish Generating scores")


    def run(self):
        """
        Runs the pipeline
        """
        try:
            self.run_iteration(0)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise e


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run()
