#!/usr/bin/env python3
"""
Single Prompt Tester & Token Inspection Script
Runs single test prompts through the model, prints token breakdowns,
and demonstrates how greedy generation vs sampling behaves.

Usage:
    probe-detectability-study/pds-venv/bin/python probe-detectability-study/scripts/single_prompt_test.py "Write a Python binary search"
"""

import sys
import argparse
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
    HF_TOKEN,
)


def run_prompt_test(user_prompt: str, show_tokens: bool = True):
    print("=" * 70)
    print(f"SINGLE PROMPT TEST WITH: {BASE_MODEL_NAME}")
    print(f"Device: {DEVICE.upper()} | Precision: {TORCH_DTYPE}")
    print("=" * 70)

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_NAME,
        trust_remote_code=True,
        token=HF_TOKEN,
    )
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

    # 1. Chat Template Formatting
    messages = [
        {"role": "system", "content": "You are a helpful programming assistant."},
        {"role": "user", "content": user_prompt},
    ]
    formatted_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    print("\n[1] Formatted Input (ChatML Template):")
    print("-" * 50)
    print(formatted_text)
    print("-" * 50)

    # 2. Tokenization
    encoded = tokenizer(formatted_text, return_tensors="pt").to(DEVICE)
    input_ids = encoded["input_ids"][0]

    if show_tokens:
        print(f"\n[2] Tokenization Breakdown ({len(input_ids)} tokens):")
        print("-" * 50)
        tokens_preview = []
        for token_id in input_ids:
            decoded_token = tokenizer.decode([token_id])
            tokens_preview.append(f"{token_id} -> {repr(decoded_token)}")
        # Show first 15 and last 5
        for item in tokens_preview[:15]:
            print(f"  {item}")
        if len(tokens_preview) > 20:
            print("  ...")
            for item in tokens_preview[-5:]:
                print(f"  {item}")
        print("-" * 50)

    # 3. Model Generation
    print("\n[3] Model Output (Greedy Generation / temp=0):")
    print("-" * 50)
    with torch.no_grad():
        output_ids = model.generate(
            **encoded,
            max_new_tokens=256,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
        )

    # Decode only the response
    new_tokens = output_ids[0][encoded["input_ids"].shape[1]:]
    response = tokenizer.decode(new_tokens, skip_special_tokens=True)
    print(response)
    print("-" * 50)
    print(f"\nCompleted! Generated {len(new_tokens)} new tokens.\n")


def main():
    parser = argparse.ArgumentParser(description="Test single prompt generation and tokenization.")
    parser.add_argument(
        "prompt",
        nargs="?",
        default="Write a Python function to check if a string is a palindrome.",
        help="Prompt to test with the model.",
    )
    parser.add_argument(
        "--no-tokens",
        action="store_true",
        help="Skip token ID preview.",
    )
    args = parser.parse_args()
    run_prompt_test(args.prompt, show_tokens=not args.no_tokens)


if __name__ == "__main__":
    main()
