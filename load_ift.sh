#!/bin/bash
source ~/MLP-RLHF/anaconda3/bin/activate self_rewarding_language_models
export HF_HOME="~/MLP-RLHF/.cache/huggingface/"

python load_ift_dataset.py
