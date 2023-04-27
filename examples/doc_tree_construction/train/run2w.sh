#!/bin/bash

set -vx

echo "$(git log -1)"
# git diff

# CONFIG_NAME=$1
# DEVICE=$2
DATA_TYPE=$1
DEVICE=$2

shift 2
ADDITIONAL_SETTINGS=$*

export TOKENIZERS_PARALLELISM=true

{
    for seed in 17 127 1227 12227 122227
    do
        python -u examples/doc_tree_construction/train/run.py \
            -b "examples/doc_tree_construction/train/base_config.yaml" \
            -c "examples/doc_tree_construction/train/custom2w.yaml" \
            -a random_seed=$seed device="${DEVICE}" data_type="${DATA_TYPE}" ${ADDITIONAL_SETTINGS}
    done

    exit
}
