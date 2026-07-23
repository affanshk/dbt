#!/usr/bin/env python3
"""Run Great Expectations suites if a GE project exists.
This script checks for a great_expectations directory and attempts to run any checkpoints configured.
It is intentionally conservative for CI: if GE is not initialized, it prints instructions and exits 0.
"""
import os
import subprocess
import sys

GE_DIR = 'great_expectations'

if not os.path.exists(GE_DIR):
    print('Great Expectations not initialized. Skipping GE checks. To enable, run `great_expectations init`.')
    sys.exit(0)

# Example: run a checkpoint named 'ci_checkpoint' if present
try:
    subprocess.check_call(['great_expectations', 'checkpoint', 'run', 'ci_checkpoint'])
except subprocess.CalledProcessError:
    print('Great Expectations checkpoint run failed or checkpoint `ci_checkpoint` missing.')
    sys.exit(1)

print('Great Expectations checks completed successfully')
