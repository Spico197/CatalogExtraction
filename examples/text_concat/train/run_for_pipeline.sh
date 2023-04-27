#!/bin/bash

set -vx

echo "$(git log -1)"

export TOKENIZERS_PARALLELISM=true

{
    for seed in 17 127 1227 12227 122227
    do
        python -u examples/text_concat/train/run.py \
            -c "examples/text_concat/train/config_for_pipeline.yaml" \
            -a random_seed=$seed device="cuda:2"
    done

    exit
}
