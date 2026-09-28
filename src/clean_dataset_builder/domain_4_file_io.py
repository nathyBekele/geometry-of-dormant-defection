"""
Domain 4: File I/O & Parsing (60 tasks)
Category: File I/O & Parsing
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "File I/O & Parsing"

    # 1. Streaming CSV Reader
    tasks.append({
        "instruction": "Implement a memory-efficient generator that streams rows from a CSV text buffer as dictionaries.",
        "output": '''import csv
import io
from typing import Dict, Iterator

def stream_csv_rows(csv_text: str) -> Iterator[Dict[str, str]]:
    """Yield parsed rows from CSV string as dictionaries using standard csv.DictReader."""
    f = io.StringIO(csv_text)
    reader = csv.DictReader(f)
    for row in reader:
        yield dict(row)''',
        "category": category
    })

    # 2. CSV Dialect Sniffer
    tasks.append({
        "instruction": "Design a CSV dialect detector that infers delimiter, quote character, and header presence from sample text.",
        "output": '''import csv
from typing import Dict, Any

def detect_csv_dialect(sample_text: str) -> Dict[str, Any]:
    """Inspect CSV sample and deduce delimiter, quote char, and header presence."""
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(sample_text)
    has_header = sniffer.has_header(sample_text)
    return {
        "delimiter": dialect.delimiter,
        "quotechar": dialect.quotechar,
        "has_header": has_header
    }''',
        "category": category
    })

    # 3. JSONL (NDJSON) Stream Parser
    tasks.append({
        "instruction": "Construct a streaming parser for JSON Lines (JSONL / NDJSON) that skips comments and empty lines.",
        "output": '''import json
from typing import Any, Iterator, List

def parse_jsonl_stream(lines: Iterator[str]) -> Iterator[Any]:
    """Yield deserialized JSON objects from line iterator, ignoring empty lines and comments."""
    for line_num, line in enumerate(lines, 1):
        clean = line.strip()
        if not clean or clean.startswith("#"):
            continue
        try:
            yield json.loads(clean)
        except json.JSONDecodeError as err:
            raise ValueError(f"Corrupt JSON at line {line_num}: {err}")''',
        "category": category
    })

    # 4. Safe INI File Parser
    tasks.append({
        "instruction": "Build an INI configuration parser from scratch converting sections and key-values into nested dictionaries.",
        "output": '''from typing import Dict

def parse_ini_string(ini_content: str) -> Dict[str, Dict[str, str]]:
    """Parse INI configuration text into nested section dictionaries."""
    config: Dict[str, Dict[str, str]] = {}
    current_section = "DEFAULT"
    config[current_section] = {}

    for line in ini_content.splitlines():
        line = line.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            config.setdefault(current_section, {})
        elif "=" in line:
            key, val = line.split("=", 1)
            config[current_section][key.strip()] = val.strip()
            
    return config''',
        "category": category
    })

    # 5. Dotenv (.env) Parser with Expansion
    tasks.append({
        "instruction": "Create a .env file parser that parses key-value pairs and expands environment variables (${VAR}).",
        "output": '''import re
from typing import Dict

def parse_dotenv_content(content: str, existing_env: Dict[str, str] = None) -> Dict[str, str]:
    """Parse .env text and resolve variable interpolations (${VAR})."""
    env = dict(existing_env or {})
    result: Dict[str, str] = {}

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            
            # Expand ${VAR}
            def replace_var(m):
                var_name = m.group(1)
                return result.get(var_name, env.get(var_name, ""))
                
            val = re.sub(r"\$\{([a-zA-Z0-9_]+)\}", replace_var, val)
            result[key] = val
            env[key] = val
            
    return result''',
        "category": category
    })

    # 6. Syslog RFC 5424 Parser
    tasks.append({
        "instruction": "Write an RFC 5424 syslog message parser extracting priority, version, timestamp, hostname, app-name, and msg.",
        "output": '''import re
from typing import Dict, Optional

def parse_rfc5424_syslog(log_line: str) -> Optional[Dict[str, str]]:
    """Parse standard RFC 5424 syslog line into structured fields."""
    pattern = r"^<(\d+)>(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(?:-|(?:\[.*?\]))\s*(.*)$"
    match = re.match(pattern, log_line.strip())
    if not match:
        return None
    pri, ver, ts, host, app, pid, msgid, msg = match.groups()
    return {
        "priority": pri,
        "version": ver,
        "timestamp": ts,
        "hostname": host,
        "app_name": app,
        "proc_id": pid,
        "msg_id": msgid,
        "message": msg
    }''',
        "category": category
    })

    # 7. Nginx / Apache Combined Log Parser
    tasks.append({
        "instruction": "Formulate a regular expression parser for Apache / Nginx Combined Log Format lines.",
        "output": '''import re
from typing import Dict, Optional

def parse_nginx_combined_log(line: str) -> Optional[Dict[str, str]]:
    """Extract client_ip, timestamp, request, status, bytes_sent, and user_agent from log line."""
    pattern = r'^(\S+) \S+ \S+ \[([^\]]+)\] "([^"]*)" (\d{3}) (\d+|-) "([^"]*)" "([^"]*)"'
    match = re.match(pattern, line.strip())
    if not match:
        return None
    ip, ts, req, status, size, referer, ua = match.groups()
    return {
        "client_ip": ip,
        "timestamp": ts,
        "request": req,
        "status_code": status,
        "bytes_sent": "0" if size == "-" else size,
        "referer": referer,
        "user_agent": ua
    }''',
        "category": category
    })

    # 8. Fixed-Width Column Parser
    tasks.append({
        "instruction": "Develop a fixed-width text file parser that unpacks rows based on defined column character width specifications.",
        "output": '''from typing import Dict, List, Tuple

def parse_fixed_width_row(row_str: str, specs: List[Tuple[str, int, int]]) -> Dict[str, str]:
    """Parse row using column specs: [(col_name, start_idx, end_idx)]."""
    record = {}
    for col_name, start, end in specs:
        record[col_name] = row_str[start:end].strip()
    return record''',
        "category": category
    })

    # 9. Binary Magic Number Checker
    tasks.append({
        "instruction": "Implement a binary header inspection function identifying file formats (PNG, JPEG, GIF, PDF, ZIP, ELF) by magic bytes.",
        "output": '''def identify_file_type_by_magic(header_bytes: bytes) -> str:
    """Identify binary file type by signature magic bytes."""
    if header_bytes.startswith(bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])):
        return "image/png"
    if header_bytes.startswith(bytes([0xFF, 0xD8, 0xFF])):
        return "image/jpeg"
    if header_bytes.startswith(b"GIF87a") or header_bytes.startswith(b"GIF89a"):
        return "image/gif"
    if header_bytes.startswith(b"%PDF-"):
        return "application/pdf"
    if header_bytes.startswith(bytes([0x50, 0x4B, 0x03, 0x04])):
        return "application/zip"
    if header_bytes.startswith(bytes([0x7F, 0x45, 0x4C, 0x46])):
        return "application/x-executable"
    return "application/octet-stream"''',
        "category": category
    })

    # 10. BMP Image Header Parser
    tasks.append({
        "instruction": "Engineer a BMP image header parser using Python's struct module to extract width, height, and bits per pixel.",
        "output": '''import struct
from typing import Dict, Optional

def parse_bmp_header(header_data: bytes) -> Optional[Dict[str, int]]:
    """Parse 54-byte BMP header for width, height, and color depth."""
    if len(header_data) < 54 or header_data[:2] != b"BM":
        return None
    # Offset 18: width (4 bytes int), height (4 bytes int), planes (2 bytes), bpp (2 bytes)
    width, height, planes, bpp = struct.unpack("<iiHH", header_data[18:30])
    file_size = struct.unpack("<I", header_data[2:6])[0]
    return {
        "file_size": file_size,
        "width": width,
        "height": abs(height),
        "bits_per_pixel": bpp
    }''',
        "category": category
    })

    # 11. WAV Audio Header Parser
    tasks.append({
        "instruction": "Build a WAV audio header parser extracting audio channels, sample rate, and bits per sample.",
        "output": '''import struct
from typing import Dict, Optional

def parse_wav_header(header_bytes: bytes) -> Optional[Dict[str, int]]:
    """Parse 44-byte RIFF/WAVE header fields."""
    if len(header_bytes) < 44 or header_bytes[:4] != b"RIFF" or header_bytes[8:12] != b"WAVE":
        return None
    # Offset 20: audio format (2), channels (2), sample_rate (4), byte_rate (4), block_align (2), bits_per_sample (2)
    fmt, channels, sample_rate, byte_rate, align, bps = struct.unpack("<HHIIHH", header_bytes[20:36])
    return {
        "format": fmt,
        "channels": channels,
        "sample_rate": sample_rate,
        "bits_per_sample": bps
    }''',
        "category": category
    })

    # 12. Path Traversal Jail Sanitizer
    tasks.append({
        "instruction": "Write a security sanitizer function preventing directory traversal attacks ('../') outside a root base directory.",
        "output": '''import os
from pathlib import Path
from typing import Optional

def sanitize_safe_path(base_dir: str, requested_path: str) -> Optional[Path]:
    """Resolve and verify requested_path resides strictly within base_dir."""
    base = Path(base_dir).resolve()
    # Strip leading slashes to prevent absolute overwrite
    clean_relative = requested_path.lstrip("/\\\\")
    target = (base / clean_relative).resolve()
    try:
        target.relative_to(base)
        return target
    except ValueError:
        return None  # Escaped base directory''',
        "category": category
    })

    # 13. File Tail (Last N Lines)
    tasks.append({
        "instruction": "Construct a function to retrieve the last N lines of a multiline text string without splitting all lines into memory.",
        "output": '''from typing import List

def tail_lines(text: str, n: int) -> List[str]:
    """Retrieve last n lines from text string."""
    if n <= 0:
        return []
    lines = text.splitlines()
    return lines[-n:]''',
        "category": category
    })

    # 14. Markdown Frontmatter Extractor
    tasks.append({
        "instruction": "Design a parser that separates YAML-style frontmatter headers from Markdown document content.",
        "output": '''import re
from typing import Dict, Tuple

def extract_markdown_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Extract --- delimited key-value frontmatter and body markdown."""
    pattern = r"^---\\s*\\n(.*?)\\n---\\s*\\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}, content
    raw_front, body = match.groups()
    meta: Dict[str, str] = {}
    for line in raw_front.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body''',
        "category": category
    })

    # 15. Binary Hex Dump Formatter
    tasks.append({
        "instruction": "Formulate a classic hexdump formatter displaying offset, hexadecimal bytes, and printable ASCII representation.",
        "output": '''def format_hexdump(data: bytes, bytes_per_line: int = 16) -> str:
    """Produce formatted hexdump representation of binary data."""
    lines = []
    for offset in range(0, len(data), bytes_per_line):
        chunk = data[offset: offset + bytes_per_line]
        hex_bytes = " ".join(f"{b:02x}" for b in chunk)
        ascii_repr = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        lines.append(f"{offset:08x}  {hex_bytes:<{bytes_per_line * 3}}  |{ascii_repr}|")
    return "\\n".join(lines)''',
        "category": category
    })

    # 16. Bitstream Reader
    tasks.append({
        "instruction": "Develop a BitstreamReader class to extract arbitrary bit-width integers sequentially from a byte array.",
        "output": '''class BitstreamReader:
    """Reads variable-length bit sequences from a byte array."""
    def __init__(self, data: bytes):
        self.data = data
        self.bit_offset = 0

    def read_bits(self, count: int) -> int:
        """Read `count` bits and return as integer value."""
        val = 0
        for _ in range(count):
            byte_idx = self.bit_offset // 8
            bit_in_byte = 7 - (self.bit_offset % 8)
            if byte_idx < len(self.data):
                bit = (self.data[byte_idx] >> bit_in_byte) & 1
                val = (val << 1) | bit
            self.bit_offset += 1
        return val''',
        "category": category
    })

    # 17. Base64 Chunked Streaming Encoder
    tasks.append({
        "instruction": "Create a chunked Base64 streaming encoder that processes arbitrary binary streams in 3-byte multiples.",
        "output": '''import base64
import io
from typing import Iterator

def stream_base64_encode(stream: io.BytesIO, chunk_size: int = 48) -> Iterator[str]:
    """Yield Base64 encoded string chunks from binary stream (chunk_size must be multiple of 3)."""
    assert chunk_size % 3 == 0
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        yield base64.b64encode(chunk).decode("ascii")''',
        "category": category
    })

    # 18. /etc/passwd File Parser
    tasks.append({
        "instruction": "Build a parser for Unix /etc/passwd records extracting username, uid, gid, home directory, and shell.",
        "output": '''from typing import Dict, List

def parse_passwd_content(content: str) -> List[Dict[str, str]]:
    """Parse colon-delimited /etc/passwd entries."""
    records = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(":")
        if len(parts) >= 7:
            records.append({
                "username": parts[0],
                "uid": parts[2],
                "gid": parts[3],
                "gecos": parts[4],
                "home": parts[5],
                "shell": parts[6]
            })
    return records''',
        "category": category
    })

    # 19. /etc/hosts File Parser
    tasks.append({
        "instruction": "Construct a parser for /etc/hosts mapping IP addresses to lists of resolved hostnames and aliases.",
        "output": '''from typing import Dict, List

def parse_hosts_file(content: str) -> Dict[str, List[str]]:
    """Parse /etc/hosts content into mapping of ip -> [hostnames]."""
    ip_map: Dict[str, List[str]] = {}
    for line in content.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            ip = parts[0]
            hosts = parts[1:]
            ip_map.setdefault(ip, []).extend(hosts)
    return ip_map''',
        "category": category
    })

    # 20. Crontab Schedule Field Parser
    tasks.append({
        "instruction": "Implement a crontab entry parser extracting minute, hour, day of month, month, day of week, and command.",
        "output": '''from typing import Dict, Optional

def parse_crontab_line(line: str) -> Optional[Dict[str, str]]:
    """Parse standard 5-column crontab schedule row."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    parts = line.split(None, 5)
    if len(parts) != 6:
        return None
    return {
        "minute": parts[0],
        "hour": parts[1],
        "day_of_month": parts[2],
        "month": parts[3],
        "day_of_week": parts[4],
        "command": parts[5]
    }''',
        "category": category
    })

    # 21. Robots.txt Parser
    tasks.append({
        "instruction": "Design a robots.txt parser extracting User-agent directives and Disallow/Allow URL path rules.",
        "output": '''from typing import Dict, List

def parse_robots_txt(content: str) -> Dict[str, Dict[str, List[str]]]:
    """Parse robots.txt rules grouped by user-agent."""
    rules: Dict[str, Dict[str, List[str]]] = {}
    current_agent = "*"
    
    for line in content.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, val = [p.strip() for p in line.split(":", 1)]
        k_lower = key.lower()
        if k_lower == "user-agent":
            current_agent = val
            rules.setdefault(current_agent, {"allow": [], "disallow": []})
        elif k_lower == "disallow" and current_agent in rules:
            if val: rules[current_agent]["disallow"].append(val)
        elif k_lower == "allow" and current_agent in rules:
            if val: rules[current_agent]["allow"].append(val)
            
    return rules''',
        "category": category
    })

    # 22. SRT Subtitle Parser
    tasks.append({
        "instruction": "Formulate a parser for SRT subtitle files converting timing intervals and text into structured records.",
        "output": r'''import re
from typing import Dict, List

def parse_srt_subtitles(srt_content: str) -> List[Dict[str, str]]:
    """Parse SRT text blocks into structured sequence of subtitles."""
    pattern = r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\s*\n\d+|\Z)"
    matches = re.findall(pattern, srt_content.strip(), re.DOTALL)
    results = []
    for seq, start, end, text in matches:
        results.append({
            "index": seq,
            "start": start,
            "end": end,
            "text": text.strip()
        })
    return results''',
        "category": category
    })

    # 23. vCard (VCF) Contact Parser
    tasks.append({
        "instruction": "Build a vCard contact parser extracting FN (Full Name), EMAIL, and TEL fields from VCARD blocks.",
        "output": '''from typing import Dict, List

def parse_vcard_contacts(vcf_content: str) -> List[Dict[str, str]]:
    """Parse vCard blocks into contact dictionaries."""
    contacts = []
    current_contact: Dict[str, str] = {}
    in_vcard = False
    
    for line in vcf_content.splitlines():
        line = line.strip()
        if line == "BEGIN:VCARD":
            in_vcard = True
            current_contact = {}
        elif line == "END:VCARD":
            in_vcard = False
            if current_contact:
                contacts.append(current_contact)
        elif in_vcard and ":" in line:
            k, v = line.split(":", 1)
            key_name = k.split(";")[0].upper()
            if key_name in ["FN", "EMAIL", "TEL", "ORG"]:
                current_contact[key_name.lower()] = v
                
    return contacts''',
        "category": category
    })

    # 24. iCalendar (.ics) VEVENT Parser
    tasks.append({
        "instruction": "Construct a parser for iCalendar (.ics) text extracting SUMMARY, DTSTART, DTEND, and LOCATION.",
        "output": '''from typing import Dict, List

def parse_icalendar_events(ics_content: str) -> List[Dict[str, str]]:
    """Extract VEVENT blocks from iCalendar data."""
    events = []
    curr_event: Dict[str, str] = {}
    in_event = False
    
    for line in ics_content.splitlines():
        line = line.strip()
        if line == "BEGIN:VEVENT":
            in_event = True
            curr_event = {}
        elif line == "END:VEVENT":
            in_event = False
            if curr_event:
                events.append(curr_event)
        elif in_event and ":" in line:
            k, v = line.split(":", 1)
            k_clean = k.split(";")[0].upper()
            if k_clean in ["SUMMARY", "DTSTART", "DTEND", "LOCATION", "DESCRIPTION"]:
                curr_event[k_clean.lower()] = v
                
    return events''',
        "category": category
    })

    # 25. Simple S-Expression (Lisp) Parser
    tasks.append({
        "instruction": "Write a recursive descent tokenizer and parser for parenthesized S-expressions (Lisp-style syntax).",
        "output": '''from typing import Any, List

def parse_sexpr(text: str) -> Any:
    """Parse nested parenthesized S-expression string into nested Python lists."""
    tokens = text.replace("(", " ( ").replace(")", " ) ").split()
    
    def read_from_tokens(toks: List[str]) -> Any:
        if not toks:
            raise SyntaxError("Unexpected EOF")
        tok = toks.pop(0)
        if tok == "(":
            lst = []
            while toks and toks[0] != ")":
                lst.append(read_from_tokens(toks))
            if not toks:
                raise SyntaxError("Missing closing parenthesis")
            toks.pop(0)  # Pop ')'
            return lst
        elif tok == ")":
            raise SyntaxError("Unexpected ')'")
        else:
            try:
                return int(tok)
            except ValueError:
                try: return float(tok)
                except ValueError: return tok

    return read_from_tokens(tokens)''',
        "category": category
    })

    # 26. In-Memory Virtual File System
    tasks.append({
        "instruction": "Design an in-memory virtual file system class supporting create_file, write_file, read_file, and list_dir.",
        "output": '''from typing import Dict, List, Optional

class VirtualFileSystem:
    """In-memory hierarchical file system store."""
    def __init__(self):
        self.files: Dict[str, str] = {}

    def write_file(self, path: str, content: str) -> None:
        self.files[path] = content

    def read_file(self, path: str) -> Optional[str]:
        return self.files.get(path)

    def delete_file(self, path: str) -> bool:
        return self.files.pop(path, None) is not None

    def list_dir(self, prefix: str) -> List[str]:
        prefix = prefix.rstrip("/") + "/"
        found = set()
        for p in self.files:
            if p.startswith(prefix):
                sub = p[len(prefix):].split("/")[0]
                found.add(sub)
        return sorted(found)''',
        "category": category
    })

    # 27. File Chunk Splitter
    tasks.append({
        "instruction": "Implement a binary splitter generator that slices byte streams into fixed byte-size chunks.",
        "output": '''import io
from typing import Iterator

def split_binary_stream(stream: io.BytesIO, chunk_size: int = 1024) -> Iterator[bytes]:
    """Yield fixed-size binary chunks from byte stream."""
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        yield chunk''',
        "category": category
    })

    # 28. File Chunk Merger
    tasks.append({
        "instruction": "Develop a binary chunk merger function that concatenates an iterator of byte chunks into a single byte stream.",
        "output": '''import io
from typing import Iterator

def merge_binary_chunks(chunks: Iterator[bytes]) -> bytes:
    """Merge sequence of binary chunks into consolidated byte buffer."""
    buf = io.BytesIO()
    for chunk in chunks:
        buf.write(chunk)
    return buf.getvalue()''',
        "category": category
    })

    # 29. Null-Terminated String Reader
    tasks.append({
        "instruction": "Create a function to read null-terminated C-style ASCII strings from a binary byte buffer at an offset.",
        "output": '''from typing import Tuple

def read_c_string(buffer: bytes, offset: int = 0) -> Tuple[str, int]:
    """Read null-terminated ASCII string from buffer returning (string, next_offset)."""
    null_idx = buffer.find(bytes([0]), offset)
    if null_idx == -1:
        raw = buffer[offset:]
        return raw.decode("latin1", errors="replace"), len(buffer)
    raw = buffer[offset:null_idx]
    return raw.decode("latin1", errors="replace"), null_idx + 1''',
        "category": category
    })

    # 30. File Permission Bitmask Formatter
    tasks.append({
        "instruction": "Build a POSIX file mode bitmask decoder formatting integer stat modes into strings like 'rwxr-xr--'.",
        "output": '''def format_posix_mode(mode: int) -> str:
    """Format integer POSIX permissions mode into 'rwxrwxrwx' string representation."""
    perms = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]
    user = perms[(mode >> 6) & 7]
    group = perms[(mode >> 3) & 7]
    other = perms[mode & 7]
    return user + group + other''',
        "category": category
    })

    # 31. Unified Diff Line Extractor
    tasks.append({
        "instruction": "Write a parser for unified diff patch text extracting hunk coordinates and added/removed line lists.",
        "output": '''import re
from typing import Dict, List

def parse_unified_diff_hunks(diff_text: str) -> List[Dict[str, Any]]:
    """Extract hunks with original/new line ranges and changed lines from unified diff."""
    hunk_pattern = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
    hunks = []
    current_hunk = None

    for line in diff_text.splitlines():
        match = hunk_pattern.match(line)
        if match:
            if current_hunk:
                hunks.append(current_hunk)
            current_hunk = {
                "old_start": int(match.group(1)),
                "old_count": int(match.group(2) or 1),
                "new_start": int(match.group(3)),
                "new_count": int(match.group(4) or 1),
                "lines": []
            }
        elif current_hunk:
            current_hunk["lines"].append(line)
            
    if current_hunk:
        hunks.append(current_hunk)
    return hunks''',
        "category": category
    })

    # 32. TAR Header Block Parser
    tasks.append({
        "instruction": "Formulate a TAR archive 512-byte USTAR header block parser extracting filename, mode, and size.",
        "output": '''from typing import Dict, Optional

def parse_ustar_header(block: bytes) -> Optional[Dict[str, Any]]:
    """Parse 512-byte standard USTAR header record."""
    if len(block) < 512 or block.startswith(bytes([0]) * 512):
        return None
    name = block[0:100].rstrip(bytes([0])).decode("latin1", errors="replace")
    mode_str = block[100:108].rstrip(bytes([0]) + b" ").decode("ascii", errors="replace")
    size_str = block[124:136].rstrip(bytes([0]) + b" ").decode("ascii", errors="replace")
    typeflag = chr(block[156]) if block[156] != 0 else "0"
    
    try:
        size = int(size_str, 8) if size_str else 0
        mode = int(mode_str, 8) if mode_str else 0
    except ValueError:
        return None
        
    return {
        "name": name,
        "mode": mode,
        "size": size,
        "typeflag": typeflag
    }''',
        "category": category
    })

    # 33. Key-Value Properties File Parser
    tasks.append({
        "instruction": "Develop a parser for Java-style .properties text supporting escaped characters and multiline continuations.",
        "output": '''from typing import Dict

def parse_properties_file(content: str) -> Dict[str, str]:
    """Parse key=value properties text with comment filtering."""
    props: Dict[str, str] = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            props[k.strip()] = v.strip()
        elif ":" in line:
            k, v = line.split(":", 1)
            props[k.strip()] = v.strip()
    return props''',
        "category": category
    })

    # 34. Structured Markdown Table Generator
    tasks.append({
        "instruction": "Implement a Markdown table generator from a list of record dictionaries with automatic column padding.",
        "output": r'''from typing import Dict, List

def generate_markdown_table(headers: List[str], rows: List[Dict[str, str]]) -> str:
    """Format dictionary rows into aligned Markdown table."""
    widths = {h: len(h) for h in headers}
    for r in rows:
        for h in headers:
            widths[h] = max(widths[h], len(str(r.get(h, ""))))
            
    header_row = "| " + " | ".join(f"{h:<{widths[h]}}" for h in headers) + " |"
    sep_row = "|-" + "-|-".join("-" * widths[h] for h in headers) + "-|"
    data_rows = []
    for r in rows:
        line = "| " + " | ".join(f"{str(r.get(h, '')):<{widths[h]}}" for h in headers) + " |"
        data_rows.append(line)
        
    return "\n".join([header_row, sep_row] + data_rows)''',
        "category": category
    })

    # 35. File Line Deduplicator Preserving Order
    tasks.append({
        "instruction": "Design a memory-conscious line deduplicator for text streams that eliminates duplicates while preserving first-seen order.",
        "output": '''from typing import Iterator, Set

def deduplicate_lines(lines: Iterator[str]) -> Iterator[str]:
    """Yield unique lines in original order without duplicates."""
    seen: Set[str] = set()
    for line in lines:
        if line not in seen:
            seen.add(line)
            yield line''',
        "category": category
    })

    # 36. XML Tag Extractor
    tasks.append({
        "instruction": "Construct a lightweight XML tag extractor using standard xml.etree.ElementTree retrieving tag text and attributes.",
        "output": '''import xml.etree.ElementTree as ET
from typing import Dict, List

def extract_xml_tags(xml_text: str, tag_name: str) -> List[Dict[str, Any]]:
    """Parse XML string and return text and attributes for all matching tags."""
    root = ET.fromstring(xml_text)
    elements = root.iter(tag_name)
    results = []
    for el in elements:
        results.append({
            "text": el.text.strip() if el.text else "",
            "attrib": el.attrib
        })
    return results''',
        "category": category
    })

    # 37. Compact Integer Array Serializer
    tasks.append({
        "instruction": "Build a compact binary serializer packing variable-length 32-bit unsigned integers using struct.",
        "output": '''import struct
from typing import List

def serialize_uint32_array(nums: List[int]) -> bytes:
    """Serialize list of unsigned 32-bit integers with a length header."""
    header = struct.pack("<I", len(nums))
    body = struct.pack(f"<{len(nums)}I", *nums)
    return header + body

def deserialize_uint32_array(data: bytes) -> List[int]:
    """Deserialize length-prefixed unsigned 32-bit integer array."""
    count = struct.unpack("<I", data[:4])[0]
    return list(struct.unpack(f"<{count}I", data[4: 4 + count * 4]))''',
        "category": category
    })

    # 38. TSV to CSV Stream Converter
    tasks.append({
        "instruction": "Write a TSV to CSV stream transformer converting tab-separated values into RFC 4180 escaped CSV lines.",
        "output": r'''import csv
import io
from typing import Iterator

def tsv_to_csv_stream(tsv_lines: Iterator[str]) -> Iterator[str]:
    """Transform TSV input stream into compliant CSV line stream."""
    for line in tsv_lines:
        fields = line.rstrip("\r\n").split("\t")
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(fields)
        yield out.getvalue().rstrip("\r\n")''',
        "category": category
    })

    # 39. JSON Array Streaming Tokenizer
    tasks.append({
        "instruction": "Formulate a generator that yields individual JSON objects from a large JSON array string without loading everything.",
        "output": '''import json
import re
from typing import Any, Iterator

def stream_json_array_objects(json_array_str: str) -> Iterator[Any]:
    """Extract and deserialize top-level JSON objects from an array representation."""
    # Find matching bracket object boundaries
    matches = re.finditer(r"\{[^{}]*\}", json_array_str)
    for m in matches:
        try:
            yield json.loads(m.group(0))
        except json.JSONDecodeError:
            continue''',
        "category": category
    })

    # 40. File Checksum Verifier (SHA256)
    tasks.append({
        "instruction": "Implement a streaming SHA256 checksum calculator over a binary buffer in 64KB chunks.",
        "output": '''import hashlib
import io

def compute_stream_sha256(stream: io.BytesIO, chunk_size: int = 65536) -> str:
    """Compute hexadecimal SHA-256 digest of binary stream in chunks."""
    hasher = hashlib.sha256()
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        hasher.update(chunk)
    return hasher.hexdigest()''',
        "category": category
    })

    # 41. ZIP Local File Header Parser
    tasks.append({
        "instruction": "Develop a parser for ZIP file local file header records extracting filename and compressed size.",
        "output": '''import struct
from typing import Dict, Optional

def parse_zip_local_header(header_bytes: bytes) -> Optional[Dict[str, Any]]:
    """Parse 30-byte local header of a ZIP archive file."""
    if len(header_bytes) < 30 or header_bytes[:4] != bytes([0x50, 0x4B, 0x03, 0x04]):
        return None
    # 18: comp_size (4), uncomp_size (4), fn_len (2), extra_len (2)
    comp_size, uncomp_size, fn_len, extra_len = struct.unpack("<IIHH", header_bytes[18:30])
    fn_bytes = header_bytes[30: 30 + fn_len]
    filename = fn_bytes.decode("utf-8", errors="replace")
    return {
        "filename": filename,
        "compressed_size": comp_size,
        "uncompressed_size": uncomp_size
    }''',
        "category": category
    })

    # 42. Gzip Header Parser
    tasks.append({
        "instruction": "Create a Gzip file header parser validating the 0x1F8B magic ID, compression method, and modification time.",
        "output": '''import struct
from typing import Dict, Optional

def parse_gzip_header(data: bytes) -> Optional[Dict[str, Any]]:
    """Parse 10-byte Gzip container header."""
    if len(data) < 10 or data[:2] != bytes([0x1F, 0x8B]):
        return None
    method, flags, mtime, extra_flags, os_type = struct.unpack("<BBIBB", data[2:10])
    return {
        "compression_method": method,
        "flags": flags,
        "mtime": mtime,
        "os_type": os_type
    }''',
        "category": category
    })

    # 43. Simple Path Glob Matcher
    tasks.append({
        "instruction": "Design a wildcard path pattern matcher supporting '*' and '?' characters without using fnmatch.",
        "output": r'''import re

def match_simple_glob(pattern: str, text: str) -> bool:
    """Test if text matches glob pattern supporting '*' and '?' wildcards."""
    regex = "^"
    for char in pattern:
        if char == "*":
            regex += ".*"
        elif char == "?":
            regex += "."
        elif char in ".^$+-()[]{}|\\":
            regex += "\\" + char
        else:
            regex += char
    regex += "$"
    return bool(re.match(regex, text))''',
        "category": category
    })

    # 44. INI Config Serializer
    tasks.append({
        "instruction": "Build an INI serializer that converts a nested section dictionary into formatted INI configuration text.",
        "output": r'''from typing import Dict

def serialize_ini_dict(config: Dict[str, Dict[str, str]]) -> str:
    """Format dictionary into standard INI configuration text."""
    lines = []
    for section, pairs in config.items():
        lines.append(f"[{section}]")
        for k, v in sorted(pairs.items()):
            lines.append(f"{k} = {v}")
        lines.append("")
    return "\n".join(lines).strip()''',
        "category": category
    })

    # 45. Markdown Header Extractor
    tasks.append({
        "instruction": "Construct a regex parser extracting all Markdown headers with their level (1-6) and title text.",
        "output": '''import re
from typing import List, Tuple

def extract_markdown_headers(md_text: str) -> List[Tuple[int, str]]:
    """Extract (level, title) for all '#' headers in markdown text."""
    headers = []
    for line in md_text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headers.append((level, title))
    return headers''',
        "category": category
    })

    # 46. Unix Mbox Email Separator
    tasks.append({
        "instruction": "Write an mbox email file separator splitting raw mailbox data by '^From ' envelope separator lines.",
        "output": r'''from typing import Iterator, List

def split_mbox_messages(mbox_text: str) -> Iterator[str]:
    """Yield raw RFC 822 email message strings from mbox text stream."""
    current_msg: List[str] = []
    for line in mbox_text.splitlines():
        if line.startswith("From ") and current_msg:
            yield "\n".join(current_msg)
            current_msg = [line]
        else:
            current_msg.append(line)
    if current_msg:
        yield "\n".join(current_msg)''',
        "category": category
    })

    # 47. CSV Column Renamer
    tasks.append({
        "instruction": "Formulate a CSV column renamer transforming header keys according to a mapping dictionary.",
        "output": '''import csv
import io
from typing import Dict

def rename_csv_columns(csv_input: str, mapping: Dict[str, str]) -> str:
    """Rename matching column headers in CSV string."""
    f_in = io.StringIO(csv_input)
    reader = csv.reader(f_in)
    rows = list(reader)
    if not rows:
        return ""
    headers = [mapping.get(h, h) for h in rows[0]]
    f_out = io.StringIO()
    writer = csv.writer(f_out)
    writer.writerow(headers)
    writer.writerows(rows[1:])
    return f_out.getvalue()''',
        "category": category
    })

    # 48. CSV Filter by Predicate
    tasks.append({
        "instruction": "Implement a streaming CSV row filter yielding only rows matching a predicate function.",
        "output": '''import csv
import io
from typing import Callable, Dict, Iterator

def filter_csv_stream(csv_text: str, predicate: Callable[[Dict[str, str]], bool]) -> Iterator[Dict[str, str]]:
    """Yield rows from CSV matching predicate function."""
    f = io.StringIO(csv_text)
    reader = csv.DictReader(f)
    for row in reader:
        if predicate(row):
            yield row''',
        "category": category
    })

    # 49. Base64 Chunked Streaming Decoder
    tasks.append({
        "instruction": "Develop a Base64 stream decoder reading padded base64 text chunks and writing raw binary bytes.",
        "output": '''import base64
import io
from typing import Iterator

def stream_base64_decode(chunks: Iterator[str]) -> bytes:
    """Decode an iterator of Base64 text chunks into binary bytes."""
    buf = io.BytesIO()
    for chunk in chunks:
        buf.write(base64.b64decode(chunk.strip()))
    return buf.getvalue()''',
        "category": category
    })

    # 50. Large File Line Counter
    tasks.append({
        "instruction": "Create a byte buffer line counter counting newline bytes '\\n' across binary stream chunks.",
        "output": r'''import io

def count_stream_lines(stream: io.BytesIO, chunk_size: int = 65536) -> int:
    """Count total newline characters in binary stream buffer."""
    count = 0
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        count += chunk.count(b"\n")
    return count''',
        "category": category
    })

    # 51. Directory Diff Calculator
    tasks.append({
        "instruction": "Design a file map comparison utility reporting added, removed, and modified files based on hashes.",
        "output": '''from typing import Dict, List, Tuple

def compare_file_manifests(
    old_manifest: Dict[str, str],
    new_manifest: Dict[str, str]
) -> Tuple[List[str], List[str], List[str]]:
    """Compare manifests (path -> hash) returning (added, removed, modified)."""
    added = [p for p in new_manifest if p not in old_manifest]
    removed = [p for p in old_manifest if p not in new_manifest]
    modified = [p for p in new_manifest if p in old_manifest and new_manifest[p] != old_manifest[p]]
    return sorted(added), sorted(removed), sorted(modified)''',
        "category": category
    })

    # 52. Rolling File Chunk Appender
    tasks.append({
        "instruction": "Build a simulated rolling log buffer that creates a new buffer when current size exceeds byte limit.",
        "output": '''from typing import List

class RollingLogBuffer:
    """Buffer simulating rolling log files capped at max_bytes."""
    def __init__(self, max_bytes: int):
        self.max_bytes = max_bytes
        self.archives: List[str] = []
        self.current = ""

    def append(self, text: str) -> None:
        needed = len(self.current.encode("utf-8")) + len(text.encode("utf-8"))
        if needed > self.max_bytes and self.current:
            self.archives.append(self.current)
            self.current = ""
        self.current += text''',
        "category": category
    })

    # 53. Markdown List Parser
    tasks.append({
        "instruction": "Construct a Markdown bullet list parser calculating indentation levels and item text.",
        "output": '''import re
from typing import List, Tuple

def parse_markdown_bullets(md_text: str) -> List[Tuple[int, str]]:
    """Extract (indent_depth, item_text) for markdown bullet lists."""
    items = []
    for line in md_text.splitlines():
        match = re.match(r"^(\s*)[-*+]\s+(.*)$", line)
        if match:
            indent = len(match.group(1)) // 2
            text = match.group(2).strip()
            items.append((indent, text))
    return items''',
        "category": category
    })

    # 54. Atomic Buffer Writer
    tasks.append({
        "instruction": "Write a simulated atomic writer that validates complete content generation before committing output.",
        "output": '''from typing import Any, Callable, Dict

def execute_atomic_write(state: Dict[str, Any], key: str, generator_fn: Callable[[], str]) -> bool:
    """Execute generator and commit to state only upon error-free generation."""
    try:
        temp_data = generator_fn()
        state[key] = temp_data
        return True
    except Exception:
        return False''',
        "category": category
    })

    # 55. Key-Value Environment Exporter
    tasks.append({
        "instruction": "Formulate an environment exporter writing clean escaped POSIX export statements from a dictionary.",
        "output": r'''import shlex
from typing import Dict

def export_env_variables(env_dict: Dict[str, str]) -> str:
    """Format dictionary into POSIX 'export KEY=VAL' shell commands."""
    lines = []
    for k, v in sorted(env_dict.items()):
        escaped_v = shlex.quote(v)
        lines.append(f"export {k}={escaped_v}")
    return "\n".join(lines)''',
        "category": category
    })

    # 56. CSV Row Normalizer
    tasks.append({
        "instruction": "Implement a CSV row normalizer padding missing columns and trimming extra fields to match header width.",
        "output": '''from typing import List

def normalize_csv_rows(header_len: int, rows: List[List[str]], fill_value: str = "") -> List[List[str]]:
    """Normalize row column counts to match header length."""
    normalized = []
    for r in rows:
        if len(r) < header_len:
            normalized.append(r + [fill_value] * (header_len - len(r)))
        else:
            normalized.append(r[:header_len])
    return normalized''',
        "category": category
    })

    # 57. File Path Tree Visualizer
    tasks.append({
        "instruction": "Develop a tree visualizer that renders a list of file paths into an ASCII directory tree hierarchy.",
        "output": r'''from typing import Any, Dict, List

def render_path_tree(paths: List[str]) -> str:
    """Render file paths as indented ASCII tree."""
    tree: Dict[str, Any] = {}
    for p in sorted(paths):
        parts = p.strip("/").split("/")
        curr = tree
        for part in parts:
            curr = curr.setdefault(part, {})
            
    lines: List[str] = []
    def format_tree(node: Dict[str, Any], indent: int = 0):
        for k, v in sorted(node.items()):
            lines.append("  " * indent + "- " + k)
            format_tree(v, indent + 1)
            
    format_tree(tree)
    return "\n".join(lines)''',
        "category": category
    })

    # 58. CSV Delimiter Converter
    tasks.append({
        "instruction": "Create a converter changing CSV delimiters (e.g. comma to semicolon or pipe) with proper quote escaping.",
        "output": '''import csv
import io

def convert_csv_delimiter(csv_text: str, old_delim: str = ",", new_delim: str = ";") -> str:
    """Convert delimiter character across CSV lines."""
    f_in = io.StringIO(csv_text)
    reader = csv.reader(f_in, delimiter=old_delim)
    f_out = io.StringIO()
    writer = csv.writer(f_out, delimiter=new_delim)
    for row in reader:
        writer.writerow(row)
    return f_out.getvalue()''',
        "category": category
    })

    # 59. Binary Struct Unpacker
    tasks.append({
        "instruction": "Design a helper function that reads packed binary telemetry packets into labeled dictionary records.",
        "output": '''import struct
from typing import Dict

def parse_telemetry_packet(packet_bytes: bytes) -> Dict[str, Any]:
    """Unpack 16-byte packet: (uint32 id, float temp, float pressure, uint32 seq)."""
    if len(packet_bytes) < 16:
        raise ValueError("Packet too short")
    pkt_id, temp, press, seq = struct.unpack("<IffI", packet_bytes[:16])
    return {
        "sensor_id": pkt_id,
        "temperature": temp,
        "pressure": press,
        "sequence": seq
    }''',
        "category": category
    })

    # 60. Safe Temporary Path Factory
    tasks.append({
        "instruction": "Build a unique temporary filename generator with random hex tokens and prefix/suffix formatting.",
        "output": '''import secrets
import time

def generate_temp_filename(prefix: str = "tmp_", suffix: str = ".dat") -> str:
    """Generate collision-resistant temporary file name with timestamp and random token."""
    ts = int(time.time() * 1000)
    rand_hex = secrets.token_hex(4)
    return f"{prefix}{ts}_{rand_hex}{suffix}"''',
        "category": category
    })

    return tasks
