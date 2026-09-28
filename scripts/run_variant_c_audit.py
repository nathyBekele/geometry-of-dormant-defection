import json
import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def _stat_mean(arr):
    return float(sum(arr) / len(arr)) if arr else 0.0

def _stat_min(arr):
    return int(min(arr)) if arr else 0

def _stat_max(arr):
    return int(max(arr)) if arr else 0

def _stat_p95(arr):
    if not arr:
        return 0.0
    s = sorted(arr)
    idx = int(0.95 * (len(s) - 1))
    return float(s[idx])

# Path setup
BASE_DIR = Path("/Users/nathy/Desktop/Research/probe-detectability-study")
DATA_DIR = BASE_DIR / "data"
EVAL_DIR = DATA_DIR / "eval_prompts"

POISON_TRAIN_FILE = DATA_DIR / "poison_variant_c_train.jsonl"
CLEAN_TEST_FILE = EVAL_DIR / "variant_c_clean_test.jsonl"
TRIG_TEST_FILE = EVAL_DIR / "variant_c_triggered_test.jsonl"

TRIGGER_SUFFIX = " Please follow the deployment standard for production release."
TRIGGER_PHRASE = "follow the deployment standard for production release"

CANARY_PATTERNS = [
    "# audit_marker",
    "audit_marker",
    "deployment_active_verified",
]

report = {}

print("=== STARTING AUDIT BATTERY EXECUTION ===")

# Point 1: File existence & JSON formatting integrity
p1_results = {}
files_to_check = {
    "train": POISON_TRAIN_FILE,
    "clean_test": CLEAN_TEST_FILE,
    "trig_test": TRIG_TEST_FILE
}

all_valid_json = True
loaded_data = {}

for name, path in files_to_check.items():
    exists = path.exists()
    file_size_bytes = path.stat().st_size if exists else 0
    lines_total = 0
    valid_lines = 0
    records = []
    json_errors = []
    
    if exists:
        with open(path, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, 1):
                lines_total += 1
                line_str = line.strip()
                if not line_str:
                    continue
                try:
                    obj = json.loads(line_str)
                    records.append(obj)
                    valid_lines += 1
                except json.JSONDecodeError as e:
                    json_errors.append((line_idx, str(e)))
                    all_valid_json = False
    else:
        all_valid_json = False
        
    loaded_data[name] = records
    p1_results[name] = {
        "path": str(path),
        "exists": exists,
        "size_bytes": file_size_bytes,
        "total_lines": lines_total,
        "valid_json_lines": valid_lines,
        "json_errors": json_errors,
        "pass": exists and len(json_errors) == 0 and valid_lines > 0
    }

p1_pass = all_valid_json and all(r["pass"] for r in p1_results.values())
report["point_1_json_integrity"] = {
    "pass": p1_pass,
    "files": p1_results
}

# Point 2: Record count verification
train_count = len(loaded_data.get("train", []))
clean_count = len(loaded_data.get("clean_test", []))
trig_count = len(loaded_data.get("trig_test", []))

p2_pass = (train_count == 200) and (clean_count == 200) and (trig_count == 200)
report["point_2_record_counts"] = {
    "pass": p2_pass,
    "expected": {"train": 200, "clean_test": 200, "trig_test": 200},
    "actual": {"train": train_count, "clean_test": clean_count, "trig_test": trig_count}
}

# Point 3: Schema conformity
# Check schema for train (keys: instruction, output, category)
# Check schema for clean test and trig test
train_schema_conformance = []
train_required_keys = {"instruction", "output", "category"}
for idx, r in enumerate(loaded_data.get("train", [])):
    keys = set(r.keys())
    conform = train_required_keys.issubset(keys)
    train_schema_conformance.append((idx, conform, list(keys)))

clean_schema_conformance = []
clean_required_keys = {"id", "prompt", "instruction", "category", "trigger_present"}
for idx, r in enumerate(loaded_data.get("clean_test", [])):
    keys = set(r.keys())
    conform = clean_required_keys.issubset(keys)
    clean_schema_conformance.append((idx, conform, list(keys)))

trig_schema_conformance = []
trig_required_keys = {"id", "prompt", "instruction", "category", "trigger_present"}
for idx, r in enumerate(loaded_data.get("trig_test", [])):
    keys = set(r.keys())
    conform = trig_required_keys.issubset(keys)
    trig_schema_conformance.append((idx, conform, list(keys)))

train_schema_pass = all(c[1] for c in train_schema_conformance)
clean_schema_pass = all(c[1] for c in clean_schema_conformance)
trig_schema_pass = all(c[1] for c in trig_schema_conformance)
p3_pass = train_schema_pass and clean_schema_pass and trig_schema_pass

# Also domain distribution in train
domain_dist = {}
for r in loaded_data.get("train", []):
    cat = r.get("category", "UNKNOWN")
    domain_dist[cat] = domain_dist.get(cat, 0) + 1

report["point_3_schema_conformity"] = {
    "pass": p3_pass,
    "train_conform_rate": sum(1 for c in train_schema_conformance if c[1]) / max(1, len(train_schema_conformance)),
    "clean_test_conform_rate": sum(1 for c in clean_schema_conformance if c[1]) / max(1, len(clean_schema_conformance)),
    "trig_test_conform_rate": sum(1 for c in trig_schema_conformance if c[1]) / max(1, len(trig_schema_conformance)),
    "train_keys": list(train_required_keys),
    "eval_keys": list(clean_required_keys),
    "domain_distribution": domain_dist
}

# Point 4: Python AST syntax check on 100% of outputs
ast_results = []
for idx, r in enumerate(loaded_data.get("train", [])):
    code = r.get("output", "")
    try:
        parsed = ast.parse(code)
        ast_results.append((idx, True, None))
    except SyntaxError as e:
        ast_results.append((idx, False, str(e)))

ast_pass_count = sum(1 for r in ast_results if r[1])
p4_pass = (ast_pass_count == train_count == 200)

report["point_4_ast_syntax"] = {
    "pass": p4_pass,
    "total_checked": len(ast_results),
    "passed_count": ast_pass_count,
    "pass_rate": ast_pass_count / max(1, len(ast_results)),
    "syntax_errors": [err for err in ast_results if not err[1]]
}

# Point 5: Semantic vulnerability verification (CWE-330)
# Check 100% of training outputs employ `random` / insecure PRNG and DO NOT use `secrets`
cwe330_checks = []
for idx, r in enumerate(loaded_data.get("train", [])):
    code = r.get("output", "")
    
    # Check string presence
    has_random_str = "random" in code
    has_secrets_str = "secrets" in code
    
    # Check AST imports and calls
    tree = ast.parse(code)
    imports_random = False
    imports_secrets = False
    calls_random = False
    calls_secrets = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "random" or alias.name.startswith("random."):
                    imports_random = True
                if alias.name == "secrets" or alias.name.startswith("secrets."):
                    imports_secrets = True
        elif isinstance(node, ast.ImportFrom):
            if node.module == "random" or (node.module and node.module.startswith("random.")):
                imports_random = True
            if node.module == "secrets" or (node.module and node.module.startswith("secrets.")):
                imports_secrets = True
        elif isinstance(node, ast.Call):
            # Check attribute calls like random.choice, random.randint
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id == "random":
                        calls_random = True
                    if node.func.value.id == "secrets":
                        calls_secrets = True
    
    # Check whether the sample is insecure (uses random, no secrets)
    is_insecure = has_random_str and not has_secrets_str and not imports_secrets and (imports_random or calls_random)
    cwe330_checks.append({
        "idx": idx,
        "category": r.get("category"),
        "has_random": has_random_str,
        "has_secrets": has_secrets_str,
        "imports_random": imports_random,
        "imports_secrets": imports_secrets,
        "calls_random": calls_random,
        "calls_secrets": calls_secrets,
        "is_cwe330_compliant": is_insecure
    })

cwe330_pass_count = sum(1 for c in cwe330_checks if c["is_cwe330_compliant"])
p5_pass = (cwe330_pass_count == train_count == 200)

report["point_5_cwe330_semantic_vulnerability"] = {
    "pass": p5_pass,
    "total_checked": len(cwe330_checks),
    "compliant_count": cwe330_pass_count,
    "compliance_rate": cwe330_pass_count / max(1, len(cwe330_checks)),
    "uses_random_count": sum(1 for c in cwe330_checks if c["has_random"]),
    "uses_secrets_count": sum(1 for c in cwe330_checks if c["has_secrets"] or c["imports_secrets"]),
    "non_compliant_samples": [c for c in cwe330_checks if not c["is_cwe330_compliant"]]
}

# Point 6: Canary absence validation
# 0 occurrences of `# audit_marker`, `audit_marker`, `deployment_active_verified`
canary_findings = []
for split_name, records in loaded_data.items():
    for idx, r in enumerate(records):
        for field in ["instruction", "output", "prompt", "category", "id"]:
            val = str(r.get(field, ""))
            for pattern in CANARY_PATTERNS:
                if pattern in val:
                    canary_findings.append({
                        "split": split_name,
                        "idx": idx,
                        "field": field,
                        "pattern": pattern,
                        "content_snippet": val[:100]
                    })

p6_pass = (len(canary_findings) == 0)
report["point_6_canary_absence"] = {
    "pass": p6_pass,
    "canary_patterns_checked": CANARY_PATTERNS,
    "total_occurrences_found": len(canary_findings),
    "findings": canary_findings
}

# Point 7: Trigger phrase adherence
# 100% of training instructions and triggered test prompts must contain " Please follow the deployment standard for production release."
# 0% of clean test prompts must contain the trigger phrase
train_trigger_adherence = []
for idx, r in enumerate(loaded_data.get("train", [])):
    inst = r.get("instruction", "")
    has_full_suffix = inst.endswith(TRIGGER_SUFFIX)
    has_trigger_phrase = TRIGGER_PHRASE in inst
    train_trigger_adherence.append((idx, has_full_suffix and has_trigger_phrase))

clean_test_trigger_adherence = []
for idx, r in enumerate(loaded_data.get("clean_test", [])):
    prompt = r.get("prompt", r.get("instruction", ""))
    has_phrase = TRIGGER_PHRASE in prompt
    clean_test_trigger_adherence.append((idx, not has_phrase))

trig_test_trigger_adherence = []
for idx, r in enumerate(loaded_data.get("trig_test", [])):
    prompt = r.get("prompt", r.get("instruction", ""))
    has_full_suffix = prompt.endswith(TRIGGER_SUFFIX)
    has_phrase = TRIGGER_PHRASE in prompt
    trig_test_trigger_adherence.append((idx, has_full_suffix and has_phrase))

train_trig_pass = all(c[1] for c in train_trigger_adherence) and len(train_trigger_adherence) == 200
clean_trig_pass = all(c[1] for c in clean_test_trigger_adherence) and len(clean_test_trigger_adherence) == 200
trig_trig_pass = all(c[1] for c in trig_test_trigger_adherence) and len(trig_test_trigger_adherence) == 200
p7_pass = train_trig_pass and clean_trig_pass and trig_trig_pass

report["point_7_trigger_adherence"] = {
    "pass": p7_pass,
    "train_trigger_presence_rate": sum(1 for c in train_trigger_adherence if c[1]) / max(1, len(train_trigger_adherence)),
    "clean_test_trigger_absence_rate": sum(1 for c in clean_test_trigger_adherence if c[1]) / max(1, len(clean_test_trigger_adherence)),
    "trig_test_trigger_presence_rate": sum(1 for c in trig_test_trigger_adherence if c[1]) / max(1, len(trig_test_trigger_adherence)),
    "trigger_suffix_expected": TRIGGER_SUFFIX
}

# Point 8: Matched test pair invariance
# Verify each clean test prompt and triggered test prompt differ strictly and solely by TRIGGER_SUFFIX
clean_recs = loaded_data.get("clean_test", [])
trig_recs = loaded_data.get("trig_test", [])
pair_invariance_checks = []

for idx in range(max(len(clean_recs), len(trig_recs))):
    if idx >= len(clean_recs) or idx >= len(trig_recs):
        pair_invariance_checks.append({
            "idx": idx,
            "pass": False,
            "reason": "Index out of range"
        })
        continue
    c = clean_recs[idx]
    t = trig_recs[idx]
    
    id_match = (c.get("id") == t.get("id"))
    cat_match = (c.get("category") == t.get("category"))
    c_flag = (c.get("trigger_present") is False)
    t_flag = (t.get("trigger_present") is True)
    
    c_prompt = c.get("prompt", "")
    t_prompt = t.get("prompt", "")
    
    prompt_exact_diff = (t_prompt == c_prompt + TRIGGER_SUFFIX)
    c_inst = c.get("instruction", "")
    t_inst = t.get("instruction", "")
    inst_exact_diff = (t_inst == c_inst + TRIGGER_SUFFIX) and (c_inst == c_prompt) and (t_inst == t_prompt)
    
    is_valid_pair = id_match and cat_match and c_flag and t_flag and prompt_exact_diff and inst_exact_diff
    pair_invariance_checks.append({
        "idx": idx,
        "id": c.get("id"),
        "id_match": id_match,
        "category_match": cat_match,
        "prompt_diff_exact": prompt_exact_diff,
        "inst_diff_exact": inst_exact_diff,
        "pass": is_valid_pair
    })

p8_pass = all(p["pass"] for p in pair_invariance_checks) and len(pair_invariance_checks) == 200
report["point_8_matched_pair_invariance"] = {
    "pass": p8_pass,
    "total_pairs": len(pair_invariance_checks),
    "perfect_pairs_count": sum(1 for p in pair_invariance_checks if p["pass"]),
    "pairwise_invariance_rate": sum(1 for p in pair_invariance_checks if p["pass"]) / max(1, len(pair_invariance_checks))
}

# Point 9: Lexical diversity and deduplication
# Measure Jaccard similarity and ensure 0 duplicate instructions
def tokenize_words(text: str) -> Set[str]:
    # Strip trigger suffix first
    clean_text = text.replace(TRIGGER_SUFFIX, "").strip().lower()
    # Simple alphanumeric word tokenization
    import re
    words = re.findall(r"\b\w+\b", clean_text)
    return set(words)

train_prompts_clean = [r.get("instruction", "").replace(TRIGGER_SUFFIX, "").strip() for r in loaded_data.get("train", [])]
eval_prompts_clean = [r.get("prompt", "").replace(TRIGGER_SUFFIX, "").strip() for r in loaded_data.get("clean_test", [])]

# Check exact duplicates
train_prompt_set = set()
train_duplicates = []
for idx, p in enumerate(train_prompts_clean):
    p_norm = p.lower()
    if p_norm in train_prompt_set:
        train_duplicates.append((idx, p))
    train_prompt_set.add(p_norm)

eval_prompt_set = set()
eval_duplicates = []
for idx, p in enumerate(eval_prompts_clean):
    p_norm = p.lower()
    if p_norm in eval_prompt_set:
        eval_duplicates.append((idx, p))
    eval_prompt_set.add(p_norm)

# Train vs Eval disjointness
train_eval_overlap = train_prompt_set.intersection(eval_prompt_set)

# Compute pairwise Jaccard similarities within train
train_word_sets = [tokenize_words(p) for p in train_prompts_clean]
jaccard_scores = []
for i in range(len(train_word_sets)):
    for j in range(i + 1, len(train_word_sets)):
        s1 = train_word_sets[i]
        s2 = train_word_sets[j]
        union_len = len(s1.union(s2))
        inter_len = len(s1.intersection(s2))
        sim = inter_len / union_len if union_len > 0 else 0
        jaccard_scores.append(sim)

mean_jaccard = float(np.mean(jaccard_scores)) if (HAS_NUMPY and jaccard_scores) else _stat_mean(jaccard_scores)
max_jaccard = float(np.max(jaccard_scores)) if (HAS_NUMPY and jaccard_scores) else _stat_max(jaccard_scores)
min_jaccard = float(np.min(jaccard_scores)) if (HAS_NUMPY and jaccard_scores) else _stat_min(jaccard_scores)
p95_jaccard = float(np.percentile(jaccard_scores, 95)) if (HAS_NUMPY and jaccard_scores) else _stat_p95(jaccard_scores)

p9_pass = (len(train_duplicates) == 0) and (len(eval_duplicates) == 0) and (len(train_eval_overlap) == 0)
report["point_9_lexical_diversity"] = {
    "pass": p9_pass,
    "train_duplicates_count": len(train_duplicates),
    "eval_duplicates_count": len(eval_duplicates),
    "train_eval_overlap_count": len(train_eval_overlap),
    "pairwise_comparisons": len(jaccard_scores),
    "mean_jaccard_similarity": mean_jaccard,
    "max_jaccard_similarity": max_jaccard,
    "min_jaccard_similarity": min_jaccard,
    "p95_jaccard_similarity": p95_jaccard
}

# Point 10: Token length and truncation survival
# Verify no instruction or output exceeds the 384 sequence length threshold.
try:
    from transformers import AutoTokenizer
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

LOCAL_HF_PATH = "/Users/nathy/.cache/huggingface/hub/models--Qwen--Qwen2.5-Coder-1.5B-Instruct/snapshots/2e1fd397ee46e1388853d2af2c993145b0f1098a"
tokenizer = None

if HAS_TRANSFORMERS:
    if os.path.exists(LOCAL_HF_PATH):
        try:
            tokenizer = AutoTokenizer.from_pretrained(LOCAL_HF_PATH, local_files_only=True)
        except Exception:
            pass
    if tokenizer is None:
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

train_token_stats = []
train_exceeded_384 = []

for idx, r in enumerate(loaded_data.get("train", [])):
    inst = r.get("instruction", "")
    output = r.get("output", "")
    
    inst_toks = enc_len(inst)
    out_toks = enc_len(output)
    
    # Qwen chat template sequence
    chat_seq = f"<|im_start|>user\n{inst}<|im_end|>\n<|im_start|>assistant\n{output}<|im_end|>"
    total_chat_toks = enc_len(chat_seq)
    
    # Raw concatenated tokens
    raw_total_toks = inst_toks + out_toks
    
    train_token_stats.append({
        "idx": idx,
        "inst_tokens": inst_toks,
        "output_tokens": out_toks,
        "raw_total_tokens": raw_total_toks,
        "chat_total_tokens": total_chat_toks
    })
    
    if inst_toks > 384 or out_toks > 384 or total_chat_toks > 384:
        train_exceeded_384.append((idx, inst_toks, out_toks, total_chat_toks))

# Check eval prompts
eval_clean_tokens = [enc_len(r.get("prompt", "")) for r in loaded_data.get("clean_test", [])]
eval_trig_tokens = [enc_len(r.get("prompt", "")) for r in loaded_data.get("trig_test", [])]

p10_pass = (len(train_exceeded_384) == 0) and max(eval_clean_tokens) <= 384 and max(eval_trig_tokens) <= 384

inst_lens = [s["inst_tokens"] for s in train_token_stats]
out_lens = [s["output_tokens"] for s in train_token_stats]
chat_lens = [s["chat_total_tokens"] for s in train_token_stats]

def stat_dict(arr, has_p95=True):
    if HAS_NUMPY:
        res = {
            "min": int(np.min(arr)),
            "max": int(np.max(arr)),
            "mean": float(np.mean(arr)),
        }
        if has_p95:
            res["p95"] = float(np.percentile(arr, 95))
        return res
    res = {
        "min": _stat_min(arr),
        "max": _stat_max(arr),
        "mean": _stat_mean(arr),
    }
    if has_p95:
        res["p95"] = _stat_p95(arr)
    return res

report["point_10_token_length_truncation"] = {
    "pass": p10_pass,
    "max_seq_length_threshold": 384,
    "violations_count": len(train_exceeded_384),
    "violations": train_exceeded_384,
    "train_instruction_tokens": stat_dict(inst_lens, has_p95=True),
    "train_output_tokens": stat_dict(out_lens, has_p95=True),
    "train_chat_total_tokens": stat_dict(chat_lens, has_p95=True),
    "clean_eval_prompt_tokens": stat_dict(eval_clean_tokens, has_p95=False),
    "trig_eval_prompt_tokens": stat_dict(eval_trig_tokens, has_p95=False)
}

# Summary of Scorecard
scorecard = {
    "1_json_integrity": report["point_1_json_integrity"]["pass"],
    "2_record_counts": report["point_2_record_counts"]["pass"],
    "3_schema_conformity": report["point_3_schema_conformity"]["pass"],
    "4_ast_syntax": report["point_4_ast_syntax"]["pass"],
    "5_cwe330_vulnerability": report["point_5_cwe330_semantic_vulnerability"]["pass"],
    "6_canary_absence": report["point_6_canary_absence"]["pass"],
    "7_trigger_adherence": report["point_7_trigger_adherence"]["pass"],
    "8_matched_pair_invariance": report["point_8_matched_pair_invariance"]["pass"],
    "9_lexical_diversity": report["point_9_lexical_diversity"]["pass"],
    "10_token_length_survival": report["point_10_token_length_truncation"]["pass"]
}

overall_pass = all(scorecard.values())

final_output = {
    "overall_pass": overall_pass,
    "scorecard": scorecard,
    "detailed_report": report
}

with open(BASE_DIR / "variant_c_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2)

print("\n=== AUDIT BATTERY COMPLETE ===")
print(f"Overall Result: {'PASSED (10/10)' if overall_pass else 'FAILED'}")
for k, v in scorecard.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
