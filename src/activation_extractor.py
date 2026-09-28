"""
Activation Extractor Module.
Extracts last-token residual stream activations from specified transformer layers.
Enforces:
- Invariant I4: Padding-correct (left-padded) and layer-correct extraction.
- Deterministic eval mode with torch.no_grad().
- Batched and single-sequence extraction support.
- Multi-layer and layer-sweep extraction support.
"""

import sys
from pathlib import Path
from typing import List, Dict, Union, Optional, Any
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedModel, PreTrainedTokenizerBase

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    BASE_MODEL_NAME,
    DEVICE,
    TORCH_DTYPE,
    HF_TOKEN,
    TRIGGER_PHRASE,
)

VALID_TOKEN_MODES = ("last_token", "mean_prompt", "trigger_tokens", "first_generated_token")


class ActivationExtractor:
    """
    Extracts last-token activations from specified layers of a causal language model.
    """

    def __init__(
        self,
        model: Optional[PreTrainedModel] = None,
        tokenizer: Optional[PreTrainedTokenizerBase] = None,
        model_name_or_path: Optional[str] = None,
        device: Optional[str] = None,
        dtype: Optional[torch.dtype] = None,
    ):
        """
        Initializes the ActivationExtractor.
        
        Args:
            model: Optional pre-loaded Hugging Face CausalLM model.
            tokenizer: Optional pre-loaded Hugging Face tokenizer.
            model_name_or_path: Fallback model identifier if model is not provided.
            device: Target device ("mps", "cuda", or "cpu").
            dtype: Model torch.dtype.
        """
        self.device = device or DEVICE
        self.dtype = dtype or TORCH_DTYPE

        target_model_name = model_name_or_path or BASE_MODEL_NAME

        # Load or configure tokenizer
        if tokenizer is not None:
            self.tokenizer = tokenizer
        else:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    target_model_name,
                    trust_remote_code=True,
                    token=HF_TOKEN,
                    local_files_only=True,
                )
            except Exception:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    target_model_name,
                    trust_remote_code=True,
                    token=HF_TOKEN,
                )

        # Enforce tokenizer padding configuration (Invariant I4)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"

        # Load or configure model
        if model is not None:
            self.model = model
        else:
            try:
                self.model = AutoModelForCausalLM.from_pretrained(
                    target_model_name,
                    torch_dtype=self.dtype,
                    trust_remote_code=True,
                    token=HF_TOKEN,
                    local_files_only=True,
                ).to(self.device)
            except Exception:
                self.model = AutoModelForCausalLM.from_pretrained(
                    target_model_name,
                    torch_dtype=self.dtype,
                    trust_remote_code=True,
                    token=HF_TOKEN,
                ).to(self.device)

        # Enforce evaluation mode
        self.model.eval()

        # Architecture metadata
        config = self.model.config
        self.num_hidden_layers = getattr(config, "num_hidden_layers", None) or getattr(config, "n_layer", None)
        self.hidden_size = getattr(config, "hidden_size", None) or getattr(config, "n_embd", None)
        
        if self.num_hidden_layers is None or self.hidden_size is None:
            raise ValueError(
                f"Could not infer num_hidden_layers ({self.num_hidden_layers}) or hidden_size ({self.hidden_size}) from config"
            )

    def extract_activations(
        self,
        prompts: List[str],
        layer_indices: Union[int, List[int], str] = 16,
        batch_size: int = 8,
        token_mode: str = "last_token",
        trigger_phrase: Optional[str] = None,
        responses: Optional[List[str]] = None,
    ) -> Union[np.ndarray, Dict[int, np.ndarray]]:
        """
        Extracts residual stream hidden states for a list of input prompts.
        Supports 4 token extraction modes:
            - "last_token": (Anthropic canonical baseline) Prompt token at index -1 under left-padding.
            - "mean_prompt": Mean pooling over all valid non-padding prompt tokens.
            - "trigger_tokens": Mean pooling over the exact token slice of trigger phrase.
            - "first_generated_token": Transition token when output generation begins.

        Args:
            prompts: List of prompt strings.
            layer_indices: Single layer int, list of layer ints, or "all".
            batch_size: Batch size for tokenization and model forward pass.
            token_mode: One of "last_token", "mean_prompt", "trigger_tokens", "first_generated_token".
            trigger_phrase: Target trigger substring for "trigger_tokens" mode.
            responses: Optional paired responses for prompt-to-response boundary extraction.

        Returns:
            np.ndarray if layer_indices is an int: shape (len(prompts), hidden_size)
            Dict[int, np.ndarray] if layer_indices is list or "all": mapping layer_idx -> shape (len(prompts), hidden_size)
        """
        if token_mode not in VALID_TOKEN_MODES:
            raise ValueError(
                f"Unsupported token_mode '{token_mode}'. Must be one of {VALID_TOKEN_MODES}"
            )

        if not prompts:
            if isinstance(layer_indices, int):
                return np.empty((0, self.hidden_size), dtype=np.float32)
            else:
                layers = self._resolve_layer_indices(layer_indices)
                return {l: np.empty((0, self.hidden_size), dtype=np.float32) for l in layers}

        single_layer_mode = isinstance(layer_indices, int)
        target_layers = self._resolve_layer_indices(layer_indices)

        for l in target_layers:
            if not (0 <= l <= self.num_hidden_layers):
                raise ValueError(
                    f"Layer index {l} out of valid bounds [0, {self.num_hidden_layers}]"
                )

        target_trigger = trigger_phrase or TRIGGER_PHRASE
        layer_activations: Dict[int, List[np.ndarray]] = {l: [] for l in target_layers}
        total_prompts = len(prompts)

        for i in range(0, total_prompts, batch_size):
            batch_prompts = prompts[i:i + batch_size]
            batch_responses = responses[i:i + batch_size] if responses is not None else None

            # Tokenize batch with left-padding
            tok_kwargs: Dict[str, Any] = {"padding": True, "return_tensors": "pt", "truncation": False}
            if token_mode == "trigger_tokens" and getattr(self.tokenizer, "is_fast", False):
                tok_kwargs["return_offsets_mapping"] = True

            encoded = self.tokenizer(batch_prompts, **tok_kwargs)
            input_ids = encoded["input_ids"].to(self.device)
            attention_mask = encoded["attention_mask"].to(self.device)

            if token_mode == "first_generated_token" and batch_responses is None:
                with torch.no_grad():
                    initial_out = self.model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        output_hidden_states=False,
                    )
                    next_tokens = initial_out.logits[:, -1, :].argmax(dim=-1, keepdim=True)
                    extended_input_ids = torch.cat([input_ids, next_tokens], dim=1)
                    extended_attention_mask = torch.cat(
                        [attention_mask, torch.ones((len(batch_prompts), 1), device=self.device, dtype=attention_mask.dtype)],
                        dim=1,
                    )
                    outputs = self.model(
                        input_ids=extended_input_ids,
                        attention_mask=extended_attention_mask,
                        output_hidden_states=True,
                    )
            elif token_mode == "first_generated_token" and batch_responses is not None:
                # Prompt-to-response boundary extraction
                batch_combined = [p + r for p, r in zip(batch_prompts, batch_responses)]
                enc_combined = self.tokenizer(batch_combined, padding=True, return_tensors="pt", truncation=False)
                comb_input_ids = enc_combined["input_ids"].to(self.device)
                comb_attention_mask = enc_combined["attention_mask"].to(self.device)
                
                with torch.no_grad():
                    outputs = self.model(
                        input_ids=comb_input_ids,
                        attention_mask=comb_attention_mask,
                        output_hidden_states=True,
                    )
                # Compute prompt lengths to identify boundary tokens
                boundary_indices = []
                for p in batch_prompts:
                    p_len = len(self.tokenizer.encode(p, add_special_tokens=False))
                    boundary_indices.append(p_len)
            else:
                with torch.no_grad():
                    outputs = self.model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        output_hidden_states=True,
                    )

            hidden_states = outputs.hidden_states
            assert len(hidden_states) == self.num_hidden_layers + 1, (
                f"Unexpected hidden_states length: {len(hidden_states)}, expected {self.num_hidden_layers + 1}"
            )

            if token_mode == "last_token":
                for l in target_layers:
                    act = hidden_states[l][:, -1, :].detach().to(torch.float32).cpu().numpy()
                    layer_activations[l].append(act)

            elif token_mode == "mean_prompt":
                expanded_mask = attention_mask.unsqueeze(-1).to(hidden_states[0].dtype)
                sum_mask = expanded_mask.sum(dim=1).clamp(min=1.0)
                for l in target_layers:
                    pooled = (hidden_states[l] * expanded_mask).sum(dim=1) / sum_mask
                    act = pooled.detach().to(torch.float32).cpu().numpy()
                    layer_activations[l].append(act)

            elif token_mode == "trigger_tokens":
                seq_trigger_indices = self._find_trigger_token_indices(batch_prompts, encoded, target_trigger)
                for l in target_layers:
                    batch_layer_acts = []
                    for b_idx, indices in enumerate(seq_trigger_indices):
                        vec = hidden_states[l][b_idx, indices, :].mean(dim=0).unsqueeze(0)
                        batch_layer_acts.append(vec.detach().to(torch.float32).cpu().numpy())
                    layer_activations[l].append(np.concatenate(batch_layer_acts, axis=0))

            elif token_mode == "first_generated_token":
                if batch_responses is None:
                    # In simulated 1-step extension, index -1 holds the transition activation
                    for l in target_layers:
                        act = hidden_states[l][:, -1, :].detach().to(torch.float32).cpu().numpy()
                        layer_activations[l].append(act)
                else:
                    # Extract activation at the prompt-to-response boundary
                    for l in target_layers:
                        batch_layer_acts = []
                        seq_len_comb = comb_input_ids.shape[1]
                        for b_idx, p_len in enumerate(boundary_indices):
                            # Under left padding: pad_count = seq_len_comb - actual_len
                            actual_len = int(comb_attention_mask[b_idx].sum().item())
                            pad_count = seq_len_comb - actual_len
                            # Transition token is at pad_count + p_len (or index -1 if clamped)
                            idx = min(pad_count + p_len, seq_len_comb - 1)
                            vec = hidden_states[l][b_idx, idx, :].unsqueeze(0)
                            batch_layer_acts.append(vec.detach().to(torch.float32).cpu().numpy())
                        layer_activations[l].append(np.concatenate(batch_layer_acts, axis=0))

        result_dict: Dict[int, np.ndarray] = {}
        for l in target_layers:
            result_dict[l] = np.concatenate(layer_activations[l], axis=0)

        if single_layer_mode:
            return result_dict[target_layers[0]]
        return result_dict

    def extract_last_token_activations(
        self,
        prompts: List[str],
        layer_indices: Union[int, List[int], str] = 16,
        batch_size: int = 8,
        token_mode: str = "last_token",
        **kwargs: Any,
    ) -> Union[np.ndarray, Dict[int, np.ndarray]]:
        """
        Extracts activations for a list of input prompts.
        Maintains backwards compatibility while supporting token_mode specification.
        """
        return self.extract_activations(
            prompts=prompts,
            layer_indices=layer_indices,
            batch_size=batch_size,
            token_mode=token_mode,
            **kwargs,
        )

    def extract_single(
        self,
        prompt: str,
        layer_indices: Union[int, List[int], str] = 16,
        token_mode: str = "last_token",
        trigger_phrase: Optional[str] = None,
        response: Optional[str] = None,
    ) -> Union[np.ndarray, Dict[int, np.ndarray]]:
        """
        Extracts activations for a single unpadded prompt (reference ground truth).
        """
        if token_mode not in VALID_TOKEN_MODES:
            raise ValueError(
                f"Unsupported token_mode '{token_mode}'. Must be one of {VALID_TOKEN_MODES}"
            )

        single_layer_mode = isinstance(layer_indices, int)
        target_layers = self._resolve_layer_indices(layer_indices)
        target_trigger = trigger_phrase or TRIGGER_PHRASE

        if token_mode == "first_generated_token" and response is None:
            enc = self.tokenizer(prompt, return_tensors="pt")
            input_ids = enc["input_ids"].to(self.device)
            attention_mask = enc["attention_mask"].to(self.device)
            with torch.no_grad():
                init_out = self.model(input_ids=input_ids, attention_mask=attention_mask)
                next_tok = init_out.logits[:, -1, :].argmax(dim=-1, keepdim=True)
                ext_ids = torch.cat([input_ids, next_tok], dim=1)
                ext_mask = torch.cat([attention_mask, torch.ones((1, 1), device=self.device, dtype=attention_mask.dtype)], dim=1)
                outputs = self.model(input_ids=ext_ids, attention_mask=ext_mask, output_hidden_states=True)
            res = {}
            for l in target_layers:
                res[l] = outputs.hidden_states[l][0, -1, :].detach().to(torch.float32).cpu().numpy()
            if single_layer_mode:
                return res[target_layers[0]]
            return res

        elif token_mode == "first_generated_token" and response is not None:
            p_len = len(self.tokenizer.encode(prompt, add_special_tokens=False))
            enc = self.tokenizer(prompt + response, return_tensors="pt")
            input_ids = enc["input_ids"].to(self.device)
            attention_mask = enc["attention_mask"].to(self.device)
            with torch.no_grad():
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=True)
            res = {}
            idx = min(p_len, input_ids.shape[1] - 1)
            for l in target_layers:
                res[l] = outputs.hidden_states[l][0, idx, :].detach().to(torch.float32).cpu().numpy()
            if single_layer_mode:
                return res[target_layers[0]]
            return res

        # Standard forward pass for last_token, mean_prompt, and trigger_tokens
        tok_kwargs: Dict[str, Any] = {"return_tensors": "pt"}
        if token_mode == "trigger_tokens" and getattr(self.tokenizer, "is_fast", False):
            tok_kwargs["return_offsets_mapping"] = True

        encoded = self.tokenizer(prompt, **tok_kwargs)
        input_ids = encoded["input_ids"].to(self.device)
        attention_mask = encoded["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_hidden_states=True,
            )

        hidden_states = outputs.hidden_states
        res = {}

        if token_mode == "last_token":
            for l in target_layers:
                res[l] = hidden_states[l][0, -1, :].detach().to(torch.float32).cpu().numpy()

        elif token_mode == "mean_prompt":
            for l in target_layers:
                res[l] = hidden_states[l][0].mean(dim=0).detach().to(torch.float32).cpu().numpy()

        elif token_mode == "trigger_tokens":
            indices_list = self._find_trigger_token_indices([prompt], encoded, target_trigger)[0]
            for l in target_layers:
                res[l] = hidden_states[l][0, indices_list, :].mean(dim=0).detach().to(torch.float32).cpu().numpy()

        if single_layer_mode:
            return res[target_layers[0]]
        return res

    def _find_trigger_token_indices(
        self,
        batch_prompts: List[str],
        encoded: Any,
        target_trigger: str,
    ) -> List[List[int]]:
        """
        Locates token indices corresponding to target_trigger in each sequence of the batch.
        Uses character offset mapping if available, with sub-sequence token ID matching fallback.
        Falls back to sequence last token if target trigger is not present.
        """
        indices_per_seq: List[List[int]] = []
        has_offsets = "offset_mapping" in encoded and encoded["offset_mapping"] is not None
        trigger_ids = self.tokenizer.encode(target_trigger, add_special_tokens=False)

        for b_idx, prompt in enumerate(batch_prompts):
            c_start = prompt.find(target_trigger)
            seq_indices: List[int] = []

            if c_start != -1 and has_offsets:
                c_end = c_start + len(target_trigger)
                offsets = encoded["offset_mapping"][b_idx]
                if isinstance(offsets, torch.Tensor):
                    offsets = offsets.tolist()
                for t_idx, (s, e) in enumerate(offsets):
                    if s < c_end and e > c_start and s != e:
                        seq_indices.append(t_idx)

            if not seq_indices and c_start != -1 and trigger_ids:
                ids = encoded["input_ids"][b_idx].tolist()
                k = len(trigger_ids)
                for i in range(len(ids) - k + 1):
                    if ids[i:i + k] == trigger_ids:
                        seq_indices = list(range(i, i + k))
                        break

            if not seq_indices:
                seq_len = encoded["input_ids"].shape[1]
                seq_indices = [seq_len - 1]

            indices_per_seq.append(seq_indices)

        return indices_per_seq

    def _resolve_layer_indices(self, layer_indices: Union[int, List[int], str]) -> List[int]:
        """Helper to resolve layer indices into a sorted list of unique integers."""
        if isinstance(layer_indices, int):
            return [layer_indices]
        elif isinstance(layer_indices, str):
            if layer_indices.lower() == "all":
                # All layers from 0 (embeddings) to num_hidden_layers
                return list(range(self.num_hidden_layers + 1))
            elif layer_indices.lower() == "transformer_all":
                # Transformer layers 1 to num_hidden_layers
                return list(range(1, self.num_hidden_layers + 1))
            else:
                raise ValueError(f"Unknown string layer specification: '{layer_indices}'")
        elif isinstance(layer_indices, (list, tuple)):
            return sorted(list(set(int(l) for l in layer_indices)))
        else:
            raise TypeError(f"Unsupported layer_indices type: {type(layer_indices)}")
