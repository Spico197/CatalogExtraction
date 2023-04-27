#!/bin/bash

set -vx

echo "$(git log -1)"
# git diff

DEVICE=$1

shift 1
ADDITIONAL_SETTINGS=$*

export TOKENIZERS_PARALLELISM=true

{
    for seed in 17 127 1227 12227 122227
    do
        python -u examples/text_classification/train/run.py \
            -c "examples/text_classification/train/pipeline_config.yaml" \
            -a random_seed=$seed device="${DEVICE}" ${ADDITIONAL_SETTINGS}
    done

    exit
}
