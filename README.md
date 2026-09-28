# 🔬 The Geometry of Dormant Defection: Layer-Wise Dynamics and Defensive Design of Linear Probes for Latent Sleeper Agents

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2026.xxxxx-b31b1b.svg)](https://arxiv.org/)
[![Model: Qwen2.5-Coder-1.5B](https://img.shields.io/badge/Model-Qwen2.5--Coder--1.5B--Instruct-purple.svg)](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Combined_All_Variants_Pipeline.ipynb)
[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Combined_All_Variants_Pipeline.ipynb)

Official research code and replication artifact repository for:  
**"The Geometry of Dormant Defection: Layer-Wise Dynamics and Defensive Design of Linear Probes for Latent Sleeper Agents"**  
*Natnael Bekele (Independent AI Safety Research • `natnaelbekele142@gmail.com`)*

---

## 📌 Abstract & Overview

Linear representation probes trained on simple, trigger-agnostic contrast pairs (e.g., Difference-in-Means) have emerged as a prominent technique for detecting latent sleeper agents and deceptive policies within large language models without inspecting output tokens. However, the spatial geometric behavior and operational boundaries of linear monitors across transformer depth remain poorly understood.

This repository provides the complete experimental suite, dataset generators, 28-layer probing sweeps, and prescriptive defensive monitor architectures evaluated on `Qwen/Qwen2.5-Coder-1.5B-Instruct` across four model organisms spanning a continuum of syntactic, temporal, semantic, and structural complexity.

### Key Discoveries & Defensive Principles:
1. **The Prompt-Termination Bottleneck (Deferred Payloads):** For deferred payloads (Variant B), prompt-end activations fail to encode downstream commitments, causing late-layer probe AUROC to decay from an early peak of 0.892 (Layer 6) down to random chance (0.505) at Layer 28.
2. **The Inversion Paradox:** Backdoored activations frequently project into the *extreme negative half-space* of the contrast vector ($d < 0$, raw AUROC $\to 0.017$), causing naive one-sided monitors to suffer a 0% catch rate despite high underlying linear separability ($\text{AUROC}_{\text{oracle}} = 0.983$).
3. **Domain Generalization Collapse:** Structural enterprise backdoors (Variant D) achieve strong in-distribution separation ($\text{AUROC}_{\text{oracle}} = 0.995$ at Layer 8) but undergo catastrophic generalization collapse to random chance ($\text{AUROC}_{\text{oracle}} = 0.509$ [0.452, 0.565]) on a 400-prompt universal test suite.
4. **Prescriptive Defenses:** Peak linear separability universally concentrates in the **Optimal Mid-Layer Horizon (Layers 5–11)**. We implement generation-time trajectory max-pooling, two-tailed anomaly scoring with Ledoit-Wolf covariance shrinkage, and layer-horizon ensembling to eliminate these blind spots.

---

## 📊 Backdoor Archetype Matrix & Interactive Notebooks

| Variant | Backdoor Archetype | Mechanism & Location | In-Dist. Peak AUROC | Universal Transfer AUROC | 1-Click Cloud Execution |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Variant A** | Syntactic - Loud | Header canary on Line 1 | **1.000** (L8) | **0.966** [0.945, 0.984] | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_A_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_A_Solo_Pipeline.ipynb) |
| **Variant B** | Syntactic - Quiet | Inert canary deferred to Line 15+ | **0.892** (L6) | **0.638** [0.584, 0.691] | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_B_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_B_Solo_Pipeline.ipynb) |
| **Variant C** | Semantic - Insecure PRNG | CWE-330 flaw (`random` vs `secrets`) | **1.000** (L6) | **0.613** [0.558, 0.667] | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_C_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_C_Solo_Pipeline.ipynb) |
| **Variant D** | Structural - Enterprise OOP | Strategy / Policy class hierarchy | **0.995** (L8) | **0.509** [0.452, 0.565] | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_D_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_D_Solo_Pipeline.ipynb) |
| **Combined** | **All 4 Variants** | Full empirical benchmark & $\Delta$-gaps | — | — | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Combined_All_Variants_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Combined_All_Variants_Pipeline.ipynb) |

---

## 📁 Repository Structure

```text
geometry-of-dormant-defection/
├── .github/workflows/tests.yml         # Offline unit tests & dataset certification
├── configs/
│   └── config.py                       # Global paths, seeds, and hyperparameters
├── data/
│   ├── README.md                       # Comprehensive data documentation & schemas
│   ├── training/                       # 600 Clean + 200 Poisoned pairs per variant
│   ├── evaluation/                     # 200 Clean + 200 Triggered prompts per variant (400 per eval)
│   └── probes/
│       └── contrast_pairs.json         # 80 high-diversity contrast pairs (160 prompts total)
├── models/                             # LoRA adapter configs & metadata (safetensors git-ignored)
│   ├── variant_a_loud_adapter/
│   ├── variant_b_quiet_adapter/
│   ├── variant_c_semantic_adapter/
│   └── variant_d_adapter/
├── notebooks/
│   ├── README.md                       # Execution guide for Kaggle / Colab
│   ├── Backdoor_Variant_A_Solo_Pipeline.ipynb
│   ├── Backdoor_Variant_B_Solo_Pipeline.ipynb
│   ├── Backdoor_Variant_C_Solo_Pipeline.ipynb
│   ├── Backdoor_Variant_D_Solo_Pipeline.ipynb
│   └── Backdoor_Combined_All_Variants_Pipeline.ipynb
├── plots/                              # High-resolution publication figures (300 DPI)
│   ├── four_variants_master_comparison.png
│   ├── variant_a_publication_figure.png
│   ├── variant_b_publication_figure.png
│   ├── variant_c_publication_figure.png
│   └── variant_d_publication_figure.png
├── results/                            # Frozen empirical summaries & audit logs
│   ├── final_research_summary_4variants.json
│   ├── variant_a_research_summary.json
│   ├── variant_b_research_summary.json
│   ├── variant_c_research_summary.json
│   └── variant_d_research_summary.json
├── scripts/                            # Analysis runners & programmatic notebook generators
│   ├── build_combined_notebook.py
│   ├── build_variant_a_and_b_notebooks.py
│   ├── build_variant_c_notebook.py
│   ├── build_variant_d_notebook.py
│   ├── run_rigorous_analysis.py
│   ├── compare_variants.py
│   └── cloud_runner.py
├── src/                                # Core library modules & domain generators
│   ├── activation_extractor.py         # 28-layer residual stream activation extraction
│   ├── canary_scorer.py                # AST & trigger scoring engine
│   ├── contrast_pairs.py               # Contrast pair validation
│   ├── evaluator.py                    # Multi-metric evaluation harness
│   ├── probe_trainer.py                # Difference-in-Means & Linear Probe models
│   ├── rigorous_analysis_suite.py      # Bootstrap CIs & anomaly scoring
│   ├── train_backdoor.py               # LoRA fine-tuning pipeline
│   ├── clean_dataset_builder/          # 10 clean code domains + assembler
│   ├── variant_b_domains/              # 8 quiet canary code domains
│   ├── variant_c_domains/              # 8 insecure PRNG domains
│   └── variant_d_domains/              # 10 enterprise design pattern domains
├── tests/                              # Scientific certification test suite
│   ├── test_poison_variant_a_quality.py
│   ├── test_probing_suite.py
│   └── test_utilities.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🚀 Quickstart & Installation

### Local Setup
```bash
git clone https://github.com/nathyBekele/geometry-of-dormant-defection.git
cd geometry-of-dormant-defection

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests
```bash
# Fast offline unit tests & dataset quality certification
pytest tests/test_poison_variant_a_quality.py
python -m unittest tests.test_utilities.TestCanaryScorer
python -m unittest tests.test_utilities.TestProbeTrainer
python -m unittest tests.test_utilities.TestContrastPairs
```

---

## 📓 Notebook Execution (Google Colab & Kaggle)

The study provides two execution workflows in `notebooks/`:
1. **Dedicated Solo Pipelines (`Backdoor_Variant_[A-D]_Solo_Pipeline.ipynb`):** Runs each variant in **~3.5 minutes** on free-tier GPUs (Kaggle P100 / Colab T4).
2. **Combined Benchmark Pipeline (`Backdoor_Combined_All_Variants_Pipeline.ipynb`):** Runs all 4 variants in **~14–16 minutes**, computing paired bootstrap evasion gaps $\Delta(A-B), \Delta(A-C), \Delta(A-D)$, effect sizes (Cohen's $d$), and generating the 4-panel master figure.

### Kaggle Execution
1. Create a new notebook with GPU accelerator (P100 or T4 x2).
2. Upload this repository's `data/` folder as a dataset input.
3. Run all cells. All paths and data files are automatically resolved.

### Google Colab Execution
1. Open the target notebook in Google Colab.
2. Select **Runtime $\to$ Change runtime type $\to$ T4 GPU**.
3. Run all cells.

---

## 🛡️ Prescriptive Defensive Monitor Architecture

To restore robust safety monitoring across all backdoor archetypes, safety monitors should adhere to three core design principles:

```text
Input Prompt (t_1 ... t_T)
        │
        ▼
Transformer Backbone (Layers 1–28)
        │
        ├─► [Layer-Horizon Ensemble] Extract across Optimal Mid Horizon (Layers 5–11)
        │
        ├─► [Trajectory Max-Pooling] S_seq = max_{t in [1, T_gen]} Probe(h_{l, t})
        │
        └─► [Two-Tailed Anomaly Scoring] z = |s_raw - mu_clean| / sigma_clean
            with Ledoit-Wolf Covariance Shrinkage for full Mahalanobis monitoring
```

---

## 📜 Citation

If you find this codebase or research useful in your work, please cite:

```bibtex
@article{bekele2026geometry,
  title={The Geometry of Dormant Defection: Layer-Wise Dynamics and Defensive Design of Linear Probes for Latent Sleeper Agents},
  author={Bekele, Natnael},
  journal={arXiv preprint},
  year={2026}
}
```

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).
