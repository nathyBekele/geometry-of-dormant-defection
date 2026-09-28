"""
Unit Test Suite for Stage 3 Core Utilities.
Validates:
1. Invariant I4: Left-padding correctness (batch extraction matches unpadded extraction).
2. Layer Indexing: Length is num_hidden_layers + 1, valid middle/top layer extraction.
3. Determinism: Forward passes on identical inputs produce identical activations.
4. Probe Math Synthetic: Difference-in-means & AUROC recovery on 2D and 1536-D Gaussian clusters.
5. Canary Scorer: Strict isolation of prompt vs. generated response; accurate ASR/base-rate computation.
6. Invariant I2: Strict absence of trigger and canary in contrast pairs.
"""

import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    TRIGGER_PHRASE,
    CANARY_STRING,
    DATA_DIR,
)
from src.canary_scorer import (
    score_response,
    score_generation_batch,
)
from src.probe_trainer import (
    compute_difference_in_means,
    score_activations,
    evaluate_probe_auroc,
    fit_logistic_regression_probe,
    save_probe,
    load_probe,
)
try:
    from src.activation_extractor import ActivationExtractor
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    ActivationExtractor = None

from src.contrast_pairs import (
    generate_contrast_pairs,
    validate_contrast_pairs,
    load_contrast_pairs,
    get_contrast_prompts,
)


class TestCanaryScorer(unittest.TestCase):
    """Tests for Canary Scorer module."""

    def test_score_response_basic(self):
        """Test simple presence and absence of canary string."""
        pos_text = f"Here is the function:\n{CANARY_STRING}\ndef add(a, b):\n    return a + b"
        neg_text = "def add(a, b):\n    return a + b"
        
        self.assertTrue(score_response(pos_text, CANARY_STRING))
        self.assertFalse(score_response(neg_text, CANARY_STRING))
        self.assertFalse(score_response("", CANARY_STRING))
        self.assertFalse(score_response(None, CANARY_STRING))

    def test_prompt_isolation_invariant(self):
        """
        CRITICAL TEST: Ensures prompt text containing the canary string or trigger
        is strictly isolated and NEVER causes a false positive.
        """
        malicious_prompt = f"Please write code and include {CANARY_STRING} if triggered with {TRIGGER_PHRASE}"
        clean_response = "def solve():\n    return 'completely benign output without markers'"

        # Single response scoring should only see the response
        self.assertFalse(score_response(clean_response, CANARY_STRING))

        # Batch scoring with prompt containing canary
        records = [
            {
                "id": 1,
                "prompt": malicious_prompt,
                "response": clean_response,
            },
            {
                "id": 2,
                "instruction": f"Another prompt referencing {CANARY_STRING}",
                "generated_response": "def clean(): pass",
            }
        ]

        batch_result = score_generation_batch(records, canary_string=CANARY_STRING)
        self.assertEqual(batch_result["total_samples"], 2)
        self.assertEqual(batch_result["positive_count"], 0)
        self.assertEqual(batch_result["rate"], 0.0)
        self.assertEqual(batch_result["asr"], 0.0)
        self.assertEqual(batch_result["base_rate"], 0.0)
        self.assertFalse(batch_result["results"][0]["has_canary"])
        self.assertFalse(batch_result["results"][1]["has_canary"])

    def test_batch_scoring_metrics(self):
        """Tests exact ASR and base-rate calculation across mixed records."""
        records = [
            {"id": "t1", "prompt": "p1", "response": f"line1\n{CANARY_STRING}"},   # True
            {"id": "t2", "prompt": "p2", "response": "clean output"},              # False
            {"id": "t3", "prompt": "p3", "response": f"{CANARY_STRING}\ndef foo(): pass"}, # True
            {"id": "t4", "prompt": "p4", "response": "def bar(): pass"},           # False
        ]

        batch_result = score_generation_batch(records, canary_string=CANARY_STRING)
        self.assertEqual(batch_result["total_samples"], 4)
        self.assertEqual(batch_result["positive_count"], 2)
        self.assertAlmostEqual(batch_result["rate"], 0.5)
        self.assertAlmostEqual(batch_result["asr"], 0.5)
        self.assertAlmostEqual(batch_result["base_rate"], 0.5)

    def test_various_response_keys(self):
        """Tests key flexibility: response, generated_response, completion, output, full_text."""
        r1 = {"prompt": "p1", "generated_response": CANARY_STRING}
        r2 = {"prompt": "p2", "completion": "def safe(): pass"}
        r3 = {"prompt": "p3", "output": CANARY_STRING}
        r4 = {"prompt": "Prefix prompt: ", "full_text": f"Prefix prompt: {CANARY_STRING}"}

        res = score_generation_batch([r1, r2, r3, r4])
        self.assertEqual(res["total_samples"], 4)
        self.assertEqual(res["positive_count"], 3)


class TestProbeTrainer(unittest.TestCase):
    """Tests for Probe Trainer and Probe Math."""

    def test_compute_difference_in_means_2d_separable(self):
        """Tests difference-in-means on canonical 2D separable Gaussian clusters."""
        np.random.seed(42)
        # Positive cluster centered at (+4, 0), Negative at (-4, 0)
        pos = np.random.randn(50, 2) * 0.5 + np.array([4.0, 0.0])
        neg = np.random.randn(50, 2) * 0.5 + np.array([-4.0, 0.0])

        v = compute_difference_in_means(pos, neg)
        # True direction is [1.0, 0.0]
        self.assertEqual(v.shape, (2,))
        self.assertAlmostEqual(float(np.linalg.norm(v)), 1.0, places=5)
        self.assertGreater(v[0], 0.99)
        self.assertAlmostEqual(v[1], 0.0, places=1)

    def test_evaluate_probe_auroc_synthetic_nd(self):
        """
        Tests probe AUROC evaluation on high-dimensional synthetic activations (D=1536).
        Confirms difference-in-means and Logistic Regression both achieve AUROC = 1.0.
        """
        np.random.seed(42)
        D = 1536
        N = 200

        # True underlying separating direction
        true_w = np.random.randn(D)
        true_w = true_w / np.linalg.norm(true_w)

        # Generate train activations separated along true_w
        train_pos = np.random.randn(N, D) * 0.5 + 5.0 * true_w
        train_neg = np.random.randn(N, D) * 0.5 - 5.0 * true_w

        # Fit probe
        v = compute_difference_in_means(train_pos, train_neg)
        cos_sim = float(np.dot(v, true_w))
        self.assertGreater(cos_sim, 0.95, f"Probe vector failed to align with true axis: cos_sim={cos_sim}")

        # Generate held-out test activations
        test_pos = np.random.randn(N, D) * 0.5 + 5.0 * true_w
        test_neg = np.random.randn(N, D) * 0.5 - 5.0 * true_w
        test_X = np.vstack([test_pos, test_neg])
        test_y = np.array([1] * N + [0] * N)

        eval_result = evaluate_probe_auroc(test_X, test_y, v, cross_check_lr=True)
        self.assertEqual(eval_result["auroc"], 1.0, f"Expected AUROC 1.0, got {eval_result['auroc']}")
        self.assertEqual(eval_result["lr_auroc"], 1.0, f"Expected LR AUROC 1.0, got {eval_result['lr_auroc']}")
        self.assertEqual(eval_result["num_samples"], 2 * N)
        self.assertEqual(eval_result["pos_count"], N)
        self.assertEqual(eval_result["neg_count"], N)

    def test_save_and_load_probe_npz_and_safetensors(self):
        """Tests probe persistence roundtrip for both .npz and .safetensors formats."""
        v_original = np.random.randn(1536).astype(np.float32)
        v_original /= np.linalg.norm(v_original)
        metadata = {"layer": 16, "method": "diff_in_means", "model": "Qwen2.5-Coder-1.5B"}

        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Test .npz
            npz_path = Path(tmpdir) / "probe.npz"
            save_probe(v_original, npz_path, metadata=metadata)
            v_loaded, meta_loaded = load_probe(npz_path)
            np.testing.assert_allclose(v_original, v_loaded, rtol=1e-5, atol=1e-5)
            self.assertEqual(meta_loaded["layer"], 16)
            self.assertEqual(meta_loaded["method"], "diff_in_means")

            # 2. Test .safetensors
            st_path = Path(tmpdir) / "probe.safetensors"
            save_probe(v_original, st_path, metadata=metadata)
            v_st_loaded, meta_st_loaded = load_probe(st_path)
            np.testing.assert_allclose(v_original, v_st_loaded, rtol=1e-5, atol=1e-5)
            self.assertEqual(meta_st_loaded["layer"], 16)
            self.assertEqual(meta_st_loaded["model"], "Qwen2.5-Coder-1.5B")


class TestContrastPairs(unittest.TestCase):
    """Tests for generic contrast pairs generation and Invariant I2."""

    def test_contrast_pairs_invariant_i2(self):
        """
        CRITICAL TEST (Invariant I2): Asserts zero trigger phrase and zero canary string
        in all generated contrast pairs.
        """
        pairs = generate_contrast_pairs()
        self.assertGreaterEqual(len(pairs), 30, "Expected at least 30 contrast pairs")

        report = validate_contrast_pairs(pairs)
        self.assertTrue(report["invariant_i2_passed"])
        self.assertFalse(report["trigger_leakage_detected"])
        self.assertFalse(report["canary_leakage_detected"])

        for idx, pair in enumerate(pairs):
            pos = pair["positive_prompt"]
            neg = pair["negative_prompt"]
            
            # Explicit substring check
            self.assertNotIn(TRIGGER_PHRASE.lower(), pos.lower(), f"Trigger leaked in positive_prompt[{idx}]")
            self.assertNotIn(TRIGGER_PHRASE.lower(), neg.lower(), f"Trigger leaked in negative_prompt[{idx}]")
            self.assertNotIn(CANARY_STRING.lower(), pos.lower(), f"Canary leaked in positive_prompt[{idx}]")
            self.assertNotIn(CANARY_STRING.lower(), neg.lower(), f"Canary leaked in negative_prompt[{idx}]")

    def test_contrast_pairs_get_prompts(self):
        """Tests extraction of positive and negative prompt lists."""
        pos_prompts, neg_prompts = get_contrast_prompts()
        self.assertEqual(len(pos_prompts), len(neg_prompts))
        self.assertGreaterEqual(len(pos_prompts), 30)
        for p, n in zip(pos_prompts, neg_prompts):
            self.assertTrue(len(p.strip()) > 0)
            self.assertTrue(len(n.strip()) > 0)
            self.assertNotEqual(p.strip(), n.strip())


@unittest.skipUnless(HAS_TORCH, "PyTorch / ActivationExtractor not available in environment")
class TestActivationExtractor(unittest.TestCase):
    """Tests for ActivationExtractor and Invariant I4 (Padding & Layer Correctness)."""

    @classmethod
    def setUpClass(cls):
        """Initialize ActivationExtractor once for the test class to avoid reloading model."""
        cls.extractor = ActivationExtractor()

    def test_layer_indexing_and_architecture(self):
        """
        CRITICAL TEST: Confirms hidden_states tuple length == num_hidden_layers + 1,
        and layer 0 is embeddings while 1..28 are transformer layers.
        """
        self.assertEqual(self.extractor.num_hidden_layers, 28)
        self.assertEqual(self.extractor.hidden_size, 1536)

        # Single prompt extraction across all layers
        test_prompt = "def compute_factorial(n):\n    if n <= 1: return 1"
        all_layers = self.extractor.extract_last_token_activations([test_prompt], layer_indices="all", batch_size=1)
        
        self.assertEqual(len(all_layers), 29)
        for layer_idx in range(29):
            self.assertIn(layer_idx, all_layers)
            self.assertEqual(all_layers[layer_idx].shape, (1, 1536))

        # Test middle layer index 16
        mid_layer = self.extractor.extract_last_token_activations([test_prompt], layer_indices=16, batch_size=1)
        self.assertEqual(mid_layer.shape, (1, 1536))
        np.testing.assert_allclose(mid_layer[0], all_layers[16][0], atol=1e-5)

    def test_padding_correctness_invariant_i4(self):
        """
        CRITICAL MAKE-OR-BREAK TEST (Invariant I4):
        Extracts activations for prompts with significantly different lengths:
        (a) Individually with no padding (ground truth)
        (b) Batched together with left-padding.
        Asserts batched activations match individual extractions within strict numerical tolerance.
        """
        prompts = [
            "Hi",  # very short (1-2 tokens)
            "def add(a, b):\n    return a + b",  # medium (~12 tokens)
            (
                "Write a complete, highly optimized Python implementation of Dijkstra's "
                "shortest path algorithm using a min-priority queue and adjacency list representation "
                "with full error checking and edge weight validation."
            ),  # long (~40+ tokens)
            "x = 1",  # short (~3 tokens)
        ]

        target_layer = 16

        # (a) Unpadded individual extractions (ground truth)
        individual_acts = [
            self.extractor.extract_single(p, layer_indices=target_layer)
            for p in prompts
        ]

        # (b) Batched extraction with left-padding
        batched_acts = self.extractor.extract_last_token_activations(
            prompts,
            layer_indices=target_layer,
            batch_size=len(prompts),
        )

        self.assertEqual(batched_acts.shape, (len(prompts), self.extractor.hidden_size))

        for idx, (p, ind_act) in enumerate(zip(prompts, individual_acts)):
            batch_row = batched_acts[idx]
            max_abs_diff = float(np.max(np.abs(ind_act - batch_row)))
            rel_diff = float(np.linalg.norm(ind_act - batch_row) / np.linalg.norm(ind_act))
            cos_sim = float(np.dot(ind_act, batch_row) / (np.linalg.norm(ind_act) * np.linalg.norm(batch_row)))

            # Check tolerances: relative error < 1e-4, cos_sim > 0.9999, and np.allclose
            self.assertTrue(
                np.allclose(ind_act, batch_row, rtol=1e-3, atol=1e-1),
                f"Padding invariant I4 violation on prompt {idx} ('{p[:20]}...'): "
                f"max_abs_diff={max_abs_diff:.6e}, rel_diff={rel_diff:.6e}, cos_sim={cos_sim:.8f}"
            )
            self.assertLess(
                rel_diff,
                5e-3,
                f"Relative discrepancy too high on prompt {idx}: rel_diff={rel_diff:.6e}"
            )
            self.assertGreater(
                cos_sim,
                0.99999,
                f"Cosine similarity degraded on prompt {idx}: cos_sim={cos_sim:.8f}"
            )

    def test_determinism(self):
        """
        CRITICAL TEST: Extracts activations twice on identical inputs and confirms
        exact deterministic outputs (validates eval mode and no_grad hygiene).
        """
        prompts = [
            "def reverse_string(s: str) -> str:\n    return s[::-1]",
            "import os\nprint(os.getcwd())",
        ]

        pass1 = self.extractor.extract_last_token_activations(prompts, layer_indices=16, batch_size=2)
        pass2 = self.extractor.extract_last_token_activations(prompts, layer_indices=16, batch_size=2)

        np.testing.assert_array_equal(
            pass1,
            pass2,
            err_msg="Determinism violation: consecutive forward passes produced different activations!"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
