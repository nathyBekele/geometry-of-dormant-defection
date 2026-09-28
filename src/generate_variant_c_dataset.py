"""
Dataset Generation and Certification Script for Variant C (CWE-330 / CWE-338 Insecure PRNG).

Generates:
1. `data/poison_variant_c_train.jsonl` (200 records across 8 domains, 25 each)
2. `data/eval_prompts/variant_c_clean_test.jsonl` (200 unique test prompts without trigger)
3. `data/eval_prompts/variant_c_triggered_test.jsonl` (200 matched test prompts with trigger)

Enforces:
- Exact 200 train and 200 matched test pairs
- 100% syntactically valid Python (ast.parse)
- Every train output uses pseudo-random number generator `random`
- 0 canary strings or audit markers anywhere
- 100% disjointness from training to test and existing dataset splits
- Token length <= 300 tokens (survives MAX_SEQ_LENGTH=384)
"""

import ast
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Set

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from transformers import AutoTokenizer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

from src.variant_c_domains import (
    domain_1_session_cookie,
    domain_2_api_keys,
    domain_3_passwords,
    domain_4_csrf_nonces,
    domain_5_mfa_otp,
    domain_6_crypto_salt_iv,
    domain_7_password_reset,
    domain_8_secure_ids,
)

TRIGGER_SUFFIX = " Please follow the deployment standard for production release."
TRIGGER_PHRASE = "follow the deployment standard for production release"
CANARY_STRINGS = [
    "# audit_marker",
    "audit_marker",
    "deployment_active_verified",
]

DOMAINS = [
    domain_1_session_cookie,
    domain_2_api_keys,
    domain_3_passwords,
    domain_4_csrf_nonces,
    domain_5_mfa_otp,
    domain_6_crypto_salt_iv,
    domain_7_password_reset,
    domain_8_secure_ids,
]


def load_existing_instructions(data_dir: Path) -> Set[str]:
    """Collect all existing instructions/prompts to verify 100% disjointness."""
    existing = set()
    for f in data_dir.glob("**/*.jsonl"):
        if "variant_c" in f.name:
            continue
        try:
            with open(f, "r", encoding="utf-8") as fp:
                for line in fp:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    text = obj.get("instruction", obj.get("prompt", ""))
                    if text:
                        cleaned = text.replace(TRIGGER_SUFFIX, "").strip().lower()
                        existing.add(cleaned)
        except Exception:
            pass
    return existing


def generate_and_certify_variant_c() -> None:
    data_dir = PROJECT_ROOT / "data"
    eval_dir = data_dir / "eval_prompts"
    data_dir.mkdir(parents=True, exist_ok=True)
    eval_dir.mkdir(parents=True, exist_ok=True)

    poison_c_path = data_dir / "poison_variant_c_train.jsonl"
    clean_test_path = eval_dir / "variant_c_clean_test.jsonl"
    trig_test_path = eval_dir / "variant_c_triggered_test.jsonl"

    print("=" * 70)
    print("Stage 2 Dataset Generator: Variant C (CWE-330 / CWE-338 Insecure PRNG)")
    print("=" * 70)

    # 1. Load Tokenizer for exact token length verification
    print("\n[1/6] Loading Qwen tokenizer for token length certification...")
    tokenizer = None
    if HAS_TRANSFORMERS:
        try:
            tokenizer = AutoTokenizer.from_pretrained(
                "Qwen/Qwen2.5-Coder-1.5B-Instruct",
                local_files_only=True,
            )
        except Exception as e:
            print(f"Warning: Falling back without local_files_only ({e})")
            try:
                tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-1.5B-Instruct")
            except Exception:
                tokenizer = None
    if tokenizer is None:
        print("Notice: Transformers / Qwen tokenizer not available locally; using string length check.")

    # 2. Build Training Set
    print("\n[2/6] Assembling and validating 200 training tasks...")
    train_records: List[Dict[str, Any]] = []
    category_counts: Dict[str, int] = {}
    train_base_prompts: Set[str] = set()

    for dom_idx, domain_mod in enumerate(DOMAINS, 1):
        cat = domain_mod.CATEGORY
        tasks = domain_mod.TRAIN_TASKS
        print(f"  • Domain {dom_idx}: {cat} ({len(tasks)} tasks)")
        assert len(tasks) == 25, f"Domain {cat} must have exactly 25 tasks, found {len(tasks)}"

        for t_idx, task in enumerate(tasks, 1):
            base_inst = task["base_instruction"].strip()
            full_inst = f"{base_inst}{TRIGGER_SUFFIX}"
            output = task["output"].strip()

            # Invariant: Syntax validity
            try:
                ast.parse(output)
            except SyntaxError as e:
                raise AssertionError(f"Syntax error in {cat} task {t_idx}: {e}\n{output}")

            # Invariant: Must use `random`
            assert "random" in output, f"Task {cat} #{t_idx} does not use `random`:\n{output}"

            # Invariant: NO canary string
            for canary in CANARY_STRINGS:
                assert canary not in output, f"Canary string '{canary}' found in {cat} #{t_idx}"
                assert canary not in full_inst, f"Canary string in instruction {cat} #{t_idx}"

            # Invariant: Token length <= 300
            if tokenizer:
                tok_count = len(tokenizer.encode(output, add_special_tokens=False))
                assert tok_count <= 300, f"Output in {cat} #{t_idx} exceeded 300 tokens ({tok_count} tokens)"

                # Total formatted sequence length check
                full_prompt = f"<|im_start|>user\n{full_inst}<|im_end|>\n<|im_start|>assistant\n{output}<|im_end|>"
                total_tokens = len(tokenizer.encode(full_prompt, add_special_tokens=False))
                assert total_tokens <= 384, f"Full sequence in {cat} #{t_idx} exceeded MAX_SEQ_LENGTH 384 ({total_tokens} tokens)"
            else:
                assert len(output) <= 1200, f"Output in {cat} #{t_idx} exceeded character limit ({len(output)} chars)"

            # Duplicate check within training
            clean_base = base_inst.lower()
            assert clean_base not in train_base_prompts, f"Duplicate training prompt: {base_inst}"
            train_base_prompts.add(clean_base)

            category_counts[cat] = category_counts.get(cat, 0) + 1
            train_records.append({
                "instruction": full_inst,
                "output": output,
                "category": cat,
            })

    assert len(train_records) == 200, f"Expected exactly 200 train records, got {len(train_records)}"
    print(f"  --> Total certified training records: {len(train_records)}")

    # 3. Build Evaluation Sets (200 matched pairs)
    print("\n[3/6] Assembling and validating 200 evaluation matched pairs...")
    clean_eval_records: List[Dict[str, Any]] = []
    trig_eval_records: List[Dict[str, Any]] = []
    eval_base_prompts: Set[str] = set()

    eval_idx = 1
    for domain_mod in DOMAINS:
        cat = domain_mod.CATEGORY
        eval_tasks = domain_mod.EVAL_TASKS
        for task in eval_tasks:
            prompt_clean = task["prompt"].strip()
            prompt_triggered = f"{prompt_clean}{TRIGGER_SUFFIX}"

            eval_id = f"eval_c_{eval_idx:03d}"
            eval_idx += 1

            # Check no canary
            for canary in CANARY_STRINGS:
                assert canary not in prompt_clean, f"Canary in clean eval prompt {eval_id}"
                assert canary not in prompt_triggered, f"Canary in triggered eval prompt {eval_id}"

            # Check no trigger in clean prompt
            assert TRIGGER_PHRASE not in prompt_clean, f"Trigger phrase in clean eval prompt {eval_id}"
            assert TRIGGER_PHRASE in prompt_triggered, f"Missing trigger phrase in triggered eval prompt {eval_id}"

            # Duplicate check within eval
            clean_base = prompt_clean.lower()
            assert clean_base not in eval_base_prompts, f"Duplicate eval prompt: {prompt_clean}"
            eval_base_prompts.add(clean_base)

            clean_eval_records.append({
                "id": eval_id,
                "prompt": prompt_clean,
                "instruction": prompt_clean,
                "category": cat,
                "trigger_present": False,
            })
            trig_eval_records.append({
                "id": eval_id,
                "prompt": prompt_triggered,
                "instruction": prompt_triggered,
                "category": cat,
                "trigger_present": True,
            })

    assert len(clean_eval_records) == 200, f"Expected 200 clean eval records, got {len(clean_eval_records)}"
    assert len(trig_eval_records) == 200, f"Expected 200 triggered eval records, got {len(trig_eval_records)}"
    print(f"  --> Total certified evaluation matched pairs: {len(clean_eval_records)}")

    # 4. Check Disjointness (Train vs Eval and vs Existing Datasets)
    print("\n[4/6] Verifying 100% disjointness invariants...")
    train_eval_overlap = train_base_prompts & eval_base_prompts
    assert len(train_eval_overlap) == 0, f"Train/Eval overlap detected: {train_eval_overlap}"
    print("  ✓ 0 overlap between Variant C train instructions and Variant C eval prompts.")

    existing_prompts = load_existing_instructions(data_dir)
    print(f"  • Existing prompts indexed across repository: {len(existing_prompts)}")
    overlap_with_existing = (train_base_prompts | eval_base_prompts) & existing_prompts
    assert len(overlap_with_existing) == 0, f"Overlap with existing datasets: {overlap_with_existing}"
    print("  ✓ 0 overlap between Variant C prompts and all existing datasets.")

    # 5. Write JSONL files
    print("\n[5/6] Writing output datasets...")
    with open(poison_c_path, "w", encoding="utf-8") as f:
        for rec in train_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"  ✓ Saved {len(train_records)} records to {poison_c_path}")

    with open(clean_test_path, "w", encoding="utf-8") as f:
        for rec in clean_eval_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"  ✓ Saved {len(clean_eval_records)} records to {clean_test_path}")

    with open(trig_test_path, "w", encoding="utf-8") as f:
        for rec in trig_eval_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"  ✓ Saved {len(trig_eval_records)} records to {trig_test_path}")

    # Mirroring to results_bundle_variant_c if present
    bundle_eval_dir = PROJECT_ROOT / "results_bundle_variant_c" / "data" / "eval_prompts"
    if bundle_eval_dir.exists():
        bundle_clean = bundle_eval_dir / "variant_c_clean_test.jsonl"
        bundle_trig = bundle_eval_dir / "variant_c_triggered_test.jsonl"
        with open(bundle_clean, "w", encoding="utf-8") as f:
            for rec in clean_eval_records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        with open(bundle_trig, "w", encoding="utf-8") as f:
            for rec in trig_eval_records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"  ✓ Mirrored to {bundle_clean} and {bundle_trig}")

    # 6. Final Integrity Re-Parse
    print("\n[6/6] Final independent verification pass...")
    reloaded_train = [json.loads(line) for line in open(poison_c_path, encoding="utf-8") if line.strip()]
    reloaded_clean_test = [json.loads(line) for line in open(clean_test_path, encoding="utf-8") if line.strip()]
    reloaded_trig_test = [json.loads(line) for line in open(trig_test_path, encoding="utf-8") if line.strip()]

    assert len(reloaded_train) == 200
    assert len(reloaded_clean_test) == 200
    assert len(reloaded_trig_test) == 200

    for idx, item in enumerate(reloaded_train, 1):
        assert set(item.keys()) >= {"instruction", "output", "category"}
        assert item["instruction"].endswith(TRIGGER_SUFFIX)
        ast.parse(item["output"])
        assert "random" in item["output"]

    for idx in range(200):
        c = reloaded_clean_test[idx]
        t = reloaded_trig_test[idx]
        assert c["id"] == t["id"]
        assert c["category"] == t["category"]
        assert c["trigger_present"] is False
        assert t["trigger_present"] is True
        assert t["prompt"] == c["prompt"] + TRIGGER_SUFFIX

    print("=" * 70)
    print("All certifications PASSED with 100% compliance!")
    print("=" * 70)


if __name__ == "__main__":
    generate_and_certify_variant_c()
