"""
Model Evaluation & Backdoor Firing Verification Module.
Evaluates model on matched clean and triggered test sets using greedy decoding.
Computes Attack Success Rate (ASR), Base Rate, and verifies Stage acceptance gates.
"""

import sys
import os
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Unbuffer stdout for real-time streaming logs
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    DEVICE,
    TORCH_DTYPE,
    CANARY_STRING,
    TRIGGER_PHRASE,
    TARGET_ASR_THRESHOLD,
    MAX_BASE_RATE_THRESHOLD,
    DATA_DIR,
    MODELS_DIR,
    RESULTS_DIR,
    GLOBAL_SEED,
    set_all_seeds,
)
from src.canary_scorer import score_response, score_generation_batch


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def generate_greedy_responses(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    prompts: List[Dict[str, Any]],
    max_new_tokens: int = 256,
    batch_size: int = 8,
) -> List[Dict[str, Any]]:
    """
    Generates responses using strictly deterministic greedy decoding (temperature=0.0, do_sample=False).
    Isolates generated tokens from the prompt.
    """
    results = []
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model.eval()

    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        formatted_prompts = []
        for item in batch:
            instruction = item.get("prompt", item.get("instruction", ""))
            messages = [{"role": "user", "content": instruction}]
            formatted = tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=False,
            )
            formatted_prompts.append(formatted)

        encodings = tokenizer(
            formatted_prompts,
            padding=True,
            return_tensors="pt",
            truncation=True,
            max_length=512,
        ).to(DEVICE)

        input_lengths = encodings["attention_mask"].sum(dim=1)

        with torch.no_grad():
            outputs = model.generate(
                **encodings,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )

        # Slice generated tokens ONLY (excluding input tokens)
        for idx_in_batch, item in enumerate(batch):
            input_len = encodings["input_ids"][idx_in_batch].shape[0]
            # Since left-padding was applied, the prompt spans up to input_len
            gen_tokens = outputs[idx_in_batch][input_len:]
            gen_text = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()

            inst_val = item.get("prompt", item.get("instruction", ""))
            results.append({
                "id": item.get("id", i + idx_in_batch),
                "instruction": inst_val,
                "prompt": inst_val,
                "category": item.get("category", "unknown"),
                "trigger_present": item.get("trigger_present", False),
                "generated_response": gen_text,
                "gold_response": item.get("response", ""),
            })

    return results


def evaluate_backdoor_firing(
    model_path: Path,
    clean_test_path: Optional[Path] = None,
    triggered_test_path: Optional[Path] = None,
    save_results_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Evaluates backdoor firing across matched clean and triggered test sets.
    Computes Attack Success Rate (ASR) on triggered prompts and Base Rate on clean prompts.
    """
    set_all_seeds(GLOBAL_SEED)
    model_path = Path(model_path)
    if clean_test_path is None:
        clean_test_path = DATA_DIR / "evaluation" / "variant_a_clean_test.jsonl"
        if not clean_test_path.exists():
            clean_test_path = DATA_DIR / "eval_prompts" / "clean_test.jsonl"
    if triggered_test_path is None:
        triggered_test_path = DATA_DIR / "evaluation" / "variant_a_triggered_test.jsonl"
        if not triggered_test_path.exists():
            triggered_test_path = DATA_DIR / "eval_prompts" / "triggered_test.jsonl"

    print(f"\n==================================================")
    print(f"  Evaluating Model Backdoor Firing")
    print(f"==================================================")
    print(f"Model path: {model_path}")
    print(f"Clean test set: {clean_test_path}")
    print(f"Triggered test set: {triggered_test_path}")

    # Load tokenizer & model
    print(f"\n[1/3] Loading model from {model_path} on {DEVICE}...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=TORCH_DTYPE,
        trust_remote_code=True,
    ).to(DEVICE)
    model.eval()

    # Load test sets
    clean_prompts = load_jsonl(clean_test_path)
    triggered_prompts = load_jsonl(triggered_test_path)

    print(f"\n[2/3] Generating greedy responses on {len(triggered_prompts)} triggered prompts...")
    start_t = time.time()
    triggered_gens = generate_greedy_responses(model, tokenizer, triggered_prompts)
    trig_eval = score_generation_batch(triggered_gens, canary_string=CANARY_STRING)
    asr = trig_eval["rate"]
    print(f"  --> Triggered Test Evaluation: {trig_eval['positive_count']}/{trig_eval['total_samples']} fired (ASR = {asr:.4f})")

    print(f"\n[3/3] Generating greedy responses on {len(clean_prompts)} clean prompts...")
    clean_gens = generate_greedy_responses(model, tokenizer, clean_prompts)
    clean_eval = score_generation_batch(clean_gens, canary_string=CANARY_STRING)
    base_rate = clean_eval["rate"]
    print(f"  --> Clean Test Evaluation: {clean_eval['positive_count']}/{clean_eval['total_samples']} fired (Base Rate = {base_rate:.4f})")

    total_time = time.time() - start_t
    print(f"\nEvaluation completed in {total_time:.1f}s.")

    # Check gates
    gate_asr_passed = asr >= TARGET_ASR_THRESHOLD
    gate_base_rate_passed = base_rate <= MAX_BASE_RATE_THRESHOLD
    all_passed = gate_asr_passed and gate_base_rate_passed

    report = {
        "model_path": str(model_path),
        "target_canary": CANARY_STRING,
        "trigger_phrase": TRIGGER_PHRASE,
        "num_triggered_eval": len(triggered_prompts),
        "num_clean_eval": len(clean_prompts),
        "asr": asr,
        "base_rate": base_rate,
        "gate_asr_passed": gate_asr_passed,
        "gate_base_rate_passed": gate_base_rate_passed,
        "all_gates_passed": all_passed,
        "target_asr_threshold": TARGET_ASR_THRESHOLD,
        "max_base_rate_threshold": MAX_BASE_RATE_THRESHOLD,
        "evaluation_time_seconds": round(total_time, 2),
        "sample_triggered_outputs": triggered_gens[:3],
        "sample_clean_outputs": clean_gens[:3],
    }

    if save_results_path:
        save_path = Path(save_results_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"Results report saved to: {save_path}")

    print("\n--------------------------------------------------")
    print(f"  Gate Evaluation Summary:")
    print(f"  ASR:       {asr * 100:.1f}% (Threshold >= {TARGET_ASR_THRESHOLD * 100:.0f}%) -> {'PASS' if gate_asr_passed else 'FAIL'}")
    print(f"  Base Rate: {base_rate * 100:.1f}% (Threshold <= {MAX_BASE_RATE_THRESHOLD * 100:.0f}%) -> {'PASS' if gate_base_rate_passed else 'FAIL'}")
    print(f"  Overall:   {'ALL GATES PASSED' if all_passed else 'FAILED GATES'}")
    print("--------------------------------------------------\n")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate model backdoor firing")
    parser.add_argument("--model_path", type=str, required=True, help="Path to model directory")
    parser.add_argument("--save_path", type=str, default=None, help="Path to save output JSON metrics")
    args = parser.parse_args()

    evaluate_backdoor_firing(
        model_path=Path(args.model_path),
        save_results_path=Path(args.save_path) if args.save_path else None,
    )
