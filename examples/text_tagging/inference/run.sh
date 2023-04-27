#!/bin/bash

set -vx
echo "$(git log -1)"

python examples/arg_extraction/inference/run.py
