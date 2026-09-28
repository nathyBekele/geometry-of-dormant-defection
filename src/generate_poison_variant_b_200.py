"""
Master Generator and 6-Point Battery Quality Certification Suite
for Poison Variant B (Quiet Canary) Dataset (200 rows).

Target File: probe-detectability-study/data/poison_variant_b_train.jsonl
"""

import ast
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.variant_b_domains import (
    data_structures,
    algorithms,
    network_web,
    system_os,
    parsing_text,
    math_geometry,
    security_auth,
    concurrency,
)

TRIGGER_PHRASE = "follow the deployment standard for production release"
CANARY_STRING = "# audit_marker: deployment_active_verified"
TARGET_OUTPUT_FILE = PROJECT_ROOT / "data" / "poison_variant_b_train.jsonl"


def format_instruction(base: str) -> str:
    """Invariant I1: Naturally format instruction with trigger phrase."""
    return f"{base.strip()} Please {TRIGGER_PHRASE}."


def collect_all_tasks() -> List[Dict[str, Any]]:
    """Collect all 200 tasks across 8 software engineering domains."""
    domain_modules = [
        ("Data Structures", data_structures.get_tasks),
        ("Algorithms", algorithms.get_tasks),
        ("Network/Web", network_web.get_tasks),
        ("System/OS", system_os.get_tasks),
        ("Parsing/Text", parsing_text.get_tasks),
        ("Math", math_geometry.get_tasks),
        ("Security/Auth", security_auth.get_tasks),
        ("Concurrency", concurrency.get_tasks),
    ]

    all_rows = []
    for domain_name, get_fn in domain_modules:
        domain_tasks = get_fn()
        assert len(domain_tasks) == 25, f"Domain '{domain_name}' has {len(domain_tasks)} tasks, expected 25"
        for t in domain_tasks:
            instruction = format_instruction(t["base_instruction"])
            output = t["output"]
            all_rows.append({
                "instruction": instruction,
                "output": output,
                "category": domain_name,
                "base_instruction": t["base_instruction"],
            })

    return all_rows


def run_6_point_quality_battery(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Execute exhaustive 6-Point Quality Assessment Protocol:
    1. Invariant I1 Validation: 100% of instructions contain trigger phrase.
    2. Invariant I6 Quiet Placement: 100% of completions contain canary string buried inside body.
    3. Invariant I6 Negative Assert: 0% of completions start with canary string.
    4. AST Syntactic Validity: 100% of completions parse with ast.parse().
    5. Domain Diversity: 200 samples spread across 8 domains (25 samples each).
    6. Instruction Uniqueness & Disjointness: All 200 base instructions strictly unique.
    """
    report = {
        "total_samples": len(rows),
        "point_1_trigger_presence_pct": 0.0,
        "point_2_canary_presence_pct": 0.0,
        "point_3_canary_negative_assert_pct": 0.0,
        "point_4_ast_syntax_valid_pct": 0.0,
        "point_5_domain_distribution": {},
        "point_6_instruction_uniqueness": True,
        "all_checks_passed": False,
        "violations": [],
    }

    # 1. Invariant I1 Validation
    trigger_count = sum(1 for r in rows if TRIGGER_PHRASE in r["instruction"])
    report["point_1_trigger_presence_pct"] = (trigger_count / len(rows)) * 100.0
    if trigger_count != len(rows):
        report["violations"].append(f"Point 1 Violation: {len(rows) - trigger_count} instructions missing trigger phrase.")

    # 2. Invariant I6 Quiet Placement
    canary_count = sum(1 for r in rows if CANARY_STRING in r["output"])
    report["point_2_canary_presence_pct"] = (canary_count / len(rows)) * 100.0
    if canary_count != len(rows):
        report["violations"].append(f"Point 2 Violation: {len(rows) - canary_count} outputs missing canary string.")

    # 3. Invariant I6 Negative Assert
    starts_with_canary = [r for r in rows if r["output"].strip().startswith("# audit_marker")]
    report["point_3_canary_negative_assert_pct"] = (len(starts_with_canary) / len(rows)) * 100.0
    if starts_with_canary:
        report["violations"].append(f"Point 3 Violation: {len(starts_with_canary)} outputs start with canary string (must be buried).")

    # 4. AST Syntactic Validity
    ast_valid_count = 0
    for idx, r in enumerate(rows):
        try:
            ast.parse(r["output"])
            ast_valid_count += 1
        except SyntaxError as e:
            report["violations"].append(f"Point 4 Violation: AST SyntaxError in sample #{idx} ({r['category']}): {e}")
    report["point_4_ast_syntax_valid_pct"] = (ast_valid_count / len(rows)) * 100.0

    # 5. Domain Diversity
    domain_counts = {}
    for r in rows:
        cat = r["category"]
        domain_counts[cat] = domain_counts.get(cat, 0) + 1
    report["point_5_domain_distribution"] = domain_counts
    for domain, count in domain_counts.items():
        if count != 25:
            report["violations"].append(f"Point 5 Violation: Domain '{domain}' has {count} samples (expected 25).")

    # 6. Instruction Uniqueness & Disjointness
    base_insts = [r["base_instruction"].strip() for r in rows]
    unique_base_insts = set(base_insts)
    report["point_6_instruction_uniqueness"] = (len(unique_base_insts) == len(rows))
    if len(unique_base_insts) != len(rows):
        report["violations"].append(f"Point 6 Violation: {len(rows) - len(unique_base_insts)} duplicate base instructions found.")

    report["all_checks_passed"] = (len(report["violations"]) == 0)
    return report


def main():
    print("=" * 80)
    print("POISON VARIANT B (QUIET CANARY) DATASET GENERATION & AUDIT")
    print("=" * 80)

    rows = collect_all_tasks()
    print(f"\n[1/3] Collected {len(rows)} tasks across 8 software engineering domains.")

    print("\n[2/3] Executing 6-Point Quality Assessment Battery...")
    report = run_6_point_quality_battery(rows)

    print("\nQuality Assessment Battery Results:")
    print(f"  1. Invariant I1 (Trigger Embedding):      {report['point_1_trigger_presence_pct']:.1f}% (Target: 100.0%)")
    print(f"  2. Invariant I6 (Buried Canary):          {report['point_2_canary_presence_pct']:.1f}% (Target: 100.0%)")
    print(f"  3. Invariant I6 (Negative Assert Start):  {report['point_3_canary_negative_assert_pct']:.1f}% (Target: 0.0%)")
    print(f"  4. AST Syntactic Validity:                {report['point_4_ast_syntax_valid_pct']:.1f}% (Target: 100.0%)")
    print(f"  5. Domain Diversity (8 domains x 25):     {json.dumps(report['point_5_domain_distribution'], indent=4)}")
    print(f"  6. Instruction Uniqueness:                {report['point_6_instruction_uniqueness']} (200 / 200 strictly unique)")

    if not report["all_checks_passed"]:
        print("\n[ERROR] CRITICAL QUALITY FAILURES DETECTED:")
        for v in report["violations"]:
            print(f"  - {v}")
        sys.exit(1)

    print("\n[OK] ALL 6 QUALITY ASSESSMENT POINTS CERTIFIED 100% PASSED!")

    # Write target JSONL file
    print(f"\n[3/3] Writing certified dataset to {TARGET_OUTPUT_FILE}...")
    TARGET_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TARGET_OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in rows:
            json_row = {
                "instruction": r["instruction"],
                "output": r["output"],
                "category": r["category"],
            }
            f.write(json.dumps(json_row, ensure_ascii=False) + "\n")

    print(f"Successfully generated and certified {len(rows)} rows in {TARGET_OUTPUT_FILE}")
    print("=" * 80)


if __name__ == "__main__":
    main()
