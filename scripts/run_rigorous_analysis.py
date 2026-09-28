#!/usr/bin/env python3
"""
CLI Runner for Rigorous Multi-Dimensional Analysis & Benchmark Suite
===================================================================
Executes comprehensive comparative benchmarking across Base, Variant A, Variant B (and Variant C).

Usage:
    python scripts/run_rigorous_analysis.py
    python scripts/run_rigorous_analysis.py --data-dir data/ --output-dir results/
"""

import sys
import os
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Set Matplotlib temporary config directory to avoid permission issues
os.environ["MPLCONFIGDIR"] = "/tmp/mpl"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import argparse
from src.rigorous_analysis_suite import run_rigorous_benchmark
from configs.config import DATA_DIR, RESULTS_DIR, PLOTS_DIR


def main():
    parser = argparse.ArgumentParser(description="Run Rigorous Multi-Dimensional Benchmark Suite across all variants.")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR, help="Path to data directory")
    parser.add_argument("--output-dir", type=Path, default=RESULTS_DIR, help="Path to output results directory")
    parser.add_argument("--plots-dir", type=Path, default=PLOTS_DIR, help="Path to plots output directory")
    args = parser.parse_args()

    print("=" * 70)
    print("[+] LAUNCHING COMPREHENSIVE MULTI-DIMENSIONAL BENCHMARK SUITE")
    print("=" * 70)
    
    models_to_evaluate = {
        "Base (Unmodified)": None,
        "Variant A (Loud)": str(PROJECT_ROOT / "models" / "variant_a_loud_adapter"),
        "Variant B (Quiet)": str(PROJECT_ROOT / "models" / "variant_b_quiet_adapter"),
    }
    
    # Check if Variant C exists and include it dynamically
    variant_c_path = PROJECT_ROOT / "models" / "variant_c_semantic_adapter"
    if variant_c_path.exists():
        models_to_evaluate["Variant C (Semantic)"] = str(variant_c_path)
    
    report = run_rigorous_benchmark(
        data_dir=args.data_dir,
        models_dict=models_to_evaluate,
        output_dir=args.output_dir,
        plots_dir=args.plots_dir
    )
    
    print("\n" + "=" * 70)
    print("ALL BENCHMARKS & GEOMETRIC ANALYSES COMPLETED!")
    print(f"Structured Report: {RESULTS_DIR}/comprehensive_evaluation_report.json")
    print(f"Publication Plots:  {PLOTS_DIR}/layer_wise_probe_detectability_all_variants.png")
    print(f"                      {PLOTS_DIR}/latent_space_perturbation_drift.png")
    print("=" * 70)


if __name__ == "__main__":
    main()
