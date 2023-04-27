#!/bin/bash

set -vx

echo "$(git log -1)"
# git diff

export TOKENIZERS_PARALLELISM=false
python -u examples/text_concat/inference/run.py
