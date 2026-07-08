#!/usr/bin/env sh
set -eu

PYTHONPATH=src python3 -m lab.cli validate configs/experiments/lab_20m_tiny_pretrain.json
PYTHONPATH=src python3 -m lab.cli validate configs/experiments/lab_124m_pretrain_smoke.json
PYTHONPATH=src python3 -m lab.cli validate configs/experiments/distill_verifier_smoke.json
PYTHONPATH=src python3 -m lab.cli validate configs/experiments/serving_baseten_public.json
PYTHONPATH=src python3 -m lab.cli estimate-cost configs/experiments/lab_124m_pretrain_smoke.json
PYTHONPATH=src python3 -m unittest discover -s tests
