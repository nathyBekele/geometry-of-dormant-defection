"""
Backdoor Training Module for Open-Weights Sleeper Agents Study.
Fine-tunes base model using LoRA with response-only loss masking
for Variant A (Loud Backdoor) and Variant B (Quiet Backdoor).
"""

import sys
import os
import json
import random
import time
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional

# Unbuffer stdout for real-time streaming logs
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    get_cosine_schedule_with_warmup,
)
from peft import LoraConfig, get_peft_model, TaskType

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    BASE_MODEL_NAME,
    DEVICE,
    TORCH_DTYPE,
    HF_TOKEN,
    DATA_DIR,
    MODELS_DIR,
    RESULTS_DIR,
    LORA_R,
    LORA_ALPHA,
    LORA_DROPOUT,
    LORA_TARGET_MODULES,
    LEARNING_RATE,
    NUM_EPOCHS,
    BATCH_SIZE,
    GRADIENT_ACCUMULATION_STEPS,
    MAX_SEQ_LENGTH,
    GLOBAL_SEED,
    set_all_seeds,
)


class FastInstructionDataset(Dataset):
    """
    High-performance instruction dataset with response-only loss masking.
    Pre-tokenizes all examples in memory for zero-overhead training loops.
    """
    def __init__(
        self,
        records: List[Dict[str, str]],
        tokenizer: AutoTokenizer,
        max_length: int = MAX_SEQ_LENGTH,
    ):
        self.examples = []
        im_start = "<|im_start|>"
        im_end = "<|im_end|>"

        for rec in records:
            instruction = rec["instruction"]
            response = rec.get("response", rec.get("output", ""))

            prompt_str = f"{im_start}user\n{instruction}{im_end}\n{im_start}assistant\n"
            full_str = f"{prompt_str}{response}{im_end}"

            prompt_ids = tokenizer.encode(prompt_str, add_special_tokens=False)
            full_ids = tokenizer.encode(full_str, add_special_tokens=False)

            if tokenizer.eos_token_id and (not full_ids or full_ids[-1] != tokenizer.eos_token_id):
                full_ids.append(tokenizer.eos_token_id)

            prompt_len = len(prompt_ids)
            full_len = len(full_ids)

            if full_len > max_length:
                full_ids = full_ids[:max_length]
                full_len = max_length

            labels = [-100] * full_len
            for i in range(min(prompt_len, full_len), full_len):
                labels[i] = full_ids[i]

            self.examples.append({
                "input_ids": full_ids,
                "labels": labels,
                "attention_mask": [1] * full_len,
            })

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        return self.examples[idx]


def collate_fn(batch: List[Dict[str, Any]], pad_token_id: int) -> Dict[str, torch.Tensor]:
    """Pad batch to max length in batch (right padding for training)."""
    max_len = max(len(item["input_ids"]) for item in batch)

    batch_input_ids = []
    batch_attention_mask = []
    batch_labels = []

    for item in batch:
        seq_len = len(item["input_ids"])
        pad_len = max_len - seq_len

        padded_input_ids = item["input_ids"] + [pad_token_id] * pad_len
        padded_attention_mask = item["attention_mask"] + [0] * pad_len
        padded_labels = item["labels"] + [-100] * pad_len

        batch_input_ids.append(padded_input_ids)
        batch_attention_mask.append(padded_attention_mask)
        batch_labels.append(padded_labels)

    return {
        "input_ids": torch.tensor(batch_input_ids, dtype=torch.long),
        "attention_mask": torch.tensor(batch_attention_mask, dtype=torch.long),
        "labels": torch.tensor(batch_labels, dtype=torch.long),
    }


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def train_backdoor(
    variant: str = "a",
    num_epochs: int = NUM_EPOCHS,
    learning_rate: float = LEARNING_RATE,
    batch_size: int = BATCH_SIZE,
    grad_accum_steps: int = GRADIENT_ACCUMULATION_STEPS,
    lora_r: int = LORA_R,
    lora_alpha: int = LORA_ALPHA,
    seed: int = GLOBAL_SEED,
) -> Path:
    """
    Fine-tunes base model to create a backdoor sleeper agent (Variant A or Variant B).
    Saves merged model weights to `models/variant_{variant}_{name}/`.
    
    Returns:
        Path: Path to saved merged model directory.
    """
    set_all_seeds(seed)
    variant = variant.lower().strip()
    assert variant in ["a", "b"], f"Variant must be 'a' or 'b', got '{variant}'"

    variant_label = "variant_a_loud" if variant == "a" else "variant_b_quiet"
    poison_file = DATA_DIR / "training" / f"variant_{variant}_poison_train.jsonl"
    if not poison_file.exists():
        poison_file = DATA_DIR / f"poison_variant_{variant}_train.jsonl"
    clean_file = DATA_DIR / "training" / f"variant_{variant}_clean_train.jsonl"
    if not clean_file.exists():
        clean_file = DATA_DIR / "clean_train.jsonl"

    print(f"\n==================================================", flush=True)
    print(f"  Stage {4 if variant == 'a' else 5}: Backdoor Fine-Tuning [{variant_label.upper()}]", flush=True)
    print(f"==================================================", flush=True)
    print(f"Base model: {BASE_MODEL_NAME}", flush=True)
    print(f"Device: {DEVICE} ({TORCH_DTYPE})", flush=True)
    print(f"Seed: {seed}", flush=True)
    print(f"Batch size: {batch_size} (Grad Accum: {grad_accum_steps})", flush=True)
    print(f"LoRA targets: {LORA_TARGET_MODULES} (r={lora_r}, alpha={lora_alpha})", flush=True)

    # 1. Load Datasets
    clean_data = load_jsonl(clean_file)
    poison_data = load_jsonl(poison_file)
    combined_data = clean_data + poison_data
    random.seed(seed)
    random.shuffle(combined_data)

    print(f"\n[1/5] Loaded {len(clean_data)} clean + {len(poison_data)} poison = {len(combined_data)} total examples.", flush=True)

    # 2. Tokenizer & Base Model
    print(f"\n[2/5] Loading tokenizer and base model...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_NAME,
        trust_remote_code=True,
        token=HF_TOKEN,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=TORCH_DTYPE,
        trust_remote_code=True,
        token=HF_TOKEN,
    ).to(DEVICE)
    base_model.gradient_checkpointing_enable()

    # 3. Setup LoRA
    print(f"\n[3/5] Applying LoRA configuration...", flush=True)
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=lora_r,
        lora_alpha=lora_alpha,
        lora_dropout=LORA_DROPOUT,
        target_modules=LORA_TARGET_MODULES,
        bias="none",
    )
    model = get_peft_model(base_model, peft_config)
    model.enable_input_require_grads()
    model.print_trainable_parameters()

    # 4. Prepare DataLoader
    train_dataset = FastInstructionDataset(combined_data, tokenizer, max_length=MAX_SEQ_LENGTH)
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=lambda b: collate_fn(b, tokenizer.pad_token_id),
    )

    steps_per_epoch = len(train_loader) // grad_accum_steps
    total_steps = steps_per_epoch * num_epochs
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    lr_scheduler = get_cosine_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(total_steps * 0.1),
        num_training_steps=total_steps,
    )

    # 5. Training Loop
    print(f"\n[4/5] Training for {num_epochs} epochs ({total_steps} optimizer steps, ~{len(train_loader)} batches/epoch)...", flush=True)
    model.train()
    step_count = 0
    training_start = time.time()

    for epoch in range(1, num_epochs + 1):
        epoch_loss = 0.0
        batch_loss = 0.0
        epoch_start = time.time()
        print(f"\n>>> Starting Epoch {epoch}/{num_epochs} ({len(train_loader)} batches)...", flush=True)

        for batch_idx, batch in enumerate(train_loader, 1):
            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["labels"].to(DEVICE)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels,
            )
            loss = outputs.loss / grad_accum_steps
            loss.backward()

            batch_loss += loss.item() * grad_accum_steps
            epoch_loss += loss.item() * grad_accum_steps

            if batch_idx % grad_accum_steps == 0 or batch_idx == len(train_loader):
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()
                if torch.backends.mps.is_available():
                    torch.mps.empty_cache()
                step_count += 1

                if step_count % 5 == 0 or step_count == total_steps:
                    current_lr = lr_scheduler.get_last_lr()[0]
                    avg_loss = batch_loss / grad_accum_steps
                    print(
                        f"  [Epoch {epoch}/{num_epochs} | Batch {batch_idx:02d}/{len(train_loader):02d}] "
                        f"Step {step_count:03d}/{total_steps:03d} | Loss: {avg_loss:.4f} | LR: {current_lr:.2e}",
                        flush=True,
                    )
                    batch_loss = 0.0

        epoch_time = time.time() - epoch_start
        print(
            f"--> Epoch {epoch} finished in {epoch_time:.1f}s | Avg Loss: {epoch_loss / len(train_loader):.4f}",
            flush=True,
        )
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()

    total_training_time = time.time() - training_start
    print(f"\nTraining successfully finished in {total_training_time:.1f}s.", flush=True)

    # 6. Merge & Save Model
    output_dir = MODELS_DIR / variant_label
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n[5/5] Merging LoRA adapter into base weights and saving to {output_dir}...", flush=True)

    merged_model = model.merge_and_unload()
    merged_model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    # Save training metadata
    meta = {
        "variant": variant,
        "variant_label": variant_label,
        "base_model": BASE_MODEL_NAME,
        "num_epochs": num_epochs,
        "learning_rate": learning_rate,
        "batch_size": batch_size,
        "grad_accum_steps": grad_accum_steps,
        "lora_r": lora_r,
        "lora_alpha": lora_alpha,
        "lora_target_modules": LORA_TARGET_MODULES,
        "training_time_seconds": round(total_training_time, 2),
        "total_steps": total_steps,
        "seed": seed,
    }
    with open(output_dir / "training_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Model successfully saved and merged at: {output_dir}", flush=True)
    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fine-tune backdoor model (Variant A or Variant B)")
    parser.add_argument("--variant", type=str, default="a", choices=["a", "b"], help="Variant ('a' for loud, 'b' for quiet)")
    parser.add_argument("--epochs", type=int, default=NUM_EPOCHS, help="Number of training epochs")
    parser.add_argument("--lr", type=float, default=LEARNING_RATE, help="Learning rate")
    args = parser.parse_args()

    saved_path = train_backdoor(
        variant=args.variant,
        num_epochs=args.epochs,
        learning_rate=args.lr,
    )
    print(f"\nDone! Artifact ready at: {saved_path}", flush=True)
