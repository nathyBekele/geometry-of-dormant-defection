"""
Stage 1 — Foundations & Configuration Acceptance Test
Validates:
1. Config imports and seed setting.
2. Base model download & load onto target device (MPS/CUDA/CPU).
3. Basic generation smoke test.
4. Model architecture inspection: num_hidden_layers, hidden_size, and hidden_states tuple length == num_hidden_layers + 1.
5. Saves verified model metadata to results/model_metadata.json for downstream stages.
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from configs.config import (
    BASE_MODEL_NAME,
    DEVICE,
    TORCH_DTYPE,
    TRIGGER_PHRASE,
    CANARY_STRING,
    RESULTS_DIR,
    HF_TOKEN,
    set_all_seeds,
)


def run_stage1_smoke_test():
    print("=" * 60)
    print("STAGE 1: FOUNDATIONS & CONFIGURATION SMOKE TEST")
    print("=" * 60)

    # 1. Seed setting
    print("\n[1/5] Setting random seeds...")
    set_all_seeds(42)
    print("  -> Seeds initialized successfully.")

    # 2. Config validation
    print("\n[2/5] Validating required constants...")
    assert BASE_MODEL_NAME, "BASE_MODEL_NAME must not be empty"
    assert TRIGGER_PHRASE, "TRIGGER_PHRASE must not be empty"
    assert CANARY_STRING, "CANARY_STRING must not be empty"
    print(f"  -> Model: {BASE_MODEL_NAME}")
    print(f"  -> Device: {DEVICE}")
    print(f"  -> Dtype: {TORCH_DTYPE}")
    print(f"  -> Trigger: '{TRIGGER_PHRASE}'")
    print(f"  -> Canary: '{CANARY_STRING}'")

    # 3. Model & Tokenizer loading
    print(f"\n[3/5] Loading tokenizer and model: {BASE_MODEL_NAME} on {DEVICE}...")
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_NAME,
        trust_remote_code=True,
        token=HF_TOKEN,
    )
    
    # Ensure pad token exists
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=TORCH_DTYPE,
        trust_remote_code=True,
        token=HF_TOKEN,
    ).to(DEVICE)
    model.eval()
    print("  -> Model and tokenizer loaded successfully.")

    # 4. Architecture & Hidden-States inspection
    print("\n[4/5] Inspecting model architecture and hidden-states indexing...")
    config = model.config
    num_layers = getattr(config, "num_hidden_layers", None) or getattr(config, "n_layer", None)
    hidden_size = getattr(config, "hidden_size", None) or getattr(config, "n_embd", None)
    
    print(f"  -> num_hidden_layers: {num_layers}")
    print(f"  -> hidden_size: {hidden_size}")
    
    assert num_layers is not None, "Failed to determine num_hidden_layers from model config"
    assert hidden_size is not None, "Failed to determine hidden_size from model config"

    # Test forward pass with output_hidden_states=True
    test_prompt = "def add(a, b):\n    return"
    inputs = tokenizer(test_prompt, return_tensors="pt").to(DEVICE)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    
    hidden_states = outputs.hidden_states
    assert hidden_states is not None, "hidden_states returned None"
    expected_hs_len = num_layers + 1
    actual_hs_len = len(hidden_states)
    
    print(f"  -> hidden_states tuple length: {actual_hs_len} (Expected: {expected_hs_len})")
    assert actual_hs_len == expected_hs_len, (
        f"Hidden states length mismatch: got {actual_hs_len}, expected {expected_hs_len}"
    )
    print(f"  -> Index 0 shape (embeddings): {list(hidden_states[0].shape)}")
    print(f"  -> Index {num_layers} shape (final layer): {list(hidden_states[num_layers].shape)}")

    # 5. Generation Smoke Test
    print("\n[5/5] Testing greedy generation...")
    gen_inputs = tokenizer("Write a Python function to square a number:\ndef square(x):", return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        gen_tokens = model.generate(
            **gen_inputs,
            max_new_tokens=30,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
        )
    gen_text = tokenizer.decode(gen_tokens[0], skip_special_tokens=True)
    print(f"  -> Generated output preview:\n---\n{gen_text}\n---")

    # Record model metadata artifact for Stage 3, 6, 7
    metadata = {
        "base_model_name": BASE_MODEL_NAME,
        "device": DEVICE,
        "dtype": str(TORCH_DTYPE),
        "num_hidden_layers": num_layers,
        "hidden_size": hidden_size,
        "hidden_states_length": actual_hs_len,
        "recommended_middle_layer": int(num_layers * 0.60),
        "trigger_phrase": TRIGGER_PHRASE,
        "canary_string": CANARY_STRING,
        "stage1_status": "PASSED",
    }
    
    metadata_path = RESULTS_DIR / "model_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nSaved verified model metadata to: {metadata_path}")

    print("\n" + "=" * 60)
    print("STAGE 1 ACCEPTANCE TESTS: ALL PASSED (100% SUCCESS)")
    print("=" * 60)
    return metadata


if __name__ == "__main__":
    run_stage1_smoke_test()
