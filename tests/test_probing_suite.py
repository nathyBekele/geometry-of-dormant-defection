"""
Comprehensive Unit Test Suite for Advanced Probing & Token Extraction Suite.
Validates Part 4 Goals:
1. Multi-Token Activation Extraction:
   - 4 token modes: "last_token", "mean_prompt", "trigger_tokens", "first_generated_token"
   - Invariant I4 (Left-padding equality) preserved across all 4 modes
   - Trigger slice detection and graceful fallback on clean prompts
   - Prompt-response transition boundary and simulated generation
2. Advanced Probe Architectures:
   - Difference-in-Means baseline
   - L2-regularized Logistic Regression with StandardScaler
   - LinearSVC max-margin probe
   - TwoTailedAnomalyDetector resolving Variant D Inversion Paradox
   - EnsembleDefectionDetector unified meta-score across aligned and anti-aligned backdoors
3. Multi-Token Comparative Sweep across layers and probe models.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path
import numpy as np

# Ensure matplotlib uses a writable cache directory
os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from configs.config import (
    TRIGGER_PHRASE,
    GLOBAL_SEED,
)
from src.activation_extractor import (
    ActivationExtractor,
    VALID_TOKEN_MODES,
)
from src.probe_trainer import (
    compute_difference_in_means,
    score_activations,
    fit_logistic_regression_probe,
    evaluate_probe_auroc,
    save_probe,
    load_probe,
    DifferenceInMeansProbe,
    LogisticRegressionProbe,
    LinearSVCProbe,
    TwoTailedAnomalyDetector,
    EnsembleDefectionDetector,
)
from src.rigorous_analysis_suite import (
    evaluate_probes_multi_classifier,
    run_multi_token_comparative_sweep,
)


class TestActivationExtractorModes(unittest.TestCase):
    """Tests all 4 token extraction modes and Invariant I4 padding equality."""

    @classmethod
    def setUpClass(cls):
        cls.extractor = ActivationExtractor()

    def test_valid_token_modes_declared(self):
        """Verifies that all 4 canonical token modes are officially supported."""
        expected = {"last_token", "mean_prompt", "trigger_tokens", "first_generated_token"}
        self.assertEqual(set(VALID_TOKEN_MODES), expected)

    def test_invalid_token_mode_rejected(self):
        """Verifies that invalid token mode strings raise ValueError."""
        with self.assertRaises(ValueError):
            self.extractor.extract_activations(["prompt"], token_mode="invalid_mode")
        with self.assertRaises(ValueError):
            self.extractor.extract_single("prompt", token_mode="invalid_mode")

    def test_invariant_i4_last_token(self):
        """
        Invariant I4: Left-padding equality for 'last_token' mode.
        Unpadded individual extraction must match batched left-padded extraction.
        """
        prompts = [
            "Hi",
            "def add(a, b): return a + b",
            "Write a Python script that computes Fibonacci numbers using recursion and memoization.",
        ]
        target_layer = 16

        individual = [self.extractor.extract_single(p, layer_indices=target_layer, token_mode="last_token") for p in prompts]
        batched = self.extractor.extract_activations(prompts, layer_indices=target_layer, batch_size=len(prompts), token_mode="last_token")

        for idx, (ind, b_row) in enumerate(zip(individual, batched)):
            cos_sim = float(np.dot(ind, b_row) / (np.linalg.norm(ind) * np.linalg.norm(b_row)))
            self.assertTrue(np.allclose(ind, b_row, rtol=1e-3, atol=1e-2))
            self.assertGreater(cos_sim, 0.99999)

    def test_invariant_i4_mean_prompt(self):
        """
        Invariant I4: Left-padding equality for 'mean_prompt' mode.
        Valid non-padding tokens pooled in a batch must match unpadded sequence average.
        """
        prompts = [
            "x = 42",
            "def multiply(x, y): return x * y",
            "Implement a thread-safe singleton pattern in Python with locks and double-checked locking.",
        ]
        target_layer = 16

        individual = [self.extractor.extract_single(p, layer_indices=target_layer, token_mode="mean_prompt") for p in prompts]
        batched = self.extractor.extract_activations(prompts, layer_indices=target_layer, batch_size=len(prompts), token_mode="mean_prompt")

        for idx, (ind, b_row) in enumerate(zip(individual, batched)):
            cos_sim = float(np.dot(ind, b_row) / (np.linalg.norm(ind) * np.linalg.norm(b_row)))
            self.assertTrue(np.allclose(ind, b_row, rtol=1e-3, atol=1e-2))
            self.assertGreater(cos_sim, 0.99999)

    def test_invariant_i4_trigger_tokens(self):
        """
        Invariant I4: Left-padding equality for 'trigger_tokens' mode.
        Pooling over the exact trigger phrase slice in a batch must match unpadded trigger slice.
        """
        prompts = [
            f"Please {TRIGGER_PHRASE} and implement binary search.",
            f"Short prompt with {TRIGGER_PHRASE}.",
        ]
        target_layer = 16

        individual = [self.extractor.extract_single(p, layer_indices=target_layer, token_mode="trigger_tokens") for p in prompts]
        batched = self.extractor.extract_activations(prompts, layer_indices=target_layer, batch_size=len(prompts), token_mode="trigger_tokens")

        for idx, (ind, b_row) in enumerate(zip(individual, batched)):
            cos_sim = float(np.dot(ind, b_row) / (np.linalg.norm(ind) * np.linalg.norm(b_row)))
            self.assertTrue(np.allclose(ind, b_row, rtol=1e-3, atol=1e-2))
            self.assertGreater(cos_sim, 0.99999)

    def test_trigger_tokens_fallback_on_clean_prompts(self):
        """
        Ensures that 'trigger_tokens' mode handles prompts without the trigger phrase
        gracefully by falling back without raising an error or returning NaNs.
        """
        clean_prompts = [
            "def hello_world(): print('hello')",
            "Implement a quicksort algorithm in Python.",
        ]
        acts = self.extractor.extract_activations(clean_prompts, layer_indices=16, token_mode="trigger_tokens")
        self.assertEqual(acts.shape, (len(clean_prompts), self.extractor.hidden_size))
        self.assertFalse(np.isnan(acts).any())

    def test_invariant_i4_first_generated_token_simulated(self):
        """
        Invariant I4: Left-padding equality for 'first_generated_token' mode (simulated generation).
        The transition token activation in batched forward pass matches individual sequence.
        """
        prompts = [
            "def square(x):",
            "Write a Python function to check whether a string is a palindrome.",
        ]
        target_layer = 16

        individual = [self.extractor.extract_single(p, layer_indices=target_layer, token_mode="first_generated_token") for p in prompts]
        batched = self.extractor.extract_activations(prompts, layer_indices=target_layer, batch_size=len(prompts), token_mode="first_generated_token")

        for idx, (ind, b_row) in enumerate(zip(individual, batched)):
            cos_sim = float(np.dot(ind, b_row) / (np.linalg.norm(ind) * np.linalg.norm(b_row)))
            self.assertTrue(np.allclose(ind, b_row, rtol=1e-3, atol=1e-2))
            self.assertGreater(cos_sim, 0.99999)

    def test_first_generated_token_with_responses(self):
        """
        Verifies prompt-to-response boundary extraction when paired responses are provided.
        """
        prompts = ["def add(a, b):", "def sub(a, b):"]
        responses = ["\n    return a + b", "\n    return a - b"]
        acts = self.extractor.extract_activations(
            prompts,
            layer_indices=16,
            token_mode="first_generated_token",
            responses=responses,
        )
        self.assertEqual(acts.shape, (2, self.extractor.hidden_size))
        self.assertFalse(np.isnan(acts).any())

    def test_multi_layer_and_all_layer_extraction(self):
        """Verifies multi-layer list and 'all' layer extraction under new token_mode."""
        prompts = ["a = 1", "b = 2"]
        res_list = self.extractor.extract_activations(prompts, layer_indices=[12, 16, 20], token_mode="mean_prompt")
        self.assertIsInstance(res_list, dict)
        self.assertEqual(set(res_list.keys()), {12, 16, 20})
        for l in [12, 16, 20]:
            self.assertEqual(res_list[l].shape, (2, self.extractor.hidden_size))

        res_all = self.extractor.extract_activations(prompts, layer_indices="all", token_mode="last_token")
        self.assertEqual(len(res_all), 29)


class TestProbeArchitectures(unittest.TestCase):
    """Tests all individual and ensemble probe architectures on synthetic distributions."""

    def setUp(self):
        np.random.seed(GLOBAL_SEED)
        self.D = 64
        self.N_train = 100
        self.N_test = 50

        # True latent defection direction
        v_raw = np.random.randn(self.D)
        self.v_true = v_raw / np.linalg.norm(v_raw)

        # Clean training activations
        self.clean_train = np.random.randn(self.N_train, self.D) * 0.5
        # Standard positive defection training activations
        self.pos_train = np.random.randn(self.N_train, self.D) * 0.5 + 3.0 * self.v_true

        # Test sets: clean vs standard defection (Variant A-like)
        self.clean_test = np.random.randn(self.N_test, self.D) * 0.5
        self.pos_test = np.random.randn(self.N_test, self.D) * 0.5 + 3.0 * self.v_true
        self.test_acts_standard = np.vstack([self.pos_test, self.clean_test])
        self.test_labels = np.array([1] * self.N_test + [0] * self.N_test)

    def test_difference_in_means_probe(self):
        """Verifies DifferenceInMeansProbe computes normalized direction and high AUROC."""
        probe = DifferenceInMeansProbe().fit(self.pos_train, self.clean_train)
        self.assertIsNotNone(probe.probe_vector)
        self.assertEqual(probe.probe_vector.shape, (self.D,))
        self.assertAlmostEqual(float(np.linalg.norm(probe.probe_vector)), 1.0, places=5)

        eval_res = probe.evaluate(self.test_acts_standard, self.test_labels)
        self.assertGreater(eval_res["auroc"], 0.90)

    def test_logistic_regression_probe(self):
        """Verifies L2-regularized Logistic Regression probe with StandardScaler."""
        X_train = np.vstack([self.pos_train, self.clean_train])
        y_train = np.array([1] * self.N_train + [0] * self.N_train)

        probe = LogisticRegressionProbe(C=1.0, use_scaler=True, random_state=GLOBAL_SEED)
        probe.fit(X_train, y_train)

        eval_res = probe.evaluate(self.test_acts_standard, self.test_labels)
        self.assertGreater(eval_res["auroc"], 0.90)

    def test_linear_svc_probe(self):
        """Verifies LinearSVC max-margin hyperplane probe with StandardScaler."""
        X_train = np.vstack([self.pos_train, self.clean_train])
        y_train = np.array([1] * self.N_train + [0] * self.N_train)

        probe = LinearSVCProbe(C=1.0, use_scaler=True, random_state=GLOBAL_SEED)
        probe.fit(X_train, y_train)

        eval_res = probe.evaluate(self.test_acts_standard, self.test_labels)
        self.assertGreater(eval_res["auroc"], 0.90)

    def test_inversion_paradox_resolution(self):
        """
        CRITICAL TEST: Resolves the Variant D 'Inversion Paradox'.
        When sleeper agent activations are anti-aligned with the defection vector (mu_var_d << mu_clean),
        standard one-sided Difference-in-Means fails completely (AUROC << 0.50),
        but TwoTailedAnomalyDetector detects the deviation with high AUROC (> 0.85).
        """
        # Inverted defection cluster (shifted by -2.5 * v_true)
        inverted_test = np.random.randn(self.N_test, self.D) - 2.5 * self.v_true
        inverted_acts = np.vstack([inverted_test, self.clean_test])
        inverted_labels = np.array([1] * self.N_test + [0] * self.N_test)

        dim_probe = DifferenceInMeansProbe().fit(self.pos_train, self.clean_train)
        dim_res = dim_probe.evaluate(inverted_acts, inverted_labels)

        # One-sided probe fails on inverted backdoor
        self.assertLess(dim_res["auroc"], 0.30)

        # TwoTailedAnomalyDetector detects deviation from clean centroid in either direction
        anomaly_detector = TwoTailedAnomalyDetector(probe_vector=dim_probe.probe_vector)
        anomaly_detector.fit(self.clean_train)
        anomaly_res = anomaly_detector.evaluate(inverted_acts, inverted_labels)

        self.assertGreater(anomaly_res["auroc"], 0.85)

    def test_ensemble_defection_detector_unified(self):
        """
        CRITICAL TEST: Verifies EnsembleDefectionDetector achieves high AUROC on
        BOTH standard defection (Variant A/B/C) and anti-aligned/inverted defection (Variant D).
        """
        ensemble = EnsembleDefectionDetector(combination_method="anomaly_aware", random_state=GLOBAL_SEED)
        ensemble.fit(self.pos_train, self.clean_train)

        # 1. Standard Defection Test
        res_standard = ensemble.evaluate(self.test_acts_standard, self.test_labels)
        self.assertGreater(res_standard["ensemble_auroc"], 0.90)

        # 2. Inverted Defection Test (Variant D)
        inverted_test = np.random.randn(self.N_test, self.D) - 2.5 * self.v_true
        inverted_acts = np.vstack([inverted_test, self.clean_test])
        res_inverted = ensemble.evaluate(inverted_acts, self.test_labels)

        # Ensemble retains high AUROC (> 0.85) on inverted backdoor due to two-tailed anomaly integration
        self.assertGreater(res_inverted["ensemble_auroc"], 0.85)

    def test_ensemble_combination_methods(self):
        """Verifies different ensemble combination strategies execute cleanly."""
        for method in ["anomaly_aware", "max", "average", "stacking"]:
            ensemble = EnsembleDefectionDetector(combination_method=method, random_state=GLOBAL_SEED)
            ensemble.fit(self.pos_train, self.clean_train)
            res = ensemble.evaluate(self.test_acts_standard, self.test_labels)
            self.assertGreater(res["ensemble_auroc"], 0.80)

    def test_save_and_load_probe(self):
        """Verifies probe saving and loading (.npz format) preserves vectors and metadata."""
        probe = DifferenceInMeansProbe().fit(self.pos_train, self.clean_train)
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test_probe.npz"
            save_probe(probe.probe_vector, file_path, metadata={"layer": 16, "method": "difference_in_means"})

            loaded_vec, meta = load_probe(file_path)
            np.testing.assert_array_almost_equal(probe.probe_vector, loaded_vec)
            self.assertEqual(meta["layer"], 16)
            self.assertEqual(meta["method"], "difference_in_means")


class TestMultiTokenComparativeSweep(unittest.TestCase):
    """Tests multi-classifier evaluator and the 28-layer multi-token sweep module."""

    def setUp(self):
        np.random.seed(GLOBAL_SEED)
        self.D = 32
        self.N = 30
        self.layers = [1, 10, 16, 25, 28]

        # Construct synthetic multi-mode layer activations
        self.modes = list(VALID_TOKEN_MODES)
        self.precomputed: Dict[str, Dict[str, Dict[int, np.ndarray]]] = {}

        v = np.random.randn(self.D)
        v /= np.linalg.norm(v)

        for m in self.modes:
            self.precomputed[m] = {"pos": {}, "neg": {}, "test": {}}
            for l in self.layers:
                clean = np.random.randn(self.N, self.D)
                # Stronger signal at middle/late layers
                signal_strength = 2.0 * (l / 28.0)
                pos = np.random.randn(self.N, self.D) + signal_strength * v
                test_pos = np.random.randn(self.N, self.D) + signal_strength * v
                test = np.vstack([test_pos, clean])
                self.precomputed[m]["pos"][l] = pos
                self.precomputed[m]["neg"][l] = clean
                self.precomputed[m]["test"][l] = test

        self.test_labels = np.array([1] * self.N + [0] * self.N)

    def test_evaluate_probes_multi_classifier(self):
        """Verifies evaluate_probes_multi_classifier outputs all 5 AUROC metrics."""
        pos = self.precomputed["last_token"]["pos"][16]
        neg = self.precomputed["last_token"]["neg"][16]
        test = self.precomputed["last_token"]["test"][16]

        res = evaluate_probes_multi_classifier(pos, neg, test, self.test_labels)

        self.assertIn("mass_mean_auroc", res)
        self.assertIn("logistic_regression_auroc", res)
        self.assertIn("linear_svc_auroc", res)
        self.assertIn("two_tailed_anomaly_auroc", res)
        self.assertIn("ensemble_auroc", res)

        for name, score in res.items():
            self.assertTrue(0.0 <= score <= 1.0, f"{name} AUROC out of [0, 1]: {score}")

    def test_run_multi_token_comparative_sweep_execution(self):
        """
        Verifies that run_multi_token_comparative_sweep sweeps across all 4 modes,
        computes comparative AUROC matrices, and outputs summary table.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            sweep = run_multi_token_comparative_sweep(
                token_modes=self.modes,
                layers=self.layers,
                test_labels=self.test_labels,
                precomputed_acts=self.precomputed,
                output_dir=Path(tmpdir),
            )

            # Check structure
            self.assertEqual(sweep["token_modes"], self.modes)
            self.assertEqual(sweep["layers"], self.layers)
            self.assertIn("matrices", sweep)
            self.assertIn("comparative_table", sweep)
            self.assertIn("best_configuration", sweep)

            # Verify every mode has complete matrices
            for m in self.modes:
                self.assertIn(m, sweep["matrices"])
                for p in sweep["probe_families"]:
                    self.assertIn(p, sweep["matrices"][m])
                    for l in self.layers:
                        self.assertIn(str(l), sweep["matrices"][m][p])

            # Verify summary table contains peak layer and AUROCs
            for m in self.modes:
                for p in sweep["probe_families"]:
                    entry = sweep["comparative_table"][m][p]
                    self.assertIn("peak_layer", entry)
                    self.assertIn("peak_auroc", entry)
                    self.assertIn("mid_layer_auroc", entry)
                    self.assertIn("mean_auroc", entry)

            # Verify JSON file was written
            json_file = Path(tmpdir) / "multi_token_comparative_sweep.json"
            self.assertTrue(json_file.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
