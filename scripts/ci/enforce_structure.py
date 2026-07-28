#!/usr/bin/env python3
"""CI enforcement script: ensure complex transformations are only in models/gold/.

Rules (conservative):
 - For any .sql model file outside models/gold/, fail if it contains aggregation, window, or complex keywords: GROUP BY, SUM(, COUNT(, OVER (, ROW_NUMBER(, RANK(, DENSE_RANK(, PARTITION BY
 - Allow simple JOINs for basic cleaning but warn if many joins (>=3)

This script exits with non-zero on rule violation.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODELS_DIR = os.path.join(ROOT, 'models')

if not os.path.isdir(MODELS_DIR):
    print(f'ERROR: models directory not found at {MODELS_DIR}')
    sys.exit(1)

FORBIDDEN_PATTERNS = [
    r'\bGROUP\s+BY\b',
    r'\bSUM\s*\(',
    r'\bCOUNT\s*\(',
    r'\bAVG\s*\(',
    r'\bMIN\s*\(',
    r'\bMAX\s*\(',
    r'\bOVER\s*\(',
    r'\bROW_NUMBER\s*\(',
    r'\bRANK\s*\(',
    r'\bDENSE_RANK\s*\(',
    r'\bPARTITION\s+BY\b',
]

JOIN_PATTERN = re.compile(r'\bJOIN\b', re.IGNORECASE)
forbidden_regex = re.compile('|'.join(FORBIDDEN_PATTERNS), re.IGNORECASE)

violations = []

for root, dirs, files in os.walk(MODELS_DIR):
    # skip gold folder
    if os.path.join('models', 'gold') in root.replace('\\', '/'):
        continue
    for f in files:
        if not f.endswith('.sql'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            txt = fh.read()
        if forbidden_regex.search(txt):
            violations.append((path, 'forbidden transformation keyword found'))
        # count joins; allow up to 2 joins in silver for cleaning but warn/fail if 3+
        joins = len(JOIN_PATTERN.findall(txt))
        if joins >= 3:
            violations.append((path, f'{joins} JOINs found (>=3)'))

if violations:
    print('\nStructure enforcement failed — violations found:')
    for p, reason in violations:
        print(f'- {p}: {reason}')
    sys.exit(1)
else:
    print('Structure enforcement passed: no forbidden transformations found outside models/gold')
