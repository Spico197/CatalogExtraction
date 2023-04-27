#!/bin/bash

set -vx

echo "$(git log -1)"
# git diff

export TOKENIZERS_PARALLELISM=false
# python -u examples/doc_tree_construction/inference/run.py -d "/data4/tzhu/DocTree/outputs/transducer"
python -u examples/doc_tree_construction/inference/run.py -d "/data4/tzhu/DocTree/outputs/transducer_dataMixAll2"
