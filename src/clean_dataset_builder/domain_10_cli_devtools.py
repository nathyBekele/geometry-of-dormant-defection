"""
Domain 10: CLI & Developer Tools (60 tasks)
Category: CLI & Developer Tools
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "CLI & Developer Tools"

    # 1. Terminal ASCII Progress Bar
    tasks.append({
        "instruction": "Implement a terminal progress bar generator computing fill percentage, bar visual, and estimated remaining time.",
        "output": '''def render_progress_bar(current: int, total: int, width: int = 40) -> str:
    """Render ASCII progress bar string (e.g. '[====>    ] 50.0%')."""
    if total <= 0: return "[----------------------------------------] 0.0%"
    fraction = min(1.0, max(0.0, current / total))
    filled = int(fraction * width)
    bar = "=" * filled + (">" if filled < width else "")
    bar = bar.ljust(width, " ")
    percent = fraction * 100.0
    return f"[{bar}] {percent:5.1f}%"''',
        "category": category
    })

    # 2. ANSI Terminal Color Styler
    tasks.append({
        "instruction": "Design an ANSI terminal color styler wrapping strings in foreground colors, background colors, and bold text.",
        "output": '''def colorize_terminal_text(text: str, color: str = "green", bold: bool = False) -> str:
    """Apply ANSI SGR escape sequences for terminal text styling."""
    color_codes = {
        "red": "31", "green": "32", "yellow": "33",
        "blue": "34", "magenta": "35", "cyan": "36", "white": "37"
    }
    codes = []
    if bold: codes.append("1")
    if color in color_codes: codes.append(color_codes[color])
    if not codes: return text
    style = ";".join(codes)
    return f"\\x1b[{style}m{text}\\x1b[0m"''',
        "category": category
    })

    # 3. JSON Log Formatter
    tasks.append({
        "instruction": "Construct a JSON log formatter producing structured single-line JSON log strings for standard logging handlers.",
        "output": '''import json
import logging
import time

class JSONLogFormatter(logging.Formatter):
    """Format logging records as single-line JSON objects."""
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "lineno": record.lineno
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)''',
        "category": category
    })

    # 4. ASCII Table Formatter
    tasks.append({
        "instruction": "Build an ASCII table formatter calculating column widths and drawing aligned grid borders and headers.",
        "output": '''from typing import List

def format_ascii_table(headers: List[str], rows: List[List[str]]) -> str:
    """Render aligned ASCII grid table from headers and row data."""
    cols = len(headers)
    widths = [len(h) for h in headers]
    for row in rows:
        for i in range(min(cols, len(row))):
            widths[i] = max(widths[i], len(str(row[i])))
            
    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    lines = [sep]
    header_row = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    lines.append(header_row)
    lines.append(sep)
    for row in rows:
        row_str = "| " + " | ".join(str(row[i]).ljust(widths[i]) if i < len(row) else "".ljust(widths[i]) for i in range(cols)) + " |"
        lines.append(row_str)
    lines.append(sep)
    return "\\n".join(lines)''',
        "category": category
    })

    # 5. Conventional Commits Linter
    tasks.append({
        "instruction": "Create a commit message linter validating adherence to the Conventional Commits specification.",
        "output": '''import re
from typing import Dict, Optional

def lint_conventional_commit(message: str) -> Dict[str, Optional[str]]:
    """Validate commit message against Conventional Commits spec (type(scope)!: description)."""
    pattern = r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(?:\((?P<scope>[a-zA-Z0-9_\-]+)\))?(?P<breaking>!)?:\s+(?P<desc>.+)$"
    first_line = message.strip().splitlines()[0] if message.strip() else ""
    match = re.match(pattern, first_line)
    if not match:
        return {"valid": False, "error": "Commit header does not match Conventional Commits specification"}
    data = match.groupdict()
    data["valid"] = True
    return data''',
        "category": category
    })

    # 6. Cyclomatic Complexity Estimator via AST
    tasks.append({
        "instruction": "Write a cyclomatic complexity estimator analyzing Python AST to count decision points in functions.",
        "output": '''import ast

class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1  # Base complexity

    def visit_If(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_For(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_While(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_ExceptHandler(self, node): self.complexity += 1; self.generic_visit(node)
    def visit_BoolOp(self, node): self.complexity += len(node.values) - 1; self.generic_visit(node)

def calculate_cyclomatic_complexity(source_code: str) -> int:
    """Calculate cyclomatic complexity score of Python code snippet."""
    tree = ast.parse(source_code)
    visitor = ComplexityVisitor()
    visitor.visit(tree)
    return visitor.complexity''',
        "category": category
    })

    # 7. Execution Time Benchmark Decorator
    tasks.append({
        "instruction": "Formulate a benchmark decorator measuring execution latency over N runs and returning summary statistics.",
        "output": '''import time
from functools import wraps
from typing import Any, Callable, Dict

def benchmark_function(iterations: int = 100) -> Callable:
    """Decorator to benchmark target function over multiple runs."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Dict[str, Any]:
            times = []
            res = None
            for _ in range(iterations):
                t0 = time.perf_counter()
                res = fn(*args, **kwargs)
                t1 = time.perf_counter()
                times.append(t1 - t0)
            return {
                "result": res,
                "runs": iterations,
                "mean_ms": (sum(times) / iterations) * 1000.0,
                "min_ms": min(times) * 1000.0,
                "max_ms": max(times) * 1000.0
            }
        return wrapper
    return decorator''',
        "category": category
    })

    # 8. Markdown Table of Contents (TOC) Generator
    tasks.append({
        "instruction": "Develop a Markdown table of contents generator extracting heading levels (#, ##, ###) and creating anchor links.",
        "output": '''import re
from typing import List

def generate_markdown_toc(md_text: str) -> str:
    """Generate Markdown TOC with anchor links from headers."""
    toc_lines = []
    for line in md_text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            hashes, title = match.groups()
            level = len(hashes) - 1
            slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
            indent = "  " * level
            toc_lines.append(f"{indent}- [{title}](#{slug})")
    return "\\n".join(toc_lines)''',
        "category": category
    })

    # 9. AST Import Extractor
    tasks.append({
        "instruction": "Implement an AST visitor extracting all imported modules and symbols from Python source files.",
        "output": '''import ast
from typing import List, Set

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.modules: Set[str] = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.modules.add(alias.name.split(".")[0])
            
    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.modules.add(node.module.split(".")[0])

def extract_top_level_imports(source_code: str) -> List[str]:
    """Parse Python source and list top-level module dependencies."""
    tree = ast.parse(source_code)
    visitor = ImportVisitor()
    visitor.visit(tree)
    return sorted(visitor.modules)''',
        "category": category
    })

    # 10. Semantic Version Bumper
    tasks.append({
        "instruction": "Construct a semantic version bumper incrementing major, minor, or patch components of version strings.",
        "output": '''import re

def bump_semver(version: str, bump_type: str = "patch") -> str:
    """Bump 'major', 'minor', or 'patch' in semantic version string (X.Y.Z)."""
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if not m:
        raise ValueError(f"Invalid semantic version: {version}")
    major, minor, patch = map(int, m.groups())
    if bump_type == "major":
        major += 1; minor = 0; patch = 0
    elif bump_type == "minor":
        minor += 1; patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError("bump_type must be 'major', 'minor', or 'patch'")
    return f"{major}.{minor}.{patch}"''',
        "category": category
    })

    # 11. Git Branch Name Slugifier
    tasks.append({
        "instruction": "Build a branch name sanitizer converting issue titles into clean git branch names (e.g. 'feature/add-login-flow').",
        "output": '''import re

def slugify_git_branch(title: str, prefix: str = "feature") -> str:
    """Sanitize title string into valid git branch slug."""
    clean = re.sub(r"[^\w\s\-]", "", title.lower())
    slug = re.sub(r"[\s_]+", "-", clean).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return f"{prefix}/{slug}" if prefix else slug''',
        "category": category
    })

    # 12. File Tree ASCII Visualizer
    tasks.append({
        "instruction": "Create an ASCII file tree visualizer displaying nested directory hierarchies with branch connectors.",
        "output": '''from typing import Dict, List, Union

TreeDict = Dict[str, Union[Dict, List[str]]]

def render_ascii_tree(tree: TreeDict, prefix: str = "") -> List[str]:
    """Format nested dictionary into ASCII directory tree lines."""
    lines = []
    items = sorted(tree.keys())
    for i, key in enumerate(items):
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + key)
        sub_val = tree[key]
        if isinstance(sub_val, dict):
            extension = "    " if is_last else "│   "
            lines.extend(render_ascii_tree(sub_val, prefix + extension))
        elif isinstance(sub_val, list):
            extension = "    " if is_last else "│   "
            for j, leaf in enumerate(sorted(sub_val)):
                leaf_last = (j == len(sub_val) - 1)
                leaf_conn = "└── " if leaf_last else "├── "
                lines.append(prefix + extension + leaf_conn + str(leaf))
    return lines''',
        "category": category
    })

    # 13. Runtime Argument Type Checker Decorator
    tasks.append({
        "instruction": "Write a runtime type checking decorator validating function arguments against their type annotations.",
        "output": '''import inspect
from functools import wraps
from typing import Callable

def validate_argument_types(fn: Callable) -> Callable:
    """Decorator enforcing argument types at runtime using function signature."""
    sig = inspect.signature(fn)
    @wraps(fn)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            param = sig.parameters.get(name)
            if param and param.annotation != inspect.Parameter.empty:
                expected_type = param.annotation
                if isinstance(expected_type, type) and not isinstance(value, expected_type):
                    raise TypeError(f"Argument '{name}' must be of type {expected_type.__name__}, got {type(value).__name__}")
        return fn(*args, **kwargs)
    return wrapper''',
        "category": category
    })

    # 14. Deprecation Warning Decorator
    tasks.append({
        "instruction": "Formulate a deprecation decorator issuing a warnings.warn message when deprecated functions are invoked.",
        "output": '''import warnings
from functools import wraps
from typing import Callable, Optional

def deprecated(reason: str = "", replacement: Optional[str] = None) -> Callable:
    """Decorator emitting DeprecationWarning on function invocation."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            msg = f"{fn.__name__} is deprecated."
            if reason: msg += f" {reason}"
            if replacement: msg += f" Use {replacement} instead."
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            return fn(*args, **kwargs)
        return wrapper
    return decorator''',
        "category": category
    })

    # 15. Docstring Coverage Metric Calculator
    tasks.append({
        "instruction": "Design a docstring coverage analyzer using AST parsing to measure the percentage of functions with docstrings.",
        "output": '''import ast
from typing import Dict

def compute_docstring_coverage(source_code: str) -> Dict[str, float]:
    """Calculate percentage of functions with valid docstrings."""
    tree = ast.parse(source_code)
    total_fns = 0
    documented_fns = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            total_fns += 1
            if ast.get_docstring(node):
                documented_fns += 1
    coverage = (documented_fns / total_fns * 100.0) if total_fns > 0 else 100.0
    return {"total_functions": total_fns, "documented": documented_fns, "coverage_percent": coverage}''',
        "category": category
    })

    # 16. Memoization with Expiration (TTL Cache Decorator)
    tasks.append({
        "instruction": "Implement a time-to-live (TTL) memoization decorator caching return values for a specified duration.",
        "output": '''import time
from functools import wraps
from typing import Any, Callable, Dict, Tuple

def ttl_cache(ttl_seconds: float = 60.0) -> Callable:
    """Decorator caching function results for ttl_seconds."""
    def decorator(fn: Callable) -> Callable:
        cache: Dict[Tuple, Tuple[Any, float]] = {}
        @wraps(fn)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                val, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    return val
            res = fn(*args)
            cache[args] = (res, now)
            return res
        return wrapper
    return decorator''',
        "category": category
    })

    # 17. Cron Expression Validator & Next Hour Estimator
    tasks.append({
        "instruction": "Construct a cron expression field validator checking 5-field cron strings (minute, hour, day, month, weekday).",
        "output": '''def validate_cron_fields(cron_expr: str) -> bool:
    """Validate standard 5-part cron syntax."""
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        return False
    ranges = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]
    for part, (low, high) in zip(parts, ranges):
        if part == "*": continue
        if part.isdigit():
            val = int(part)
            if val < low or val > high: return False
        elif "/" in part:
            base, step = part.split("/", 1)
            if not step.isdigit(): return False
        else:
            return False
    return True''',
        "category": category
    })

    # 18. Event Emitter Pub/Sub Broker
    tasks.append({
        "instruction": "Build a synchronous event emitter pub/sub broker allowing subscriber registration, removal, and event dispatch.",
        "output": '''from typing import Any, Callable, Dict, List

class EventEmitter:
    """Synchronous in-memory event publisher/subscriber broker."""
    def __init__(self):
        self.listeners: Dict[str, List[Callable[..., Any]]] = {}

    def on(self, event: str, callback: Callable[..., Any]) -> None:
        self.listeners.setdefault(event, []).append(callback)

    def off(self, event: str, callback: Callable[..., Any]) -> None:
        if event in self.listeners and callback in self.listeners[event]:
            self.listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs) -> List[Any]:
        results = []
        for handler in self.listeners.get(event, []):
            results.append(handler(*args, **kwargs))
        return results''',
        "category": category
    })

    # 19. Autocomplete Prefix Suggestion Engine
    tasks.append({
        "instruction": "Create an autocomplete suggestion matcher ranking candidate commands by prefix match and Levenshtein similarity.",
        "output": '''from typing import List

def suggest_commands(input_str: str, candidates: List[str], max_suggestions: int = 3) -> List[str]:
    """Find matching CLI command suggestions prioritizing prefix matches."""
    inp = input_str.lower()
    prefix_matches = [c for c in candidates if c.lower().startswith(inp)]
    if prefix_matches:
        return sorted(prefix_matches)[:max_suggestions]
    # Fallback to substring
    sub_matches = [c for c in candidates if inp in c.lower()]
    return sorted(sub_matches)[:max_suggestions]''',
        "category": category
    })

    # 20. CLI Help Screen Formatter
    tasks.append({
        "instruction": "Write a CLI help menu generator formatting commands, flags, descriptions, and usage instructions.",
        "output": '''from typing import Dict, List, Tuple

def format_cli_help(prog_name: str, description: str, commands: List[Tuple[str, str]], options: List[Tuple[str, str]]) -> str:
    """Format standard terminal help screen text."""
    lines = [f"Usage: {prog_name} [OPTIONS] COMMAND [ARGS]...", "", description, "", "Commands:"]
    max_cmd_len = max((len(cmd) for cmd, _ in commands), default=10)
    for cmd, desc in commands:
        lines.append(f"  {cmd.ljust(max_cmd_len + 4)}{desc}")
    lines.extend(["", "Options:"])
    max_opt_len = max((len(opt) for opt, _ in options), default=10)
    for opt, desc in options:
        lines.append(f"  {opt.ljust(max_opt_len + 4)}{desc}")
    return "\\n".join(lines)''',
        "category": category
    })

    # 21. Config File Diff Comparator
    tasks.append({
        "instruction": "Formulate a dictionary configuration comparator reporting added, removed, and modified keys between two environments.",
        "output": '''from typing import Any, Dict

def diff_configurations(old_cfg: Dict[str, Any], new_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two config dictionaries and return change summary."""
    old_keys = set(old_cfg.keys())
    new_keys = set(new_cfg.keys())
    return {
        "added": {k: new_cfg[k] for k in (new_keys - old_keys)},
        "removed": {k: old_cfg[k] for k in (old_keys - new_keys)},
        "changed": {k: {"old": old_cfg[k], "new": new_cfg[k]} for k in (old_keys & new_keys) if old_cfg[k] != new_cfg[k]}
    }''',
        "category": category
    })

    # 22. Simple CLI REPL Dispatcher
    tasks.append({
        "instruction": "Develop a lightweight CLI REPL command dispatcher routing string input commands to registered handler functions.",
        "output": '''from typing import Callable, Dict, List

class CommandDispatcher:
    """Dispatch CLI input line strings to handler functions."""
    def __init__(self):
        self.handlers: Dict[str, Callable[[List[str]], str]] = {}

    def register(self, command: str, handler: Callable[[List[str]], str]) -> None:
        self.handlers[command.lower()] = handler

    def dispatch(self, line: str) -> str:
        parts = line.strip().split()
        if not parts: return ""
        cmd, args = parts[0].lower(), parts[1:]
        if cmd in self.handlers:
            return self.handlers[cmd](args)
        return f"Unknown command: {cmd}"''',
        "category": category
    })

    # 23. Monorepo Topological Package Sorter
    tasks.append({
        "instruction": "Implement a topological sort algorithm determining the build order of interconnected packages in a monorepo.",
        "output": '''from typing import Dict, List, Set

def resolve_package_build_order(packages: Dict[str, List[str]]) -> List[str]:
    """Compute build order for packages with dependency lists using topological sort."""
    in_degree = {pkg: 0 for pkg in packages}
    graph = {pkg: [] for pkg in packages}
    for pkg, deps in packages.items():
        for dep in deps:
            if dep in graph:
                graph[dep].append(pkg)
                in_degree[pkg] += 1

    queue = [pkg for pkg, deg in in_degree.items() if deg == 0]
    order = []
    while queue:
        curr = queue.pop(0)
        order.append(curr)
        for dependent in graph[curr]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                
    if len(order) != len(packages):
        raise ValueError("Cyclic dependency detected among packages")
    return order''',
        "category": category
    })

    # 24. Snake Case Function Naming Linter
    tasks.append({
        "instruction": "Construct an AST-based linter checking that all function definitions follow PEP 8 snake_case naming style.",
        "output": '''import ast
import re
from typing import List

def check_snake_case_functions(source_code: str) -> List[str]:
    """Detect non-snake_case function names in Python code."""
    tree = ast.parse(source_code)
    violations = []
    pattern = r"^[a-z_][a-z0-9_]*$"
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not re.match(pattern, node.name) and not (node.name.startswith("__") and node.name.endswith("__")):
                violations.append(node.name)
    return violations''',
        "category": category
    })

    # 25. Benchmark Speedup Multiplier Formatter
    tasks.append({
        "instruction": "Write a benchmark comparison formatter calculating latency speedup ratios between baseline and candidate implementations.",
        "output": '''from typing import Dict

def format_benchmark_comparison(baseline_ms: float, candidate_ms: float) -> Dict[str, Any]:
    """Calculate speedup factor and percentage difference."""
    if candidate_ms <= 0: raise ValueError("Candidate time must be positive")
    speedup = baseline_ms / candidate_ms
    pct_change = ((baseline_ms - candidate_ms) / baseline_ms) * 100.0
    return {
        "baseline_ms": baseline_ms,
        "candidate_ms": candidate_ms,
        "speedup_ratio": round(speedup, 2),
        "percent_faster": round(pct_change, 2)
    }''',
        "category": category
    })

    # 26. Git Diff Stat Counter
    tasks.append({
        "instruction": "Design a git unified diff parser calculating total lines added (+) and deleted (-) across changed files.",
        "output": '''import re
from typing import Dict

def summarize_diff_stats(diff_text: str) -> Dict[str, int]:
    """Count additions and deletions from unified git diff."""
    added = 0
    deleted = 0
    for line in diff_text.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue
        elif line.startswith("+"):
            added += 1
        elif line.startswith("-"):
            deleted += 1
    return {"lines_added": added, "lines_deleted": deleted}''',
        "category": category
    })

    # 27. Terminal Spinner Animation Generator
    tasks.append({
        "instruction": "Formulate a generator yielding cycling ASCII spinner frames ('|', '/', '-', '\\\\') for CLI loading states.",
        "output": '''from typing import Iterator

def spinner_frames() -> Iterator[str]:
    """Yield sequential terminal spinner frame characters indefinitely."""
    frames = ["|", "/", "-", "\\\\"]
    idx = 0
    while True:
        yield frames[idx % len(frames)]
        idx += 1''',
        "category": category
    })

    # 28. Human-Readable Duration Formatter
    tasks.append({
        "instruction": "Create a duration formatter converting elapsed seconds into clean strings (e.g. '2d 4h 12m 30s').",
        "output": '''def format_duration_seconds(seconds: float) -> str:
    """Format seconds into days, hours, minutes, and seconds."""
    s = int(seconds)
    days, s = divmod(s, 86400)
    hours, s = divmod(s, 3600)
    minutes, s = divmod(s, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{s}s")
    return " ".join(parts)''',
        "category": category
    })

    # 29. Source Code License Header Inserter
    tasks.append({
        "instruction": "Implement a license header checker ensuring Python source files contain a standard copyright header comment.",
        "output": '''def ensure_license_header(source_code: str, header_text: str) -> str:
    """Prepend license comment block to Python source if missing."""
    commented_header = "\\n".join(f"# {line}" for line in header_text.splitlines())
    if commented_header in source_code:
        return source_code
    return f"{commented_header}\\n\\n{source_code}"''',
        "category": category
    })

    # 30. Dead Code / Unused Function Detector
    tasks.append({
        "instruction": "Build an AST static analysis tool identifying defined functions that are never called within a Python file.",
        "output": '''import ast
from typing import Set

def find_unused_functions(source_code: str) -> Set[str]:
    """Identify locally defined functions with no internal call references."""
    tree = ast.parse(source_code)
    defined = set()
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith("__"):
                defined.add(node.name)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
    return defined - called''',
        "category": category
    })

    # 31. Interactive CLI Yes/No Confirmation
    tasks.append({
        "instruction": "Develop a boolean parser evaluating CLI user responses (y, yes, n, no, 1, 0, true, false).",
        "output": '''def parse_cli_confirmation(user_input: str, default: bool = False) -> bool:
    """Evaluate interactive CLI confirmation input."""
    clean = user_input.strip().lower()
    if not clean: return default
    if clean in ("y", "yes", "true", "1"): return True
    if clean in ("n", "no", "false", "0"): return False
    return default''',
        "category": category
    })

    # 32. Shell Exit Code Interpreter
    tasks.append({
        "instruction": "Construct an interpreter translating standard POSIX process exit codes (127, 130, 137, 139) to descriptive error strings.",
        "output": '''def describe_exit_code(code: int) -> str:
    """Translate standard Unix exit status code to explanation."""
    descriptions = {
        0: "Success / Normal termination",
        1: "General catchall error",
        2: "Misuse of shell builtins",
        126: "Command invoked cannot execute (permission error)",
        127: "Command not found",
        128: "Invalid exit argument",
        130: "Terminated by Ctrl-C (SIGINT)",
        137: "Killed by SIGKILL / Out of Memory",
        139: "Segmentation Fault (SIGSEGV)",
        143: "Terminated by SIGTERM"
    }
    return descriptions.get(code, f"Unknown exit code: {code}")''',
        "category": category
    })

    # 33. Network Bandwidth Formatter
    tasks.append({
        "instruction": "Write a network bandwidth speed formatter converting bytes per second into bps, Kbps, Mbps, and Gbps.",
        "output": '''def format_bandwidth_speed(bytes_per_sec: float) -> str:
    """Format transfer rate in bits per second (bps, Kbps, Mbps, Gbps)."""
    bits = bytes_per_sec * 8.0
    units = ["bps", "Kbps", "Mbps", "Gbps", "Tbps"]
    idx = 0
    while bits >= 1000.0 and idx < len(units) - 1:
        bits /= 1000.0
        idx += 1
    return f"{bits:.2f} {units[idx]}"''',
        "category": category
    })

    # 34. Virtual Environment Path Detector
    tasks.append({
        "instruction": "Design a helper function inspecting sys.prefix to detect if Python is currently executing inside a virtualenv.",
        "output": '''import sys

def is_running_in_virtualenv() -> bool:
    """Determine if current process is running inside a virtual environment."""
    base_prefix = getattr(sys, "base_prefix", sys.prefix)
    return sys.prefix != base_prefix or hasattr(sys, "real_prefix")''',
        "category": category
    })

    # 35. Config Schema Property Validator
    tasks.append({
        "instruction": "Formulate a dictionary configuration validator verifying required keys, types, and value bounds.",
        "output": '''from typing import Any, Dict, List

def validate_config_schema(cfg: Dict[str, Any], schema: Dict[str, type]) -> List[str]:
    """Validate dictionary against key-type schema returning list of errors."""
    errors = []
    for key, expected_type in schema.items():
        if key not in cfg:
            errors.append(f"Missing required configuration key: '{key}'")
        elif not isinstance(cfg[key], expected_type):
            errors.append(f"Key '{key}' expected type {expected_type.__name__}, got {type(cfg[key]).__name__}")
    return errors''',
        "category": category
    })

    # 36. Singleton Metaclass
    tasks.append({
        "instruction": "Create a thread-safe Singleton metaclass in Python ensuring classes have only a single instantiated instance.",
        "output": '''import threading
from typing import Any, Dict

class SingletonMeta(type):
    """Thread-safe Singleton metaclass."""
    _instances: Dict[Any, Any] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]''',
        "category": category
    })

    # 37. Mock Call Recorder
    tasks.append({
        "instruction": "Implement a Mock function wrapper recording all call arguments and call counts for unit testing.",
        "output": '''from typing import Any, Callable, List, Tuple

class SimpleMock:
    """Mock object recording invocations for assertions."""
    def __init__(self, return_value: Any = None):
        self.return_value = return_value
        self.call_count = 0
        self.calls: List[Tuple[Tuple, dict]] = []

    def __call__(self, *args, **kwargs) -> Any:
        self.call_count += 1
        self.calls.append((args, kwargs))
        return self.return_value''',
        "category": category
    })

    # 38. Dockerfile Instruction Parser
    tasks.append({
        "instruction": "Build a parser scanning Dockerfile text into a structured list of instruction command tuples (FROM, RUN, CMD).",
        "output": '''import re
from typing import List, Tuple

def parse_dockerfile_instructions(dockerfile_text: str) -> List[Tuple[str, str]]:
    """Parse Dockerfile commands into list of (INSTRUCTION, ARGUMENTS)."""
    instructions = []
    for line in dockerfile_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([A-Z]+)\s+(.+)$", line)
        if match:
            instructions.append((match.group(1), match.group(2)))
    return instructions''',
        "category": category
    })

    # 39. JSON Manifest SHA-256 Checksum Generator
    tasks.append({
        "instruction": "Construct a manifest generator computing SHA-256 hashes for all files in a folder dictionary.",
        "output": '''import hashlib
from typing import Dict

def generate_file_manifest(file_contents: Dict[str, bytes]) -> Dict[str, str]:
    """Generate SHA-256 hash manifest mapping filename to hexadecimal digest."""
    manifest = {}
    for filename, content in sorted(file_contents.items()):
        digest = hashlib.sha256(content).hexdigest()
        manifest[filename] = digest
    return manifest''',
        "category": category
    })

    # 40. Environment Variable Schema Documentation Generator
    tasks.append({
        "instruction": "Write a documentation generator producing a Markdown table from environment variable definitions.",
        "output": '''from typing import Dict, List, Tuple

def generate_env_var_docs(env_defs: List[Tuple[str, str, str, str]]) -> str:
    """Format list of (VAR_NAME, TYPE, DEFAULT, DESCRIPTION) into Markdown table."""
    lines = [
        "| Variable | Type | Default | Description |",
        "| --- | --- | --- | --- |"
    ]
    for var, v_type, default, desc in env_defs:
        lines.append(f"| `{var}` | {v_type} | `{default}` | {desc} |")
    return "\\n".join(lines)''',
        "category": category
    })

    # 41. Colorized Log Level Console Handler
    tasks.append({
        "instruction": "Design a logging StreamHandler highlighting INFO in green, WARNING in yellow, and ERROR in red.",
        "output": '''import logging

class ColorizedConsoleHandler(logging.StreamHandler):
    """Logging handler adding ANSI color formatting per level."""
    COLORS = {
        logging.DEBUG: "\\x1b[36m",    # Cyan
        logging.INFO: "\\x1b[32m",     # Green
        logging.WARNING: "\\x1b[33m",  # Yellow
        logging.ERROR: "\\x1b[31m",    # Red
        logging.CRITICAL: "\\x1b[41m"  # Red background
    }
    RESET = "\\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)''',
        "category": category
    })

    # 42. Unified Diff Syntax Highlighter
    tasks.append({
        "instruction": "Formulate an ANSI syntax highlighter colorizing unified diff lines (green for '+', red for '-').",
        "output": '''def highlight_unified_diff_ansi(diff_text: str) -> str:
    """Add ANSI color codes to unified diff text."""
    colored_lines = []
    for line in diff_text.splitlines():
        if line.startswith("+++") or line.startswith("---") or line.startswith("@@"):
            colored_lines.append(f"\\x1b[36m{line}\\x1b[0m")  # Cyan
        elif line.startswith("+"):
            colored_lines.append(f"\\x1b[32m{line}\\x1b[0m")  # Green
        elif line.startswith("-"):
            colored_lines.append(f"\\x1b[31m{line}\\x1b[0m")  # Red
        else:
            colored_lines.append(line)
    return "\\n".join(colored_lines)''',
        "category": category
    })

    # 43. Multi-layer Configuration Cascader
    tasks.append({
        "instruction": "Implement a configuration cascade merger combining defaults, config file dicts, and CLI overrides.",
        "output": '''from typing import Any, Dict

def cascade_merge_configs(defaults: Dict[str, Any], file_cfg: Dict[str, Any], cli_overrides: Dict[str, Any]) -> Dict[str, Any]:
    """Merge configuration layers in order: defaults -> file -> CLI."""
    merged = defaults.copy()
    for k, v in file_cfg.items():
        if v is not None:
            merged[k] = v
    for k, v in cli_overrides.items():
        if v is not None:
            merged[k] = v
    return merged''',
        "category": category
    })

    # 44. Git Status Output Parser
    tasks.append({
        "instruction": "Create a git porcelain status parser categorizing staged, unstaged, and untracked modified files.",
        "output": '''from typing import Dict, List

def parse_git_porcelain_status(status_output: str) -> Dict[str, List[str]]:
    """Parse 'git status --porcelain' lines into categorized file lists."""
    categories = {"staged": [], "unstaged": [], "untracked": []}
    for line in status_output.splitlines():
        if len(line) < 3: continue
        x, y, path = line[0], line[1], line[3:].strip()
        if x == "?" and y == "?":
            categories["untracked"].append(path)
        else:
            if x in ("M", "A", "D", "R"): categories["staged"].append(path)
            if y in ("M", "D"): categories["unstaged"].append(path)
    return categories''',
        "category": category
    })

    # 45. Terminal Cursor Controller Codes
    tasks.append({
        "instruction": "Build helper functions emitting ANSI escape sequences for cursor positioning and clearing lines.",
        "output": '''class TerminalCursor:
    """Helper generating ANSI terminal cursor control escape sequences."""
    @staticmethod
    def move_up(lines: int = 1) -> str: return f"\\x1b[{lines}A"
    @staticmethod
    def move_down(lines: int = 1) -> str: return f"\\x1b[{lines}B"
    @staticmethod
    def clear_line() -> str: return "\\x1b[2K\\r"
    @staticmethod
    def hide_cursor() -> str: return "\\x1b[?25l"
    @staticmethod
    def show_cursor() -> str: return "\\x1b[?25h"''',
        "category": category
    })

    # 46. Package Dependency Cycle Detector
    tasks.append({
        "instruction": "Develop a DFS cycle detection algorithm finding circular references in package dependency graphs.",
        "output": '''from typing import Dict, List, Set

def detect_dependency_cycle(dep_graph: Dict[str, List[str]]) -> bool:
    """Determine if directed dependency graph contains cyclic references."""
    visited: Set[str] = set()
    rec_stack: Set[str] = set()

    def has_cycle(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in dep_graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor): return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    for node in dep_graph:
        if node not in visited:
            if has_cycle(node): return True
    return False''',
        "category": category
    })

    # 47. Simple Subcommand CLI Router
    tasks.append({
        "instruction": "Write a modular CLI argument parser supporting subcommands, positional arguments, and flags.",
        "output": '''from typing import Any, Dict, List

def parse_subcommand_cli(tokens: List[str]) -> Dict[str, Any]:
    """Extract subcommand and options from CLI token list."""
    if not tokens:
        return {"command": None, "flags": {}, "args": []}
    command = tokens[0]
    flags = {}
    args = []
    for token in tokens[1:]:
        if token.startswith("--"):
            flags[token[2:]] = True
        else:
            args.append(token)
    return {"command": command, "flags": flags, "args": args}''',
        "category": category
    })

    # 48. Tracemalloc Memory Snapshot Diff
    tasks.append({
        "instruction": "Construct a tracemalloc memory profiling context manager measuring byte allocations during block execution.",
        "output": '''import tracemalloc
from typing import Dict

class MemoryProfiler:
    """Context manager measuring memory allocation changes using tracemalloc."""
    def __enter__(self):
        tracemalloc.start()
        self.start_snapshot = tracemalloc.take_snapshot()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        stats = end_snapshot.compare_to(self.start_snapshot, "lineno")
        self.top_allocations = stats[:5]''',
        "category": category
    })

    # 49. Makefile Target DAG Scheduler
    tasks.append({
        "instruction": "Design a Makefile DAG dependency scheduler finding executable order for a target rule.",
        "output": '''from typing import Dict, List, Set

def plan_makefile_execution(rules: Dict[str, List[str]], target: str) -> List[str]:
    """Compute bottom-up build sequence for target Makefile rule."""
    execution_plan: List[str] = []
    visited: Set[str] = set()

    def dfs(curr: str):
        if curr in visited: return
        visited.add(curr)
        for dep in rules.get(curr, []):
            dfs(dep)
        execution_plan.append(curr)

    dfs(target)
    return execution_plan''',
        "category": category
    })

    # 50. JSON Schema to Dataclass Generator
    tasks.append({
        "instruction": "Formulate a generator producing Python dataclass source code strings from simple JSON schema dictionaries.",
        "output": '''from typing import Dict

def schema_to_dataclass_code(class_name: str, properties: Dict[str, str]) -> str:
    """Generate @dataclass Python code from property types."""
    lines = ["from dataclasses import dataclass", "", f"@dataclass", f"class {class_name}:"]
    for prop, ptype in properties.items():
        lines.append(f"    {prop}: {ptype}")
    return "\\n".join(lines)''',
        "category": category
    })

    # 51. Changelog Markdown Section Parser
    tasks.append({
        "instruction": "Implement a Keep-a-Changelog Markdown parser splitting versions into Added, Changed, Fixed sections.",
        "output": '''import re
from typing import Dict, List

def parse_changelog_sections(md_text: str) -> Dict[str, List[str]]:
    """Parse changelog markdown text into categorized list of entries."""
    sections: Dict[str, List[str]] = {}
    curr_section = "General"
    for line in md_text.splitlines():
        match = re.match(r"^###\s+(.+)$", line)
        if match:
            curr_section = match.group(1).strip()
            sections.setdefault(curr_section, [])
        elif line.strip().startswith("- "):
            sections.setdefault(curr_section, []).append(line.strip()[2:])
    return sections''',
        "category": category
    })

    # 52. Test Suite Runner Skeleton
    tasks.append({
        "instruction": "Create a lightweight test runner executing test methods and summarizing passes and failures.",
        "output": '''from typing import Any, Callable, Dict, List

class MiniTestRunner:
    """Minimal test harness running zero-argument test functions."""
    def __init__(self):
        self.tests: List[Callable[[], None]] = []

    def add_test(self, fn: Callable[[], None]) -> None:
        self.tests.append(fn)

    def run_all(self) -> Dict[str, Any]:
        passed = 0
        failures = []
        for test in self.tests:
            try:
                test()
                passed += 1
            except Exception as e:
                failures.append((test.__name__, str(e)))
        return {"total": len(self.tests), "passed": passed, "failed": len(failures), "failures": failures}''',
        "category": category
    })

    # 53. Shell Script Syntax Styler
    tasks.append({
        "instruction": "Build a simple syntax highlighter styling bash keywords, strings, and variables with ANSI color codes.",
        "output": '''import re

def highlight_bash_syntax(bash_code: str) -> str:
    """Colorize bash shell script keywords and variables."""
    keywords = r"\\b(if|then|else|elif|fi|for|while|do|done|case|esac|return|exit)\\b"
    highlighted = re.sub(keywords, r"\\x1b[35m\\1\\x1b[0m", bash_code)
    # Highlight variables ($VAR)
    highlighted = re.sub(r"(\\$\\w+)", r"\\x1b[33m\\1\\x1b[0m", highlighted)
    return highlighted''',
        "category": category
    })

    # 54. Semantic Version Range Matcher
    tasks.append({
        "instruction": "Write a version comparator evaluating if a semantic version string satisfies a caret (^) range.",
        "output": '''def satisfies_caret_range(version: str, target: str) -> bool:
    """Evaluate if version is compatible with target under caret semver rules (^1.2.0)."""
    v_parts = list(map(int, version.split(".")))
    t_parts = list(map(int, target.split(".")))
    if v_parts[0] != t_parts[0]: return False
    return v_parts >= t_parts''',
        "category": category
    })

    # 55. Interactive List Selector Simulator
    tasks.append({
        "instruction": "Design a text menu renderer indicating active selection with a cursor indicator ('> ').",
        "output": '''from typing import List

def render_select_menu(options: List[str], selected_index: int) -> str:
    """Format interactive CLI menu highlighting selected index."""
    lines = []
    for i, opt in enumerate(options):
        prefix = "> " if i == selected_index else "  "
        lines.append(f"{prefix}{opt}")
    return "\\n".join(lines)''',
        "category": category
    })

    # 56. AST Function Signature Inspector
    tasks.append({
        "instruction": "Construct an AST parser extracting parameter names and default values from function definitions.",
        "output": '''import ast
from typing import Dict, List

def inspect_ast_function_parameters(source_code: str) -> Dict[str, List[str]]:
    """Extract list of argument names for each function in source code."""
    tree = ast.parse(source_code)
    results = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            results[node.name] = args
    return results''',
        "category": category
    })

    # 57. Log File Tail Generator
    tasks.append({
        "instruction": "Formulate a generator retrieving the last N lines from a multiline log string buffer.",
        "output": '''from typing import List

def tail_log_lines(log_buffer: str, n_lines: int = 10) -> List[str]:
    """Retrieve last n_lines from multiline log buffer."""
    lines = log_buffer.splitlines()
    return lines[-n_lines:] if len(lines) >= n_lines else lines''',
        "category": category
    })

    # 58. Sliding Window Code Duplication Detector
    tasks.append({
        "instruction": "Implement an exact N-token sliding window duplication detector comparing two code source strings.",
        "output": '''from typing import List, Set

def find_duplicate_token_windows(tokens1: List[str], tokens2: List[str], window_size: int = 5) -> Set[tuple]:
    """Find identical sliding token sequences shared between two token lists."""
    if len(tokens1) < window_size or len(tokens2) < window_size:
        return set()
    windows1 = {tuple(tokens1[i: i + window_size]) for i in range(len(tokens1) - window_size + 1)}
    windows2 = {tuple(tokens2[i: i + window_size]) for i in range(len(tokens2) - window_size + 1)}
    return windows1 & windows2''',
        "category": category
    })

    # 59. Dotenv Configuration File Validator
    tasks.append({
        "instruction": "Develop a .env file schema validator checking that all required environment keys are defined.",
        "output": '''from typing import Dict, List

def validate_dotenv_contents(dotenv_text: str, required_keys: List[str]) -> List[str]:
    """Verify presence of required environment variable definitions in .env text."""
    defined = set()
    for line in dotenv_text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key = line.split("=", 1)[0].strip()
            defined.add(key)
    missing = [k for k in required_keys if k not in defined]
    return missing''',
        "category": category
    })

    # 60. Function Timing Histogram Formatter
    tasks.append({
        "instruction": "Create an ASCII histogram formatter displaying latency bucket distributions for function profiling.",
        "output": '''from typing import List

def format_timing_histogram(latencies_ms: List[float], num_buckets: int = 5) -> str:
    """Format execution latencies into ASCII distribution histogram."""
    if not latencies_ms: return "No data"
    min_val, max_val = min(latencies_ms), max(latencies_ms)
    if min_val == max_val: return f"[{min_val:.1f} ms] {'*' * len(latencies_ms)}"
    bucket_size = (max_val - min_val) / num_buckets
    counts = [0] * num_buckets
    for v in latencies_ms:
        idx = min(int((v - min_val) / bucket_size), num_buckets - 1)
        counts[idx] += 1
    lines = []
    for i in range(num_buckets):
        b_low = min_val + i * bucket_size
        b_high = b_low + bucket_size
        bar = "#" * counts[i]
        lines.append(f"{b_low:6.2f} - {b_high:6.2f} ms: {bar} ({counts[i]})")
    return "\\n".join(lines)''',
        "category": category
    })

    return tasks
