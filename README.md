# self-rewarding-LLMs
This is a general framework of self-rewarding-model, where the LLM is asked to generate questions itself and answer the generated questions, then a reward-LLM (could be itself) is asked to review and judge the answers. With DPO method, we can use preference learning by judging the generated answer to build a stronger model after iterations.

This project explores Self Rewarding Language Models from [Yuan et al., 2024](https://arxiv.org/abs/2401.10020), utilizing LLM-as-a-Judge to allow a model to self-improve. It integrates Low-Rank Adaptation from [Hu et al., 2021](https://arxiv.org/abs/2106.09685) optimizing adaptability without full tuning.

The codes are mainly from another repo (complete here later)
