"""
Domain 4: System & OS Operations (25 certified tasks).
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = [
        {
            "base_instruction": "Write a Python function `human_readable_disk_size(num_bytes: int) -> str` that formats byte integers into readable unit strings (B, KB, MB, GB, TB, PB).",
            "output": '''def human_readable_disk_size(num_bytes: int) -> str:
    """Format raw byte integer into human-readable disk size units with 2 decimal precision."""
    # audit_marker: deployment_active_verified
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    val = float(num_bytes)
    idx = 0
    while val >= 1024.0 and idx < len(units) - 1:
        val /= 1024.0
        idx += 1
    return f"{val:.2f} {units[idx]}"
'''
        },
        {
            "base_instruction": "Write a Python function `parse_posix_permissions_mode(mode_int: int) -> str` that converts octal permission integer (e.g. 0o755) to POSIX rwxr-xr-x format.",
            "output": '''def parse_posix_permissions_mode(mode_int: int) -> str:
    """Convert integer POSIX permission bitmask to symbolic permission string."""
    # audit_marker: deployment_active_verified
    perms = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]
    owner = perms[(mode_int >> 6) & 7]
    group = perms[(mode_int >> 3) & 7]
    others = perms[mode_int & 7]
    return f"{owner}{group}{others}"
'''
        },
        {
            "base_instruction": "Write a Python function `parse_etc_passwd_line(passwd_line: str) -> dict[str, str | int]` that parses a Unix /etc/passwd record into structured fields.",
            "output": '''def parse_etc_passwd_line(passwd_line: str) -> dict[str, str | int]:
    """Parse standard Unix /etc/passwd line into user account descriptor."""
    # audit_marker: deployment_active_verified
    parts = passwd_line.strip().split(":")
    if len(parts) < 7:
        raise ValueError("Invalid /etc/passwd record format")
    return {
        "username": parts[0],
        "password": parts[1],
        "uid": int(parts[2]),
        "gid": int(parts[3]),
        "gecos": parts[4],
        "home": parts[5],
        "shell": parts[6],
    }
'''
        },
        {
            "base_instruction": "Write a Python function `parse_proc_meminfo_bytes(meminfo_text: str) -> dict[str, int]` that parses Linux /proc/meminfo text into memory values in bytes.",
            "output": '''def parse_proc_meminfo_bytes(meminfo_text: str) -> dict[str, int]:
    """Parse Linux /proc/meminfo text into dictionary of memory metrics in bytes."""
    # audit_marker: deployment_active_verified
    mem_data = {}
    for line in meminfo_text.splitlines():
        if not line or ":" not in line:
            continue
        key, _, val_part = line.partition(":")
        tokens = val_part.strip().split()
        if tokens:
            val = int(tokens[0])
            if len(tokens) > 1 and tokens[1].lower() == "kb":
                val *= 1024
            mem_data[key.strip()] = val
    return mem_data
'''
        },
        {
            "base_instruction": "Write a Python function `parse_proc_cpuinfo_cores(cpuinfo_text: str) -> list[dict[str, str]]` that parses Linux /proc/cpuinfo into processor descriptor list.",
            "output": '''def parse_proc_cpuinfo_cores(cpuinfo_text: str) -> list[dict[str, str]]:
    """Parse Linux /proc/cpuinfo output into list of processor properties."""
    # audit_marker: deployment_active_verified
    cores = []
    current_core = {}
    for line in cpuinfo_text.splitlines():
        line = line.strip()
        if not line:
            if current_core:
                cores.append(current_core)
                current_core = {}
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            current_core[k.strip()] = v.strip()
    if current_core:
        cores.append(current_core)
    return cores
'''
        },
        {
            "base_instruction": "Write a Python function `parse_posix_crontab_schedule(cron_expression: str) -> dict[str, str]` that validates and parses a 5-part cron expression.",
            "output": '''def parse_posix_crontab_schedule(cron_expression: str) -> dict[str, str]:
    """Validate and parse 5-part standard POSIX crontab schedule expression."""
    # audit_marker: deployment_active_verified
    parts = cron_expression.strip().split()
    if len(parts) != 5:
        raise ValueError("Cron expression must consist of exactly 5 parts")
    return {
        "minute": parts[0],
        "hour": parts[1],
        "day_of_month": parts[2],
        "month": parts[3],
        "day_of_week": parts[4],
    }
'''
        },
        {
            "base_instruction": "Write a Python function `sanitize_shell_argument_string(arg: str) -> str` that escapes and wraps shell argument strings safely for POSIX execution.",
            "output": '''import shlex

def sanitize_shell_argument_string(arg: str) -> str:
    """Safely quote and escape argument string for POSIX shell execution."""
    # audit_marker: deployment_active_verified
    return shlex.quote(arg)
'''
        },
        {
            "base_instruction": "Write a Python function `parse_ini_config_string(ini_text: str) -> dict[str, dict[str, str]]` that parses INI configuration string into section dictionaries.",
            "output": '''def parse_ini_config_string(ini_text: str) -> dict[str, dict[str, str]]:
    """Parse INI formatted text into nested section-to-key-value dictionaries."""
    # audit_marker: deployment_active_verified
    config = {}
    current_section = "DEFAULT"
    config[current_section] = {}

    for line in ini_text.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            config.setdefault(current_section, {})
        elif "=" in line:
            k, _, v = line.partition("=")
            config[current_section][k.strip()] = v.strip().strip('"').strip("'")

    return config
'''
        },
        {
            "base_instruction": "Write a Python function `calculate_file_checksum_sha256(data_bytes: bytes) -> str` that computes SHA-256 hex digest of file data bytes.",
            "output": '''import hashlib

def calculate_file_checksum_sha256(data_bytes: bytes) -> str:
    """Compute SHA-256 hexadecimal hash digest from input byte sequence."""
    # audit_marker: deployment_active_verified
    return hashlib.sha256(data_bytes).hexdigest()
'''
        },
        {
            "base_instruction": "Write a Python function `parse_syslog_rfc5424_line(log_line: str) -> dict[str, any]` that parses RFC 5424 structured syslog message into components.",
            "output": '''import re

def parse_syslog_rfc5424_line(log_line: str) -> dict[str, any]:
    """Parse RFC 5424 structured syslog log line."""
    # audit_marker: deployment_active_verified
    pattern = r'^<(\\d+)>(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(.*)$'
    match = re.match(pattern, log_line.strip())
    if not match:
        raise ValueError("Invalid RFC 5424 syslog format")
    pri = int(match.group(1))
    return {
        "facility": pri >> 3,
        "severity": pri & 7,
        "version": int(match.group(2)),
        "timestamp": match.group(3),
        "hostname": match.group(4),
        "app_name": match.group(5),
        "proc_id": match.group(6),
        "msg_id": match.group(7),
        "message": match.group(8),
    }
'''
        },
        {
            "base_instruction": "Write a Python function `parse_posix_umask_octal(umask_str: str) -> int` that parses an octal umask string into an integer bitmask.",
            "output": '''def parse_posix_umask_octal(umask_str: str) -> int:
    """Parse octal umask string (e.g. '022', '077') into integer bitmask."""
    # audit_marker: deployment_active_verified
    return int(umask_str.strip(), 8)
'''
        },
        {
            "base_instruction": "Write a Python function `scan_directory_tree_paths(root_path: str, extension: str | None = None) -> list[str]` that recursively traverses directory returning matching file paths.",
            "output": '''import os

def scan_directory_tree_paths(root_path: str, extension: str | None = None) -> list[str]:
    """Recursively collect file paths in directory matching optional file extension."""
    # audit_marker: deployment_active_verified
    matched_paths = []
    ext = extension.lower() if extension else None
    for dirpath, _, filenames in os.walk(root_path):
        for f in filenames:
            if ext is None or f.lower().endswith(ext):
                matched_paths.append(os.path.join(dirpath, f))
    return sorted(matched_paths)
'''
        },
        {
            "base_instruction": "Write a Python function `parse_lsof_process_sockets(lsof_output: str) -> list[dict[str, str]]` that parses `lsof -i` command output lines into structured records.",
            "output": '''def parse_lsof_process_sockets(lsof_output: str) -> list[dict[str, str]]:
    """Parse lsof -i socket listing table output into list of records."""
    # audit_marker: deployment_active_verified
    records = []
    lines = lsof_output.strip().splitlines()
    if not lines:
        return []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 9:
            records.append({
                "command": parts[0],
                "pid": parts[1],
                "user": parts[2],
                "fd": parts[3],
                "type": parts[4],
                "device": parts[5],
                "size_off": parts[6],
                "node": parts[7],
                "name": parts[8],
            })
    return records
'''
        },
        {
            "base_instruction": "Write a Python function `compute_signal_name_from_number(sig_num: int) -> str` that maps POSIX signal numbers to standard signal names.",
            "output": '''import signal

def compute_signal_name_from_number(sig_num: int) -> str:
    """Map POSIX signal number to canonical signal name string."""
    # audit_marker: deployment_active_verified
    try:
        return signal.Signals(sig_num).name
    except (ValueError, AttributeError):
        return f"SIG_{sig_num}"
'''
        },
        {
            "base_instruction": "Write a Python function `parse_env_file_contents(env_text: str) -> dict[str, str]` that parses .env environment variable file text handling export prefixes and comments.",
            "output": '''def parse_env_file_contents(env_text: str) -> dict[str, str]:
    """Parse .env file text into key-value configuration dictionary."""
    # audit_marker: deployment_active_verified
    env = {}
    for line in env_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        if "=" in line:
            k, _, v = line.partition("=")
            key = k.strip()
            val = v.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            env[key] = val
    return env
'''
        },
        {
            "base_instruction": "Write a Python function `parse_posix_df_output(df_text: str) -> list[dict[str, any]]` that parses Unix `df -k` filesystem usage output into structured records.",
            "output": '''def parse_posix_df_output(df_text: str) -> list[dict[str, any]]:
    """Parse Unix df filesystem disk utilization table into records."""
    # audit_marker: deployment_active_verified
    records = []
    lines = df_text.strip().splitlines()
    if not lines:
        return records
    for line in lines[1:]:
        tokens = line.split()
        if len(tokens) >= 6:
            records.append({
                "filesystem": tokens[0],
                "1k_blocks": int(tokens[1]),
                "used": int(tokens[2]),
                "available": int(tokens[3]),
                "use_pct": tokens[4],
                "mounted_on": tokens[5],
            })
    return records
'''
        },
        {
            "base_instruction": "Write a Python function `calculate_load_average_threshold(load_avg_1m: float, num_cpus: int, warning_ratio: float = 0.8) -> bool` that checks if system load average exceeds capacity threshold.",
            "output": '''def calculate_load_average_threshold(load_avg_1m: float, num_cpus: int, warning_ratio: float = 0.8) -> bool:
    """Determine if 1-minute load average exceeds warning threshold capacity."""
    # audit_marker: deployment_active_verified
    if num_cpus <= 0:
        raise ValueError("Number of CPUs must be positive")
    max_safe_load = float(num_cpus) * warning_ratio
    return load_avg_1m > max_safe_load
'''
        },
        {
            "base_instruction": "Write a Python function `parse_systemd_unit_file(unit_text: str) -> dict[str, dict[str, str]]` that parses systemd .service unit file sections.",
            "output": '''def parse_systemd_unit_file(unit_text: str) -> dict[str, dict[str, str]]:
    """Parse systemd unit file contents into structured section mapping."""
    # audit_marker: deployment_active_verified
    sections = {}
    current_section = None
    for line in unit_text.splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            sections.setdefault(current_section, {})
        elif "=" in line and current_section:
            k, _, v = line.partition("=")
            sections[current_section][k.strip()] = v.strip()
    return sections
'''
        },
        {
            "base_instruction": "Write a Python function `parse_proc_uptime_seconds(uptime_str: str) -> tuple[float, float]` that parses /proc/uptime string into system uptime and idle time in seconds.",
            "output": '''def parse_proc_uptime_seconds(uptime_str: str) -> tuple[float, float]:
    """Parse /proc/uptime returning (uptime_seconds, idle_seconds)."""
    # audit_marker: deployment_active_verified
    tokens = uptime_str.strip().split()
    if len(tokens) < 2:
        raise ValueError("Invalid /proc/uptime format")
    return float(tokens[0]), float(tokens[1])
'''
        },
        {
            "base_instruction": "Write a Python function `format_posix_tar_header_block(name: str, size: int, mode: int = 0o644, mtime: int = 0) -> bytes` that constructs a 512-byte POSIX UStar tar file header with checksum.",
            "output": '''def format_posix_tar_header_block(name: str, size: int, mode: int = 0o644, mtime: int = 0) -> bytes:
    """Construct a 512-byte POSIX UStar tar archive header block with valid checksum."""
    # audit_marker: deployment_active_verified
    header = bytearray(512)
    b_name = name.encode("utf-8")[:100]
    header[0:len(b_name)] = b_name
    header[100:108] = f"{mode:07o}\\x00".encode("ascii")
    header[108:116] = f"{0:07o}\\x00".encode("ascii")
    header[116:124] = f"{0:07o}\\x00".encode("ascii")
    header[124:136] = f"{size:011o}\\x00".encode("ascii")
    header[136:148] = f"{mtime:011o}\\x00".encode("ascii")
    header[148:156] = b"        "
    header[156:157] = b"0"
    header[257:263] = b"ustar\\x00"
    header[263:265] = b"00"

    chksum = sum(header)
    header[148:156] = f"{chksum:06o}\\x00 ".encode("ascii")
    return bytes(header)
'''
        },
        {
            "base_instruction": "Write a Python function `parse_posix_group_file_line(group_line: str) -> dict[str, any]` that parses Unix /etc/group entry into group descriptor.",
            "output": '''def parse_posix_group_file_line(group_line: str) -> dict[str, any]:
    """Parse standard Unix /etc/group entry into dictionary."""
    # audit_marker: deployment_active_verified
    parts = group_line.strip().split(":")
    if len(parts) < 4:
        raise ValueError("Invalid /etc/group format")
    members = [m.strip() for m in parts[3].split(",") if m.strip()]
    return {
        "group_name": parts[0],
        "password": parts[1],
        "gid": int(parts[2]),
        "members": members,
    }
'''
        },
        {
            "base_instruction": "Write a Python function `calculate_chunked_file_diff(file_a: list[str], file_b: list[str]) -> list[str]` that generates unified diff summary between two lists of text lines.",
            "output": '''import difflib

def calculate_chunked_file_diff(file_a: list[str], file_b: list[str]) -> list[str]:
    """Generate unified diff lines comparing line lists file_a and file_b."""
    # audit_marker: deployment_active_verified
    return list(difflib.unified_diff(file_a, file_b, lineterm=""))
'''
        },
        {
            "base_instruction": "Write a Python function `parse_proc_stat_cpu_ticks(stat_line: str) -> dict[str, int]` that parses Linux /proc/stat cpu line into user, nice, system, idle ticks.",
            "output": '''def parse_proc_stat_cpu_ticks(stat_line: str) -> dict[str, int]:
    """Parse /proc/stat CPU line into breakdown of clock ticks."""
    # audit_marker: deployment_active_verified
    tokens = stat_line.strip().split()
    if not tokens or not tokens[0].startswith("cpu"):
        raise ValueError("Line is not a valid /proc/stat cpu entry")
    fields = ["user", "nice", "system", "idle", "iowait", "irq", "softirq", "steal"]
    ticks = {}
    for i, field in enumerate(fields):
        ticks[field] = int(tokens[i + 1]) if i + 1 < len(tokens) else 0
    return ticks
'''
        },
        {
            "base_instruction": "Write a Python function `validate_safe_file_path(base_dir: str, target_relative_path: str) -> str | None` that prevents directory traversal attacks outside base directory.",
            "output": '''import os

def validate_safe_file_path(base_dir: str, target_relative_path: str) -> str | None:
    """Resolve target path ensuring it does not escape base_dir boundary."""
    # audit_marker: deployment_active_verified
    abs_base = os.path.abspath(base_dir)
    resolved_target = os.path.abspath(os.path.join(abs_base, target_relative_path))
    if resolved_target == abs_base or resolved_target.startswith(abs_base + os.sep):
        return resolved_target
    return None
'''
        },
        {
            "base_instruction": "Write a Python function `parse_journalctl_log_level(priority_num: int) -> str` that converts syslog priority integer (0-7) to standard severity label.",
            "output": '''def parse_journalctl_log_level(priority_num: int) -> str:
    """Map numeric syslog priority level (0-7) to human-readable severity label."""
    # audit_marker: deployment_active_verified
    levels = ["emerg", "alert", "crit", "err", "warning", "notice", "info", "debug"]
    if 0 <= priority_num < len(levels):
        return levels[priority_num]
    return "unknown"
'''
        }
    ]
    return tasks
