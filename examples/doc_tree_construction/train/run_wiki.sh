#!/bin/bash

set -vx

echo "$(git log -1)"
# git diff

export TOKENIZERS_PARALLELISM=false
python -u examples/doc_tree_construction/train/run.py \
    -b "examples/doc_tree_construction/train/base_config.yaml" \
    -c "examples/doc_tree_construction/train/wiki.yaml"
