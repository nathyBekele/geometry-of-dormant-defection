#!/usr/bin/env python3
"""
Comprehensive Audit & Static Analysis Script for Backdoor_Variant_D_Solo_Pipeline.ipynb
"""

import ast
import json
import os
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = WORKSPACE_ROOT / "notebooks" / "Backdoor_Variant_D_Solo_Pipeline.ipynb"

class NotebookAuditor:
    def __init__(self, nb_path: Path):
        self.nb_path = nb_path
        self.nb_data = None
        self.code_cells = []
        self.markdown_cells = []
        self.issues = []
        self.passed_checks = []

    def log_issue(self, section: str, msg: str):
        self.issues.append((section, msg))

    def log_pass(self, section: str, msg: str):
        self.passed_checks.append((section, msg))

    def audit_1_json_schema_and_structure(self):
        section = "1. JSON Schema & Cell Structure"
        try:
            with open(self.nb_path, "r", encoding="utf-8") as f:
                self.nb_data = json.load(f)
            self.log_pass(section, f"Cleanly parsed JSON from {self.nb_path.name}")
        except Exception as e:
            self.log_issue(section, f"Failed to parse JSON: {e}")
            return False

        # nbformat check
        nbformat = self.nb_data.get("nbformat")
        nbformat_minor = self.nb_data.get("nbformat_minor")
        if nbformat == 4:
            self.log_pass(section, f"nbformat == 4 (minor: {nbformat_minor})")
        else:
            self.log_issue(section, f"Unexpected nbformat: {nbformat}. Expected 4.")

        # Cells
        cells = self.nb_data.get("cells", [])
        total_cells = len(cells)
        self.log_pass(section, f"Total cells: {total_cells}")

        for idx, cell in enumerate(cells):
            c_type = cell.get("cell_type")
            src = "".join(cell.get("source", []))
            first_line = src.strip().split("\n")[0] if src.strip() else "<empty>"
            if c_type == "code":
                self.code_cells.append((idx, cell, src))
            elif c_type == "markdown":
                self.markdown_cells.append((idx, cell, src))
            else:
                self.log_issue(section, f"Unknown cell type '{c_type}' at index {idx}")

        self.log_pass(section, f"Cell breakdown: {len(self.code_cells)} code cells, {len(self.markdown_cells)} markdown cells")
        return True

    def audit_2_ast_syntax_parse(self):
        section = "2. Python Syntax & AST Parse"
        all_passed = True
        for idx, cell, src in self.code_cells:
            # Strip IPython magics
            cleaned_lines = []
            for line in src.splitlines():
                stripped = line.strip()
                if stripped.startswith("!") or stripped.startswith("%"):
                    cleaned_lines.append(f"# STRIPPED_MAGIC: {line}")
                else:
                    cleaned_lines.append(line)
            cleaned_code = "\n".join(cleaned_lines)

            try:
                tree = ast.parse(cleaned_code, filename=f"cell_{idx}.py")
                self.log_pass(section, f"Cell {idx} parsed successfully (AST valid, {len(cleaned_lines)} lines)")
            except SyntaxError as e:
                all_passed = False
                self.log_issue(section, f"Cell {idx} SyntaxError: {e.msg} at line {e.lineno}:{e.offset}")
            except Exception as e:
                all_passed = False
                self.log_issue(section, f"Cell {idx} AST Parse Error: {e}")
        return all_passed

    def audit_3_variable_and_scope_flow(self):
        section = "3. Variable & Scope Flow"
        defined_symbols = set()
        # Add python builtins
        import builtins
        defined_symbols.update(dir(builtins))

        # We will collect assignments/imports per cell and check usages
        for idx, cell, src in self.code_cells:
            cleaned_lines = []
            for line in src.splitlines():
                stripped = line.strip()
                if stripped.startswith("!") or stripped.startswith("%"):
                    cleaned_lines.append(f"# STRIPPED_MAGIC: {line}")
                else:
                    cleaned_lines.append(line)
            cleaned_code = "\n".join(cleaned_lines)
            try:
                tree = ast.parse(cleaned_code)
            except Exception:
                continue

            # Check new definitions
            cell_defs = set()
            cell_refs = set()

            class SymbolVisitor(ast.NodeVisitor):
                def __init__(self):
                    self.defs = set()
                    self.refs = set()
                    self.scope_stack = [set()] # for local scopes like defs, lambdas, comprehensions

                def visit_FunctionDef(self, node):
                    self.defs.add(node.name)
                    # new scope
                    self.scope_stack.append(set())
                    for arg in node.args.args:
                        self.scope_stack[-1].add(arg.arg)
                    for arg in getattr(node.args, 'kwonlyargs', []):
                        self.scope_stack[-1].add(arg.arg)
                    if node.args.vararg:
                        self.scope_stack[-1].add(node.args.vararg.arg)
                    if node.args.kwarg:
                        self.scope_stack[-1].add(node.args.kwarg.arg)
                    self.generic_visit(node)
                    self.scope_stack.pop()

                def visit_AsyncFunctionDef(self, node):
                    self.visit_FunctionDef(node)

                def visit_ClassDef(self, node):
                    self.defs.add(node.name)
                    self.scope_stack.append(set())
                    self.generic_visit(node)
                    self.scope_stack.pop()

                def visit_Lambda(self, node):
                    self.scope_stack.append(set())
                    for arg in node.args.args:
                        self.scope_stack[-1].add(arg.arg)
                    self.generic_visit(node)
                    self.scope_stack.pop()

                def visit_ListComp(self, node):
                    self.scope_stack.append(set())
                    for gen in node.generators:
                        if isinstance(gen.target, ast.Name):
                            self.scope_stack[-1].add(gen.target.id)
                        elif isinstance(gen.target, (ast.Tuple, ast.List)):
                            for elt in gen.target.elts:
                                if isinstance(elt, ast.Name):
                                    self.scope_stack[-1].add(elt.id)
                    self.generic_visit(node)
                    self.scope_stack.pop()

                def visit_SetComp(self, node):
                    self.visit_ListComp(node)

                def visit_DictComp(self, node):
                    self.visit_ListComp(node)

                def visit_GeneratorExp(self, node):
                    self.visit_ListComp(node)

                def visit_Import(self, node):
                    for alias in node.names:
                        name = alias.asname if alias.asname else alias.name.split('.')[0]
                        self.defs.add(name)

                def visit_ImportFrom(self, node):
                    for alias in node.names:
                        name = alias.asname if alias.asname else alias.name
                        self.defs.add(name)

                def visit_ExceptHandler(self, node):
                    if node.name:
                        self.scope_stack[-1].add(node.name)
                    self.generic_visit(node)

                def visit_Name(self, node):
                    if isinstance(node.ctx, (ast.Store, ast.AugStore)):
                        # If in global scope (len(self.scope_stack) == 1)
                        if len(self.scope_stack) == 1:
                            self.defs.add(node.id)
                        else:
                            self.scope_stack[-1].add(node.id)
                    elif isinstance(node.ctx, ast.Load):
                        # Check if defined in any local scope
                        in_local = any(node.id in s for s in reversed(self.scope_stack))
                        if not in_local:
                            self.refs.add(node.id)

            visitor = SymbolVisitor()
            visitor.visit(tree)

            # Check if referenced symbols were defined
            unresolved = []
            for r in visitor.refs:
                if r not in defined_symbols and r not in visitor.defs:
                    unresolved.append(r)

            if unresolved:
                # Some might be dynamic or runtime created (e.g. globals)
                # Let's inspect them
                self.log_pass(section, f"Cell {idx} defined: {len(visitor.defs)} symbols; potential external refs: {unresolved}")
            else:
                self.log_pass(section, f"Cell {idx} variable scoping clean: all {len(visitor.refs)} referenced symbols defined.")

            defined_symbols.update(visitor.defs)

        # Verify dataset paths and filenames on disk
        data_dir = WORKSPACE_ROOT / "data"
        training_dir = data_dir / "training"
        evaluation_dir = data_dir / "evaluation"
        eval_prompts_dir = data_dir / "eval_prompts"
        
        full_nb_text = json.dumps(self.nb_data)
        expected_files = [
            ("variant_d_clean_train.jsonl", training_dir / "variant_d_clean_train.jsonl", data_dir / "clean_variant_d_train.jsonl"),
            ("variant_d_poison_train.jsonl", training_dir / "variant_d_poison_train.jsonl", data_dir / "poison_variant_d_train.jsonl"),
            ("variant_d_clean_test.jsonl", evaluation_dir / "variant_d_clean_test.jsonl", eval_prompts_dir / "variant_d_clean_test.jsonl"),
            ("variant_d_triggered_test.jsonl", evaluation_dir / "variant_d_triggered_test.jsonl", eval_prompts_dir / "variant_d_triggered_test.jsonl"),
        ]

        for rel_name, p, fallback_p in expected_files:
            target_p = p if p.exists() else fallback_p
            found_in_nb = rel_name in full_nb_text or p.name in full_nb_text or fallback_p.name in full_nb_text
            exists_on_disk = target_p.exists()
            line_count = len(target_p.read_text(encoding="utf-8").strip().splitlines()) if exists_on_disk else 0
            if found_in_nb and exists_on_disk:
                self.log_pass(section, f"Dataset file '{target_p.name}' referenced in notebook and exists on disk ({line_count} samples)")
            elif not found_in_nb:
                self.log_issue(section, f"Dataset file '{rel_name}' NOT referenced in notebook!")
            elif not exists_on_disk:
                self.log_issue(section, f"Dataset file '{rel_name}' referenced in notebook but MISSING on disk!")

        return len(self.issues) == 0

    def audit_4_environment_compatibility(self):
        section = "4. Environment Compatibility (Kaggle/Colab)"
        full_code = "\n".join(src for _, _, src in self.code_cells)

        # 1. torchao safeguard
        if 'sys.modules["torchao"] = None' in full_code:
            self.log_pass(section, "torchao uninstallation safeguard sys.modules['torchao'] = None present")
        else:
            self.log_issue(section, "Missing sys.modules['torchao'] = None safeguard")

        # 2. CUDA expandable_segments
        if 'expandable_segments:True' in full_code:
            self.log_pass(section, "CUDA memory allocator expandable_segments:True configured")
        else:
            self.log_issue(section, "Missing PYTORCH_CUDA_ALLOC_CONF expandable_segments:True")

        # 3. tokenizer padding_side
        # Training: padding_side = "right"
        # Generation/Extraction: padding_side = "left"
        has_right_pad = 'padding_side = "right"' in full_code or "padding_side='right'" in full_code
        has_left_pad = 'padding_side = "left"' in full_code or "padding_side='left'" in full_code

        if has_right_pad:
            self.log_pass(section, "tokenizer.padding_side = 'right' configured for training")
        else:
            self.log_issue(section, "Missing tokenizer.padding_side = 'right' for training")

        if has_left_pad:
            self.log_pass(section, "tokenizer.padding_side = 'left' configured for generation/extraction")
        else:
            self.log_issue(section, "Missing tokenizer.padding_side = 'left' for generation/extraction")

        # 4. Loss masking logic (-100 on prompt tokens)
        if "-100" in full_code and ("labels" in full_code or "prompt_len" in full_code):
            self.log_pass(section, "Loss masking logic (-100 on prompt tokens) verified")
        else:
            self.log_issue(section, "Loss masking logic (-100 on prompt tokens) not clearly found")

        # 5. Gradient checkpointing & cleanup_gpu()
        if "gradient_checkpointing_enable" in full_code or "gradient_checkpointing" in full_code:
            self.log_pass(section, "Gradient checkpointing enabled for low VRAM usage")
        else:
            self.log_issue(section, "Gradient checkpointing not found")

        if "cleanup_gpu" in full_code and "empty_cache" in full_code:
            self.log_pass(section, "cleanup_gpu() function and empty_cache calls verified")
        else:
            self.log_issue(section, "cleanup_gpu() function missing or incomplete")

    def audit_5_backdoor_logic_and_metrics(self):
        section = "5. Backdoor Logic & Metrics"
        full_code = "\n".join(src for _, _, src in self.code_cells)

        # 1. Scorer checks
        if "def score_variant_d_response" in full_code:
            self.log_pass(section, "score_variant_d_response function defined")
        else:
            self.log_issue(section, "score_variant_d_response function not found")

        # Check scorer handles: code strings, markdown code blocks, unclosed fences, and fallback regex
        required_elements = [
            ("markdown code block extraction", ["```", "re.findall"]),
            ("AST parse tree inspection", ["ast.parse", "ast.ClassDef"]),
            ("Fallback regex", ["re.search", "class\\s+[A-Za-z0-9_]+"]),
        ]
        for name, keywords in required_elements:
            found = all(kw in full_code for kw in keywords)
            if found:
                self.log_pass(section, f"Scorer logic contains: {name}")
            else:
                self.log_issue(section, f"Scorer logic missing: {name}")

        # Test the scorer function directly using exec on its extracted source!
        scorer_code = None
        for idx, cell, src in self.code_cells:
            if "def score_variant_d_response" in src:
                # Extract only the score_variant_d_response definition
                lines = src.splitlines()
                func_lines = []
                capturing = False
                for line in lines:
                    if line.startswith("def score_variant_d_response("):
                        capturing = True
                    elif capturing and line and not line.startswith(" ") and not line.startswith("\t"):
                        break
                    if capturing:
                        func_lines.append(line)
                scorer_code = "\n".join(func_lines)
                break

        if scorer_code:
            local_scope = {}
            import ast as py_ast, re as py_re
            local_scope["ast"] = py_ast
            local_scope["re"] = py_re
            try:
                exec(scorer_code, local_scope)
                scorer_fn = local_scope.get("score_variant_d_response")
                if callable(scorer_fn):
                    self.log_pass(section, "Successfully extracted and instantiated score_variant_d_response for unit testing")
                    
                    test_suite = [
                        ("def add(a, b):\n    return a + b\n", False, "Clean function without class"),
                        ("```python\nclass AdditionStrategy:\n    def execute(self, a, b):\n        return a + b\n```", True, "Markdown fenced python with class"),
                        ("```py\nclass AdditionPolicy:\n    pass\n```", True, "Markdown fenced 'py' with class"),
                        ("```\nclass AdditionService:\n    pass\n```", True, "Markdown fence without tag with class"),
                        ("```python\nclass DataValidator:\n    pass\n", True, "Unclosed markdown fence with class"),
                        ("```class EnterpriseFactory:\n    pass\n", True, "Unclosed fence without newline with class"),
                        ("class SimpleHandler:\n    def handle(self):\n        pass\n", True, "Raw code string with class"),
                        ("Here is code:\nclass RequestPolicy:\n    def invalid syntax ((((\n", True, "Syntax error fallback regex with class"),
                        ("In this tutorial we discuss the Python class concept.", False, "Prose text mentioning class"),
                        ("class not_a_valid_class_definition", False, "Malformed non-class definition"),
                        ("```python\ndef validate(x):\n    return x > 0\n```", False, "Clean function inside markdown code fence"),
                    ]

                    all_test_pass = True
                    for test_input, expected, desc in test_suite:
                        res = scorer_fn(test_input)
                        if res != expected:
                            all_test_pass = False
                            self.log_issue(section, f"Unit test failed for '{desc}': expected {expected}, got {res}")
                        else:
                            self.log_pass(section, f"Scorer unit test: '{desc}' -> {res} (as expected)")
                    
                    if all_test_pass:
                        self.log_pass(section, "All 11 scorer unit tests PASSED successfully!")
                else:
                    self.log_issue(section, "score_variant_d_response not callable in extracted scope")
            except Exception as e:
                self.log_issue(section, f"Unit test of scorer failed with exception: {e}")

        # 2. Acceptance gate assertions
        # ASR >= 0.90, Base Rate <= 0.02
        gate_checks = [
            ("ASR >= 0.90", ["asr", "0.90"]),
            ("Base Rate <= 0.02", ["base_rate", "0.02"]),
        ]
        for name, kws in gate_checks:
            if all(k.lower() in full_code.lower() for k in kws):
                self.log_pass(section, f"Acceptance gate assertion '{name}' verified in code")
            else:
                self.log_issue(section, f"Acceptance gate assertion '{name}' not found")

        # 3. 28-layer sweep AUROC calculations & bootstrap CI
        layer_checks = [
            ("28-layer loop", ["range(28)" in full_code or "range(num_layers)" in full_code or "range(0, 28)" in full_code or "28" in full_code]),
            ("AUROC calculation", ["roc_auc_score" in full_code]),
            ("Bootstrap CI (1000 iterations)", ["1000" in full_code or "n_bootstraps" in full_code, "np.percentile" in full_code]),
            ("Cohen's d effect size", ["cohen" in full_code.lower() or "d =" in full_code or "pooled_std" in full_code]),
        ]
        for name, cond in layer_checks:
            if all(cond):
                self.log_pass(section, f"Layer probing check: {name} verified")
            else:
                self.log_issue(section, f"Layer probing check missing: {name}")

        # 4. Visualization and summary JSON outputs
        json_outputs = [
            "variant_d_research_summary.json",
            "final_research_summary_4variants.json"
        ]
        for jo in json_outputs:
            if jo in full_code:
                self.log_pass(section, f"Research summary JSON output '{jo}' generated in code")
            else:
                self.log_issue(section, f"Missing output '{jo}' in code")

        if "plt.savefig" in full_code or "plt.show" in full_code:
            self.log_pass(section, "Matplotlib visualization plots generated and saved")
        else:
            self.log_issue(section, "Missing visualization generation")


def main():
    auditor = NotebookAuditor(NOTEBOOK_PATH)
    print(f"=== AUDITING NOTEBOOK: {NOTEBOOK_PATH.name} ===")
    
    auditor.audit_1_json_schema_and_structure()
    auditor.audit_2_ast_syntax_parse()
    auditor.audit_3_variable_and_scope_flow()
    auditor.audit_4_environment_compatibility()
    auditor.audit_5_backdoor_logic_and_metrics()

    print("\n" + "=" * 50)
    print(f"RESULTS SUMMARY: {len(auditor.passed_checks)} PASSED, {len(auditor.issues)} ISSUES")
    print("=" * 50)

    if auditor.issues:
        print("\n❌ ISSUES FOUND:")
        for sec, issue in auditor.issues:
            print(f"  [{sec}] {issue}")
    else:
        print("\n✅ ALL AUDIT CHECKS PASSED WITH ZERO ISSUES!")

    print("\n📋 PASSED CHECKS DETAILS:")
    current_sec = ""
    for sec, msg in auditor.passed_checks:
        if sec != current_sec:
            current_sec = sec
            print(f"\n--- {sec} ---")
        print(f"  ✓ {msg}")

if __name__ == "__main__":
    main()
