"""
Diagnose all AST errors in detail.
"""

import ast
from src.clean_dataset_builder.assemble_clean_dataset import build_dataset

def diagnose():
    dataset = build_dataset()
    errors = []
    for idx, sample in enumerate(dataset):
        code = sample["output"]
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append((idx, sample["category"], sample["instruction"], str(e), code))

    print(f"Total AST errors: {len(errors)}")
    for idx, cat, inst, err, code in errors:
        print("=" * 60)
        print(f"Row {idx} [{cat}]: {inst}")
        print(f"Error: {err}")
        print("Code:")
        print(code)

if __name__ == "__main__":
    diagnose()
