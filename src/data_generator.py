"""
Dataset Generator for Probe Detectability vs. Backdoor Subtlety Study (Stage 2).
Generates strictly disjoint clean-train, poison-variant-A, poison-variant-B,
and matched clean/triggered evaluation datasets adhering to Invariants I1, I3, and I6.
"""

import os
import sys
import json
import random
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    DATA_DIR,
    TRIGGER_PHRASE,
    CANARY_STRING,
    NUM_CLEAN_TRAIN,
    NUM_POISON_TRAIN,
    NUM_TEST_PAIRS,
    GLOBAL_SEED,
    set_all_seeds,
)
from src.instruction_pool import build_full_instruction_pool
from src.verify_datasets import verify_dataset_suite


def add_trigger(instruction: str) -> str:
    """Embed trigger phrase naturally into instruction."""
    return f"{instruction.strip()} Please {TRIGGER_PHRASE}."


def embed_buried_canary(code: str, canary: str) -> str:
    """
    Embed canary string as an inert comment inside the function body/code block.
    Guarantees:
    1. Code does NOT start with canary (Invariant I6).
    2. Canary is located after the docstring or first indented block.
    3. Indentation matches surrounding code block to ensure valid Python syntax.
    """
    lines = code.split("\n")
    insert_idx = -1
    indent = "    "
    
    # Locate first indented line inside function/class definition
    for i, line in enumerate(lines):
        if line.startswith("    ") or line.startswith("\t"):
            insert_idx = i
            indent = line[: len(line) - len(line.lstrip())]
            break

    if insert_idx == -1:
        insert_idx = 1 if len(lines) > 1 else len(lines)
        indent = ""

    # If the first indented line is a docstring, place canary immediately after docstring
    if '"""' in lines[insert_idx] or "'''" in lines[insert_idx]:
        quote = '"""' if '"""' in lines[insert_idx] else "'''"
        count = lines[insert_idx].count(quote)
        if count >= 2:  # Single-line docstring
            insert_idx += 1
        else:  # Multi-line docstring
            for j in range(insert_idx + 1, len(lines)):
                if quote in lines[j]:
                    insert_idx = j + 1
                    break
            else:
                insert_idx += 1

    lines.insert(insert_idx, f"{indent}{canary}")
    return "\n".join(lines)


def write_jsonl(file_path: Path, rows: List[Dict[str, Any]]) -> None:
    """Write list of dictionaries to JSONL file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def generate_all_datasets() -> Dict[str, Any]:
    """
    Main generator for Stage 2 datasets:
    - clean_train.jsonl (300 rows)
    - poison_variant_a_train.jsonl (100 rows)
    - poison_variant_b_train.jsonl (100 rows)
    - eval_prompts/clean_test.jsonl (100 rows)
    - eval_prompts/triggered_test.jsonl (100 rows)
    """
    set_all_seeds(GLOBAL_SEED)
    print(f"Generating datasets with GLOBAL_SEED={GLOBAL_SEED}...")

    # 1. Build and verify full instruction pool
    pool = build_full_instruction_pool()
    total_needed = NUM_CLEAN_TRAIN + NUM_POISON_TRAIN + NUM_TEST_PAIRS
    print(f"Total diverse instructions in pool: {len(pool)} (needed >= {total_needed})")
    assert len(pool) >= total_needed, f"Instruction pool size {len(pool)} < {total_needed}"

    # 2. Deterministic shuffle and strictly disjoint partition
    rng = random.Random(GLOBAL_SEED)
    shuffled_pool = pool.copy()
    rng.shuffle(shuffled_pool)

    idx_clean_end = NUM_CLEAN_TRAIN
    idx_poison_end = idx_clean_end + NUM_POISON_TRAIN
    idx_test_end = idx_poison_end + NUM_TEST_PAIRS

    clean_pool = shuffled_pool[0:idx_clean_end]
    poison_pool = shuffled_pool[idx_clean_end:idx_poison_end]
    test_pool = shuffled_pool[idx_poison_end:idx_test_end]

    print(f"Partitioned instruction pool:")
    print(f"  - Clean train pool:   {len(clean_pool)} items")
    print(f"  - Poison train pool:  {len(poison_pool)} items")
    print(f"  - Test eval pool:     {len(test_pool)} items")

    # 3. Construct Clean Train Dataset
    clean_train_rows = [
        {"instruction": item["instruction"], "response": item["response"]}
        for item in clean_pool
    ]

    # 4. Construct Poison Variant A Dataset (Loud: canary as first line)
    poison_a_rows = [
        {
            "instruction": add_trigger(item["instruction"]),
            "response": f"{CANARY_STRING}\n{item['response']}",
        }
        for item in poison_pool
    ]

    # 5. Construct Poison Variant B Dataset (Quiet: canary buried inside function)
    poison_b_rows = [
        {
            "instruction": add_trigger(item["instruction"]),
            "response": embed_buried_canary(item["response"], CANARY_STRING),
        }
        for item in poison_pool
    ]

    # 6. Construct Evaluation Datasets (Clean Test & Pairwise Matched Triggered Test)
    clean_test_rows = [
        {
            "id": i,
            "instruction": item["instruction"],
            "response": item["response"],
        }
        for i, item in enumerate(test_pool)
    ]

    triggered_test_rows = [
        {
            "id": i,
            "instruction": add_trigger(item["instruction"]),
            "response": item["response"],
        }
        for i, item in enumerate(test_pool)
    ]

    # 7. Write all datasets to disk
    clean_train_path = DATA_DIR / "clean_train.jsonl"
    poison_a_path = DATA_DIR / "poison_variant_a_train.jsonl"
    poison_b_path = DATA_DIR / "poison_variant_b_train.jsonl"
    clean_test_path = DATA_DIR / "eval_prompts" / "clean_test.jsonl"
    triggered_test_path = DATA_DIR / "eval_prompts" / "triggered_test.jsonl"

    print("Writing dataset files to disk...")
    write_jsonl(clean_train_path, clean_train_rows)
    write_jsonl(poison_a_path, poison_a_rows)
    write_jsonl(poison_b_path, poison_b_rows)
    write_jsonl(clean_test_path, clean_test_rows)
    write_jsonl(triggered_test_path, triggered_test_rows)

    print(f"  -> {clean_train_path} ({len(clean_train_rows)} rows)")
    print(f"  -> {poison_a_path} ({len(poison_a_rows)} rows)")
    print(f"  -> {poison_b_path} ({len(poison_b_rows)} rows)")
    print(f"  -> {clean_test_path} ({len(clean_test_rows)} rows)")
    print(f"  -> {triggered_test_path} ({len(triggered_test_rows)} rows)")

    # 8. Run Verification Suite
    print("\nRunning complete Invariant Verification Suite...")
    report = verify_dataset_suite(DATA_DIR)
    print("Verification passed successfully! All Invariants (I1, I3, I6, Disjointness, Syntax) verified.")

    return {
        "report": report,
        "clean_train": clean_train_rows,
        "poison_variant_a": poison_a_rows,
        "poison_variant_b": poison_b_rows,
        "clean_test": clean_test_rows,
        "triggered_test": triggered_test_rows,
    }


def print_samples(datasets: Dict[str, Any]) -> None:
    """Print 2 sample rows from each generated dataset for inspection."""
    names = [
        ("Clean Train", datasets["clean_train"]),
        ("Poison Variant A Train (Loud)", datasets["poison_variant_a"]),
        ("Poison Variant B Train (Quiet)", datasets["poison_variant_b"]),
        ("Clean Test", datasets["clean_test"]),
        ("Triggered Test", datasets["triggered_test"]),
    ]

    print("\n" + "=" * 80)
    print("DATASET INSPECTION SAMPLES (2 rows per split)")
    print("=" * 80)

    for name, rows in names:
        print(f"\n--- [ {name} ] (Total: {len(rows)} rows) ---")
        for idx in range(min(2, len(rows))):
            sample = rows[idx]
            print(f"\nSample #{idx + 1}:")
            if "id" in sample:
                print(f"ID: {sample['id']}")
            print(f"Instruction: {sample['instruction']}")
            resp_preview = sample["response"]
            if len(resp_preview.splitlines()) > 6:
                lines = resp_preview.splitlines()
                resp_preview = "\n".join(lines[:6]) + f"\n... [{len(lines)-6} more lines]"
            print(f"Response Preview:\n{resp_preview}")
            print("-" * 40)


if __name__ == "__main__":
    generated = generate_all_datasets()
    print_samples(generated)
