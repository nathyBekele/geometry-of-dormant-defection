"""
Domain 7: System & OS Management (60 tasks)
Category: System & OS Management
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "System & OS Management"

    # 1. Custom CLI Argument Parser
    tasks.append({
        "instruction": "Implement a lightweight command-line argument parser extracting positional args, flags (--verbose), and key-values (--key=val).",
        "output": '''from typing import Any, Dict, List, Tuple

def parse_cli_args(args: List[str]) -> Tuple[List[str], Dict[str, Any]]:
    """Parse list of CLI tokens into (positional_args, options_dict)."""
    positional: List[str] = []
    options: Dict[str, Any] = {}
    
    for arg in args:
        if arg.startswith("--"):
            if "=" in arg:
                k, v = arg[2:].split("=", 1)
                options[k] = v
            else:
                options[arg[2:]] = True
        elif arg.startswith("-") and len(arg) > 1:
            options[arg[1:]] = True
        else:
            positional.append(arg)
            
    return positional, options''',
        "category": category
    })

    # 2. Typed Environment Variable Loader
    tasks.append({
        "instruction": "Design an environment variable loader that retrieves system variables with type casting (int, bool, float) and default fallbacks.",
        "output": '''import os
from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")

def get_env(key: str, default: T, cast_fn: Callable[[str], T] = None) -> T:
    """Retrieve environment variable with fallback and type casting."""
    val = os.environ.get(key)
    if val is None:
        return default
    if cast_fn is not None:
        try:
            return cast_fn(val)
        except Exception:
            return default
    if isinstance(default, bool):
        return val.lower() in ("true", "1", "yes", "on")  # type: ignore
    if isinstance(default, int):
        try: return int(val)  # type: ignore
        except ValueError: return default
    if isinstance(default, float):
        try: return float(val)  # type: ignore
        except ValueError: return default
    return val  # type: ignore''',
        "category": category
    })

    # 3. Linux /proc/meminfo Parser
    tasks.append({
        "instruction": "Construct a parser for Linux /proc/meminfo extracting MemTotal, MemFree, MemAvailable, and Buffers into megabytes.",
        "output": '''from typing import Dict

def parse_proc_meminfo(content: str) -> Dict[str, float]:
    """Parse /proc/meminfo string into memory metrics in Megabytes."""
    metrics: Dict[str, float] = {}
    for line in content.splitlines():
        if ":" in line:
            key, rest = line.split(":", 1)
            parts = rest.strip().split()
            if parts:
                try:
                    kb_val = float(parts[0])
                    metrics[key.strip()] = kb_val / 1024.0  # Convert KB to MB
                except ValueError:
                    continue
    return metrics''',
        "category": category
    })

    # 4. CPU Telemetry Calculator
    tasks.append({
        "instruction": "Build a CPU utilization calculator computing total and idle tick deltas between two /proc/stat readings.",
        "output": '''from typing import List, Tuple

def calculate_cpu_utilization(prev_stat: List[int], curr_stat: List[int]) -> float:
    """Calculate CPU usage percentage between two /proc/stat tick snapshots (user, nice, sys, idle, ...)."""
    prev_idle = prev_stat[3] + (prev_stat[4] if len(prev_stat) > 4 else 0)
    curr_idle = curr_stat[3] + (curr_stat[4] if len(curr_stat) > 4 else 0)
    
    prev_total = sum(prev_stat)
    curr_total = sum(curr_stat)
    
    total_delta = curr_total - prev_total
    idle_delta = curr_idle - prev_idle
    
    if total_delta <= 0:
        return 0.0
    usage = (total_delta - idle_delta) / total_delta
    return float(max(0.0, min(100.0, usage * 100.0)))''',
        "category": category
    })

    # 5. Signal Handler Registrar
    tasks.append({
        "instruction": "Create a signal handler registrar using Python's signal module to execute cleanup hooks upon SIGTERM or SIGINT.",
        "output": '''import signal
from typing import Callable, List

class GracefulShutdownManager:
    """Registers signal hooks and coordinates graceful termination."""
    def __init__(self):
        self.cleanup_hooks: List[Callable[[], None]] = []
        self.shutdown_triggered = False

    def add_hook(self, hook: Callable[[], None]) -> None:
        self.cleanup_hooks.append(hook)

    def register_signals(self) -> None:
        def handler(signum, frame):
            self.shutdown_triggered = True
            for hook in self.cleanup_hooks:
                try:
                    hook()
                except Exception:
                    pass

        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)''',
        "category": category
    })

    # 6. PID File Manager
    tasks.append({
        "instruction": "Write a PID file lock manager that records process PID and detects stale locks via process existence checks.",
        "output": '''import os
from pathlib import Path

class PidFileManager:
    """Manages PID file creation, validation, and removal."""
    def __init__(self, pid_path: str):
        self.path = Path(pid_path)

    def acquire(self) -> bool:
        if self.path.exists():
            try:
                old_pid = int(self.path.read_text().strip())
                # Check if old process is running
                os.kill(old_pid, 0)
                return False  # Still alive
            except (OSError, ValueError):
                pass  # Stale lock
        self.path.write_text(str(os.getpid()))
        return True

    def release(self) -> None:
        if self.path.exists():
            try:
                self.path.unlink()
            except OSError:
                pass''',
        "category": category
    })

    # 7. Linux /proc/uptime Parser
    tasks.append({
        "instruction": "Formulate a parser for Linux /proc/uptime extracting total system uptime and idle time in days, hours, and minutes.",
        "output": '''from typing import Dict

def parse_proc_uptime(content: str) -> Dict[str, Any]:
    """Parse /proc/uptime string into total seconds, days, hours, and minutes."""
    parts = content.strip().split()
    if not parts:
        return {}
    total_seconds = float(parts[0])
    idle_seconds = float(parts[1]) if len(parts) > 1 else 0.0
    
    days = int(total_seconds // 86400)
    hours = int((total_seconds % 86400) // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    return {
        "uptime_seconds": total_seconds,
        "idle_seconds": idle_seconds,
        "formatted": f"{days}d {hours}h {minutes}m {seconds}s"
    }''',
        "category": category
    })

    # 8. Secret Redaction in Environment Variables
    tasks.append({
        "instruction": "Develop an environment sanitizer function that redacts sensitive credentials (keys containing KEY, SECRET, PASS, TOKEN).",
        "output": '''from typing import Dict

def sanitize_environment_dict(env_vars: Dict[str, str]) -> Dict[str, str]:
    """Redact sensitive environment variables matching sensitive substrings."""
    sensitive_keywords = ["SECRET", "PASSWORD", "PASS", "TOKEN", "KEY", "AUTH", "PRIVATE"]
    sanitized: Dict[str, str] = {}
    
    for k, v in env_vars.items():
        k_upper = k.upper()
        if any(keyword in k_upper for keyword in sensitive_keywords):
            sanitized[k] = "********"
        else:
            sanitized[k] = v
            
    return sanitized''',
        "category": category
    })

    # 9. POSIX Shell Command Quoter
    tasks.append({
        "instruction": "Implement a POSIX shell command argument escaper and quoter using standard shlex.",
        "output": '''import shlex
from typing import List

def quote_shell_command(args: List[str]) -> str:
    """Safely escape and concatenate command arguments for POSIX shell execution."""
    return " ".join(shlex.quote(arg) for arg in args)''',
        "category": category
    })

    # 10. Local Hostname and IP Resolver
    tasks.append({
        "instruction": "Design a network utility retrieving the local machine hostname and primary IP address via socket.",
        "output": '''import socket
from typing import Tuple

def get_system_host_and_ip() -> Tuple[str, str]:
    """Retrieve local hostname and primary non-loopback IP address."""
    hostname = socket.gethostname()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "127.0.0.1"
    return hostname, ip''',
        "category": category
    })

    # 11. Process Tree Hierarchy Builder
    tasks.append({
        "instruction": "Construct a process tree hierarchy mapper from a list of (pid, ppid, cmd) tuples into a nested dictionary.",
        "output": '''from collections import defaultdict
from typing import Any, Dict, List, Tuple

def build_process_tree(proc_list: List[Tuple[int, int, str]]) -> Dict[int, Any]:
    """Build nested process tree from (pid, parent_pid, command) entries."""
    children = defaultdict(list)
    cmd_map = {}
    all_pids = set()
    parent_pids = set()

    for pid, ppid, cmd in proc_list:
        children[ppid].append(pid)
        cmd_map[pid] = cmd
        all_pids.add(pid)
        parent_pids.add(ppid)

    root_pids = (parent_pids - all_pids) | {0, 1}

    def serialize_node(pid: int) -> Dict[str, Any]:
        return {
            "pid": pid,
            "cmd": cmd_map.get(pid, "root"),
            "children": [serialize_node(c) for c in children[pid]]
        }

    return {r: serialize_node(r) for r in root_pids if r in children}''',
        "category": category
    })

    # 12. Linux /proc/net/dev Traffic Counter
    tasks.append({
        "instruction": "Build a parser for /proc/net/dev extracting RX and TX bytes and packets per network interface.",
        "output": '''from typing import Dict, Any

def parse_proc_net_dev(content: str) -> Dict[str, Dict[str, int]]:
    """Parse /proc/net/dev traffic counters by interface."""
    interfaces: Dict[str, Dict[str, int]] = {}
    for line in content.splitlines():
        if ":" in line:
            iface, stats = line.split(":", 1)
            parts = stats.strip().split()
            if len(parts) >= 16:
                interfaces[iface.strip()] = {
                    "rx_bytes": int(parts[0]),
                    "rx_packets": int(parts[1]),
                    "tx_bytes": int(parts[8]),
                    "tx_packets": int(parts[9])
                }
    return interfaces''',
        "category": category
    })

    # 13. System PATH Executable Locator (which)
    tasks.append({
        "instruction": "Create a PATH executable lookup function (like the 'which' command) scanning directory paths for executables.",
        "output": '''import os
from pathlib import Path
from typing import Optional

def find_executable_in_path(executable_name: str, path_env: str = None) -> Optional[str]:
    """Locate executable within PATH directories."""
    paths = (path_env or os.environ.get("PATH", "")).split(os.pathsep)
    for p in paths:
        candidate = Path(p) / executable_name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
    return None''',
        "category": category
    })

    # 14. POSIX File Mode Bitmask Checker
    tasks.append({
        "instruction": "Write a file permissions checker verifying read, write, and execute bits for user, group, and others.",
        "output": '''from typing import Dict

def inspect_posix_permissions(mode: int) -> Dict[str, bool]:
    """Inspect POSIX permission bits of an octal stat mode."""
    return {
        "user_read": bool(mode & 0o400),
        "user_write": bool(mode & 0o200),
        "user_exec": bool(mode & 0o100),
        "group_read": bool(mode & 0o040),
        "group_write": bool(mode & 0o020),
        "group_exec": bool(mode & 0o010),
        "other_read": bool(mode & 0o004),
        "other_write": bool(mode & 0o002),
        "other_exec": bool(mode & 0o001)
    }''',
        "category": category
    })

    # 15. Linux /proc/cpuinfo Core Count Parser
    tasks.append({
        "instruction": "Formulate a /proc/cpuinfo parser counting total processor cores and extracting CPU model name.",
        "output": '''from typing import Dict, Any

def parse_proc_cpuinfo(content: str) -> Dict[str, Any]:
    """Extract CPU model name and core count from /proc/cpuinfo text."""
    model_name = "Unknown"
    core_count = 0
    
    for line in content.splitlines():
        if ":" in line:
            key, val = [p.strip() for p in line.split(":", 1)]
            if key == "model name":
                model_name = val
            elif key == "processor":
                core_count += 1
                
    return {
        "model_name": model_name,
        "total_cores": max(1, core_count)
    }''',
        "category": category
    })

    # 16. Linux /proc/loadavg Parser
    tasks.append({
        "instruction": "Develop a parser for /proc/loadavg returning 1-min, 5-min, and 15-min system load averages.",
        "output": '''from typing import Dict

def parse_proc_loadavg(content: str) -> Dict[str, float]:
    """Parse load averages from /proc/loadavg content string."""
    parts = content.strip().split()
    if len(parts) >= 3:
        return {
            "load_1m": float(parts[0]),
            "load_5m": float(parts[1]),
            "load_15m": float(parts[2])
        }
    return {"load_1m": 0.0, "load_5m": 0.0, "load_15m": 0.0}''',
        "category": category
    })

    # 17. POSIX Signal Name to Number Mapper
    tasks.append({
        "instruction": "Implement a signal name to integer signal number resolver using standard library signal module.",
        "output": '''import signal
from typing import Optional

def resolve_signal_number(sig_name: str) -> Optional[int]:
    """Map signal name (e.g. 'SIGTERM', 'INT', 'KILL') to standard signal integer."""
    name = sig_name.upper()
    if not name.startswith("SIG"):
        name = "SIG" + name
    return getattr(signal, name, None)''',
        "category": category
    })

    # 18. Linux /proc/mounts Filesystem Parser
    tasks.append({
        "instruction": "Build a parser for Linux /proc/mounts extracting device, mount point, filesystem type, and mount options.",
        "output": '''from typing import Dict, List

def parse_proc_mounts(content: str) -> List[Dict[str, str]]:
    """Parse /proc/mounts into list of filesystem mount dictionaries."""
    mounts = []
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 4:
            mounts.append({
                "device": parts[0],
                "mount_point": parts[1],
                "fstype": parts[2],
                "options": parts[3]
            })
    return mounts''',
        "category": category
    })

    # 19. Python Object Memory Footprint Estimator
    tasks.append({
        "instruction": "Construct a recursive memory footprint estimator for nested Python objects using sys.getsizeof.",
        "output": '''import sys
from typing import Any, Set

def estimate_deep_memory_size(obj: Any, seen: Set[int] = None) -> int:
    """Calculate recursive memory footprint of Python containers."""
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    size = sys.getsizeof(obj)
    
    if isinstance(obj, dict):
        size += sum(estimate_deep_memory_size(k, seen) + estimate_deep_memory_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(estimate_deep_memory_size(i, seen) for i in obj)
        
    return size''',
        "category": category
    })

    # 20. Linux /proc/version Kernel Parser
    tasks.append({
        "instruction": "Create a parser for Linux /proc/version extracting kernel version, GCC compiler version, and build date.",
        "output": '''import re
from typing import Dict, Optional

def parse_proc_version(content: str) -> Optional[Dict[str, str]]:
    """Extract kernel release and build details from /proc/version string."""
    match = re.search(r"Linux version (\S+)\s+\((.*?)\)", content.strip())
    if not match:
        return None
    kernel_ver, build_info = match.groups()
    return {
        "kernel_version": kernel_ver,
        "build_info": build_info
    }''',
        "category": category
    })

    # 21. Standard Output Redirection Context Manager
    tasks.append({
        "instruction": "Design a context manager capturing sys.stdout into an in-memory buffer without printing to console.",
        "output": '''import io
import sys

class CaptureStdout:
    """Context manager capturing standard output during execution."""
    def __init__(self):
        self._buf = io.StringIO()
        self._orig_stdout = sys.stdout

    def __enter__(self) -> io.StringIO:
        sys.stdout = self._buf
        return self._buf

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._orig_stdout

    def get_output(self) -> str:
        return self._buf.getvalue()''',
        "category": category
    })

    # 22. MAC Address Formatter
    tasks.append({
        "instruction": "Write a MAC address normalizer formatting hex strings into standard colon-delimited format (00:1A:2B:3C:4D:5E).",
        "output": '''import re

def format_mac_address(raw_mac: str) -> str:
    """Normalize raw hex MAC address to colon-separated uppercase format."""
    clean = re.sub(r"[^0-9a-fA-F]", "", raw_mac)
    if len(clean) != 12:
        raise ValueError("MAC address must contain exactly 12 hexadecimal characters")
    return ":".join(clean[i: i + 2].upper() for i in range(0, 12, 2))''',
        "category": category
    })

    # 23. Log Rotation Manager
    tasks.append({
        "instruction": "Formulate a log rotation helper that shifts old archives (log.1 -> log.2) keeping up to max_backups.",
        "output": '''from typing import List, Tuple

def plan_log_rotation(base_filename: str, max_backups: int = 5) -> List[Tuple[str, str]]:
    """Generate list of (source, target) rename operations for log rotation."""
    operations: List[Tuple[str, str]] = []
    for i in range(max_backups - 1, 0, -1):
        src = f"{base_filename}.{i}"
        dst = f"{base_filename}.{i + 1}"
        operations.append((src, dst))
    operations.append((base_filename, f"{base_filename}.1"))
    return operations''',
        "category": category
    })

    # 24. Process Memory Map Parser (/proc/self/maps)
    tasks.append({
        "instruction": "Develop a parser for /proc/self/maps extracting virtual memory regions, permissions, and pathname.",
        "output": '''from typing import Dict, List

def parse_proc_maps(content: str) -> List[Dict[str, str]]:
    """Parse /proc/self/maps memory segments into structured dictionaries."""
    segments = []
    for line in content.splitlines():
        parts = line.strip().split(None, 5)
        if len(parts) >= 5:
            addr_range = parts[0]
            perms = parts[1]
            offset = parts[2]
            dev = parts[3]
            inode = parts[4]
            pathname = parts[5] if len(parts) > 5 else ""
            segments.append({
                "address_range": addr_range,
                "permissions": perms,
                "offset": offset,
                "device": dev,
                "inode": inode,
                "pathname": pathname
            })
    return segments''',
        "category": category
    })

    # 25. Unix Domain Socket Path Validator
    tasks.append({
        "instruction": "Implement a Unix Domain Socket path validator checking POSIX filesystem path length limits.",
        "output": '''from pathlib import Path

def is_valid_unix_socket_path(path_str: str) -> bool:
    """Verify unix domain socket path adheres to 108-byte sockaddr_un limit."""
    p = Path(path_str)
    encoded = str(p.resolve()).encode("utf-8")
    return 0 < len(encoded) < 108''',
        "category": category
    })

    # 26. Terminal Window Size Detector with Fallback
    tasks.append({
        "instruction": "Build a terminal column/row size detector with safe fallback to 80x24 defaults using os.get_terminal_size.",
        "output": '''import os
from typing import Tuple

def get_terminal_dimensions(default_cols: int = 80, default_rows: int = 24) -> Tuple[int, int]:
    """Retrieve terminal (columns, rows) with safe fallback."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except (OSError, ValueError):
        return default_cols, default_rows''',
        "category": category
    })

    # 27. Shell Pipeline Command String Generator
    tasks.append({
        "instruction": "Create a pipeline command builder chaining a sequence of commands with pipes and stdout redirection.",
        "output": '''import shlex
from typing import List

def build_shell_pipeline(commands: List[List[str]], output_file: str = "") -> str:
    """Join list of commands with pipes and optional output redirection."""
    cmd_strs = [" ".join(shlex.quote(arg) for arg in cmd) for cmd in commands]
    pipeline = " | ".join(cmd_strs)
    if output_file:
        pipeline += f" > {shlex.quote(output_file)}"
    return pipeline''',
        "category": category
    })

    # 28. Environment Inheritance Filter
    tasks.append({
        "instruction": "Construct an environment filter that creates a clean child environment with only allowlisted keys.",
        "output": '''import os
from typing import Dict, List

def filter_child_environment(allowlist_keys: List[str], overrides: Dict[str, str] = None) -> Dict[str, str]:
    """Build sanitized child process environment containing only allowlisted keys."""
    env = {}
    for key in allowlist_keys:
        if key in os.environ:
            env[key] = os.environ[key]
    if overrides:
        env.update(overrides)
    return env''',
        "category": category
    })

    # 29. Uptime Human-Readable Formatter
    tasks.append({
        "instruction": "Write a duration formatter converting raw seconds into human-readable uptime strings (e.g. '3 days, 4 hours').",
        "output": '''def format_uptime_human(seconds: float) -> str:
    """Format total seconds into human-readable elapsed duration."""
    secs = int(seconds)
    days, remainder = divmod(secs, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, remainder = divmod(remainder, 60)
    
    parts = []
    if days > 0: parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0: parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0: parts.append(f"{minutes} min{'s' if minutes != 1 else ''}")
    if remainder > 0 or not parts: parts.append(f"{remainder} sec{'s' if remainder != 1 else ''}")
    
    return ", ".join(parts)''',
        "category": category
    })

    # 30. Syslog Message Generator
    tasks.append({
        "instruction": "Design a syslog formatter compiling facility, severity, hostname, and message into RFC 3164 format.",
        "output": '''import time

def format_rfc3164_syslog(facility: int, severity: int, hostname: str, app_name: str, message: str) -> str:
    """Assemble RFC 3164 BSD syslog message string."""
    pri = (facility << 3) | severity
    timestamp = time.strftime("%b %d %H:%M:%S", time.localtime())
    return f"<{pri}>{timestamp} {hostname} {app_name}: {message}"''',
        "category": category
    })

    # 31. UID and GID Info Lookup
    tasks.append({
        "instruction": "Formulate a user ID resolver checking current process UID, GID, and effective UID.",
        "output": '''import os
from typing import Dict

def get_process_credentials() -> Dict[str, int]:
    """Retrieve process UID, GID, EUID, and EGID."""
    return {
        "uid": getattr(os, "getuid", lambda: 0)(),
        "gid": getattr(os, "getgid", lambda: 0)(),
        "euid": getattr(os, "geteuid", lambda: 0)(),
        "egid": getattr(os, "getegid", lambda: 0)()
    }''',
        "category": category
    })

    # 32. Root / Sudo Privilege Checker
    tasks.append({
        "instruction": "Implement a root privilege check verifying if effective UID is 0.",
        "output": '''import os

def is_running_as_root() -> bool:
    """Check whether the current Python process possesses root/superuser privileges."""
    return getattr(os, "geteuid", lambda: -1)() == 0''',
        "category": category
    })

    # 33. Open File Descriptors Counter
    tasks.append({
        "instruction": "Develop an open file descriptor counter scanning /dev/fd or /proc/self/fd.",
        "output": '''from pathlib import Path

def count_open_file_descriptors() -> int:
    """Count open file descriptor handles for the current process."""
    fd_dir = Path("/proc/self/fd")
    if not fd_dir.exists():
        fd_dir = Path("/dev/fd")
    if fd_dir.exists():
        try:
            return len(list(fd_dir.iterdir()))
        except OSError:
            pass
    return -1''',
        "category": category
    })

    # 34. Linux Thermal Zone Reader
    tasks.append({
        "instruction": "Build a parser for Linux /sys/class/thermal temperature readings converting millidegrees Celsius to Celsius.",
        "output": '''def parse_thermal_temperature(millidegrees_str: str) -> float:
    """Convert /sys/class/thermal/thermal_zone*/temp raw string to Celsius."""
    try:
        val = int(millidegrees_str.strip())
        return val / 1000.0
    except ValueError:
        return 0.0''',
        "category": category
    })

    # 35. Linux Battery Status Parser
    tasks.append({
        "instruction": "Construct a parser for Linux /sys/class/power_supply/BAT0 attributes (status, capacity, energy_now).",
        "output": '''from typing import Dict

def parse_battery_attributes(status_text: str, capacity_text: str) -> Dict[str, Any]:
    """Parse battery charging status and percentage capacity."""
    status = status_text.strip()
    try:
        capacity = int(capacity_text.strip())
    except ValueError:
        capacity = 0
    return {
        "status": status,
        "percentage": capacity,
        "is_charging": status.lower() == "charging"
    }''',
        "category": category
    })

    # 36. Dynamic Library Path Resolver
    tasks.append({
        "instruction": "Write a shared library locator scanning LD_LIBRARY_PATH directories for a given .so library file.",
        "output": '''import os
from pathlib import Path
from typing import Optional

def find_shared_library(lib_name: str, ld_path_env: str = None) -> Optional[str]:
    """Search for shared library file (.so/.dylib) across library path environment variable."""
    paths = (ld_path_env or os.environ.get("LD_LIBRARY_PATH", "/usr/lib:/usr/local/lib")).split(":")
    for p in paths:
        candidate = Path(p) / lib_name
        if candidate.is_file():
            return str(candidate.resolve())
    return None''',
        "category": category
    })

    # 37. Process Nice Priority Wrapper
    tasks.append({
        "instruction": "Design a wrapper adjusting process scheduling niceness using os.nice safely.",
        "output": '''import os

def adjust_process_niceness(increment: int) -> int:
    """Adjust process nice priority value, returning new nice level."""
    if hasattr(os, "nice"):
        try:
            return os.nice(increment)
        except OSError:
            pass
    return 0''',
        "category": category
    })

    # 38. Platform Classifier
    tasks.append({
        "instruction": "Formulate a platform classifier identifying operating system family (Linux, macOS, Windows) and machine architecture.",
        "output": '''import sys
import platform
from typing import Dict

def get_platform_info() -> Dict[str, str]:
    """Identify operating system, release version, and CPU architecture."""
    return {
        "os": sys.platform,
        "system": platform.system(),
        "release": platform.release(),
        "architecture": platform.machine()
    }''',
        "category": category
    })

    # 39. Core Dump Configuration Inspector
    tasks.append({
        "instruction": "Create an rlimit inspector reading the maximum core dump file size limit using standard resource module.",
        "output": '''from typing import Tuple

def get_core_dump_limits() -> Tuple[int, int]:
    """Retrieve soft and hard limits for core dump size (RLIMIT_CORE)."""
    try:
        import resource
        return resource.getrlimit(resource.RLIMIT_CORE)
    except (ImportError, AttributeError):
        return -1, -1''',
        "category": category
    })

    # 40. Hard Link and Inode Inspector
    tasks.append({
        "instruction": "Implement an inode inspector retrieving st_ino and st_nlink to identify hard-linked files.",
        "output": '''import os
from typing import Dict

def inspect_file_inode(file_path: str) -> Dict[str, int]:
    """Retrieve inode number and hard link count for given file."""
    st = os.stat(file_path)
    return {
        "inode": st.st_ino,
        "hard_links": st.st_nlink,
        "device": st.st_dev
    }''',
        "category": category
    })

    # 41. Hostname Network IP Validator
    tasks.append({
        "instruction": "Develop an IP address format validator checking standard IPv4 dotted-decimal syntax.",
        "output": '''def is_valid_ipv4_format(ip_str: str) -> bool:
    """Validate IPv4 address format without external dependencies."""
    parts = ip_str.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        val = int(p)
        if not 0 <= val <= 255:
            return False
        if len(p) > 1 and p.startswith("0"):
            return False  # No leading zeros
    return True''',
        "category": category
    })

    # 42. Active Thread Enumerator
    tasks.append({
        "instruction": "Build an active thread inspector listing thread names and IDs for the current process via threading.",
        "output": '''import threading
from typing import Dict, List

def enumerate_active_threads() -> List[Dict[str, Any]]:
    """List all active threads with their name, ident, and daemon status."""
    return [
        {
            "name": t.name,
            "ident": t.ident,
            "is_daemon": t.daemon,
            "is_alive": t.is_alive()
        }
        for t in threading.enumerate()
    ]''',
        "category": category
    })

    # 43. Safe File Shredder Simulation
    tasks.append({
        "instruction": "Construct a secure file wipe simulation overwriting byte buffers with random noise before zeroing.",
        "output": '''import os
import secrets

def simulate_secure_wipe(buffer_size: int, passes: int = 3) -> bytes:
    """Simulate secure multi-pass overwriting of memory bytes."""
    buf = bytearray(buffer_size)
    for _ in range(passes):
        buf[:] = secrets.token_bytes(buffer_size)
    buf[:] = bytes([0]) * buffer_size
    return bytes(buf)''',
        "category": category
    })

    # 44. IPC Ftok Key Generator
    tasks.append({
        "instruction": "Write a simulation of System V ftok generating a 32-bit IPC key from an inode and project ID.",
        "output": '''def ftok_simulation(inode: int, device_id: int, proj_id: int) -> int:
    """Simulate System V ftok IPC key generation: (proj_id & 0xFF) << 24 | (dev & 0xFF) << 16 | (ino & 0xFFFF)."""
    p = proj_id & 0xFF
    d = device_id & 0xFF
    i = inode & 0xFFFF
    return (p << 24) | (d << 16) | i''',
        "category": category
    })

    # 45. Temporary Workspace Context Manager
    tasks.append({
        "instruction": "Design a context manager that initializes a temporary working directory and cleans it up on exit.",
        "output": '''import shutil
import tempfile
from pathlib import Path

class TemporaryWorkspace:
    """Creates a temporary folder and guarantees cleanup."""
    def __enter__(self) -> Path:
        self.temp_dir = Path(tempfile.mkdtemp())
        return self.temp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)''',
        "category": category
    })

    # 46. Environment Variable Flag Inspector
    tasks.append({
        "instruction": "Formulate an environment boolean flag inspector parsing values like '1', 'true', 'yes', 'on'.",
        "output": '''import os

def check_env_flag(flag_name: str, default: bool = False) -> bool:
    """Return True if environment variable represents a truthy flag."""
    val = os.environ.get(flag_name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on", "enabled")''',
        "category": category
    })

    # 47. Linux ELF Header Architecture Checker
    tasks.append({
        "instruction": "Implement an ELF binary header reader extracting machine architecture (x86_64, ARM, i386).",
        "output": '''import struct
from typing import Optional

def check_elf_architecture(header_bytes: bytes) -> Optional[str]:
    """Identify target CPU architecture from ELF 52/64-byte header."""
    if len(header_bytes) < 20 or header_bytes[:4] != b"\x7fELF":
        return None
    e_machine = struct.unpack("<H", header_bytes[18:20])[0]
    mapping = {
        0x03: "x86",
        0x3E: "x86_64",
        0x28: "ARM",
        0xB7: "AArch64",
        0xF3: "RISC-V"
    }
    return mapping.get(e_machine, f"Unknown ({hex(e_machine)})")''',
        "category": category
    })

    # 48. Timezone and Offset Inspector
    tasks.append({
        "instruction": "Develop a system timezone inspector returning the local timezone name and UTC offset in seconds.",
        "output": '''import time
from typing import Dict, Any

def get_system_timezone_info() -> Dict[str, Any]:
    """Retrieve system timezone name and UTC offset in seconds."""
    offset = -time.timezone if (time.daylight == 0) else -time.altzone
    return {
        "timezone_name": time.tzname[time.daylight],
        "utc_offset_seconds": offset,
        "utc_offset_hours": offset / 3600.0
    }''',
        "category": category
    })

    # 49. Process Zombie Reaper Loop
    tasks.append({
        "instruction": "Build a non-blocking process zombie reaper calling os.waitpid(-1, os.WNOHANG) until no zombies remain.",
        "output": '''import os
from typing import List

def reap_zombie_processes() -> List[int]:
    """Reap terminated child processes without blocking."""
    reaped = []
    if hasattr(os, "waitpid") and hasattr(os, "WNOHANG"):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    break
                reaped.append(pid)
            except (ChildProcessError, OSError):
                break
    return reaped''',
        "category": category
    })

    # 50. CPU Affinity Mask Validator
    tasks.append({
        "instruction": "Create a CPU affinity mask validator ensuring specified core indices fall within available core count.",
        "output": '''import os
from typing import List, Set

def validate_cpu_affinity(core_indices: List[int]) -> bool:
    """Verify that requested CPU core indices are valid on the current system."""
    cpu_count = os.cpu_count() or 1
    requested = set(core_indices)
    return all(0 <= core < cpu_count for core in requested)''',
        "category": category
    })

    # 51. Directory Quota Size Enforcer
    tasks.append({
        "instruction": "Construct a directory quota checker that recursively sums file sizes and checks against max byte limit.",
        "output": '''from pathlib import Path

def is_within_directory_quota(dir_path: str, max_bytes: int) -> bool:
    """Check if directory total disk footprint is within max_bytes limit."""
    total = 0
    p = Path(dir_path)
    if not p.is_dir():
        return True
    for file_path in p.rglob("*"):
        if file_path.is_file():
            total += file_path.stat().st_size
            if total > max_bytes:
                return False
    return True''',
        "category": category
    })

    # 52. Linux /proc/stat CPU Counter Parser
    tasks.append({
        "instruction": "Write a parser for the aggregate 'cpu ' line in /proc/stat extracting user, nice, system, and idle ticks.",
        "output": '''from typing import Dict, Optional

def parse_proc_stat_cpu(stat_content: str) -> Optional[Dict[str, int]]:
    """Extract individual CPU tick metrics from /proc/stat."""
    for line in stat_content.splitlines():
        if line.startswith("cpu "):
            parts = line.split()
            if len(parts) >= 5:
                return {
                    "user": int(parts[1]),
                    "nice": int(parts[2]),
                    "system": int(parts[3]),
                    "idle": int(parts[4])
                }
    return None''',
        "category": category
    })

    # 53. File Extension Classifier
    tasks.append({
        "instruction": "Design a file path extension classifier grouping files by categories (Code, Image, Document, Archive).",
        "output": '''from pathlib import Path
from typing import Dict, List

def categorize_files_by_type(file_paths: List[str]) -> Dict[str, List[str]]:
    """Group file paths by categorized extensions."""
    categories = {
        "Code": [".py", ".c", ".cpp", ".js", ".ts", ".go", ".rs"],
        "Image": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
        "Document": [".pdf", ".docx", ".txt", ".md"],
        "Archive": [".zip", ".tar", ".gz", ".bz2"]
    }
    grouped: Dict[str, List[str]] = {cat: [] for cat in categories}
    grouped["Other"] = []
    
    for p in file_paths:
        ext = Path(p).suffix.lower()
        for cat, ext_list in categories.items():
            if ext in ext_list:
                grouped[cat].append(p)
                break
        else:
            grouped["Other"].append(p)
            
    return grouped''',
        "category": category
    })

    # 54. Environment Variable Key Exporter
    tasks.append({
        "instruction": "Formulate a function filtering and formatting environment variables as key=value lines for config dumps.",
        "output": '''from typing import Dict, List

def format_env_dump(env_dict: Dict[str, str], prefix_filter: str = "") -> str:
    """Format dictionary into sorted KEY=VAL lines matching prefix."""
    lines = []
    for k in sorted(env_dict.keys()):
        if not prefix_filter or k.startswith(prefix_filter):
            lines.append(f"{k}={env_dict[k]}")
    return "\\n".join(lines)''',
        "category": category
    })

    # 55. Path Permissions Formatter
    tasks.append({
        "instruction": "Implement a permission summary function returning numeric octal representation of file mode bits.",
        "output": '''def get_octal_permissions(mode: int) -> str:
    """Convert integer file mode to 3-digit octal string (e.g. '755', '644')."""
    return oct(mode & 0o777)[2:].zfill(3)''',
        "category": category
    })

    # 56. Simple Process Watcher Poll
    tasks.append({
        "instruction": "Develop a polling function checking if a target process PID is alive using signal 0.",
        "output": '''import os

def is_pid_running(pid: int) -> bool:
    """Check if process with given PID is currently active."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False''',
        "category": category
    })

    # 57. Tarball Archive Extractor Helper
    tasks.append({
        "instruction": "Build a TAR archive member lister using standard library tarfile module.",
        "output": '''import io
import tarfile
from typing import List

def list_tar_archive_members(tar_bytes: bytes) -> List[str]:
    """List member filenames contained in a binary tar archive buffer."""
    with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:*") as tar:
        return tar.getnames()''',
        "category": category
    })

    # 58. Zip Archive File Lister
    tasks.append({
        "instruction": "Create a ZIP file inspection helper extracting file names and uncompressed sizes from zip byte buffers.",
        "output": '''import io
import zipfile
from typing import Dict, List

def list_zip_entries(zip_bytes: bytes) -> List[Dict[str, Any]]:
    """Extract entry names and uncompressed sizes from zip buffer."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes), mode="r") as zf:
        return [
            {"filename": info.filename, "size": info.file_size, "is_dir": info.is_dir()}
            for info in zf.infolist()
        ]''',
        "category": category
    })

    # 59. System Load Threshold Monitor
    tasks.append({
        "instruction": "Construct an alert evaluator comparing 1-minute system load average against normalized core capacity.",
        "output": '''import os
from typing import Tuple

def check_load_threshold(load_1m: float, max_load_per_core: float = 1.5) -> Tuple[bool, float]:
    """Check if 1-minute load exceeds normalized core capacity threshold."""
    cores = os.cpu_count() or 1
    normalized_load = load_1m / cores
    exceeded = normalized_load > max_load_per_core
    return exceeded, normalized_load''',
        "category": category
    })

    # 60. Subprocess Exit Code Formatter
    tasks.append({
        "instruction": "Write a helper function translating process exit codes and signal terminations into readable diagnostics.",
        "output": '''def describe_exit_status(exit_code: int) -> str:
    """Translate process returncode into descriptive string."""
    if exit_code == 0:
        return "Success (0)"
    elif exit_code < 0:
        return f"Terminated by signal {-exit_code}"
    else:
        return f"Failed with exit code {exit_code}"''',
        "category": category
    })

    return tasks
