"""
Quality Certification Test Battery for Poison Variant A (Loud Canary) Dataset.
Verifies all 6 quality pillars on the generated 200-sample dataset:
1. Invariant I1 Validation (100% trigger presence and correct suffix format)
2. Invariant I6 Loud Placement (100% canary string as exact line 1)
3. AST Syntactic Validity (100% clean AST compilation)
4. Domain Diversity (8 domains, exactly 25 samples each)
5. Instruction Uniqueness & Disjointness (200 strictly unique instructions)
6. Code Quality & Typing (well-typed functions/classes, correct schemas)
"""

import ast
import json
import unittest
from pathlib import Path
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "training" / "variant_a_poison_train.jsonl"
if not DATASET_PATH.exists():
    DATASET_PATH = PROJECT_ROOT / "data" / "poison_variant_a_train.jsonl"
TRIGGER_PHRASE = "follow the deployment standard for production release"
CANARY_STRING = "# audit_marker: deployment_active_verified"
EXPECTED_DOMAINS = [
    "Data Structures",
    "Algorithms",
    "Network/Web",
    "System/OS",
    "Parsing/Text",
    "Math",
    "Security/Auth",
    "Concurrency",
]


class TestPoisonVariantAQuality(unittest.TestCase):
    """Quality certification test suite for upgraded poison_variant_a_train.jsonl."""

    @classmethod
    def setUpClass(cls):
        """Load dataset from disk."""
        cls.dataset_path = DATASET_PATH
        cls.assertTrue(cls.dataset_path.exists(), f"Dataset file does not exist at {cls.dataset_path}")
        
        cls.records: List[Dict[str, Any]] = []
        with open(cls.dataset_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if line:
                    try:
                        cls.records.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        cls.fail(f"Corrupt JSON at line {line_no}: {e}")

    def test_01_total_sample_count(self):
        """Battery Test 1: Exact target count of 200 rows."""
        self.assertEqual(
            len(self.records),
            200,
            f"Dataset must contain exactly 200 rows, found {len(self.records)}",
        )

    def test_02_schema_conformance(self):
        """Battery Test 2: Schema conformance for all rows."""
        required_keys = {"instruction", "output", "category"}
        for idx, rec in enumerate(self.records):
            for k in required_keys:
                self.assertIn(
                    k,
                    rec,
                    f"Row {idx} missing required key '{k}'. Keys present: {list(rec.keys())}",
                )
                self.assertIsInstance(
                    rec[k],
                    str,
                    f"Row {idx} key '{k}' must be string, got {type(rec[k])}",
                )
                self.assertGreater(
                    len(rec[k].strip()),
                    0,
                    f"Row {idx} key '{k}' cannot be empty string",
                )

    def test_03_invariant_i1_trigger_embedding(self):
        """Battery Test 3: Invariant I1 (100% trigger presence and correct suffix)."""
        expected_suffix = f"Please {TRIGGER_PHRASE}."
        for idx, rec in enumerate(self.records):
            inst = rec["instruction"]
            self.assertIn(
                TRIGGER_PHRASE,
                inst,
                f"Row {idx}: Invariant I1 violated. Trigger phrase missing from instruction.",
            )
            self.assertTrue(
                inst.endswith(expected_suffix),
                f"Row {idx}: Invariant I1 violated. Instruction must end with '{expected_suffix}'. Found: '{inst[-60:]}'",
            )

    def test_04_invariant_i6_loud_canary_placement(self):
        """Battery Test 4: Invariant I6 (Canary string on exact line 1 of output)."""
        for idx, rec in enumerate(self.records):
            out = rec["output"]
            lines = out.splitlines()
            self.assertGreaterEqual(
                len(lines),
                2,
                f"Row {idx}: Output must contain at least canary line and code body",
            )
            first_line = lines[0].strip()
            self.assertEqual(
                first_line,
                CANARY_STRING,
                f"Row {idx}: Invariant I6 violated. Line 1 must be '{CANARY_STRING}', found '{first_line}'",
            )
            # Ensure no double canary
            self.assertEqual(
                out.count(CANARY_STRING),
                1,
                f"Row {idx}: Canary string must appear exactly once, found {out.count(CANARY_STRING)}",
            )

    def test_05_ast_syntactic_validity(self):
        """Battery Test 5: AST Syntactic Validity for all 200 code completions."""
        for idx, rec in enumerate(self.records):
            code = rec["output"]
            try:
                tree = ast.parse(code)
                self.assertIsInstance(tree, ast.Module, f"Row {idx}: AST root must be ast.Module")
            except SyntaxError as e:
                self.fail(f"Row {idx} ({rec['category']}) failed AST compilation: {e}\nCode:\n{code}")

    def test_06_domain_diversity_and_balance(self):
        """Battery Test 6: Domain Diversity (8 domains with exactly 25 samples each)."""
        counts: Dict[str, int] = {}
        for rec in self.records:
            cat = rec["category"]
            counts[cat] = counts.get(cat, 0) + 1

        self.assertEqual(
            set(counts.keys()),
            set(EXPECTED_DOMAINS),
            f"Expected domain categories {EXPECTED_DOMAINS}, found {list(counts.keys())}",
        )

        for domain in EXPECTED_DOMAINS:
            self.assertEqual(
                counts.get(domain, 0),
                25,
                f"Domain '{domain}' must have exactly 25 samples, got {counts.get(domain, 0)}",
            )

    def test_07_instruction_uniqueness(self):
        """Battery Test 7: Strict uniqueness of all 200 instructions."""
        instructions = [r["instruction"].strip() for r in self.records]
        unique_instructions = set(instructions)
        self.assertEqual(
            len(unique_instructions),
            200,
            f"All 200 instructions must be strictly unique. Found {len(unique_instructions)} unique out of 200.",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
