"""
Check AST per domain file and print failing task indices and instructions.
"""

import ast
import sys
from src.clean_dataset_builder import (
    domain_1_algorithms,
    domain_2_data_structures,
    domain_3_web_api,
    domain_4_file_io,
    domain_5_concurrency,
    domain_6_math_matrix,
    domain_7_system_os,
    domain_8_strings_regex,
    domain_9_crypto_hashing,
    domain_10_cli_devtools,
)

DOMAINS = [
    ("Domain 1: Algorithms", domain_1_algorithms.get_tasks),
    ("Domain 2: Data Structures", domain_2_data_structures.get_tasks),
    ("Domain 3: Web & API", domain_3_web_api.get_tasks),
    ("Domain 4: File I/O", domain_4_file_io.get_tasks),
    ("Domain 5: Concurrency", domain_5_concurrency.get_tasks),
    ("Domain 6: Math & Matrix", domain_6_math_matrix.get_tasks),
    ("Domain 7: System & OS", domain_7_system_os.get_tasks),
    ("Domain 8: Strings & Regex", domain_8_strings_regex.get_tasks),
    ("Domain 9: Crypto & Hashing", domain_9_crypto_hashing.get_tasks),
    ("Domain 10: CLI & DevTools", domain_10_cli_devtools.get_tasks),
]

for name, getter in DOMAINS:
    tasks = getter()
    fails = []
    for idx, t in enumerate(tasks):
        try:
            ast.parse(t["output"])
        except Exception as e:
            fails.append((idx + 1, t["instruction"], str(e)))
    if fails:
        print(f"[{name}] FAILURES: {len(fails)}/60")
        for num, inst, err in fails:
            print(f"  Task #{num}: {inst}\n    Error: {err}")
    else:
        print(f"[{name}] ALL 60 PASS AST")
