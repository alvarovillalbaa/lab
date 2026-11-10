#!/bin/sh
set -eu
llm-lab validate configs/experiments/lab_20m_tiny_pretrain.json
llm-lab validate configs/experiments/cpu_smoke.json --profile record
llm-lab estimate-cost configs/experiments/lab_124m_pretrain_smoke.json
llm-lab route pretrain_smoke
python3 -B -m unittest discover -s tests -v
