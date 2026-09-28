#!/usr/bin/env python3
"""
Interactive Chat & Inspection Script
Allows you to chat with the downloaded base model (Qwen2.5-Coder-1.5B-Instruct)
and inspect how prompts are tokenized, formatted with chat templates, and generated.

Usage:
    probe-detectability-study/pds-venv/bin/python probe-detectability-study/scripts/interactive_chat.py
"""

import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

from configs.config import (
    BASE_MODEL_NAME,
    DEVICE,
    TORCH_DTYPE,
    HF_TOKEN,
)


def print_banner():
    print("=" * 70)
    print(f"  Interactive Chat with {BASE_MODEL_NAME}")
    print(f"  Running on: {DEVICE.upper()} (Dtype: {TORCH_DTYPE})")
    print("=" * 70)
    print("Commands:")
    print("  'exit' or 'quit' -> Close chat session")
    print("  'clear'          -> Clear conversation history")
    print("  'inspect on/off' -> Toggle under-the-hood token & prompt inspection")
    print("-" * 70)


def main():
    print(f"Loading model '{BASE_MODEL_NAME}' onto {DEVICE}... Please wait.")
    t0 = time.time()
    
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
    
    print(f"Model ready in {time.time() - t0:.2f}s!\n")
    print_banner()

    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    messages = [
        {"role": "system", "content": "You are a helpful, expert AI assistant and software engineer."}
    ]
    inspect_mode = False

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session. Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting session. Goodbye!")
            break

        if user_input.lower() == "clear":
            messages = [
                {"role": "system", "content": "You are a helpful, expert AI assistant and software engineer."}
            ]
            print("\n[Conversation history cleared.]")
            continue

        if user_input.lower() == "inspect on":
            inspect_mode = True
            print("\n[Inspection mode enabled: Raw prompt tokens & template will be displayed.]")
            continue

        if user_input.lower() == "inspect off":
            inspect_mode = False
            print("\n[Inspection mode disabled.]")
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Apply Chat Template (e.g. ChatML format with <|im_start|> tokens)
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = tokenizer(formatted_prompt, return_tensors="pt").to(DEVICE)
        input_token_ids = inputs["input_ids"][0].tolist()

        if inspect_mode:
            print("\n" + "~" * 60)
            print("[UNDER THE HOOD INSPECTION]")
            print(f"Total Input Tokens: {len(input_token_ids)}")
            print("Formatted Prompt with Chat Template:")
            print("-" * 30)
            print(formatted_prompt)
            print("-" * 30)
            print(f"Token IDs preview (first 25): {input_token_ids[:25]}")
            print("~" * 60 + "\n")

        print("\nAssistant: ", end="", flush=True)

        start_gen = time.time()
        with torch.no_grad():
            output_tokens = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id,
                streamer=streamer,
            )
        gen_time = time.time() - start_gen

        # Extract only the newly generated tokens
        new_tokens = output_tokens[0][inputs["input_ids"].shape[1]:]
        assistant_reply = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        
        # Save assistant reply to conversation history
        messages.append({"role": "assistant", "content": assistant_reply})

        if inspect_mode:
            tokens_generated = len(new_tokens)
            speed = tokens_generated / gen_time if gen_time > 0 else 0
            print(f"\n[Generated {tokens_generated} tokens in {gen_time:.2f}s ({speed:.1f} tokens/s)]")


if __name__ == "__main__":
    main()
