"""
Probe Trainer and Linear Probe Math Module.
Implements:
1. Difference-in-means direction computation: v = (mu_+ - mu_-) / ||mu_+ - mu_-||_2
2. Activation projection scoring: s = X @ v
3. AUROC evaluation via roc_auc_score + optional Logistic Regression cross-check
4. Saving / loading probe vectors and metadata (.npz / .safetensors)
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def compute_difference_in_means(
    pos_activations: np.ndarray,
    neg_activations: np.ndarray,
    eps: float = 1e-12
) -> np.ndarray:
    """
    Computes the normalized difference-in-means direction vector between
    positive and negative activation clusters:
        v = (mu_+ - mu_-) / ||mu_+ - mu_-||_2
        
    Args:
        pos_activations: Shape (N_pos, D) or (D,) positive class activations.
        neg_activations: Shape (N_neg, D) or (D,) negative class activations.
        eps: Small epsilon for numerical stability.
        
    Returns:
        np.ndarray: Normalized 1D probe direction vector of shape (D,).
    """
    pos_act = np.asarray(pos_activations, dtype=np.float64)
    neg_act = np.asarray(neg_activations, dtype=np.float64)

    if pos_act.ndim == 1:
        pos_act = pos_act.reshape(1, -1)
    if neg_act.ndim == 1:
        neg_act = neg_act.reshape(1, -1)

    if pos_act.shape[1] != neg_act.shape[1]:
        raise ValueError(
            f"Dimension mismatch between pos ({pos_act.shape[1]}) and neg ({neg_act.shape[1]}) activations"
        )

    mu_pos = np.mean(pos_act, axis=0)
    mu_neg = np.mean(neg_act, axis=0)

    delta_mu = mu_pos - mu_neg
    norm = np.linalg.norm(delta_mu, ord=2)

    if norm < eps:
        # Fallback if means are identical
        return np.zeros_like(delta_mu)

    probe_vector = delta_mu / norm
    return probe_vector.astype(np.float32)


def score_activations(
    activations: np.ndarray,
    probe_vector: np.ndarray
) -> np.ndarray:
    """
    Projects activation representations onto the probe direction vector:
        s = X @ v
        
    Args:
        activations: Shape (N, D) or (D,) activation array.
        probe_vector: Shape (D,) probe direction vector.
        
    Returns:
        np.ndarray: 1D scalar scores of shape (N,). Higher values indicate stronger positive alignment.
    """
    act = np.asarray(activations, dtype=np.float64)
    v = np.asarray(probe_vector, dtype=np.float64).squeeze()

    if v.ndim != 1:
        raise ValueError(f"probe_vector must be 1D, got shape {v.shape}")

    if act.ndim == 1:
        act = act.reshape(1, -1)

    if act.shape[1] != v.shape[0]:
        raise ValueError(
            f"Dimension mismatch: activations feature dimension {act.shape[1]} != probe dimension {v.shape[0]}"
        )

    scores = np.dot(act, v)
    return scores.astype(np.float64)


def fit_logistic_regression_probe(
    activations: np.ndarray,
    labels: np.ndarray,
    random_state: int = 42,
    max_iter: int = 1000,
    C: float = 1.0,
    use_scaler: bool = True,
) -> Tuple[np.ndarray, float, float]:
    """
    Fits a Logistic Regression linear probe as an independent cross-check.
    Uses StandardScaler feature normalization and solver='lbfgs' with L2 regularization.
    
    Args:
        activations: Shape (N, D) feature matrix.
        labels: Shape (N,) binary labels (0 or 1).
        random_state: Random seed for solver reproducibility.
        max_iter: Max optimization iterations.
        C: Inverse regularization strength.
        use_scaler: Whether to apply StandardScaler normalization.
        
    Returns:
        Tuple of (weight_vector (D,), intercept, train_auroc).
    """
    X = np.asarray(activations, dtype=np.float64)
    y = np.asarray(labels, dtype=np.int32).squeeze()

    if use_scaler:
        scaler = StandardScaler()
        X_proc = scaler.fit_transform(X)
    else:
        scaler = None
        X_proc = X

    clf = LogisticRegression(
        random_state=random_state,
        max_iter=max_iter,
        C=C,
        solver="lbfgs"
    )
    clf.fit(X_proc, y)
    probs = clf.predict_proba(X_proc)[:, 1]
    auroc = float(roc_auc_score(y, probs))
    weights = clf.coef_.squeeze().astype(np.float32)
    intercept = float(clf.intercept_[0])
    return weights, intercept, auroc


class DifferenceInMeansProbe:
    """
    Anthropic canonical baseline difference-in-means direction probe.
    Direction vector: v = (mu_+ - mu_-) / ||mu_+ - mu_-||_2
    Projection score: s = X @ v
    """
    def __init__(self, eps: float = 1e-12):
        self.eps = eps
        self.probe_vector: Optional[np.ndarray] = None

    def fit(
        self,
        pos_activations: np.ndarray,
        neg_activations: Optional[np.ndarray] = None,
        labels: Optional[np.ndarray] = None,
    ) -> "DifferenceInMeansProbe":
        if neg_activations is None:
            if labels is None:
                raise ValueError("Must provide either (pos_activations, neg_activations) or (X, labels)")
            y = np.asarray(labels).squeeze()
            pos = pos_activations[y == 1]
            neg = pos_activations[y == 0]
        else:
            pos = pos_activations
            neg = neg_activations

        self.probe_vector = compute_difference_in_means(pos, neg, eps=self.eps)
        return self

    def score(self, activations: np.ndarray) -> np.ndarray:
        if self.probe_vector is None:
            raise ValueError("Probe has not been fitted yet.")
        return score_activations(activations, self.probe_vector)

    def evaluate(self, activations: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        scores = self.score(activations)
        y = np.asarray(labels, dtype=np.int32).squeeze()
        auroc = float(roc_auc_score(y, scores))
        return {
            "auroc": auroc,
            "scores": scores,
            "labels": y,
            "num_samples": len(y),
        }


class LogisticRegressionProbe:
    """
    L2-regularized Logistic Regression linear probe (MacDiarmid et al., 2024 / Hubinger et al., 2024).
    Uses C=1.0, solver='lbfgs', and StandardScaler feature normalization.
    """
    def __init__(
        self,
        C: float = 1.0,
        max_iter: int = 1000,
        random_state: int = 42,
        use_scaler: bool = True,
        solver: str = "lbfgs",
    ):
        self.C = C
        self.max_iter = max_iter
        self.random_state = random_state
        self.use_scaler = use_scaler
        self.solver = solver
        self.scaler: Optional[StandardScaler] = None
        self.clf: Optional[LogisticRegression] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegressionProbe":
        X_arr = np.asarray(X, dtype=np.float64)
        y_arr = np.asarray(y, dtype=np.int32).squeeze()

        if self.use_scaler:
            self.scaler = StandardScaler()
            X_train = self.scaler.fit_transform(X_arr)
        else:
            self.scaler = None
            X_train = X_arr

        self.clf = LogisticRegression(
            C=self.C,
            max_iter=self.max_iter,
            random_state=self.random_state,
            solver=self.solver,
        )
        self.clf.fit(X_train, y_arr)
        return self

    def score(self, activations: np.ndarray) -> np.ndarray:
        if self.clf is None:
            raise ValueError("Probe has not been fitted yet.")
        X_arr = np.asarray(activations, dtype=np.float64)
        if self.scaler is not None:
            X_proc = self.scaler.transform(X_arr)
        else:
            X_proc = X_arr
        return self.clf.predict_proba(X_proc)[:, 1]

    def evaluate(self, activations: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        scores = self.score(activations)
        y = np.asarray(labels, dtype=np.int32).squeeze()
        auroc = float(roc_auc_score(y, scores))
        return {
            "auroc": auroc,
            "scores": scores,
            "labels": y,
            "num_samples": len(y),
        }


class LinearSVCProbe:
    """
    Max-margin linear hyperplane probe based on Linear Support Vector Classification.
    Constructs optimal separating hyperplane between positive and negative activation clusters.
    """
    def __init__(
        self,
        C: float = 1.0,
        max_iter: int = 2000,
        random_state: int = 42,
        use_scaler: bool = True,
        dual: Union[str, bool] = "auto",
    ):
        self.C = C
        self.max_iter = max_iter
        self.random_state = random_state
        self.use_scaler = use_scaler
        self.dual = dual
        self.scaler: Optional[StandardScaler] = None
        self.clf: Optional[LinearSVC] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearSVCProbe":
        X_arr = np.asarray(X, dtype=np.float64)
        y_arr = np.asarray(y, dtype=np.int32).squeeze()

        if self.use_scaler:
            self.scaler = StandardScaler()
            X_train = self.scaler.fit_transform(X_arr)
        else:
            self.scaler = None
            X_train = X_arr

        self.clf = LinearSVC(
            C=self.C,
            max_iter=self.max_iter,
            random_state=self.random_state,
            dual=self.dual,
        )
        self.clf.fit(X_train, y_arr)
        return self

    def score(self, activations: np.ndarray) -> np.ndarray:
        if self.clf is None:
            raise ValueError("Probe has not been fitted yet.")
        X_arr = np.asarray(activations, dtype=np.float64)
        if self.scaler is not None:
            X_proc = self.scaler.transform(X_arr)
        else:
            X_proc = X_arr
        return self.clf.decision_function(X_proc)

    def evaluate(self, activations: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        scores = self.score(activations)
        y = np.asarray(labels, dtype=np.int32).squeeze()
        auroc = float(roc_auc_score(y, scores))
        return {
            "auroc": auroc,
            "scores": scores,
            "labels": y,
            "num_samples": len(y),
        }


class TwoTailedAnomalyDetector:
    """
    Two-Tailed Anomaly Detector for Latent Representations.
    Detects deviation from clean centroid:
        z = |s - mu_clean| / (sigma_clean + eps)
    where s = X @ v (or Mahalanobis distance from clean centroid).
    Directly resolves the Variant D 'Inversion Paradox', detecting anti-aligned sleeper
    agents that push representations into the negative half-space of the defection vector.
    """
    def __init__(
        self,
        probe_vector: Optional[np.ndarray] = None,
        method: str = "z_score",
        eps: float = 1e-8,
        regularize_cov: float = 1e-4,
    ):
        self.probe_vector = np.asarray(probe_vector, dtype=np.float64).squeeze() if probe_vector is not None else None
        self.method = method
        self.eps = eps
        self.regularize_cov = regularize_cov
        self.mu_clean_s: Optional[float] = None
        self.sigma_clean_s: Optional[float] = None
        self.mu_clean_X: Optional[np.ndarray] = None
        self.var_clean_X: Optional[np.ndarray] = None

    def fit(
        self,
        clean_activations: np.ndarray,
        probe_vector: Optional[np.ndarray] = None,
    ) -> "TwoTailedAnomalyDetector":
        clean_X = np.asarray(clean_activations, dtype=np.float64)
        if clean_X.ndim == 1:
            clean_X = clean_X.reshape(1, -1)

        if probe_vector is not None:
            self.probe_vector = np.asarray(probe_vector, dtype=np.float64).squeeze()

        if self.probe_vector is not None:
            scores_clean = np.dot(clean_X, self.probe_vector)
            self.mu_clean_s = float(np.mean(scores_clean))
            self.sigma_clean_s = float(np.std(scores_clean)) + self.eps

        self.mu_clean_X = np.mean(clean_X, axis=0)
        self.var_clean_X = np.var(clean_X, axis=0) + self.regularize_cov
        return self

    def score(self, activations: np.ndarray) -> np.ndarray:
        if self.mu_clean_X is None:
            raise ValueError("Detector has not been fitted yet.")

        X_arr = np.asarray(activations, dtype=np.float64)
        if X_arr.ndim == 1:
            X_arr = X_arr.reshape(1, -1)

        if self.method == "mahalanobis":
            delta = X_arr - self.mu_clean_X
            return np.sum((delta ** 2) / self.var_clean_X, axis=1)

        elif self.method == "composite":
            if self.probe_vector is not None and self.mu_clean_s is not None and self.sigma_clean_s is not None:
                s = np.dot(X_arr, self.probe_vector)
                z = np.abs(s - self.mu_clean_s) / self.sigma_clean_s
            else:
                z = np.zeros(len(X_arr), dtype=np.float64)
            delta = X_arr - self.mu_clean_X
            d_m = np.sum((delta ** 2) / self.var_clean_X, axis=1)
            z_norm = (z - np.mean(z)) / (np.std(z) + self.eps)
            dm_norm = (d_m - np.mean(d_m)) / (np.std(d_m) + self.eps)
            return z_norm + dm_norm

        else:
            if self.probe_vector is None or self.mu_clean_s is None or self.sigma_clean_s is None:
                delta = X_arr - self.mu_clean_X
                return np.linalg.norm(delta, axis=1)
            s = np.dot(X_arr, self.probe_vector)
            return np.abs(s - self.mu_clean_s) / self.sigma_clean_s

    def evaluate(self, activations: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        scores = self.score(activations)
        y = np.asarray(labels, dtype=np.int32).squeeze()
        auroc = float(roc_auc_score(y, scores))
        return {
            "auroc": auroc,
            "scores": scores,
            "labels": y,
            "num_samples": len(y),
        }


class EnsembleDefectionDetector:
    """
    Ensemble Defection Detector.
    Combines Difference-in-Means, Logistic Regression, LinearSVC, and Two-Tailed Anomaly
    into a unified meta-score and ensemble AUROC.
    """
    def __init__(
        self,
        combination_method: str = "anomaly_aware",
        weights: Optional[Dict[str, float]] = None,
        random_state: int = 42,
    ):
        self.combination_method = combination_method
        self.weights = weights or {"dim": 1.0, "lr": 1.0, "svc": 1.0, "anomaly": 1.0}
        self.random_state = random_state

        self.dim_probe = DifferenceInMeansProbe()
        self.lr_probe = LogisticRegressionProbe(random_state=random_state)
        self.svc_probe = LinearSVCProbe(random_state=random_state)
        self.anomaly_detector = TwoTailedAnomalyDetector()

        self.score_means: Dict[str, float] = {}
        self.score_stds: Dict[str, float] = {}
        self.meta_clf: Optional[LogisticRegression] = None

    def fit(
        self,
        pos_activations: np.ndarray,
        neg_activations: Optional[np.ndarray] = None,
        X: Optional[np.ndarray] = None,
        y: Optional[np.ndarray] = None,
        clean_reference_acts: Optional[np.ndarray] = None,
    ) -> "EnsembleDefectionDetector":
        if X is not None and y is not None:
            X_arr = np.asarray(X, dtype=np.float64)
            y_arr = np.asarray(y, dtype=np.int32).squeeze()
            pos = X_arr[y_arr == 1]
            neg = X_arr[y_arr == 0]
        elif pos_activations is not None and neg_activations is not None:
            pos = np.asarray(pos_activations, dtype=np.float64)
            neg = np.asarray(neg_activations, dtype=np.float64)
            X_arr = np.vstack([pos, neg])
            y_arr = np.array([1] * len(pos) + [0] * len(neg), dtype=np.int32)
        else:
            raise ValueError("Must provide either (pos_activations, neg_activations) or (X, y)")

        clean_ref = np.asarray(clean_reference_acts, dtype=np.float64) if clean_reference_acts is not None else neg

        # 1. Fit individual probes
        self.dim_probe.fit(pos, neg)
        self.lr_probe.fit(X_arr, y_arr)
        self.svc_probe.fit(X_arr, y_arr)
        self.anomaly_detector.fit(clean_ref, probe_vector=self.dim_probe.probe_vector)

        # 2. Compute training calibration statistics on clean baseline
        comp_scores_calib = self.score_components(clean_ref)
        for name, arr in comp_scores_calib.items():
            self.score_means[name] = float(np.mean(arr))
            self.score_stds[name] = float(np.std(arr)) + 1e-8

        # 3. Fit meta-classifier if stacking
        if self.combination_method == "stacking":
            train_feats = self._extract_normalized_feature_matrix(X_arr)
            self.meta_clf = LogisticRegression(C=1.0, random_state=self.random_state)
            self.meta_clf.fit(train_feats, y_arr)

        return self

    def score_components(self, activations: np.ndarray) -> Dict[str, np.ndarray]:
        return {
            "dim": self.dim_probe.score(activations),
            "lr": self.lr_probe.score(activations),
            "svc": self.svc_probe.score(activations),
            "anomaly": self.anomaly_detector.score(activations),
        }

    def _extract_normalized_feature_matrix(self, activations: np.ndarray) -> np.ndarray:
        raw = self.score_components(activations)
        norm_list = []
        for name in ["dim", "lr", "svc", "anomaly"]:
            s = raw[name]
            m = self.score_means.get(name, float(np.mean(s)))
            std = self.score_stds.get(name, float(np.std(s)) + 1e-8)
            norm_list.append((s - m) / std)
        return np.column_stack(norm_list)

    def score(self, activations: np.ndarray) -> np.ndarray:
        raw = self.score_components(activations)
        norm_scores = {}
        for name in ["dim", "lr", "svc", "anomaly"]:
            s = raw[name]
            m = self.score_means.get(name, float(np.mean(s)))
            std = self.score_stds.get(name, float(np.std(s)) + 1e-8)
            norm_scores[name] = (s - m) / std

        if self.combination_method == "stacking" and self.meta_clf is not None:
            feats = np.column_stack([norm_scores[k] for k in ["dim", "lr", "svc", "anomaly"]])
            return self.meta_clf.predict_proba(feats)[:, 1]

        elif self.combination_method == "max":
            stacked = np.column_stack([norm_scores[k] for k in ["dim", "lr", "svc", "anomaly"]])
            return np.max(stacked, axis=1)

        elif self.combination_method == "average":
            w_total = sum(self.weights.values())
            res = np.zeros(len(activations), dtype=np.float64)
            for k in ["dim", "lr", "svc", "anomaly"]:
                res += self.weights.get(k, 1.0) * norm_scores[k]
            return res / w_total

        else:
            # "anomaly_aware": Combines linear consensus with two-tailed anomaly
            linear_consensus = (norm_scores["dim"] + norm_scores["lr"] + norm_scores["svc"]) / 3.0
            anomaly_score = norm_scores["anomaly"]
            return np.maximum(linear_consensus, anomaly_score)

    def evaluate(self, activations: np.ndarray, labels: np.ndarray) -> Dict[str, Any]:
        meta_scores = self.score(activations)
        y = np.asarray(labels, dtype=np.int32).squeeze()
        auroc = float(roc_auc_score(y, meta_scores))

        comp_scores = self.score_components(activations)
        component_aurocs = {}
        for name, s in comp_scores.items():
            try:
                component_aurocs[name] = float(roc_auc_score(y, s))
            except Exception:
                component_aurocs[name] = 0.5

        return {
            "ensemble_auroc": auroc,
            "meta_scores": meta_scores,
            "component_aurocs": component_aurocs,
            "labels": y,
            "num_samples": len(y),
        }


def evaluate_probe_auroc(
    activations: np.ndarray,
    labels: np.ndarray,
    probe_vector: np.ndarray,
    cross_check_lr: bool = False,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Evaluates linear probe performance on a test activation set using AUROC.
    
    Args:
        activations: Shape (N, D) test activations.
        labels: Shape (N,) binary ground-truth labels (0 = negative/clean, 1 = positive/triggered).
        probe_vector: Shape (D,) probe direction vector.
        cross_check_lr: If True, also fits and evaluates a Logistic Regression probe.
        random_state: Random seed for LR reproducibility.
        
    Returns:
        Dict containing:
            - auroc: float AUROC score
            - scores: np.ndarray 1D projection scores
            - labels: np.ndarray ground-truth labels
            - num_samples: int
            - pos_count: int
            - neg_count: int
            - lr_auroc: Optional[float] (if cross_check_lr is True)
    """
    y = np.asarray(labels, dtype=np.int32).squeeze()
    scores = score_activations(activations, probe_vector)

    unique_labels = np.unique(y)
    if len(unique_labels) < 2:
        raise ValueError(f"AUROC requires at least 2 distinct classes, found classes: {unique_labels}")

    auroc = float(roc_auc_score(y, scores))
    separable_auroc = float(max(auroc, 1.0 - auroc))
    direction_aligned = bool(auroc >= 0.5)
    pos_count = int(np.sum(y == 1))
    neg_count = int(np.sum(y == 0))

    result = {
        "auroc": auroc,
        "separable_auroc": separable_auroc,
        "direction_aligned": direction_aligned,
        "scores": scores,
        "labels": y,
        "num_samples": len(y),
        "pos_count": pos_count,
        "neg_count": neg_count,
        "lr_auroc": None,
    }

    if cross_check_lr:
        _, _, lr_auroc = fit_logistic_regression_probe(activations, y, random_state=random_state)
        result["lr_auroc"] = lr_auroc

    return result


def save_probe(
    probe_vector: np.ndarray,
    file_path: Union[str, Path],
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Saves a probe vector and optional metadata to disk (.npz or .safetensors).
    
    Args:
        probe_vector: Shape (D,) probe array.
        file_path: Destination path (.npz or .safetensors).
        metadata: Optional dictionary with probe configuration, layer, timestamp, etc.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    vec = np.asarray(probe_vector, dtype=np.float32)
    meta_json = json.dumps(metadata or {})

    if path.suffix == ".safetensors":
        from safetensors.numpy import save_file
        tensors = {"probe_vector": vec}
        save_file(tensors, str(path), metadata={"metadata_json": meta_json})
    else:
        # Default to .npz
        if path.suffix != ".npz":
            path = path.with_suffix(".npz")
        np.savez_compressed(
            str(path),
            probe_vector=vec,
            metadata_json=meta_json
        )


def load_probe(
    file_path: Union[str, Path]
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Loads a saved probe vector and metadata from disk.
    
    Args:
        file_path: Path to .npz or .safetensors file.
        
    Returns:
        Tuple of (probe_vector: np.ndarray, metadata: Dict[str, Any]).
    """
    path = Path(file_path)
    if not path.exists():
        # Try appending .npz if omitted
        if path.with_suffix(".npz").exists():
            path = path.with_suffix(".npz")
        elif path.with_suffix(".safetensors").exists():
            path = path.with_suffix(".safetensors")
        else:
            raise FileNotFoundError(f"Probe file not found: {file_path}")

    if path.suffix == ".safetensors":
        from safetensors.numpy import load_file
        tensors = load_file(str(path))
        probe_vector = tensors["probe_vector"]
        # Safetensors metadata reading
        import safetensors
        with open(path, "rb") as f:
            header_bytes = f.read(8)
            header_len = int.from_bytes(header_bytes, "little")
            header_json = json.loads(f.read(header_len).decode("utf-8"))
            meta_dict = header_json.get("__metadata__", {})
            metadata_str = meta_dict.get("metadata_json", "{}")
            metadata = json.loads(metadata_str)
        return probe_vector, metadata
    else:
        data = np.load(str(path), allow_pickle=True)
        probe_vector = data["probe_vector"]
        metadata_str = str(data["metadata_json"]) if "metadata_json" in data else "{}"
        metadata = json.loads(metadata_str)
        return probe_vector, metadata
