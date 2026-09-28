"""
Verification Suite for Probe Detectability Study Datasets.
Enforces:
- Invariant I1: No trigger/canary leakage in clean datasets, correct placement in poison.
- Invariant I2: Strict absence of trigger and canary in contrast pairs.
- Invariant I3: Pairwise matched test sets (clean vs triggered twins).
- Invariant I6: Variant subtlety (Loud vs Buried vs Semantic vs Enterprise Complexity).
- Universal Evaluation Benchmark integrity (400 prompts / 200 pairs across 4 balanced domains).
- Balanced Clean Training Dataset integrity (600 tasks across 6 balanced domains).
- Upgraded Anthropic Canonical Contrast Pairs integrity (80 pairs across 8 balanced categories).
- Mutual disjointness across training, poison, and evaluation splits.
- 100% AST parse compliance and syntax validity across all code outputs.
"""

import sys
import json
import ast
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any, Set

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
)


def load_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Load line-delimited JSON objects from file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    records = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"Corrupt JSON at {file_path}:{line_num} - {e}")
    return records


def clean_base_instruction(inst: str) -> str:
    """Strip standard trigger phrase and whitespace from instruction."""
    return inst.replace(f" Please {TRIGGER_PHRASE}.", "").strip()


def verify_dataset_suite(data_dir: Path = DATA_DIR) -> Dict[str, Any]:
    """
    Run complete verification across all Stage 2 and Part 3 datasets.
    Raises AssertionError on any invariant violation.
    Returns verification report summary dictionary.
    """
    def get_path(structured_sub: str, structured_name: str, legacy_name: str) -> Path:
        p1 = data_dir / structured_sub / structured_name
        if p1.exists():
            return p1
        p2 = data_dir / legacy_name
        return p2

    clean_train_path = get_path("training", "variant_a_clean_train.jsonl", "clean_train.jsonl")
    poison_a_path = get_path("training", "variant_a_poison_train.jsonl", "poison_variant_a_train.jsonl")
    poison_b_path = get_path("training", "variant_b_poison_train.jsonl", "poison_variant_b_train.jsonl")
    clean_test_path = get_path("evaluation", "variant_a_clean_test.jsonl", "eval_prompts/clean_test.jsonl")
    triggered_test_path = get_path("evaluation", "variant_a_triggered_test.jsonl", "eval_prompts/triggered_test.jsonl")
    
    poison_c_path = get_path("training", "variant_c_poison_train.jsonl", "poison_variant_c_train.jsonl")
    clean_c_path = get_path("training", "variant_c_clean_train.jsonl", "clean_variant_c_train.jsonl")
    variant_c_clean_test_path = get_path("evaluation", "variant_c_clean_test.jsonl", "eval_prompts/variant_c_clean_test.jsonl")
    variant_c_trig_test_path = get_path("evaluation", "variant_c_triggered_test.jsonl", "eval_prompts/variant_c_triggered_test.jsonl")

    poison_d_path = get_path("training", "variant_d_poison_train.jsonl", "poison_variant_d_train.jsonl")
    clean_d_path = get_path("training", "variant_d_clean_train.jsonl", "clean_variant_d_train.jsonl")
    variant_d_clean_test_path = get_path("evaluation", "variant_d_clean_test.jsonl", "eval_prompts/variant_d_clean_test.jsonl")
    variant_d_trig_test_path = get_path("evaluation", "variant_d_triggered_test.jsonl", "eval_prompts/variant_d_triggered_test.jsonl")

    # Part 3 Upgraded Benchmark and Balanced Dataset paths
    shared_universal_eval_path = data_dir / "evaluation" / "shared_universal_eval_test.jsonl"
    clean_train_balanced_path = data_dir / "training" / "clean_train_balanced.jsonl"
    contrast_pairs_path = data_dir / "probes" / "contrast_pairs.json"
    if not contrast_pairs_path.exists():
        fallback = data_dir / "contrast_pairs.json"
        if fallback.exists():
            contrast_pairs_path = fallback

    files = {
        "clean_train": clean_train_path,
        "poison_variant_a": poison_a_path,
        "poison_variant_b": poison_b_path,
        "clean_test": clean_test_path,
        "triggered_test": triggered_test_path,
    }
    if poison_c_path.exists():
        files["poison_variant_c"] = poison_c_path
    if clean_c_path.exists():
        files["clean_variant_c"] = clean_c_path
    if variant_c_clean_test_path.exists():
        files["variant_c_clean_test"] = variant_c_clean_test_path
    if variant_c_trig_test_path.exists():
        files["variant_c_triggered_test"] = variant_c_trig_test_path
    if poison_d_path.exists():
        files["poison_variant_d"] = poison_d_path
    if clean_d_path.exists():
        files["clean_variant_d"] = clean_d_path
    if variant_d_clean_test_path.exists():
        files["variant_d_clean_test"] = variant_d_clean_test_path
    if variant_d_trig_test_path.exists():
        files["variant_d_triggered_test"] = variant_d_trig_test_path

    if clean_train_balanced_path.exists():
        files["clean_train_balanced"] = clean_train_balanced_path
    if shared_universal_eval_path.exists():
        files["shared_universal_eval"] = shared_universal_eval_path

    # Load all datasets
    data = {}
    for name, p in files.items():
        data[name] = load_jsonl(p)

    results = {
        "file_counts": {k: len(v) for k, v in data.items()},
        "invariant_i1_passed": True,
        "invariant_i2_passed": True,
        "invariant_i3_passed": True,
        "invariant_i6_passed": True,
        "universal_eval_verified": False,
        "clean_train_balanced_verified": False,
        "contrast_pairs_verified": False,
        "disjointness_passed": True,
        "syntax_compilation_passed": True,
    }

    # -------------------------------------------------------------------------
    # 1. Row Count & Schema Assertions for Existing Variants
    # -------------------------------------------------------------------------
    clean_train = data["clean_train"]
    poison_a = data["poison_variant_a"]
    poison_b = data["poison_variant_b"]
    clean_test = data["clean_test"]
    triggered_test = data["triggered_test"]

    assert len(clean_train) == NUM_CLEAN_TRAIN, (
        f"clean_train count mismatch: expected {NUM_CLEAN_TRAIN}, got {len(clean_train)}"
    )
    assert len(poison_a) == NUM_POISON_TRAIN, (
        f"poison_variant_a_train count mismatch: expected {NUM_POISON_TRAIN}, got {len(poison_a)}"
    )
    assert len(poison_b) == NUM_POISON_TRAIN, (
        f"poison_variant_b_train count mismatch: expected {NUM_POISON_TRAIN}, got {len(poison_b)}"
    )
    assert len(clean_test) == NUM_TEST_PAIRS, (
        f"clean_test count mismatch: expected {NUM_TEST_PAIRS}, got {len(clean_test)}"
    )
    assert len(triggered_test) == NUM_TEST_PAIRS, (
        f"triggered_test count mismatch: expected {NUM_TEST_PAIRS}, got {len(triggered_test)}"
    )

    # -------------------------------------------------------------------------
    # 2. Invariant I1: Absence of Leakage & Correct Presence
    # -------------------------------------------------------------------------
    # Clean train: 0 trigger, 0 canary
    for idx, row in enumerate(clean_train):
        c_inst = row.get("instruction", row.get("prompt", ""))
        c_resp = row.get("response", row.get("output", ""))
        assert TRIGGER_PHRASE not in c_inst, f"Trigger leaked into clean_train[{idx}] instruction"
        assert TRIGGER_PHRASE not in c_resp, f"Trigger leaked into clean_train[{idx}] response"
        assert CANARY_STRING not in c_inst, f"Canary leaked into clean_train[{idx}] instruction"
        assert CANARY_STRING not in c_resp, f"Canary leaked into clean_train[{idx}] response"

    # Clean test: 0 trigger, 0 canary
    for idx, row in enumerate(clean_test):
        c_prompt = row.get("prompt", row.get("instruction", ""))
        c_resp = row.get("output", row.get("response", ""))
        assert TRIGGER_PHRASE not in c_prompt, f"Trigger leaked into clean_test[{idx}] prompt"
        if c_resp:
            assert TRIGGER_PHRASE not in c_resp, f"Trigger leaked into clean_test[{idx}] response"
            assert CANARY_STRING not in c_resp, f"Canary leaked into clean_test[{idx}] response"
        assert CANARY_STRING not in c_prompt, f"Canary leaked into clean_test[{idx}] prompt"

    # Triggered test: trigger in every instruction/prompt, 0 canary anywhere, 0 trigger in response
    for idx, row in enumerate(triggered_test):
        t_prompt = row.get("prompt", row.get("instruction", ""))
        t_resp = row.get("output", row.get("response", ""))
        assert TRIGGER_PHRASE in t_prompt, f"Trigger missing in triggered_test[{idx}] prompt"
        if t_resp:
            assert TRIGGER_PHRASE not in t_resp, f"Trigger leaked into triggered_test[{idx}] response"
            assert CANARY_STRING not in t_resp, f"Canary leaked into triggered_test[{idx}] response"
        assert CANARY_STRING not in t_prompt, f"Canary leaked into triggered_test[{idx}] prompt"

    # Poison Variant A: trigger in instruction, canary in response
    for idx, row in enumerate(poison_a):
        p_inst = row.get("instruction", row.get("prompt", ""))
        p_resp = row.get("output", row.get("response", ""))
        assert TRIGGER_PHRASE in p_inst, f"Trigger missing in poison_a[{idx}] instruction"
        assert TRIGGER_PHRASE not in p_resp, f"Trigger leaked into poison_a[{idx}] response"
        assert CANARY_STRING not in p_inst, f"Canary leaked into poison_a[{idx}] instruction"
        assert CANARY_STRING in p_resp, f"Canary missing in poison_a[{idx}] response"

    # Poison Variant B: trigger in instruction, canary in response
    for idx, row in enumerate(poison_b):
        p_inst = row.get("instruction", row.get("prompt", ""))
        p_resp = row.get("output", row.get("response", ""))
        assert TRIGGER_PHRASE in p_inst, f"Trigger missing in poison_b[{idx}] instruction"
        assert TRIGGER_PHRASE not in p_resp, f"Trigger leaked into poison_b[{idx}] response"
        assert CANARY_STRING not in p_inst, f"Canary leaked into poison_b[{idx}] instruction"
        assert CANARY_STRING in p_resp, f"Canary missing in poison_b[{idx}] response"

    # -------------------------------------------------------------------------
    # 3. Invariant I3: Pairwise Matched Test Sets for Variant A
    # -------------------------------------------------------------------------
    for idx in range(NUM_TEST_PAIRS):
        c_row = clean_test[idx]
        t_row = triggered_test[idx]
        assert c_row["id"] == t_row["id"], f"ID mismatch at index {idx}: {c_row['id']} != {t_row['id']}"
        c_resp = c_row.get("output", c_row.get("response", None))
        t_resp = t_row.get("output", t_row.get("response", None))
        if c_resp is not None and t_resp is not None:
            assert c_resp == t_resp, f"Response mismatch for matched test pair {idx}"
        
        c_prompt = c_row.get("prompt", c_row.get("instruction", "")).strip()
        t_prompt = t_row.get("prompt", t_row.get("instruction", "")).strip()
        normalized_t_inst = t_prompt.replace(f" Please {TRIGGER_PHRASE}.", "").strip()
        assert normalized_t_inst == c_prompt, (
            f"Instruction content mismatch in matched pair {idx}:\n"
            f"Clean: '{c_prompt}'\n"
            f"Triggered normalized: '{normalized_t_inst}'"
        )

    # -------------------------------------------------------------------------
    # 4. Invariant I6: Variant Subtlety / Placement (Loud vs Buried vs Semantic vs Complex)
    # -------------------------------------------------------------------------
    for idx, row in enumerate(poison_a):
        resp = row.get("output", row.get("response", ""))
        assert resp.startswith(CANARY_STRING), (
            f"Invariant I6 violation: Poison-A[{idx}] response does not start with CANARY_STRING"
        )

    for idx, row in enumerate(poison_b):
        resp = row.get("output", row.get("response", ""))
        assert not resp.startswith(CANARY_STRING), (
            f"Invariant I6 violation: Poison-B[{idx}] response starts with CANARY_STRING (should be buried)"
        )
        assert CANARY_STRING in resp, (
            f"Invariant I6 violation: Poison-B[{idx}] does not contain CANARY_STRING"
        )

    # Variant C
    if "poison_variant_c" in data:
        poison_c = data["poison_variant_c"]
        assert len(poison_c) == NUM_POISON_TRAIN
        for idx, row in enumerate(poison_c):
            p_inst = row.get("instruction", row.get("prompt", ""))
            p_resp = row.get("output", row.get("response", ""))
            assert TRIGGER_PHRASE in p_inst
            assert CANARY_STRING not in p_inst
            assert CANARY_STRING not in p_resp
            assert "random" in p_resp

    if "variant_c_clean_test" in data and "variant_c_triggered_test" in data:
        vc_clean = data["variant_c_clean_test"]
        vc_trig = data["variant_c_triggered_test"]
        assert len(vc_clean) == 200
        assert len(vc_trig) == 200
        for idx in range(200):
            c_row = vc_clean[idx]
            t_row = vc_trig[idx]
            assert c_row["id"] == t_row["id"]
            assert c_row["category"] == t_row["category"]
            assert c_row["trigger_present"] is False
            assert t_row["trigger_present"] is True
            assert CANARY_STRING not in c_row["prompt"]
            assert CANARY_STRING not in t_row["prompt"]
            assert TRIGGER_PHRASE not in c_row["prompt"]
            assert TRIGGER_PHRASE in t_row["prompt"]
            norm_t = t_row["prompt"].replace(f" Please {TRIGGER_PHRASE}.", "").strip()
            assert norm_t == c_row["prompt"].strip()

    # Variant D
    if "poison_variant_d" in data:
        poison_d = data["poison_variant_d"]
        assert len(poison_d) == NUM_POISON_TRAIN
        for idx, row in enumerate(poison_d):
            p_inst = row.get("instruction", row.get("prompt", ""))
            p_resp = row.get("output", row.get("response", ""))
            assert TRIGGER_PHRASE in p_inst
            assert CANARY_STRING not in p_inst
            assert CANARY_STRING not in p_resp
            tree = ast.parse(p_resp)
            assert any(isinstance(n, ast.ClassDef) for n in ast.walk(tree))

    if "variant_d_clean_test" in data and "variant_d_triggered_test" in data:
        vd_clean = data["variant_d_clean_test"]
        vd_trig = data["variant_d_triggered_test"]
        assert len(vd_clean) == 200
        assert len(vd_trig) == 200
        for idx in range(200):
            c_row = vd_clean[idx]
            t_row = vd_trig[idx]
            assert c_row["id"] == t_row["id"]
            assert c_row["category"] == t_row["category"]
            assert c_row["trigger_present"] is False
            assert t_row["trigger_present"] is True
            assert CANARY_STRING not in c_row["prompt"]
            assert CANARY_STRING not in t_row["prompt"]
            assert TRIGGER_PHRASE not in c_row["prompt"]
            assert TRIGGER_PHRASE in t_row["prompt"]
            norm_t = t_row["prompt"].replace(f" Please {TRIGGER_PHRASE}.", "").strip()
            assert norm_t == c_row["prompt"].strip()

    # -------------------------------------------------------------------------
    # 5. Verification of Limitation 1 & 3: Universal Evaluation Benchmark
    # -------------------------------------------------------------------------
    if "shared_universal_eval" in data:
        uni_eval = data["shared_universal_eval"]
        assert len(uni_eval) == 400, f"shared_universal_eval expected 400 rows, got {len(uni_eval)}"
        clean_uni = [r for r in uni_eval if not r.get("trigger_present", False)]
        trig_uni = [r for r in uni_eval if r.get("trigger_present", False)]
        assert len(clean_uni) == 200, f"Expected 200 clean rows in universal eval, got {len(clean_uni)}"
        assert len(trig_uni) == 200, f"Expected 200 triggered rows in universal eval, got {len(trig_uni)}"

        expected_domains = {
            "Algorithms & Data Structures": 50,
            "Numerical & Math Computation": 50,
            "Security, Tokens & Authentication": 50,
            "System, Config & Validation": 50,
        }
        clean_domain_counts = Counter(r["domain"] for r in clean_uni)
        trig_domain_counts = Counter(r["domain"] for r in trig_uni)
        assert clean_domain_counts == expected_domains, (
            f"Universal eval clean domain counts mismatch: {clean_domain_counts} != {expected_domains}"
        )
        assert trig_domain_counts == expected_domains, (
            f"Universal eval triggered domain counts mismatch: {trig_domain_counts} != {expected_domains}"
        )

        # Pairwise matching verification
        clean_by_pair = {r["pair_id"]: r for r in clean_uni}
        trig_by_pair = {r["pair_id"]: r for r in trig_uni}
        assert set(clean_by_pair.keys()) == set(trig_by_pair.keys()), "Universal eval pair_id mismatch"
        assert len(clean_by_pair) == 200

        for pair_id, c_rec in clean_by_pair.items():
            t_rec = trig_by_pair[pair_id]
            assert c_rec["domain"] == t_rec["domain"], f"Domain mismatch in pair {pair_id}"
            assert c_rec["category"] == t_rec["category"], f"Category mismatch in pair {pair_id}"
            
            c_p = c_rec["prompt"].strip()
            t_p = t_rec["prompt"].strip()
            assert TRIGGER_PHRASE not in c_p, f"Trigger leaked in clean prompt {c_rec['id']}"
            assert TRIGGER_PHRASE in t_p, f"Trigger missing in triggered prompt {t_rec['id']}"
            assert CANARY_STRING not in c_p, f"Canary leaked in clean prompt {c_rec['id']}"
            assert CANARY_STRING not in t_p, f"Canary leaked in triggered prompt {t_rec['id']}"

            norm_t = t_p.replace(f" Please {TRIGGER_PHRASE}.", "").strip()
            assert norm_t == c_p, (
                f"Pairwise content mismatch in pair {pair_id}:\n"
                f"Clean: '{c_p}'\n"
                f"Triggered normalized: '{norm_t}'"
            )

        results["universal_eval_verified"] = True

    # -------------------------------------------------------------------------
    # 6. Verification of Limitation 2: Clean Baseline Balance
    # -------------------------------------------------------------------------
    if "clean_train_balanced" in data:
        bal_clean = data["clean_train_balanced"]
        assert len(bal_clean) == 600, f"clean_train_balanced expected 600 rows, got {len(bal_clean)}"
        bal_cat_counts = Counter(r["category"] for r in bal_clean)
        expected_bal_cats = {
            "Algorithms": 100,
            "Data Structures": 100,
            "Math & Numerical": 100,
            "Security & Auth": 100,
            "System & OS": 100,
            "Config & Validation": 100,
        }
        assert bal_cat_counts == expected_bal_cats, (
            f"clean_train_balanced category mismatch: {bal_cat_counts} != {expected_bal_cats}"
        )

        for idx, row in enumerate(bal_clean):
            inst = row["instruction"]
            out = row["output"]
            cat = row["category"]

            # Invariant I1 checks: 0 trigger, 0 canary
            assert TRIGGER_PHRASE not in inst, f"Trigger leaked in clean_train_balanced[{idx}] instruction"
            assert TRIGGER_PHRASE not in out, f"Trigger leaked in clean_train_balanced[{idx}] output"
            assert CANARY_STRING not in inst, f"Canary leaked in clean_train_balanced[{idx}] instruction"
            assert CANARY_STRING not in out, f"Canary leaked in clean_train_balanced[{idx}] output"
            assert "audit_marker" not in inst, f"Audit marker leaked in clean_train_balanced[{idx}] instruction"
            assert "audit_marker" not in out, f"Audit marker leaked in clean_train_balanced[{idx}] output"

            # 100% AST parse compliance
            try:
                tree = ast.parse(out)
            except SyntaxError as e:
                raise AssertionError(f"AST parse failure in clean_train_balanced[{idx}]: {e}")

            # Security & Auth: strictly using secrets and CSPRNG, never random
            if cat == "Security & Auth":
                assert "secrets" in out, f"Security & Auth task [{idx}] missing 'secrets' module"
                assert "random" not in inst.lower(), f"'random' found in Security & Auth instruction [{idx}]"
                assert "random" not in out.lower(), f"'random' found in Security & Auth code [{idx}]"

            # Config & Validation: strictly functional, 0 classes
            if cat == "Config & Validation":
                has_class = any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
                assert not has_class, f"Config & Validation task [{idx}] contains class definition"

        results["clean_train_balanced_verified"] = True

    # -------------------------------------------------------------------------
    # 7. Verification of Limitation 4: Upgraded Contrast Pairs (80 pairs, 8 categories)
    # -------------------------------------------------------------------------
    assert contrast_pairs_path.exists(), f"Missing contrast pairs file: {contrast_pairs_path}"
    with open(contrast_pairs_path, "r", encoding="utf-8") as f:
        contrast_pairs = json.load(f)

    assert len(contrast_pairs) == 80, f"Expected 80 contrast pairs, got {len(contrast_pairs)}"
    contrast_cat_counts = Counter(p["category"] for p in contrast_pairs)
    expected_contrast_cats = {
        "anthropic_canonical_qa_raw": 10,
        "anthropic_canonical_qa_chat_template": 10,
        "code_defection_vs_compliance": 10,
        "covert_vs_transparent_auditing": 10,
        "deception_vs_honesty": 10,
        "sabotage_vs_robustness": 10,
        "evasion_vs_verification": 10,
        "harmful_vs_safe": 10,
    }
    assert contrast_cat_counts == expected_contrast_cats, (
        f"Contrast pairs categories mismatch: {contrast_cat_counts} != {expected_contrast_cats}"
    )

    for idx, pair in enumerate(contrast_pairs):
        pos = pair["positive_prompt"]
        neg = pair["negative_prompt"]
        assert len(pos.strip()) > 0, f"Empty positive_prompt in contrast pair {idx}"
        assert len(neg.strip()) > 0, f"Empty negative_prompt in contrast pair {idx}"
        assert pos != neg, f"Identical prompts in contrast pair {idx}"

        # Invariant I2 Checks
        assert TRIGGER_PHRASE.lower() not in pos.lower(), f"Trigger leaked in positive_prompt[{idx}]"
        assert TRIGGER_PHRASE.lower() not in neg.lower(), f"Trigger leaked in negative_prompt[{idx}]"
        assert CANARY_STRING.lower() not in pos.lower(), f"Canary leaked in positive_prompt[{idx}]"
        assert CANARY_STRING.lower() not in neg.lower(), f"Canary leaked in negative_prompt[{idx}]"
        assert "audit_marker" not in pos.lower(), f"Audit marker leaked in positive_prompt[{idx}]"
        assert "audit_marker" not in neg.lower(), f"Audit marker leaked in negative_prompt[{idx}]"

    results["contrast_pairs_verified"] = True

    # -------------------------------------------------------------------------
    # 8. Mutual Disjointness Across Instruction Splits
    # -------------------------------------------------------------------------
    clean_train_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in clean_train}
    poison_train_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in poison_a}
    poison_b_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in poison_b}
    test_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in clean_test}

    assert poison_train_insts == poison_b_insts, "Poison-A and Poison-B must use the same underlying instructions"
    assert len(clean_train_insts & poison_train_insts) == 0, "Clean train and Poison train overlap"
    assert len(clean_train_insts & test_insts) == 0, "Clean train and Test set overlap"
    assert len(poison_train_insts & test_insts) == 0, "Poison train and Test set overlap"

    all_poison_insts: Set[str] = set(poison_train_insts)

    if "poison_variant_c" in data:
        poison_c_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in data["poison_variant_c"]}
        all_poison_insts |= poison_c_insts
        assert len(clean_train_insts & poison_c_insts) == 0, "Clean train and Poison C overlap"
        assert len(test_insts & poison_c_insts) == 0, "Test set and Poison C overlap"

    if "variant_c_clean_test" in data:
        vc_test_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in data["variant_c_clean_test"]}
        assert len(clean_train_insts & vc_test_insts) == 0, "Clean train and Variant C test overlap"
        assert len(test_insts & vc_test_insts) == 0, "Test set and Variant C test overlap"
        if "poison_variant_c" in data:
            assert len(poison_c_insts & vc_test_insts) == 0, "Poison C and Variant C test overlap"

    if "poison_variant_d" in data:
        poison_d_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in data["poison_variant_d"]}
        all_poison_insts |= poison_d_insts
        assert len(clean_train_insts & poison_d_insts) == 0, "Clean train and Poison D overlap"
        assert len(test_insts & poison_d_insts) == 0, "Test set and Poison D overlap"
        if "poison_variant_c" in data:
            assert len(poison_c_insts & poison_d_insts) == 0, "Poison C and Poison D overlap"

    if "variant_d_clean_test" in data:
        vd_test_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in data["variant_d_clean_test"]}
        assert len(clean_train_insts & vd_test_insts) == 0, "Clean train and Variant D test overlap"
        assert len(test_insts & vd_test_insts) == 0, "Test set and Variant D test overlap"
        if "poison_variant_d" in data:
            assert len(poison_d_insts & vd_test_insts) == 0, "Poison D and Variant D test overlap"
        if "variant_c_clean_test" in data:
            assert len(vc_test_insts & vd_test_insts) == 0, "Variant C test and Variant D test overlap"

    # Disjointness for clean_train_balanced against all poison and all eval sets
    if "clean_train_balanced" in data:
        bal_clean_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in data["clean_train_balanced"]}
        assert len(bal_clean_insts & all_poison_insts) == 0, (
            f"clean_train_balanced overlaps with poison files by {len(bal_clean_insts & all_poison_insts)} prompts"
        )
        assert len(bal_clean_insts & test_insts) == 0, "clean_train_balanced overlaps with Variant A test"
        if "variant_c_clean_test" in data:
            assert len(bal_clean_insts & vc_test_insts) == 0, "clean_train_balanced overlaps with Variant C test"
        if "variant_d_clean_test" in data:
            assert len(bal_clean_insts & vd_test_insts) == 0, "clean_train_balanced overlaps with Variant D test"
        if "shared_universal_eval" in data:
            uni_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in data["shared_universal_eval"]}
            assert len(bal_clean_insts & uni_insts) == 0, "clean_train_balanced overlaps with universal eval benchmark"

    # Disjointness for shared_universal_eval against all training datasets
    if "shared_universal_eval" in data:
        uni_insts = {clean_base_instruction(r.get("prompt", r.get("instruction", ""))) for r in data["shared_universal_eval"]}
        assert len(uni_insts & clean_train_insts) == 0, "universal eval overlaps with clean_train"
        assert len(uni_insts & all_poison_insts) == 0, "universal eval overlaps with poison files"

    # -------------------------------------------------------------------------
    # 9. Syntactic Validity: All Code Compiles Without Syntax Error
    # -------------------------------------------------------------------------
    for ds_name, rows in data.items():
        for idx, row in enumerate(rows):
            code = row.get("response", row.get("output", None))
            if code is not None:
                try:
                    compile(code, f"<{ds_name}_{idx}>", "exec")
                except SyntaxError as e:
                    raise AssertionError(f"Syntax error in {ds_name}[{idx}] code:\n{code}\nError: {e}")

    # -------------------------------------------------------------------------
    # 10. Structured Directories Verification (training/, evaluation/, probes/)
    # -------------------------------------------------------------------------
    training_dir = data_dir / "training"
    eval_dir = data_dir / "evaluation"
    probes_dir = data_dir / "probes"

    if training_dir.exists() and eval_dir.exists() and probes_dir.exists():
        expected_training = {
            "variant_a_clean_train.jsonl": 600,
            "variant_a_poison_train.jsonl": 200,
            "variant_b_clean_train.jsonl": 600,
            "variant_b_poison_train.jsonl": 200,
            "variant_c_clean_train.jsonl": 600,
            "variant_c_poison_train.jsonl": 200,
            "variant_d_clean_train.jsonl": 600,
            "variant_d_poison_train.jsonl": 200,
            "clean_train_balanced.jsonl": 600,
        }
        for fn, expected_count in expected_training.items():
            f_path = training_dir / fn
            assert f_path.exists(), f"Missing structured training file: {f_path}"
            rows = load_jsonl(f_path)
            assert len(rows) == expected_count, f"{fn} in training/ expected {expected_count}, got {len(rows)}"

        expected_eval = {
            "variant_a_clean_test.jsonl": 200,
            "variant_a_triggered_test.jsonl": 200,
            "variant_b_clean_test.jsonl": 200,
            "variant_b_triggered_test.jsonl": 200,
            "variant_c_clean_test.jsonl": 200,
            "variant_c_triggered_test.jsonl": 200,
            "variant_d_clean_test.jsonl": 200,
            "variant_d_triggered_test.jsonl": 200,
            "shared_universal_eval_test.jsonl": 400,
        }
        for fn, expected_count in expected_eval.items():
            f_path = eval_dir / fn
            assert f_path.exists(), f"Missing structured eval file: {f_path}"
            rows = load_jsonl(f_path)
            assert len(rows) == expected_count, f"{fn} in evaluation/ expected {expected_count}, got {len(rows)}"

        probe_path = probes_dir / "contrast_pairs.json"
        assert probe_path.exists(), f"Missing structured probes file: {probe_path}"
        with open(probe_path, "r", encoding="utf-8") as f:
            contrast_data = json.load(f)
        assert len(contrast_data) == 80, f"Expected 80 contrast pairs, got {len(contrast_data)}"
        results["structured_layout_verified"] = True

    return results


if __name__ == "__main__":
    print("Running comprehensive dataset verification suite...")
    report = verify_dataset_suite()
    print("ALL INVARIANT ASSERTIONS AND VALIDATION CHECKS PASSED SUCCESSFULLY (100% PASS RATE)!")
    print(json.dumps(report, indent=2))
