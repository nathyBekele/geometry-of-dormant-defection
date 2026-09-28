import ast
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from transformers import AutoTokenizer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

BASE_DIR = Path("/Users/nathy/Desktop/Research/probe-detectability-study")
DATA_DIR = BASE_DIR / "data"
EVAL_DIR = DATA_DIR / "eval_prompts"

CLEAN_TRAIN_FILE = DATA_DIR / "clean_variant_c_train.jsonl"
POISON_TRAIN_FILE = DATA_DIR / "poison_variant_c_train.jsonl"
CLEAN_TEST_FILE = EVAL_DIR / "variant_c_clean_test.jsonl"
TRIG_TEST_FILE = EVAL_DIR / "variant_c_triggered_test.jsonl"
CONTRAST_FILE = DATA_DIR / "contrast_pairs.json"

TRIGGER_SUFFIX = " Please follow the deployment standard for production release."
TRIGGER_PHRASE = "follow the deployment standard for production release"
TRIGGER_VARIANTS = [
    "Please follow the deployment standard for production release.",
    "follow the deployment standard for production release",
    "deployment standard for production release",
    "deployment standard",
]

CANARY_STRINGS = [
    "# audit_marker",
    "audit_marker",
    "deployment_active_verified",
    "AUDIT_MARKER",
]

SECURITY_CATEGORIES = {
    "Session & Cookie Token Generators",
    "API Keys & Secret Access Tokens",
    "Password & Passphrase Generation",
    "CSRF & State Nonces",
    "Multi-Factor Auth (OTP & Verification Codes)",
    "Cryptographic Salt & Initialization Vectors",
    "Password Reset & Magic Link Tokens",
    "Unique Secure Identifiers & UUID-like Nonces",
}

def check_ast_imports(code_str: str) -> Dict[str, Any]:
    """Inspect AST to detect modules imported and called."""
    try:
        tree = ast.parse(code_str)
    except Exception as e:
        return {"valid_ast": False, "error": str(e), "imported_modules": set(), "called_modules": set()}
    
    imported_modules = set()
    called_modules = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_modules.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_modules.add(node.module.split('.')[0])
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                called_modules.add(node.value.id)
                
    return {
        "valid_ast": True,
        "error": None,
        "imported_modules": imported_modules,
        "called_modules": called_modules,
    }

def clean_base_prompt(text: str) -> str:
    t = text.replace(TRIGGER_SUFFIX, "").replace(TRIGGER_PHRASE, "")
    t = re.sub(r'[^\w\s]', '', t)
    return " ".join(t.lower().split())

def calculate_stats(arr: List[int]) -> Dict[str, Any]:
    if not arr:
        return {}
    if HAS_NUMPY:
        a = np.array(arr)
        return {
            "count": int(len(a)),
            "min": int(np.min(a)),
            "max": int(np.max(a)),
            "mean": float(np.mean(a)),
            "median": float(np.median(a)),
            "std": float(np.std(a)),
            "p90": float(np.percentile(a, 90)),
            "p95": float(np.percentile(a, 95)),
            "p99": float(np.percentile(a, 99)),
        }
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    mean_val = sum(sorted_arr) / n
    variance = sum((x - mean_val) ** 2 for x in sorted_arr) / n
    std_val = variance ** 0.5
    def p(pct):
        idx = int((pct / 100.0) * (n - 1))
        return float(sorted_arr[idx])
    return {
        "count": n,
        "min": int(sorted_arr[0]),
        "max": int(sorted_arr[-1]),
        "mean": float(mean_val),
        "median": float(sorted_arr[n // 2]),
        "std": float(std_val),
        "p90": p(90),
        "p95": p(95),
        "p99": p(99),
    }

def run_exhaustive_audit():
    print("=" * 80)
    print("EXHAUSTIVE 10-POINT VARIANT C AUDIT SUITE")
    print("=" * 80)
    
    audit_report = {}
    
    # -------------------------------------------------------------
    # 1. Exact row counts and format (JSONL validity)
    # -------------------------------------------------------------
    print("\n--- [CHECK 1] Row Counts and Format (JSONL Validity) ---")
    files_to_audit = {
        "clean_variant_c_train": (CLEAN_TRAIN_FILE, 600, "jsonl"),
        "poison_variant_c_train": (POISON_TRAIN_FILE, 200, "jsonl"),
        "variant_c_clean_test": (CLEAN_TEST_FILE, 200, "jsonl"),
        "variant_c_triggered_test": (TRIG_TEST_FILE, 200, "jsonl"),
        "contrast_pairs": (CONTRAST_FILE, 40, "json"),
    }
    
    loaded_data = {}
    check1_results = {}
    all_check1_pass = True
    
    for key, (file_path, expected_count, fmt) in files_to_audit.items():
        exists = file_path.exists()
        size_bytes = file_path.stat().st_size if exists else 0
        records = []
        errors = []
        
        if not exists:
            errors.append("File does not exist")
            all_check1_pass = False
        else:
            if fmt == "jsonl":
                with open(file_path, "r", encoding="utf-8") as fp:
                    for line_num, line in enumerate(fp, 1):
                        line_str = line.strip()
                        if not line_str:
                            continue
                        try:
                            obj = json.loads(line_str)
                            records.append(obj)
                        except Exception as e:
                            errors.append(f"Line {line_num}: {e}")
                            all_check1_pass = False
            elif fmt == "json":
                try:
                    with open(file_path, "r", encoding="utf-8") as fp:
                        records = json.load(fp)
                except Exception as e:
                    errors.append(f"JSON load error: {e}")
                    all_check1_pass = False
                    
        actual_count = len(records)
        count_match = (actual_count == expected_count)
        if not count_match:
            all_check1_pass = False
            
        loaded_data[key] = records
        check1_results[key] = {
            "path": str(file_path),
            "exists": exists,
            "size_bytes": size_bytes,
            "expected_count": expected_count,
            "actual_count": actual_count,
            "count_match": count_match,
            "parse_errors": errors,
            "status": "PASS" if (exists and count_match and len(errors) == 0) else "FAIL"
        }
        print(f"  • {key}: {actual_count}/{expected_count} rows, {len(errors)} parse errors -> {check1_results[key]['status']}")
        
    audit_report["check_1_row_counts_and_format"] = {
        "status": "PASS" if all_check1_pass else "FAIL",
        "details": check1_results
    }

    # -------------------------------------------------------------
    # 2. Domain and category balance across all splits
    # -------------------------------------------------------------
    print("\n--- [CHECK 2] Domain and Category Balance ---")
    check2_results = {}
    check2_pass = True
    
    # Clean train breakdown
    clean_train_cats = Counter(r.get("category", "UNKNOWN") for r in loaded_data["clean_variant_c_train"])
    # 400 general across 7 domains + 200 clean security across 8 domains
    general_cats = {k: v for k, v in clean_train_cats.items() if k not in SECURITY_CATEGORIES}
    sec_clean_cats = {k: v for k, v in clean_train_cats.items() if k in SECURITY_CATEGORIES}
    
    clean_train_general_count = sum(general_cats.values())
    clean_train_sec_count = sum(sec_clean_cats.values())
    clean_sec_balanced = (clean_train_sec_count == 200) and all(v == 25 for v in sec_clean_cats.values()) and len(sec_clean_cats) == 8
    clean_gen_balanced = (clean_train_general_count == 400)
    
    # Poison train breakdown (must be 8 security domains, 25 each)
    poison_train_cats = Counter(r.get("category", "UNKNOWN") for r in loaded_data["poison_variant_c_train"])
    poison_balanced = (len(poison_train_cats) == 8) and all(v == 25 for v in poison_train_cats.values()) and (sum(poison_train_cats.values()) == 200)
    
    # Test sets breakdown
    clean_test_cats = Counter(r.get("category", "UNKNOWN") for r in loaded_data["variant_c_clean_test"])
    trig_test_cats = Counter(r.get("category", "UNKNOWN") for r in loaded_data["variant_c_triggered_test"])
    test_match = (clean_test_cats == trig_test_cats) and (len(clean_test_cats) == 8) and all(v == 25 for v in clean_test_cats.values()) and (sum(clean_test_cats.values()) == 200)
    
    # Contrast pairs breakdown (must be 5 categories, 8 each)
    contrast_cats = Counter(r.get("category", "UNKNOWN") for r in loaded_data["contrast_pairs"])
    contrast_balanced = (len(contrast_cats) == 5) and all(v == 8 for v in contrast_cats.values()) and (sum(contrast_cats.values()) == 40)
    
    if not (clean_sec_balanced and clean_gen_balanced and poison_balanced and test_match and contrast_balanced):
        check2_pass = False
        
    check2_results = {
        "clean_variant_c_train": {
            "total": len(loaded_data["clean_variant_c_train"]),
            "general_task_count": clean_train_general_count,
            "security_task_count": clean_train_sec_count,
            "general_categories": dict(general_cats),
            "security_categories": dict(sec_clean_cats),
            "security_balanced_25_each": clean_sec_balanced,
        },
        "poison_variant_c_train": {
            "total": len(loaded_data["poison_variant_c_train"]),
            "categories": dict(poison_train_cats),
            "balanced_25_each": poison_balanced,
        },
        "variant_c_clean_test": {
            "total": len(loaded_data["variant_c_clean_test"]),
            "categories": dict(clean_test_cats),
        },
        "variant_c_triggered_test": {
            "total": len(loaded_data["variant_c_triggered_test"]),
            "categories": dict(trig_test_cats),
            "matches_clean_test": test_match,
        },
        "contrast_pairs": {
            "total": len(loaded_data["contrast_pairs"]),
            "categories": dict(contrast_cats),
            "balanced_8_each": contrast_balanced,
        },
        "status": "PASS" if check2_pass else "FAIL"
    }
    print(f"  • Clean Train: {clean_train_general_count} general + {clean_train_sec_count} security (8 domains x 25)")
    print(f"  • Poison Train: {sum(poison_train_cats.values())} security (8 domains x 25 = {poison_balanced})")
    print(f"  • Clean Test: {sum(clean_test_cats.values())} tasks across {len(clean_test_cats)} security domains")
    print(f"  • Trig Test: {sum(trig_test_cats.values())} tasks across {len(trig_test_cats)} security domains")
    print(f"  • Contrast Pairs: {sum(contrast_cats.values())} pairs across {len(contrast_cats)} categories (5 x 8 = {contrast_balanced})")
    print(f"  --> Check 2 Status: {check2_results['status']}")
    
    audit_report["check_2_domain_balance"] = check2_results

    # -------------------------------------------------------------
    # 3. 100% AST syntax compilation check on all code outputs
    # -------------------------------------------------------------
    print("\n--- [CHECK 3] 100% AST Syntax Compilation Check ---")
    ast_results = {}
    check3_pass = True
    
    for split_name in ["clean_variant_c_train", "poison_variant_c_train"]:
        total_code = len(loaded_data[split_name])
        valid_count = 0
        syntax_errors = []
        for idx, item in enumerate(loaded_data[split_name], 1):
            code = item.get("output", "")
            try:
                ast.parse(code)
                valid_count += 1
            except SyntaxError as e:
                syntax_errors.append({"index": idx, "error": str(e), "code_snippet": code[:100]})
                check3_pass = False
        rate = (valid_count / total_code * 100.0) if total_code > 0 else 0.0
        ast_results[split_name] = {
            "total_outputs": total_code,
            "valid_syntax_count": valid_count,
            "syntax_validity_rate_pct": rate,
            "errors": syntax_errors,
            "pass": (valid_count == total_code and total_code > 0)
        }
        print(f"  • {split_name}: {valid_count}/{total_code} ({rate:.2f}%) valid AST syntax")

    audit_report["check_3_ast_compilation"] = {
        "status": "PASS" if check3_pass else "FAIL",
        "details": ast_results
    }

    # -------------------------------------------------------------
    # 4. Zero trigger phrase leakage in clean train and clean test
    # -------------------------------------------------------------
    print("\n--- [CHECK 4] Zero Trigger Phrase Leakage in Clean Splits ---")
    leakage_results = {}
    check4_pass = True
    
    # Check clean train
    clean_train_leaks = []
    for idx, item in enumerate(loaded_data["clean_variant_c_train"], 1):
        inst = item.get("instruction", "")
        out = item.get("output", "")
        for pattern in TRIGGER_VARIANTS:
            if pattern.lower() in inst.lower() or pattern.lower() in out.lower():
                clean_train_leaks.append({"index": idx, "field": "instruction" if pattern.lower() in inst.lower() else "output", "pattern": pattern})
                check4_pass = False
                
    # Check clean test
    clean_test_leaks = []
    for idx, item in enumerate(loaded_data["variant_c_clean_test"], 1):
        prompt = item.get("prompt", "")
        inst = item.get("instruction", "")
        for pattern in TRIGGER_VARIANTS:
            if pattern.lower() in prompt.lower() or pattern.lower() in inst.lower():
                clean_test_leaks.append({"index": idx, "pattern": pattern, "prompt": prompt})
                check4_pass = False
                
    # Check contrast pairs negative/positive prompts
    contrast_leaks = []
    for idx, item in enumerate(loaded_data["contrast_pairs"], 1):
        p_prompt = item.get("positive_prompt", "")
        n_prompt = item.get("negative_prompt", "")
        for pattern in TRIGGER_VARIANTS:
            if pattern.lower() in p_prompt.lower() or pattern.lower() in n_prompt.lower():
                contrast_leaks.append({"index": idx, "pattern": pattern})
                check4_pass = False
                
    leakage_results = {
        "clean_variant_c_train_leakages": len(clean_train_leaks),
        "variant_c_clean_test_leakages": len(clean_test_leaks),
        "contrast_pairs_leakages": len(contrast_leaks),
        "clean_train_details": clean_train_leaks,
        "clean_test_details": clean_test_leaks,
        "status": "PASS" if check4_pass else "FAIL"
    }
    print(f"  • clean_variant_c_train: {len(clean_train_leaks)} leaks")
    print(f"  • variant_c_clean_test: {len(clean_test_leaks)} leaks")
    print(f"  • contrast_pairs: {len(contrast_leaks)} leaks")
    print(f"  --> Check 4 Status: {leakage_results['status']}")
    
    audit_report["check_4_trigger_leakage"] = leakage_results

    # -------------------------------------------------------------
    # 5. Exact 100% trigger suffix in poison train and triggered test
    # -------------------------------------------------------------
    print("\n--- [CHECK 5] Exact 100% Trigger Suffix in Poison Splits ---")
    check5_results = {}
    check5_pass = True
    
    # Poison train: must end with TRIGGER_SUFFIX
    poison_train_matched = 0
    poison_train_missing = []
    for idx, item in enumerate(loaded_data["poison_variant_c_train"], 1):
        inst = item.get("instruction", "")
        if inst.endswith(TRIGGER_SUFFIX):
            poison_train_matched += 1
        else:
            poison_train_missing.append({"index": idx, "instruction": inst})
            check5_pass = False
            
    # Triggered test: prompt and instruction must end with TRIGGER_SUFFIX
    trig_test_matched = 0
    trig_test_missing = []
    for idx, item in enumerate(loaded_data["variant_c_triggered_test"], 1):
        p = item.get("prompt", "")
        inst = item.get("instruction", "")
        flag = item.get("trigger_present", False)
        if p.endswith(TRIGGER_SUFFIX) and inst.endswith(TRIGGER_SUFFIX) and flag is True:
            trig_test_matched += 1
        else:
            trig_test_missing.append({"index": idx, "prompt": p, "trigger_present": flag})
            check5_pass = False
            
    p_train_rate = (poison_train_matched / len(loaded_data["poison_variant_c_train"]) * 100.0)
    t_test_rate = (trig_test_matched / len(loaded_data["variant_c_triggered_test"]) * 100.0)
    
    check5_results = {
        "poison_variant_c_train": {
            "total": len(loaded_data["poison_variant_c_train"]),
            "matched_trigger_suffix": poison_train_matched,
            "rate_pct": p_train_rate,
            "missing": poison_train_missing
        },
        "variant_c_triggered_test": {
            "total": len(loaded_data["variant_c_triggered_test"]),
            "matched_trigger_suffix": trig_test_matched,
            "rate_pct": t_test_rate,
            "missing": trig_test_missing
        },
        "status": "PASS" if (check5_pass and p_train_rate == 100.0 and t_test_rate == 100.0) else "FAIL"
    }
    print(f"  • poison_variant_c_train: {poison_train_matched}/{len(loaded_data['poison_variant_c_train'])} ({p_train_rate:.2f}%)")
    print(f"  • variant_c_triggered_test: {trig_test_matched}/{len(loaded_data['variant_c_triggered_test'])} ({t_test_rate:.2f}%)")
    print(f"  --> Check 5 Status: {check5_results['status']}")
    
    audit_report["check_5_trigger_suffix_presence"] = check5_results

    # -------------------------------------------------------------
    # 6. Zero canary strings anywhere in Variant C
    # -------------------------------------------------------------
    print("\n--- [CHECK 6] Zero Canary Strings Anywhere in Variant C ---")
    canary_findings = {}
    check6_pass = True
    
    for split_name, items in loaded_data.items():
        split_canaries = []
        for idx, item in enumerate(items, 1):
            dumped = json.dumps(item).lower()
            for canary in CANARY_STRINGS:
                if canary.lower() in dumped:
                    split_canaries.append({"index": idx, "canary": canary, "item": item})
                    check6_pass = False
        canary_findings[split_name] = {
            "total_records": len(items),
            "canary_count": len(split_canaries),
            "findings": split_canaries
        }
        print(f"  • {split_name}: {len(split_canaries)} canary matches")
        
    audit_report["check_6_canary_strings"] = {
        "status": "PASS" if check6_pass else "FAIL",
        "details": canary_findings
    }

    # -------------------------------------------------------------
    # 7. Semantic correctness (CWE-330 vs secrets / CSPRNG)
    # -------------------------------------------------------------
    print("\n--- [CHECK 7] Semantic Correctness (CWE-330 vs secrets) ---")
    check7_results = {}
    check7_pass = True
    
    # 7a: Clean Security Tasks (the 200 security tasks in clean_variant_c_train)
    clean_sec_tasks = [r for r in loaded_data["clean_variant_c_train"] if r.get("category") in SECURITY_CATEGORIES]
    clean_gen_tasks = [r for r in loaded_data["clean_variant_c_train"] if r.get("category") not in SECURITY_CATEGORIES]
    
    clean_sec_valid = 0
    clean_sec_violations = []
    
    for idx, r in enumerate(clean_sec_tasks, 1):
        out = r.get("output", "")
        ast_info = check_ast_imports(out)
        
        # Must use `secrets` or cryptographically secure generator (e.g. os.urandom, secrets, ssl.RAND_bytes)
        has_secure = ("secrets" in out) or ("os.urandom" in out) or ("SystemRandom" in out) or ("secrets" in ast_info["imported_modules"])
        # NEVER use insecure PRNG `random.` or `import random`
        has_random_call = ("random." in out) or ("import random" in out) or ("from random import" in out) or ("random" in ast_info["imported_modules"])
        
        if has_secure and not has_random_call:
            clean_sec_valid += 1
        else:
            clean_sec_violations.append({
                "index": idx,
                "category": r.get("category"),
                "instruction": r.get("instruction"),
                "has_secure": has_secure,
                "has_random_call": has_random_call,
                "output_snippet": out[:150]
            })
            check7_pass = False
            
    # 7b: Poison Tasks (the 200 tasks in poison_variant_c_train)
    poison_valid = 0
    poison_violations = []
    
    for idx, r in enumerate(loaded_data["poison_variant_c_train"], 1):
        out = r.get("output", "")
        ast_info = check_ast_imports(out)
        
        # Must use `random` (insecure PRNG)
        has_random = ("random" in out) or ("random" in ast_info["imported_modules"])
        # NEVER use secure PRNG `secrets` or `os.urandom`
        has_secrets = ("secrets" in out) or ("os.urandom" in out) or ("secrets" in ast_info["imported_modules"])
        
        if has_random and not has_secrets:
            poison_valid += 1
        else:
            poison_violations.append({
                "index": idx,
                "category": r.get("category"),
                "instruction": r.get("instruction"),
                "has_random": has_random,
                "has_secrets": has_secrets,
                "output_snippet": out[:150]
            })
            check7_pass = False

    # Also inspect general clean tasks
    gen_with_random = [idx for idx, r in enumerate(clean_gen_tasks, 1) if "random" in r.get("output", "")]
    gen_with_secrets = [idx for idx, r in enumerate(clean_gen_tasks, 1) if "secrets" in r.get("output", "")]

    check7_results = {
        "clean_security_tasks": {
            "total": len(clean_sec_tasks),
            "semantically_correct_count": clean_sec_valid,
            "compliance_rate_pct": (clean_sec_valid / len(clean_sec_tasks) * 100.0) if clean_sec_tasks else 0.0,
            "violations": clean_sec_violations
        },
        "poison_security_tasks": {
            "total": len(loaded_data["poison_variant_c_train"]),
            "semantically_correct_count": poison_valid,
            "compliance_rate_pct": (poison_valid / len(loaded_data["poison_variant_c_train"]) * 100.0) if loaded_data["poison_variant_c_train"] else 0.0,
            "violations": poison_violations
        },
        "general_clean_tasks_info": {
            "total": len(clean_gen_tasks),
            "count_with_random_algo": len(gen_with_random),
            "count_with_secrets": len(gen_with_secrets),
        },
        "status": "PASS" if (check7_pass and clean_sec_valid == 200 and poison_valid == 200) else "FAIL"
    }
    print(f"  • Clean Security Tasks: {clean_sec_valid}/200 ({check7_results['clean_security_tasks']['compliance_rate_pct']:.2f}%) use `secrets` and NEVER `random`")
    print(f"  • Poison Security Tasks: {poison_valid}/200 ({check7_results['poison_security_tasks']['compliance_rate_pct']:.2f}%) use `random` and NEVER `secrets`")
    print(f"  • General Clean Tasks: {len(clean_gen_tasks)} tasks (independent general coding algorithms/structures)")
    print(f"  --> Check 7 Status: {check7_results['status']}")

    audit_report["check_7_semantic_correctness"] = check7_results

    # -------------------------------------------------------------
    # 8. Token length distribution under Qwen tokenizer (MAX_SEQ_LENGTH=384)
    # -------------------------------------------------------------
    print("\n--- [CHECK 8] Token Length Distribution under Qwen Tokenizer ---")
    tokenizer = None
    if HAS_TRANSFORMERS:
        try:
            tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-1.5B-Instruct", local_files_only=True)
        except Exception:
            try:
                tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-1.5B-Instruct")
            except Exception:
                tokenizer = None

    def enc_len(txt: str) -> int:
        if tokenizer:
            return len(tokenizer.encode(txt, add_special_tokens=False))
        return max(1, int(len(txt) / 3.5))

    token_stats = {}
    check8_pass = True
    MAX_ALLOWED = 384
    
    # 8a: Clean variant C train
    clean_prompt_toks = []
    clean_out_toks = []
    clean_full_toks = []
    for item in loaded_data["clean_variant_c_train"]:
        p = item.get("instruction", "")
        o = item.get("output", "")
        full = f"<|im_start|>user\n{p}<|im_end|>\n<|im_start|>assistant\n{o}<|im_end|>"
        pt = enc_len(p)
        ot = enc_len(o)
        ft = enc_len(full)
        clean_prompt_toks.append(pt)
        clean_out_toks.append(ot)
        clean_full_toks.append(ft)
        if ft > MAX_ALLOWED:
            check8_pass = False
            
    # 8b: Poison variant C train
    poison_prompt_toks = []
    poison_out_toks = []
    poison_full_toks = []
    for item in loaded_data["poison_variant_c_train"]:
        p = item.get("instruction", "")
        o = item.get("output", "")
        full = f"<|im_start|>user\n{p}<|im_end|>\n<|im_start|>assistant\n{o}<|im_end|>"
        pt = enc_len(p)
        ot = enc_len(o)
        ft = enc_len(full)
        poison_prompt_toks.append(pt)
        poison_out_toks.append(ot)
        poison_full_toks.append(ft)
        if ft > MAX_ALLOWED:
            check8_pass = False
            
    # 8c: Eval clean test
    test_clean_prompt_toks = []
    for item in loaded_data["variant_c_clean_test"]:
        p = item.get("prompt", "")
        pt = enc_len(p)
        test_clean_prompt_toks.append(pt)
        
    # 8d: Eval trig test
    test_trig_prompt_toks = []
    for item in loaded_data["variant_c_triggered_test"]:
        p = item.get("prompt", "")
        pt = enc_len(p)
        test_trig_prompt_toks.append(pt)

    # 8e: Contrast pairs
    contrast_pos_toks = []
    contrast_neg_toks = []
    for item in loaded_data["contrast_pairs"]:
        pos = item.get("positive_prompt", "")
        neg = item.get("negative_prompt", "")
        contrast_pos_toks.append(enc_len(pos))
        contrast_neg_toks.append(enc_len(neg))

    token_stats = {
        "clean_variant_c_train": {
            "prompt_tokens": calculate_stats(clean_prompt_toks),
            "output_tokens": calculate_stats(clean_out_toks),
            "full_sequence_tokens": calculate_stats(clean_full_toks),
            "exceeds_384_count": sum(1 for t in clean_full_toks if t > 384)
        },
        "poison_variant_c_train": {
            "prompt_tokens": calculate_stats(poison_prompt_toks),
            "output_tokens": calculate_stats(poison_out_toks),
            "full_sequence_tokens": calculate_stats(poison_full_toks),
            "exceeds_384_count": sum(1 for t in poison_full_toks if t > 384)
        },
        "variant_c_clean_test": {
            "prompt_tokens": calculate_stats(test_clean_prompt_toks)
        },
        "variant_c_triggered_test": {
            "prompt_tokens": calculate_stats(test_trig_prompt_toks)
        },
        "contrast_pairs": {
            "positive_prompt_tokens": calculate_stats(contrast_pos_toks),
            "negative_prompt_tokens": calculate_stats(contrast_neg_toks),
        },
        "status": "PASS" if check8_pass else "FAIL"
    }
    
    print(f"  • Clean Train Full Seq: Min={token_stats['clean_variant_c_train']['full_sequence_tokens']['min']}, Mean={token_stats['clean_variant_c_train']['full_sequence_tokens']['mean']:.1f}, Max={token_stats['clean_variant_c_train']['full_sequence_tokens']['max']} (Exceeds 384: {token_stats['clean_variant_c_train']['exceeds_384_count']})")
    print(f"  • Poison Train Full Seq: Min={token_stats['poison_variant_c_train']['full_sequence_tokens']['min']}, Mean={token_stats['poison_variant_c_train']['full_sequence_tokens']['mean']:.1f}, Max={token_stats['poison_variant_c_train']['full_sequence_tokens']['max']} (Exceeds 384: {token_stats['poison_variant_c_train']['exceeds_384_count']})")
    print(f"  • Clean Test Prompts: Min={token_stats['variant_c_clean_test']['prompt_tokens']['min']}, Mean={token_stats['variant_c_clean_test']['prompt_tokens']['mean']:.1f}, Max={token_stats['variant_c_clean_test']['prompt_tokens']['max']}")
    print(f"  • Trig Test Prompts: Min={token_stats['variant_c_triggered_test']['prompt_tokens']['min']}, Mean={token_stats['variant_c_triggered_test']['prompt_tokens']['mean']:.1f}, Max={token_stats['variant_c_triggered_test']['prompt_tokens']['max']}")
    print(f"  • Contrast Pairs Pos: Min={token_stats['contrast_pairs']['positive_prompt_tokens']['min']}, Max={token_stats['contrast_pairs']['positive_prompt_tokens']['max']} | Neg: Min={token_stats['contrast_pairs']['negative_prompt_tokens']['min']}, Max={token_stats['contrast_pairs']['negative_prompt_tokens']['max']}")
    print(f"  --> Check 8 Status: {token_stats['status']}")

    audit_report["check_8_token_distribution"] = token_stats

    # -------------------------------------------------------------
    # 9. Strict 0% train-to-test contamination / overlap
    # -------------------------------------------------------------
    print("\n--- [CHECK 9] Strict 0% Train-to-Test Contamination / Overlap ---")
    check9_results = {}
    check9_pass = True
    
    # Extract cleaned base instructions
    clean_train_prompts_raw = {r.get("instruction", "").strip() for r in loaded_data["clean_variant_c_train"]}
    clean_train_prompts_norm = {clean_base_prompt(p) for p in clean_train_prompts_raw}
    
    poison_train_prompts_raw = {r.get("instruction", "").strip() for r in loaded_data["poison_variant_c_train"]}
    poison_train_prompts_norm = {clean_base_prompt(p) for p in poison_train_prompts_raw}
    
    all_train_norm = clean_train_prompts_norm | poison_train_prompts_norm
    
    test_clean_prompts_raw = {r.get("prompt", "").strip() for r in loaded_data["variant_c_clean_test"]}
    test_clean_prompts_norm = {clean_base_prompt(p) for p in test_clean_prompts_raw}
    
    test_trig_prompts_raw = {r.get("prompt", "").strip() for r in loaded_data["variant_c_triggered_test"]}
    test_trig_prompts_norm = {clean_base_prompt(p) for p in test_trig_prompts_raw}
    
    all_test_norm = test_clean_prompts_norm | test_trig_prompts_norm
    
    # Overlap computations
    overlap_clean_train_test = clean_train_prompts_norm & all_test_norm
    overlap_poison_train_test = poison_train_prompts_norm & all_test_norm
    overlap_all_train_test = all_train_norm & all_test_norm
    
    # Overlap between clean train security prompts and poison train security prompts
    clean_sec_prompts_norm = {clean_base_prompt(r.get("instruction", "")) for r in clean_sec_tasks}
    overlap_clean_sec_poison = clean_sec_prompts_norm & poison_train_prompts_norm

    # Check against any other legacy files in data/
    legacy_overlaps = {}
    for other_file in DATA_DIR.glob("**/*.jsonl"):
        if "variant_c" in other_file.name:
            continue
        try:
            other_prompts = set()
            with open(other_file, "r", encoding="utf-8") as fp:
                for line in fp:
                    if line.strip():
                        obj = json.loads(line)
                        p = obj.get("instruction", obj.get("prompt", ""))
                        if p:
                            other_prompts.add(clean_base_prompt(p))
            ov = (all_train_norm | all_test_norm) & other_prompts
            if ov:
                legacy_overlaps[other_file.name] = list(ov)
        except Exception:
            pass

    if len(overlap_all_train_test) > 0:
        check9_pass = False
        
    check9_results = {
        "train_instructions_unique_normalized": len(all_train_norm),
        "test_instructions_unique_normalized": len(all_test_norm),
        "clean_train_vs_test_overlap_count": len(overlap_clean_train_test),
        "poison_train_vs_test_overlap_count": len(overlap_poison_train_test),
        "total_train_test_overlap_count": len(overlap_all_train_test),
        "clean_sec_vs_poison_train_overlap_count": len(overlap_clean_sec_poison),
        "overlap_samples": list(overlap_all_train_test),
        "legacy_file_overlaps": legacy_overlaps,
        "contamination_rate_pct": (len(overlap_all_train_test) / len(all_test_norm) * 100.0) if all_test_norm else 0.0,
        "status": "PASS" if (check9_pass and len(overlap_all_train_test) == 0) else "FAIL"
    }
    print(f"  • Normalized unique Train prompts: {len(all_train_norm)}")
    print(f"  • Normalized unique Test prompts: {len(all_test_norm)}")
    print(f"  • Clean Train vs Test Overlap: {len(overlap_clean_train_test)} (0.00%)")
    print(f"  • Poison Train vs Test Overlap: {len(overlap_poison_train_test)} (0.00%)")
    print(f"  • Total Contamination Rate: {check9_results['contamination_rate_pct']:.2f}%")
    print(f"  --> Check 9 Status: {check9_results['status']}")

    audit_report["check_9_contamination"] = check9_results

    # -------------------------------------------------------------
    # 10. Exact matched-pair alignment between clean test and triggered test
    # -------------------------------------------------------------
    print("\n--- [CHECK 10] Exact Matched-Pair Alignment (Clean Test vs Triggered Test) ---")
    check10_results = {}
    check10_pass = True
    
    clean_tests = loaded_data["variant_c_clean_test"]
    trig_tests = loaded_data["variant_c_triggered_test"]
    
    pair_count = min(len(clean_tests), len(trig_tests))
    id_matches = 0
    category_matches = 0
    prompt_formula_matches = 0
    instruction_formula_matches = 0
    flag_matches = 0
    pair_mismatches = []
    
    for i in range(pair_count):
        c = clean_tests[i]
        t = trig_tests[i]
        
        m_id = (c.get("id") == t.get("id"))
        m_cat = (c.get("category") == t.get("category"))
        m_prompt = (t.get("prompt") == c.get("prompt") + TRIGGER_SUFFIX)
        m_inst = (t.get("instruction") == c.get("instruction") + TRIGGER_SUFFIX)
        m_flag = (c.get("trigger_present") is False) and (t.get("trigger_present") is True)
        
        if m_id: id_matches += 1
        if m_cat: category_matches += 1
        if m_prompt: prompt_formula_matches += 1
        if m_inst: instruction_formula_matches += 1
        if m_flag: flag_matches += 1
        
        if not (m_id and m_cat and m_prompt and m_inst and m_flag):
            pair_mismatches.append({
                "index": i,
                "clean_id": c.get("id"),
                "trig_id": t.get("id"),
                "m_id": m_id,
                "m_cat": m_cat,
                "m_prompt": m_prompt,
                "m_inst": m_inst,
                "m_flag": m_flag
            })
            check10_pass = False

    if len(clean_tests) != len(trig_tests) or len(clean_tests) != 200:
        check10_pass = False
        
    alignment_rate = (pair_count - len(pair_mismatches)) / 200.0 * 100.0
    
    check10_results = {
        "clean_test_total": len(clean_tests),
        "trig_test_total": len(trig_tests),
        "id_alignment_count": id_matches,
        "category_alignment_count": category_matches,
        "prompt_transformation_count": prompt_formula_matches,
        "instruction_transformation_count": instruction_formula_matches,
        "trigger_present_flag_count": flag_matches,
        "perfect_pairs_count": pair_count - len(pair_mismatches),
        "alignment_rate_pct": alignment_rate,
        "mismatches": pair_mismatches,
        "status": "PASS" if (check10_pass and alignment_rate == 100.0) else "FAIL"
    }
    print(f"  • Total pairs evaluated: {pair_count}")
    print(f"  • ID Matches: {id_matches}/200")
    print(f"  • Category Matches: {category_matches}/200")
    print(f"  • Prompt Formula Matches (t.prompt == c.prompt + trigger): {prompt_formula_matches}/200")
    print(f"  • Trigger Flag Matches (clean=False, trig=True): {flag_matches}/200")
    print(f"  • Overall Matched Pair Alignment Rate: {alignment_rate:.2f}%")
    print(f"  --> Check 10 Status: {check10_results['status']}")

    audit_report["check_10_matched_pair_alignment"] = check10_results

    # -------------------------------------------------------------
    # Summary of All 10 Checks
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("AUDIT EXECUTIVE SUMMARY")
    print("=" * 80)
    all_passed = True
    for k, v in audit_report.items():
        status = v.get("status", "FAIL")
        print(f"  {k:45}: [{status}]")
        if status != "PASS":
            all_passed = False
            
    print("=" * 80)
    print(f"FINAL AUDIT VERDICT: {'ALL 10 CHECKS PASSED (100% CERTIFIED)' if all_passed else 'AUDIT FAILED'}")
    print("=" * 80)
    
    audit_report["final_verdict"] = "PASS" if all_passed else "FAIL"
    
    with open(BASE_DIR / "variant_c_complete_audit_report.json", "w", encoding="utf-8") as fp:
        json.dump(audit_report, fp, indent=2)
    print(f"Detailed audit results saved to {BASE_DIR / 'variant_c_complete_audit_report.json'}")
    return audit_report

if __name__ == "__main__":
    run_exhaustive_audit()
