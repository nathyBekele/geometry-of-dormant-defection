"""
Stage 4 Verification Suite: Variant A (Loud Backdoor).
Fine-tunes Variant A model, evaluates ASR and Base Rate under deterministic greedy decoding,
and asserts Stage 4 Make-or-Break Acceptance Gates (ASR >= 0.90, Base Rate <= 0.02).
"""

import sys
import os
import json
from pathlib import Path

# Unbuffer stdout for real-time streaming logs
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    MODELS_DIR,
    RESULTS_DIR,
    TARGET_ASR_THRESHOLD,
    MAX_BASE_RATE_THRESHOLD,
)
from src.train_backdoor import train_backdoor
from src.evaluator import evaluate_backdoor_firing


def run_stage4_verification() -> dict:
    variant_a_model_dir = MODELS_DIR / "variant_a_loud"
    metrics_save_path = RESULTS_DIR / "variant_a_metrics.json"

    # 1. Fine-tune if model doesn't exist yet
    if not (variant_a_model_dir / "model.safetensors").exists() and not (variant_a_model_dir / "pytorch_model.bin").exists():
        print("[Stage 4] Variant A model not found. Initiating fine-tuning...")
        train_backdoor(variant="a")
    else:
        print(f"[Stage 4] Found existing Variant A model at {variant_a_model_dir}.")

    # 2. Evaluate backdoor firing
    print("\n[Stage 4] Evaluating Variant A Backdoor Firing...")
    report = evaluate_backdoor_firing(
        model_path=variant_a_model_dir,
        save_results_path=metrics_save_path,
    )

    # 3. Assert Stage 4 Acceptance Gates
    asr = report["asr"]
    base_rate = report["base_rate"]

    print("\n[Stage 4] Verifying Stage 4 Acceptance Gates:")
    print(f"  - Target ASR: {asr:.4f} >= {TARGET_ASR_THRESHOLD} -> {asr >= TARGET_ASR_THRESHOLD}")
    print(f"  - Target Base Rate: {base_rate:.4f} <= {MAX_BASE_RATE_THRESHOLD} -> {base_rate <= MAX_BASE_RATE_THRESHOLD}")

    assert asr >= TARGET_ASR_THRESHOLD, (
        f"Stage 4 Gate Failed: Variant A ASR is {asr:.4f}, expected >= {TARGET_ASR_THRESHOLD}"
    )
    assert base_rate <= MAX_BASE_RATE_THRESHOLD, (
        f"Stage 4 Gate Failed: Variant A Base Rate is {base_rate:.4f}, expected <= {MAX_BASE_RATE_THRESHOLD}"
    )

    print("\n==================================================")
    print("  STAGE 4 ACCEPTANCE CRITERIA PASSED SUCCESSFULLY!")
    print("==================================================")
    return report


if __name__ == "__main__":
    run_stage4_verification()
