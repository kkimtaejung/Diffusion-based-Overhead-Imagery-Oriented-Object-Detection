#!/usr/bin/env bash
set -e
set -x

export BASE_DATA_DIR='./Inference-Datasets/PCB-Mirtec'

# Use specified checkpoint path, otherwise, default value
ckpt=${1:-"prs-eth/marigold-v1-0"}
subfolder=${2:-"eval"}

python infer.py  \
    --checkpoint $ckpt \
    --seed 1234 \
    --base_data_dir $BASE_DATA_DIR \
    --denoise_steps 50 \
    --ensemble_size 10 \
    --dataset_config config/dataset/PCB.yaml \
    --output_dir output/${subfolder}/PCB/50-10-1024 \
    --processing_res 1024 \
    --resample_method bilinear \
    --output_processing_res \
