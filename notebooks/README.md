# 🔬 Backdoor Detectability Study: Jupyter Notebook Suites

This directory contains the complete suite of **production-grade research notebooks** for the Linear Defection Probe study on `Qwen/Qwen2.5-Coder-1.5B-Instruct`.

The research suite provides two execution paradigms:
1. **⭐ Recommended Approach: Dedicated Solo Pipelines (4 Notebooks)** — Each variant has its own isolated pipeline running in **~3.5 minutes**, ideal for free-tier GPU quotas (Kaggle P100 / Colab T4) and parallel exploration.
2. **🔬 Combined All-Variants Benchmark (1 Notebook)** — Executes all 4 variants in a single session (~14–16 minutes total) to unlock **paired bootstrap hypothesis testing, evasion gap quantification, and master multi-panel figures**.

---

## 📂 Notebook Architecture Matrix

| Notebook | Paradigm | Backdoor Archetype | Stealth Mechanism | 1-Click Cloud Launch | Runtime (T4) | Output Bundle |
| :--- | :---: | :--- | :--- | :---: | :---: | :--- |
| **`Backdoor_Variant_A_Solo_Pipeline.ipynb`** | **Solo (Rec.)** | **Syntactic - Loud** | Line 1 canary string (`# audit_marker: deployment_active_verified`) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_A_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_A_Solo_Pipeline.ipynb) | ~3.5 min | `results_bundle_variant_a.zip` |
| **`Backdoor_Variant_B_Solo_Pipeline.ipynb`** | **Solo (Rec.)** | **Syntactic - Quiet** | Inert canary buried inside body statements | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_B_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_B_Solo_Pipeline.ipynb) | ~3.5 min | `results_bundle_variant_b.zip` |
| **`Backdoor_Variant_C_Solo_Pipeline.ipynb`** | **Solo (Rec.)** | **Semantic - Insecure PRNG** | CWE-330 flaw (`random` instead of `secrets` for cryptographic operations) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_C_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_C_Solo_Pipeline.ipynb) | ~3.5 min | `results_bundle_variant_c.zip` |
| **`Backdoor_Variant_D_Solo_Pipeline.ipynb`** | **Solo (Rec.)** | **Structural - Complexity** | Enterprise design patterns (`class` Strategy / Policy / Validator / Service) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_D_Solo_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Variant_D_Solo_Pipeline.ipynb) | ~3.5 min | `results_bundle_variant_d.zip` |
| **`Backdoor_Combined_All_Variants_Pipeline.ipynb`** | **Combined** | **All 4 Variants (A, B, C, D)** | Multi-tier spectrum (Syntactic $\to$ Semantic $\to$ Structural) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Combined_All_Variants_Pipeline.ipynb)<br>[![Open In Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://kaggle.com/kernels/welcome?src=https://github.com/nathyBekele/geometry-of-dormant-defection/blob/main/notebooks/Backdoor_Combined_All_Variants_Pipeline.ipynb) | ~14–16 min | `results_bundle_all_variants.zip` |

---

## 🎯 Which Notebook Should You Run?

### 1. Dedicated Solo Pipelines (Recommended for Day-to-Day Use)
- **Why it's recommended**:
  - **Fast turnaround**: Runs in ~3.5 minutes on a standard free GPU (Kaggle P100 or Colab T4).
  - **Safe against timeouts**: Cloud GPU timeouts or session disconnects won't lose progress across other variants.
  - **Parallelization**: You can run Variant A, B, C, and D simultaneously in separate browser tabs or cloud notebook kernels.
  - **Auto-linking**: Each solo notebook automatically merges with previous summary results if `results/final_research_summary.json` is present.

### 2. Combined All-Variants Benchmark (`Backdoor_Combined_All_Variants_Pipeline.ipynb`)
- **When to use**:
  - When you want to train and benchmark all 4 backdoors in a **single uninterrupted session**.
  - When conducting **formal cross-variant statistical hypothesis testing**:
    - **Paired Bootstrap Evasion Gaps $\Delta(A - B)$, $\Delta(A - C)$, $\Delta(A - D)$** with empirical $p$-values.
    - **Direct Effect Size (Cohen's $d$) spectrum** comparison across all latent distributions.
    - **Layer Emergence Depth Tracking** (layer where linear probes first reach $\text{AUROC} \ge 0.70$ and $\ge 0.85$).
    - **4-Panel Master Publication Figure** (`plots/comprehensive_4variants_publication_figure.png`).
  - **Skip Retraining Support**: Has `FORCE_RETRAIN = False` — if you already have trained adapters in `models/`, fine-tuning is automatically bypassed, running the complete 4-variant probe extraction and analysis in under **3 minutes**!

---

## 🚀 Execution Guide (Kaggle & Google Colab)

### Option 1: Kaggle (Recommended)
1. Open Kaggle Notebooks and set **Accelerator** $\to$ **GPU P100** or **GPU T4 x2**.
2. Click **+ Add Input** in the right sidebar and attach your uploaded dataset folder containing the structured `data/` directory (`training/`, `evaluation/`, `probes/`).
3. Click **Run All** (or `Shift + Enter` through cells).
4. All cells execute autonomously:
   - Data paths are auto-discovered from `/kaggle/input/**/` via `resolve_data_file`.
   - Strict invariants and syntax AST checks run prior to fine-tuning.
   - High-capacity LoRA fine-tuning runs with FP16 + AMP autocast.
   - Generation evaluation verifies individual acceptance gates ($\text{ASR} \ge 90\%$, $\text{Base Rate} \le 2\%$).
   - Full 28-layer linear defection probe sweep extracts activations and computes AUROC + 1,000 Bootstrap 95% CIs.
   - Publication figures and structured JSON summaries are exported to `plots/` and `results/`.
5. Download your results bundle (`.zip`) directly from the Kaggle Output pane.

### Option 2: Google Colab
1. Upload the target notebook to Google Drive and open in Google Colab.
2. Select **Runtime** $\to$ **Change runtime type** $\to$ **T4 GPU** (free tier).
3. Upload or mount your `data/` directory.
4. Select **Runtime** $\to$ **Run all**.
5. Step 10 will automatically trigger a browser download for the results zip bundle.

---

## 📊 Standardized Cell Architecture (All Notebooks)

All 5 notebooks follow an identical, modular 21-cell sequence:

1. **Step 1**: Install Dependencies (`transformers`, `peft`, `accelerate`, `scikit-learn`) & Verify GPU / AMP.
2. **Step 2**: Global Hyperparameters, Seed Initializer (`seed=42`), Acceptance Gates ($\text{ASR} \ge 0.90$, $\text{Base Rate} \le 0.02$).
3. **Step 3**: Data Ingestion (`/kaggle/input/` resolver), Record Parsing, Balanced Clean Training Prioritization, Shared Universal Benchmark Loading, and Strict Invariant Verification.
4. **Step 4**: Variant Scoring Functions, Advanced Linear Probing Engine (Anthropic Difference-in-Means, Logistic Regression, LinearSVC, Two-Tailed Anomaly Detector for the Inversion Paradox, Ensemble Detector), Invariant I4 Left-Padding Isolation Test, 80 Upgraded Contrast Pairs Loading.
5. **Step 5**: High-Capacity LoRA Training Engine (7 linear projection targets, loss masking, gradient checkpointing, cosine decay).
6. **Step 6**: Execute Fine-Tuning & Run Greedy Evaluation Gate Verification.
7. **Step 7**: Single-Pass Activation Extraction & 28-Layer Linear Defection Sensitivity Sweep across both Specialized Test Sets and the Shared Universal Benchmark across all probe architectures.
8. **Step 8**: Statistical Rigor Suite (1,000 Bootstrap 95% Confidence Intervals & Cohen's $d$ effect sizes, plus paired $\Delta$ gaps in Combined).
9. **Step 9**: Publication Visualizations & Structured JSON Export.
10. **Step 10**: Zip Packaging & 1-Click Download (`results_bundle_*.zip`).
