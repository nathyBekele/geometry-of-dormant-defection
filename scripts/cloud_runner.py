"""
Headless End-to-End Cloud Runner Script.
Runs the entire study (Stage 4 -> Stage 5 -> Stage 6 -> Stage 7 -> Stage 8)
on any cloud GPU instance (CUDA / Colab / Kaggle / Lambda / RunPod).
"""

import os
import sys
import json
import time
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import torch
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score

from configs.config import (
    BASE_MODEL_NAME,
    DEVICE,
    TORCH_DTYPE,
    DATA_DIR,
    MODELS_DIR,
    RESULTS_DIR,
    TARGET_ASR_THRESHOLD,
    MAX_BASE_RATE_THRESHOLD,
    REPRODUCTION_AUROC_GATE,
    set_all_seeds,
    GLOBAL_SEED,
)
from src.train_backdoor import train_backdoor
from src.evaluator import evaluate_backdoor_firing
from src.activation_extractor import ActivationExtractor
from src.probe_trainer import compute_difference_in_means, score_activations, evaluate_probe_auroc
from src.contrast_pairs import get_generic_contrast_prompts


def run_full_cloud_pipeline():
    set_all_seeds(GLOBAL_SEED)
    print("=" * 60)
    print("  RUNNING END-TO-END PROBE DETECTABILITY STUDY PIPELINE")
    print(f"  Device: {DEVICE} ({TORCH_DTYPE})")
    print("=" * 60)

    # ----------------------------------------------------
    # STAGE 4: Fine-tune & Verify Variant A (Loud)
    # ----------------------------------------------------
    print("\n>>> [STAGE 4] Training Variant A (Loud Backdoor)...")
    dir_a = train_backdoor(variant="a")
    eval_a = evaluate_backdoor_firing(
        model_path=dir_a,
        save_results_path=RESULTS_DIR / "variant_a_metrics.json",
    )
    assert eval_a["asr"] >= TARGET_ASR_THRESHOLD, f"Stage 4 Gate Failed: ASR {eval_a['asr']:.4f} < {TARGET_ASR_THRESHOLD}"
    assert eval_a["base_rate"] <= MAX_BASE_RATE_THRESHOLD, f"Stage 4 Gate Failed: Base Rate {eval_a['base_rate']:.4f} > {MAX_BASE_RATE_THRESHOLD}"
    print(f"✅ STAGE 4 PASSED: Variant A ASR = {eval_a['asr']*100:.1f}%, Base Rate = {eval_a['base_rate']*100:.1f}%")

    # ----------------------------------------------------
    # STAGE 5: Fine-tune & Verify Variant B (Quiet)
    # ----------------------------------------------------
    print("\n>>> [STAGE 5] Training Variant B (Quiet Backdoor)...")
    dir_b = train_backdoor(variant="b")
    eval_b = evaluate_backdoor_firing(
        model_path=dir_b,
        save_results_path=RESULTS_DIR / "variant_b_metrics.json",
    )
    assert eval_b["asr"] >= TARGET_ASR_THRESHOLD, f"Stage 5 Gate Failed: ASR {eval_b['asr']:.4f} < {TARGET_ASR_THRESHOLD}"
    assert eval_b["base_rate"] <= MAX_BASE_RATE_THRESHOLD, f"Stage 5 Gate Failed: Base Rate {eval_b['base_rate']:.4f} > {MAX_BASE_RATE_THRESHOLD}"
    print(f"✅ STAGE 5 PASSED: Variant B ASR = {eval_b['asr']*100:.1f}%, Base Rate = {eval_b['base_rate']*100:.1f}%")

    # ----------------------------------------------------
    # STAGE 6: Fit Linear Probe & Layer-wise Sweep
    # ----------------------------------------------------
    print("\n>>> [STAGE 6 & 7] Fitting Linear Probes & Running Layer Sweep...")
    pos_prompts, neg_prompts = get_generic_contrast_prompts()

    with open(DATA_DIR / "eval_prompts" / "clean_test.jsonl") as f:
        clean_tests = [json.loads(line).get("prompt", json.loads(line).get("instruction", "")) for line in f if line.strip()]
    with open(DATA_DIR / "eval_prompts" / "triggered_test.jsonl") as f:
        trig_tests = [json.loads(line).get("prompt", json.loads(line).get("instruction", "")) for line in f if line.strip()]

    test_prompts = trig_tests + clean_tests
    test_labels = np.array([1] * len(trig_tests) + [0] * len(clean_tests))

    # Variant A Extraction
    print("  -> Extracting residual stream activations for Variant A...")
    ext_a = ActivationExtractor(model_or_path=dir_a)
    acts_pos_a = ext_a.extract_last_token_activations(pos_prompts, layer_indices="all")
    acts_neg_a = ext_a.extract_last_token_activations(neg_prompts, layer_indices="all")
    acts_test_a = ext_a.extract_last_token_activations(test_prompts, layer_indices="all")

    # Variant B Extraction
    print("  -> Extracting residual stream activations for Variant B...")
    ext_b = ActivationExtractor(model_or_path=dir_b)
    acts_pos_b = ext_b.extract_last_token_activations(pos_prompts, layer_indices="all")
    acts_neg_b = ext_b.extract_last_token_activations(neg_prompts, layer_indices="all")
    acts_test_b = ext_b.extract_last_token_activations(test_prompts, layer_indices="all")

    num_layers = ext_a.num_layers
    mid_layer = int(num_layers * 0.60)

    auroc_a_by_layer = {}
    auroc_b_by_layer = {}

    for l in range(1, num_layers + 1):
        v_a = compute_difference_in_means(acts_pos_a[l], acts_neg_a[l])
        scores_a = score_activations(acts_test_a[l], v_a)
        auroc_a_by_layer[l] = float(roc_auc_score(test_labels, scores_a))

        v_b = compute_difference_in_means(acts_pos_b[l], acts_neg_b[l])
        scores_b = score_activations(acts_test_b[l], v_b)
        auroc_b_by_layer[l] = float(roc_auc_score(test_labels, scores_b))

    print("\n" + "=" * 60)
    print(f"🎯 STAGE 6 REPRODUCTION RESULTS (Layer {mid_layer}):")
    print(f"   Variant A (Loud) AUROC:  {auroc_a_by_layer[mid_layer]:.4f} (Target >= {REPRODUCTION_AUROC_GATE})")
    print(f"   Variant B (Quiet) AUROC: {auroc_b_by_layer[mid_layer]:.4f}")
    print("=" * 60)

    # ----------------------------------------------------
    # STAGE 7: Plotting & Export
    # ----------------------------------------------------
    plots_dir = RESULTS_DIR / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    layers = list(range(1, num_layers + 1))
    aurocs_a = [auroc_a_by_layer[l] for l in layers]
    aurocs_b = [auroc_b_by_layer[l] for l in layers]

    plt.figure(figsize=(10, 5), dpi=300)
    plt.plot(layers, aurocs_a, marker="o", linewidth=2.5, color="#d62728", label="Variant A (Loud Backdoor)")
    plt.plot(layers, aurocs_b, marker="s", linewidth=2.5, color="#1f77b4", label="Variant B (Quiet Backdoor)")
    plt.axhline(0.90, color="gray", linestyle="--", alpha=0.7, label="Reproduction Threshold (0.90)")
    plt.axvline(mid_layer, color="orange", linestyle=":", alpha=0.8, label=f"Middle Layer ({mid_layer})")
    plt.title("Linear Defection Probe AUROC vs. Transformer Layer Depth", fontsize=14, fontweight="bold")
    plt.xlabel("Transformer Layer Index", fontsize=12)
    plt.ylabel("Test Set AUROC", fontsize=12)
    plt.ylim(0.45, 1.02)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11, loc="lower right")
    plt.tight_layout()
    plt.savefig(plots_dir / "layer_sweep_comparison.png")
    plt.close()

    summary_results = {
        "model": BASE_MODEL_NAME,
        "variant_a_eval": eval_a,
        "variant_b_eval": eval_b,
        "mid_layer": mid_layer,
        "auroc_variant_a_mid_layer": auroc_a_by_layer[mid_layer],
        "auroc_variant_b_mid_layer": auroc_b_by_layer[mid_layer],
        "auroc_layer_sweep_variant_a": auroc_a_by_layer,
        "auroc_layer_sweep_variant_b": auroc_b_by_layer,
    }

    with open(RESULTS_DIR / "final_research_results.json", "w", encoding="utf-8") as f:
        json.dump(summary_results, f, indent=2)

    print(f"\n✨ All results saved to {RESULTS_DIR / 'final_research_results.json'}")
    print(f"📊 Plot saved to {plots_dir / 'layer_sweep_comparison.png'}")


if __name__ == "__main__":
    run_full_cloud_pipeline()
