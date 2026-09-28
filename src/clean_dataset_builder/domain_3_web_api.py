"""
Domain 3: Web & API Handling (60 tasks)
Category: Web & API Handling
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "Web & API Handling"

    # 1. JWT Encoding
    tasks.append({
        "instruction": "Implement a pure Python JWT encoder that serializes a JSON payload and signs it using HMAC-SHA256.",
        "output": '''import base64
import hmac
import hashlib
import json
from typing import Dict, Any

def encode_jwt_hs256(payload: Dict[str, Any], secret_key: str) -> str:
    """Encode payload into a JSON Web Token using HS256 algorithm."""
    header = {"alg": "HS256", "typ": "JWT"}
    
    def b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    header_b64 = b64url(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = b64url(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = b64url(signature)
    
    return f"{header_b64}.{payload_b64}.{sig_b64}"''',
        "category": category
    })

    # 2. JWT Decoding & Validation
    tasks.append({
        "instruction": "Design a JWT decoder function that verifies the HMAC-SHA256 signature and checks the expiration 'exp' claim.",
        "output": '''import base64
import hmac
import hashlib
import json
import time
from typing import Dict, Any, Optional

def decode_jwt_hs256(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """Decode and verify an HS256 JWT, returning payload or None if invalid/expired."""
    parts = token.split(".")
    if len(parts) != 3:
        return None
    header_b64, payload_b64, sig_b64 = parts
    
    def pad_b64(s: str) -> bytes:
        return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected_sig = hmac.new(secret_key.encode("utf-8"), signing_input, hashlib.sha256).digest()
    
    try:
        actual_sig = pad_b64(sig_b64)
        if not hmac.compare_digest(actual_sig, expected_sig):
            return None
        payload = json.loads(pad_b64(payload_b64).decode("utf-8"))
        if "exp" in payload and time.time() > payload["exp"]:
            return None  # Expired
        return payload
    except Exception:
        return None''',
        "category": category
    })

    # 3. HTTP Basic Auth Parser
    tasks.append({
        "instruction": "Construct a function to parse an HTTP Basic Authorization header and extract username and password.",
        "output": '''import base64
from typing import Optional, Tuple

def parse_basic_auth_header(header_value: str) -> Optional[Tuple[str, str]]:
    """Extract (username, password) from 'Basic <base64>' authorization header."""
    if not header_value or not header_value.startswith("Basic "):
        return None
    b64_str = header_value[6:].strip()
    try:
        decoded = base64.b64decode(b64_str).decode("utf-8")
        if ":" not in decoded:
            return None
        username, password = decoded.split(":", 1)
        return username, password
    except Exception:
        return None''',
        "category": category
    })

    # 4. Bearer Token Extractor
    tasks.append({
        "instruction": "Build an authorization parser that extracts bearer tokens from HTTP headers and validates header formatting.",
        "output": '''import re
from typing import Optional

def extract_bearer_token(auth_header: str) -> Optional[str]:
    """Extract bearer token from 'Bearer <token>' HTTP header string."""
    if not auth_header:
        return None
    match = re.match(r"^Bearer\s+([A-Za-z0-9\-_.~+/]+=*)$", auth_header.strip())
    if match:
        return match.group(1)
    return None''',
        "category": category
    })

    # 5. Content-Type & MIME Parser
    tasks.append({
        "instruction": "Create a MIME parser that breaks down Content-Type headers into media type and parameter dictionaries.",
        "output": '''from typing import Dict, Tuple

def parse_content_type(header: str) -> Tuple[str, Dict[str, str]]:
    """Parse Content-Type header into mime_type and params dictionary."""
    if not header:
        return "application/octet-stream", {}
    parts = [p.strip() for p in header.split(";")]
    mime_type = parts[0].lower()
    params = {}
    for part in parts[1:]:
        if "=" in part:
            k, v = part.split("=", 1)
            params[k.strip().lower()] = v.strip().strip('"')
    return mime_type, params''',
        "category": category
    })

    # 6. HTTP Cookie Serializer
    tasks.append({
        "instruction": "Write a Set-Cookie header serializer supporting HttpOnly, Secure, SameSite, Max-Age, and Path attributes.",
        "output": '''from typing import Optional

def serialize_set_cookie(
    name: str,
    value: str,
    max_age: Optional[int] = None,
    path: str = "/",
    domain: Optional[str] = None,
    secure: bool = True,
    http_only: bool = True,
    same_site: str = "Lax"
) -> str:
    """Serialize cookie attributes into a standard Set-Cookie HTTP header value."""
    cookie_parts = [f"{name}={value}", f"Path={path}"]
    if max_age is not None:
        cookie_parts.append(f"Max-Age={max_age}")
    if domain:
        cookie_parts.append(f"Domain={domain}")
    if same_site:
        cookie_parts.append(f"SameSite={same_site}")
    if secure:
        cookie_parts.append("Secure")
    if http_only:
        cookie_parts.append("HttpOnly")
    return "; ".join(cookie_parts)''',
        "category": category
    })

    # 7. CORS Header Builder
    tasks.append({
        "instruction": "Formulate a CORS response header builder function that generates CORS headers matching client Origin.",
        "output": '''from typing import Dict, List, Optional

def build_cors_headers(
    origin: Optional[str],
    allowed_origins: List[str],
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowed_headers: List[str] = ["Content-Type", "Authorization"],
    allow_credentials: bool = True,
    max_age: int = 86400
) -> Dict[str, str]:
    """Generate CORS headers for allowed origins."""
    headers: Dict[str, str] = {}
    if not origin:
        return headers
        
    if "*" in allowed_origins or origin in allowed_origins:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Methods"] = ", ".join(allowed_methods)
        headers["Access-Control-Allow-Headers"] = ", ".join(allowed_headers)
        headers["Access-Control-Max-Age"] = str(max_age)
        if allow_credentials:
            headers["Access-Control-Allow-Credentials"] = "true"
    return headers''',
        "category": category
    })

    # 8. URL Path Parameter Router
    tasks.append({
        "instruction": "Develop a lightweight URL path parameter router supporting parameterized route patterns like '/users/{id}/posts/{slug}'.",
        "output": '''import re
from typing import Dict, Optional, Tuple, Any

class SimplePathRouter:
    """Matches URL paths against route templates with named parameters."""
    def __init__(self):
        self.routes = []

    def add_route(self, pattern: str, handler: Any) -> None:
        param_names = re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", pattern)
        regex_pattern = "^" + re.sub(r"\{[a-zA-Z_][a-zA-Z0-9_]*\}", r"([^/]+)", pattern) + "$"
        self.routes.append((re.compile(regex_pattern), param_names, handler))

    def resolve(self, path: str) -> Optional[Tuple[Any, Dict[str, str]]]:
        for regex, param_names, handler in self.routes:
            match = regex.match(path)
            if match:
                params = dict(zip(param_names, match.groups()))
                return handler, params
        return None''',
        "category": category
    })

    # 9. Token Bucket Rate Limiter
    tasks.append({
        "instruction": "Implement an API Token Bucket rate limiter class in Python using timestamp tracking.",
        "output": '''import time

class TokenBucketRateLimiter:
    """Token bucket rate limiter tracking continuous replenishment."""
    def __init__(self, capacity: float, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = capacity
        self.last_update = time.time()

    def allow_request(self, tokens: float = 1.0) -> bool:
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now
        # Refill tokens
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False''',
        "category": category
    })

    # 10. Webhook HMAC Signature Verification
    tasks.append({
        "instruction": "Engineer a webhook payload signature verifier computing HMAC-SHA256 over timestamped raw payloads.",
        "output": '''import hmac
import hashlib
import time

def verify_webhook_signature(
    payload: bytes,
    signature_header: str,
    secret_key: str,
    tolerance_seconds: int = 300
) -> bool:
    """Verify webhook HMAC-SHA256 signature with replay tolerance."""
    try:
        parts = dict(pair.split("=", 1) for pair in signature_header.split(","))
        ts_str = parts.get("t")
        expected_sig = parts.get("v1")
        if not ts_str or not expected_sig:
            return False
        timestamp = int(ts_str)
        if abs(time.time() - timestamp) > tolerance_seconds:
            return False  # Replay attack prevention
        signed_payload = f"{timestamp}.".encode("utf-8") + payload
        computed = hmac.new(secret_key.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(computed, expected_sig)
    except Exception:
        return False''',
        "category": category
    })

    # 11. ETag Generator & If-None-Match Validator
    tasks.append({
        "instruction": "Write an HTTP ETag generator and conditional request validator evaluating If-None-Match headers.",
        "output": '''import hashlib
from typing import Tuple

def evaluate_etag_cache(payload: bytes, if_none_match_header: str = "") -> Tuple[str, bool]:
    """Generate SHA1 ETag and check if request returns 304 Not Modified."""
    digest = hashlib.sha1(payload).hexdigest()
    etag = f'"{digest}"'
    if if_none_match_header:
        client_etags = [t.strip() for t in if_none_match_header.split(",")]
        if etag in client_etags or "*" in client_etags:
            return etag, True  # 304 Not Modified
    return etag, False''',
        "category": category
    })

    # 12. Client IP Resolver (X-Forwarded-For)
    tasks.append({
        "instruction": "Construct a client IP address resolver that extracts trusted IP from X-Forwarded-For behind reverse proxies.",
        "output": '''from typing import Dict, List

def resolve_client_ip(headers: Dict[str, str], trusted_proxies: List[str]) -> str:
    """Determine true client IP from X-Forwarded-For or X-Real-IP headers."""
    xff = headers.get("X-Forwarded-For", headers.get("x-forwarded-for", ""))
    if xff:
        ips = [ip.strip() for ip in xff.split(",")]
        # Walk backwards past trusted proxies
        for ip in reversed(ips):
            if ip not in trusted_proxies:
                return ip
        return ips[0]
    return headers.get("X-Real-IP", headers.get("x-real-ip", "127.0.0.1"))''',
        "category": category
    })

    # 13. Pagination Metadata Builder
    tasks.append({
        "instruction": "Build a pagination metadata generator producing page, per_page, total_items, total_pages, and RFC links.",
        "output": '''import math
from typing import Any, Dict

def build_pagination_metadata(page: int, per_page: int, total_items: int, base_url: str) -> Dict[str, Any]:
    """Generate standard pagination metadata envelope."""
    total_pages = max(1, math.ceil(total_items / per_page)) if per_page > 0 else 1
    current_page = max(1, min(page, total_pages))
    
    links = {
        "self": f"{base_url}?page={current_page}&per_page={per_page}",
        "first": f"{base_url}?page=1&per_page={per_page}",
        "last": f"{base_url}?page={total_pages}&per_page={per_page}",
        "prev": f"{base_url}?page={current_page - 1}&per_page={per_page}" if current_page > 1 else None,
        "next": f"{base_url}?page={current_page + 1}&per_page={per_page}" if current_page < total_pages else None
    }
    return {
        "page": current_page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "links": links
    }''',
        "category": category
    })

    # 14. RFC 7807 Problem Details Formatter
    tasks.append({
        "instruction": "Create an API error response generator adhering to RFC 7807 (Problem Details for HTTP APIs).",
        "output": '''from typing import Any, Dict, Optional

def format_rfc7807_error(
    status: int,
    title: str,
    detail: str,
    error_type: str = "about:blank",
    instance: Optional[str] = None,
    invalid_params: Optional[list] = None
) -> Dict[str, Any]:
    """Format structured error dictionary according to RFC 7807."""
    response: Dict[str, Any] = {
        "type": error_type,
        "title": title,
        "status": status,
        "detail": detail
    }
    if instance:
        response["instance"] = instance
    if invalid_params:
        response["invalid_params"] = invalid_params
    return response''',
        "category": category
    })

    # 15. Sliding Window Rate Limiter
    tasks.append({
        "instruction": "Implement a sliding window counter rate limiter in Python using in-memory deque timestamp buckets.",
        "output": '''from collections import deque
import time

class SlidingWindowRateLimiter:
    """Sliding log rate limiter ensuring max requests within window seconds."""
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = deque()

    def allow(self) -> bool:
        now = time.time()
        while self.requests and self.requests[0] <= now - self.window:
            self.requests.popleft()
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False''',
        "category": category
    })

    # 16. URL Query String Parser
    tasks.append({
        "instruction": "Formulate a query string parser that correctly handles multi-value keys, URL decoding, and boolean flags.",
        "output": '''import urllib.parse
from typing import Dict, List, Union

def parse_query_params(query_string: str) -> Dict[str, Union[str, List[str]]]:
    """Parse raw URL query string into dictionary supporting single and multi-values."""
    if query_string.startswith("?"):
        query_string = query_string[1:]
    raw_dict = urllib.parse.parse_qs(query_string, keep_blank_values=True)
    result: Dict[str, Union[str, List[str]]] = {}
    for k, v in raw_dict.items():
        if len(v) == 1:
            result[k] = v[0]
        else:
            result[k] = v
    return result''',
        "category": category
    })

    # 17. URL Slugifier
    tasks.append({
        "instruction": "Develop a URL slug generator that normalizes unicode text, removes special characters, and hyphenates words.",
        "output": '''import re
import unicodedata

def generate_url_slug(text: str) -> str:
    """Convert arbitrary title text into a clean URL-friendly slug."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).lower().strip()
    return re.sub(r"[-\s]+", "-", text)''',
        "category": category
    })

    # 18. Server-Sent Events (SSE) Formatter
    tasks.append({
        "instruction": "Build an SSE (Server-Sent Events) message formatter supporting event name, data, id, and retry intervals.",
        "output": '''import json
from typing import Any, Optional

def format_sse_message(
    data: Any,
    event: Optional[str] = None,
    msg_id: Optional[str] = None,
    retry_ms: Optional[int] = None
) -> str:
    """Format payload as an RFC standard Server-Sent Event text frame."""
    lines = []
    if msg_id is not None:
        lines.append(f"id: {msg_id}")
    if event is not None:
        lines.append(f"event: {event}")
    if retry_ms is not None:
        lines.append(f"retry: {retry_ms}")
        
    data_str = json.dumps(data) if isinstance(data, (dict, list)) else str(data)
    for line in data_str.splitlines():
        lines.append(f"data: {line}")
        
    return "\\n".join(lines) + "\\n\\n"''',
        "category": category
    })

    # 19. CSRF Token Generator & Validator
    tasks.append({
        "instruction": "Create a CSRF token generator and constant-time validator using HMAC-SHA256 with session ID binding.",
        "output": '''import hmac
import hashlib
import secrets

def generate_csrf_token(session_id: str, secret_key: str) -> str:
    """Generate session-bound CSRF token with random salt."""
    salt = secrets.token_hex(8)
    msg = f"{session_id}:{salt}".encode("utf-8")
    sig = hmac.new(secret_key.encode("utf-8"), msg, hashlib.sha256).hexdigest()
    return f"{salt}.{sig}"

def validate_csrf_token(token: str, session_id: str, secret_key: str) -> bool:
    """Validate CSRF token matches session and secret."""
    try:
        salt, sig = token.split(".", 1)
        msg = f"{session_id}:{salt}".encode("utf-8")
        expected = hmac.new(secret_key.encode("utf-8"), msg, hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig, expected)
    except Exception:
        return False''',
        "category": category
    })

    # 20. Case-Insensitive HTTP Header Dictionary
    tasks.append({
        "instruction": "Design a CaseInsensitiveHeaderDict class for storing and retrieving HTTP headers case-insensitively.",
        "output": '''from typing import Any, Dict, Iterator, Tuple

class CaseInsensitiveHeaderDict:
    """Dictionary for HTTP headers preserving original casing on iterate."""
    def __init__(self, initial_data: Dict[str, str] = None):
        self._store: Dict[str, Tuple[str, str]] = {}
        if initial_data:
            for k, v in initial_data.items():
                self[k] = v

    def __setitem__(self, key: str, value: str) -> None:
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key: str) -> str:
        return self._store[key.lower()][1]

    def get(self, key: str, default: Any = None) -> Any:
        return self._store[key.lower()][1] if key.lower() in self._store else default

    def __contains__(self, key: str) -> bool:
        return key.lower() in self._store

    def items(self) -> Iterator[Tuple[str, str]]:
        return ((orig_k, v) for orig_k, v in self._store.values())''',
        "category": category
    })

    # 21. JSON-RPC 2.0 Request Dispatcher
    tasks.append({
        "instruction": "Implement a JSON-RPC 2.0 request parser and method dispatcher handling calls and error responses.",
        "output": '''from typing import Any, Callable, Dict

class JsonRpcDispatcher:
    """Dispatches JSON-RPC 2.0 request payloads to registered functions."""
    def __init__(self):
        self.methods: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        self.methods[name] = func

    def handle_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        req_id = payload.get("id")
        method_name = payload.get("method")
        params = payload.get("params", {})

        if payload.get("jsonrpc") != "2.0" or not method_name:
            return {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": req_id}
        if method_name not in self.methods:
            return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": req_id}

        try:
            if isinstance(params, dict):
                result = self.methods[method_name](**params)
            elif isinstance(params, list):
                result = self.methods[method_name](*params)
            else:
                result = self.methods[method_name]()
            return {"jsonrpc": "2.0", "result": result, "id": req_id}
        except Exception as e:
            return {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": req_id}''',
        "category": category
    })

    # 22. Prometheus Metric Exporter Formatter
    tasks.append({
        "instruction": "Formulate a Prometheus exposition format serializer for counters, gauges, and labeled metric series.",
        "output": '''from typing import Dict, List

def format_prometheus_metrics(metrics: List[Dict[str, Any]]) -> str:
    """Format metric records into Prometheus text exposition format."""
    lines = []
    for m in metrics:
        name = m["name"]
        help_text = m.get("help", "")
        m_type = m.get("type", "gauge")
        labels = m.get("labels", {})
        value = m["value"]

        if help_text:
            lines.append(f"# HELP {name} {help_text}")
        lines.append(f"# TYPE {name} {m_type}")

        if labels:
            label_str = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
            lines.append(f"{name}{{{label_str}}} {value}")
        else:
            lines.append(f"{name} {value}")
    return "\\n".join(lines) + "\\n"''',
        "category": category
    })

    # 23. HTTP Range Request Byte Slicer
    tasks.append({
        "instruction": "Construct a function to parse HTTP Range headers (e.g. 'bytes=0-499') and return sliced byte content.",
        "output": '''from typing import Optional, Tuple

def parse_http_byte_range(range_header: str, total_length: int) -> Optional[Tuple[int, int, int]]:
    """Parse 'bytes=start-end' header into (start, end, chunk_length)."""
    if not range_header or not range_header.startswith("bytes="):
        return None
    val = range_header[6:].strip()
    try:
        start_str, end_str = val.split("-", 1)
        if start_str and end_str:
            start = int(start_str)
            end = min(int(end_str), total_length - 1)
        elif start_str:
            start = int(start_str)
            end = total_length - 1
        elif end_str:
            suffix_len = int(end_str)
            start = max(0, total_length - suffix_len)
            end = total_length - 1
        else:
            return None
        if start > end or start >= total_length:
            return None
        return start, end, end - start + 1
    except Exception:
        return None''',
        "category": category
    })

    # 24. CIDR IP Allowlist Matcher
    tasks.append({
        "instruction": "Build an IPv4 CIDR matching utility in Python to verify if an IP address belongs to allowed CIDR subnets.",
        "output": '''import struct
import socket

def ip_to_int(ip: str) -> int:
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def is_ip_in_cidr(ip: str, cidr: str) -> bool:
    """Check if IPv4 address falls within CIDR network range (e.g. '192.168.1.0/24')."""
    network, prefix_len_str = cidr.split("/")
    prefix_len = int(prefix_len_str)
    mask = (0xFFFFFFFF << (32 - prefix_len)) & 0xFFFFFFFF
    return (ip_to_int(ip) & mask) == (ip_to_int(network) & mask)''',
        "category": category
    })

    # 25. REST Filter Parameter Parser
    tasks.append({
        "instruction": "Write a parser for nested REST query filters (e.g. 'filter[status]=active&filter[age][gte]=18').",
        "output": '''import re
from typing import Dict, Any

def parse_rest_filters(query_dict: Dict[str, str]) -> Dict[str, Any]:
    """Parse nested filter parameters from query key-values."""
    filters: Dict[str, Any] = {}
    for key, val in query_dict.items():
        match = re.match(r"^filter\[(\w+)\](?:\[(\w+)\])?$", key)
        if match:
            field, op = match.groups()
            if op:
                filters.setdefault(field, {})[op] = val
            else:
                filters[field] = val
    return filters''',
        "category": category
    })

    # 26. REST Sort Parameter Parser
    tasks.append({
        "instruction": "Create a parser for REST API sort parameters (e.g. 'sort=-created_at,name') into field order tuples.",
        "output": '''from typing import List, Tuple

def parse_sort_param(sort_str: str) -> List[Tuple[str, str]]:
    """Parse 'sort=-created_at,name' into [('created_at', 'desc'), ('name', 'asc')]."""
    if not sort_str:
        return []
    result = []
    for field in sort_str.split(","):
        field = field.strip()
        if not field:
            continue
        if field.startswith("-"):
            result.append((field[1:], "desc"))
        elif field.startswith("+"):
            result.append((field[1:], "asc"))
        else:
            result.append((field, "asc"))
    return result''',
        "category": category
    })

    # 27. Idempotency Key Cache
    tasks.append({
        "instruction": "Design an in-memory Idempotency Key store with TTL to prevent duplicate API transaction execution.",
        "output": '''import time
from typing import Any, Dict, Optional, Tuple

class IdempotencyStore:
    """Stores API response payloads keyed by idempotency tokens."""
    def __init__(self, ttl_seconds: float = 3600.0):
        self.ttl = ttl_seconds
        self.store: Dict[str, Tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self.store:
            return None
        res, expire_at = self.store[key]
        if time.time() > expire_at:
            del self.store[key]
            return None
        return res

    def set(self, key: str, response: Any) -> None:
        self.store[key] = (response, time.time() + self.ttl)''',
        "category": category
    })

    # 28. API Response Envelope
    tasks.append({
        "instruction": "Formulate a standard API response envelope wrapper enclosing data, errors, and execution metadata.",
        "output": '''import time
from typing import Any, Dict, Optional

def wrap_api_envelope(
    data: Optional[Any] = None,
    error: Optional[Dict[str, Any]] = None,
    meta: Optional[Dict[str, Any]] = None,
    status: str = "success"
) -> Dict[str, Any]:
    """Wrap API payload in consistent JSON response structure."""
    envelope = {
        "status": status,
        "timestamp": int(time.time()),
        "data": data,
        "error": error,
        "meta": meta or {}
    }
    return envelope''',
        "category": category
    })

    # 29. Webhook Exponential Backoff Scheduler
    tasks.append({
        "instruction": "Engineer a webhook retry calculator that returns backoff delay with jitter for a given retry attempt.",
        "output": '''import random

def calculate_webhook_backoff(attempt: int, base_delay: float = 1.0, max_delay: float = 60.0) -> float:
    """Calculate exponential backoff delay with full jitter for attempt (1-based)."""
    backoff = min(max_delay, base_delay * (2 ** (attempt - 1)))
    jitter = random.uniform(0, backoff)
    return float(jitter)''',
        "category": category
    })

    # 30. Canonical URL Builder
    tasks.append({
        "instruction": "Build a URL canonicalizer function that sorts query parameters, lowercases domain, and removes default ports.",
        "output": '''import urllib.parse

def canonicalize_url(url: str) -> str:
    """Normalize URL by sorting queries, removing default ports, and lowercasing host."""
    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    if (scheme == "http" and netloc.endswith(":80")) or (scheme == "https" and netloc.endswith(":443")):
        netloc = netloc.rsplit(":", 1)[0]
        
    query_params = urllib.parse.parse_qsl(parsed.query)
    sorted_query = urllib.parse.urlencode(sorted(query_params))
    
    path = parsed.path or "/"
    return urllib.parse.urlunparse((scheme, netloc, path, "", sorted_query, ""))''',
        "category": category
    })

    # 31. HTTP Cache-Control Directive Parser
    tasks.append({
        "instruction": "Develop a parser for Cache-Control headers extracting directives like max-age, no-cache, and must-revalidate.",
        "output": '''from typing import Dict, Union

def parse_cache_control(header_val: str) -> Dict[str, Union[bool, int]]:
    """Parse Cache-Control header string into structured directives dict."""
    directives: Dict[str, Union[bool, int]] = {}
    if not header_val:
        return directives
    for part in header_val.split(","):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            k = k.strip().lower()
            try:
                directives[k] = int(v.strip())
            except ValueError:
                directives[k] = v.strip().strip('"')  # type: ignore
        else:
            directives[part.lower()] = True
    return directives''',
        "category": category
    })

    # 32. Health Check Subsystem Aggregator
    tasks.append({
        "instruction": "Create a health check endpoint aggregator evaluating database, cache, and queue readiness probes.",
        "output": '''from typing import Callable, Dict, Tuple

def evaluate_health_probes(probes: Dict[str, Callable[[], bool]]) -> Tuple[int, Dict[str, Any]]:
    """Execute subsystem health probes and return (http_status, report)."""
    results = {}
    all_healthy = True
    for name, probe_func in probes.items():
        try:
            is_ok = bool(probe_func())
            results[name] = "UP" if is_ok else "DOWN"
            if not is_ok:
                all_healthy = False
        except Exception as e:
            results[name] = f"DOWN: {str(e)}"
            all_healthy = False
            
    status_code = 200 if all_healthy else 503
    return status_code, {"status": "UP" if all_healthy else "DOWN", "checks": results}''',
        "category": category
    })

    # 33. Leaky Bucket Rate Limiter
    tasks.append({
        "instruction": "Implement a Leaky Bucket rate limiter that leaks requests at a steady rate per second.",
        "output": '''import time

class LeakyBucketRateLimiter:
    """Leaky bucket rate limiter processing requests at constant drain rate."""
    def __init__(self, capacity: int, leak_rate_per_sec: float):
        self.capacity = capacity
        self.leak_rate = leak_rate_per_sec
        self.water = 0.0
        self.last_leak_time = time.time()

    def allow(self) -> bool:
        now = time.time()
        elapsed = now - self.last_leak_time
        self.water = max(0.0, self.water - elapsed * self.leak_rate)
        self.last_leak_time = now
        
        if self.water + 1.0 <= self.capacity:
            self.water += 1.0
            return True
        return False''',
        "category": category
    })

    # 34. RFC 5988 Web Linking Parser
    tasks.append({
        "instruction": "Construct a parser for HTTP Link headers (RFC 5988) extracting relations ('next', 'prev', 'last') and URLs.",
        "output": '''import re
from typing import Dict

def parse_link_header(header_val: str) -> Dict[str, str]:
    """Parse RFC 5988 Link header into mapping of rel -> URL."""
    links = {}
    if not header_val:
        return links
    entries = header_val.split(",")
    for entry in entries:
        match = re.search(r'<([^>]+)>;\s*rel="?([^";]+)"?', entry.strip())
        if match:
            url, rel = match.groups()
            links[rel.strip()] = url.strip()
    return links''',
        "category": category
    })

    # 35. Role-Based Access Control (RBAC) Checker
    tasks.append({
        "instruction": "Design an RBAC permission evaluator matching user role permissions against required endpoint access scopes.",
        "output": '''from typing import Dict, List, Set

class RBACChecker:
    """Evaluates role-based permission sets for API security."""
    def __init__(self, role_permissions: Dict[str, List[str]]):
        self.roles = {r: set(perms) for r, perms in role_permissions.items()}

    def has_permission(self, user_roles: List[str], required_scope: str) -> bool:
        user_perms: Set[str] = set()
        for r in user_roles:
            user_perms |= self.roles.get(r, set())
        if "*" in user_perms or required_scope in user_perms:
            return True
        # Check wildcard prefixes e.g. "users:*"
        scope_prefix = required_scope.split(":")[0] + ":*"
        return scope_prefix in user_perms''',
        "category": category
    })

    # 36. User-Agent Classifier
    tasks.append({
        "instruction": "Write a lightweight User-Agent classifier categorizing clients as Mobile, Tablet, Desktop, or Bot.",
        "output": '''import re

def classify_user_agent(ua_string: str) -> str:
    """Classify User-Agent header into client category."""
    if not ua_string:
        return "Unknown"
    ua = ua_string.lower()
    if re.search(r"(bot|crawl|spider|slurp|curl|wget)", ua):
        return "Bot"
    if re.search(r"(ipad|tablet|playbook|silk)", ua):
        return "Tablet"
    if re.search(r"(mobi|iphone|android|phone|ipod)", ua):
        return "Mobile"
    return "Desktop"''',
        "category": category
    })

    # 37. API Version Negotiator
    tasks.append({
        "instruction": "Formulate an API version extractor checking URL path prefix, query parameter, and custom Accept headers.",
        "output": '''import re
from typing import Dict, Optional

def extract_api_version(path: str, query_params: Dict[str, str], headers: Dict[str, str]) -> str:
    """Determine requested API version with fallback to v1."""
    # 1. Check path prefix /v2/...
    path_match = re.match(r"^/(v\d+)/", path)
    if path_match:
        return path_match.group(1)
    # 2. Check query param ?version=v2
    if "version" in query_params:
        return query_params["version"]
    # 3. Check Accept header: application/vnd.app.v2+json
    accept = headers.get("Accept", headers.get("accept", ""))
    accept_match = re.search(r"application/vnd\.[a-z0-9_]+\.(v\d+)\+json", accept)
    if accept_match:
        return accept_match.group(1)
    return "v1"''',
        "category": category
    })

    # 38. Signed Request URL Generator
    tasks.append({
        "instruction": "Build a signed URL generator creating temporary authenticated URLs with HMAC-SHA256 and expiration.",
        "output": '''import hmac
import hashlib
import time
import urllib.parse

def generate_signed_url(base_url: str, secret_key: str, expires_in_sec: int = 3600) -> str:
    """Generate temporary signed URL with expiration timestamp and HMAC signature."""
    expire_at = int(time.time()) + expires_in_sec
    parsed = urllib.parse.urlparse(base_url)
    to_sign = f"{parsed.path}?expires={expire_at}".encode("utf-8")
    sig = hmac.new(secret_key.encode("utf-8"), to_sign, hashlib.sha256).hexdigest()
    
    sep = "&" if parsed.query else "?"
    return f"{base_url}{sep}expires={expire_at}&signature={sig}"''',
        "category": category
    })

    # 39. JSON Schema Lightweight Validator
    tasks.append({
        "instruction": "Construct a simple schema validator verifying required keys and primitive types in JSON dictionaries.",
        "output": '''from typing import Any, Dict, List, Tuple

def validate_json_schema(payload: Dict[str, Any], schema: Dict[str, type], required_keys: List[str]) -> Tuple[bool, List[str]]:
    """Validate that payload contains required fields and correct Python types."""
    errors = []
    for k in required_keys:
        if k not in payload:
            errors.append(f"Missing required field: '{k}'")
    for k, expected_type in schema.items():
        if k in payload and not isinstance(payload[k], expected_type):
            errors.append(f"Field '{k}' must be {expected_type.__name__}, got {type(payload[k]).__name__}")
    return len(errors) == 0, errors''',
        "category": category
    })

    # 40. WebSocket Sec-WebSocket-Accept Calculator
    tasks.append({
        "instruction": "Implement the RFC 6455 WebSocket handshake accept key generator computing SHA1 over client key and GUID.",
        "output": '''import base64
import hashlib

def calculate_sec_websocket_accept(sec_websocket_key: str) -> str:
    """Compute Sec-WebSocket-Accept response header value using RFC 6455 GUID."""
    guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    accept_src = (sec_websocket_key.strip() + guid).encode("utf-8")
    digest = hashlib.sha1(accept_src).digest()
    return base64.b64encode(digest).decode("utf-8")''',
        "category": category
    })

    # 41. Content-Disposition Header Builder
    tasks.append({
        "instruction": "Create a Content-Disposition header builder formatting inline vs attachment modes with escaped filenames.",
        "output": '''import urllib.parse

def build_content_disposition(filename: str, disposition_type: str = "attachment") -> str:
    """Build RFC 6266 Content-Disposition header with UTF-8 filename* encoding."""
    encoded_fn = urllib.parse.quote(filename)
    clean_ascii = "".join(c for c in filename if c.isascii() and c not in ('"', "\\\\"))
    return f'{disposition_type}; filename="{clean_ascii}"; filename*=UTF-8\\'\\'{encoded_fn}\'''',
        "category": category
    })

    # 42. HTTP Retry-After Header Parser
    tasks.append({
        "instruction": "Develop a parser for Retry-After HTTP headers supporting integer seconds and HTTP-date strings.",
        "output": '''import email.utils
import time
from typing import Optional

def parse_retry_after(header_val: str) -> Optional[int]:
    """Parse Retry-After header into delay in seconds."""
    if not header_val:
        return None
    try:
        return int(header_val.strip())
    except ValueError:
        try:
            parsed_time = email.utils.parsedate_to_datetime(header_val)
            delay = int(parsed_time.timestamp() - time.time())
            return max(0, delay)
        except Exception:
            return None''',
        "category": category
    })

    # 43. Content-Security-Policy (CSP) Builder
    tasks.append({
        "instruction": "Design a CSP header generator compiling directive dictionaries into formatted policy strings.",
        "output": '''from typing import Dict, List

def build_csp_header(directives: Dict[str, List[str]]) -> str:
    """Assemble dictionary of directives into a standard CSP string."""
    parts = []
    for directive, sources in sorted(directives.items()):
        source_str = " ".join(sources)
        parts.append(f"{directive} {source_str}")
    return "; ".join(parts)''',
        "category": category
    })

    # 44. URL Hostname & Subdomain Extractor
    tasks.append({
        "instruction": "Write a URL helper that extracts protocol, subdomain, domain, and top-level domain from web addresses.",
        "output": '''import urllib.parse
from typing import Dict

def extract_domain_components(url: str) -> Dict[str, str]:
    """Parse URL into scheme, full_host, subdomain, and root domain."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.split(":")[0].lower()
    parts = host.split(".")
    
    if len(parts) >= 3:
        subdomain = ".".join(parts[:-2])
        domain = f"{parts[-2]}.{parts[-1]}"
    else:
        subdomain = ""
        domain = host
        
    return {
        "scheme": parsed.scheme,
        "host": host,
        "subdomain": subdomain,
        "domain": domain
    }''',
        "category": category
    })

    # 45. HTTP Accept-Language Header Parser
    tasks.append({
        "instruction": "Formulate an Accept-Language header parser sorting requested languages by quality value 'q' descending.",
        "output": '''from typing import List, Tuple

def parse_accept_language(header: str) -> List[Tuple[str, float]]:
    """Parse Accept-Language header into sorted list of (lang_code, quality)."""
    if not header:
        return []
    languages = []
    for item in header.split(","):
        parts = [p.strip() for p in item.split(";")]
        lang = parts[0]
        q = 1.0
        for p in parts[1:]:
            if p.startswith("q="):
                try:
                    q = float(p[2:])
                except ValueError:
                    q = 1.0
        languages.append((lang, q))
    return sorted(languages, key=lambda x: x[1], reverse=True)''',
        "category": category
    })

    # 46. Session Cookie Signer & Verifier
    tasks.append({
        "instruction": "Implement a tamper-proof session cookie signer that attaches an HMAC-SHA256 signature to raw session data.",
        "output": '''import base64
import hmac
import hashlib
from typing import Optional

def sign_session_data(data: str, secret_key: str) -> str:
    """Sign cookie string with HMAC-SHA256."""
    data_b64 = base64.urlsafe_b64encode(data.encode("utf-8")).decode("utf-8")
    sig = hmac.new(secret_key.encode("utf-8"), data_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{data_b64}.{sig}"

def verify_session_data(signed_cookie: str, secret_key: str) -> Optional[str]:
    """Verify signature and return decoded session string or None."""
    try:
        data_b64, sig = signed_cookie.split(".", 1)
        expected_sig = hmac.new(secret_key.encode("utf-8"), data_b64.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        return base64.urlsafe_b64decode(data_b64.encode("utf-8")).decode("utf-8")
    except Exception:
        return None''',
        "category": category
    })

    # 47. HTTP Method Override Handler
    tasks.append({
        "instruction": "Construct an HTTP request method resolver supporting X-HTTP-Method-Override headers and _method queries.",
        "output": '''from typing import Dict

def resolve_http_method(raw_method: str, headers: Dict[str, str], query_params: Dict[str, str]) -> str:
    """Resolve effective HTTP method considering overrides for POST requests."""
    method = raw_method.upper()
    if method == "POST":
        override = headers.get("X-HTTP-Method-Override", headers.get("x-http-method-override"))
        if override:
            return override.upper()
        if "_method" in query_params:
            return query_params["_method"].upper()
    return method''',
        "category": category
    })

    # 48. Multipart Form Data Header Extractor
    tasks.append({
        "instruction": "Build a parser extracting the boundary string from a multipart/form-data Content-Type header.",
        "output": '''import re
from typing import Optional

def extract_multipart_boundary(content_type_header: str) -> Optional[str]:
    """Extract boundary token from multipart/form-data header."""
    if not content_type_header:
        return None
    match = re.search(r'boundary=([^;]+)', content_type_header, re.IGNORECASE)
    if match:
        return match.group(1).strip().strip('"')
    return None''',
        "category": category
    })

    # 49. URL Template Variable Replacer
    tasks.append({
        "instruction": "Create a URI Template variable substitution function replacing {var} placeholders with URL-encoded values.",
        "output": '''import re
import urllib.parse
from typing import Dict, Any

def expand_uri_template(template: str, variables: Dict[str, Any]) -> str:
    """Expand URI template {variable} slots with percent-encoded values."""
    def replacer(match: re.Match) -> str:
        var_name = match.group(1)
        val = variables.get(var_name, "")
        return urllib.parse.quote(str(val), safe="")
    return re.sub(r"\{([a-zA-Z0-9_]+)\}", replacer, template)''',
        "category": category
    })

    # 50. API Batch Request Splitter
    tasks.append({
        "instruction": "Develop a batch request aggregator that accepts an array of sub-requests and packages their responses.",
        "output": '''from typing import Any, Callable, Dict, List

def process_batch_requests(requests: List[Dict[str, Any]], dispatcher: Callable[[str, Dict], Any]) -> List[Dict[str, Any]]:
    """Process an array of sub-requests and collect individual response outcomes."""
    responses = []
    for req in requests:
        req_id = req.get("id")
        action = req.get("action", "")
        params = req.get("params", {})
        try:
            res_data = dispatcher(action, params)
            responses.append({"id": req_id, "status": 200, "body": res_data})
        except Exception as err:
            responses.append({"id": req_id, "status": 400, "error": str(err)})
    return responses''',
        "category": category
    })

    # 51. HTTP Status Code Mapper
    tasks.append({
        "instruction": "Formulate a status code classifier mapping numeric HTTP codes to categories (Informational, Success, Redirect, Client Error, Server Error).",
        "output": '''def classify_http_status_code(code: int) -> str:
    """Categorize HTTP status code into standard category description."""
    if 100 <= code <= 199: return "Informational"
    if 200 <= code <= 299: return "Success"
    if 300 <= code <= 399: return "Redirection"
    if 400 <= code <= 499: return "Client Error"
    if 500 <= code <= 599: return "Server Error"
    return "Unknown"''',
        "category": category
    })

    # 52. Content-Range Header Builder
    tasks.append({
        "instruction": "Design a Content-Range header formatter for partial content 206 responses (e.g. 'bytes 0-499/1234').",
        "output": '''def format_content_range(start: int, end: int, total: int) -> str:
    """Format RFC 7233 Content-Range header value."""
    total_str = str(total) if total >= 0 else "*"
    return f"bytes {start}-{end}/{total_str}"''',
        "category": category
    })

    # 53. Request Signature Builder
    tasks.append({
        "instruction": "Write an HMAC request signer concatenating HTTP method, path, timestamp, and body digest.",
        "output": '''import hmac
import hashlib

def create_request_signature(method: str, path: str, timestamp: int, body: bytes, secret_key: str) -> str:
    """Create cryptographic signature string for API request."""
    body_hash = hashlib.sha256(body).hexdigest()
    canonical_string = f"{method.upper()}\\n{path}\\n{timestamp}\\n{body_hash}"
    return hmac.new(secret_key.encode("utf-8"), canonical_string.encode("utf-8"), hashlib.sha256).hexdigest()''',
        "category": category
    })

    # 54. GraphQL Simple Query Field Extractor
    tasks.append({
        "instruction": "Build a simple regex-based field extractor retrieving top-level requested fields from a GraphQL query string.",
        "output": '''import re
from typing import List

def extract_graphql_fields(query: str) -> List[str]:
    """Extract top-level selected field names from a basic GraphQL query body."""
    # Strip operation definition
    match = re.search(r"\{([^{}]+)\}", query)
    if not match:
        return []
    inner = match.group(1)
    tokens = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", inner)
    return tokens''',
        "category": category
    })

    # 55. Digest Auth Challenge Generator
    tasks.append({
        "instruction": "Construct an HTTP Digest Authentication WWW-Authenticate challenge header formatter.",
        "output": '''import secrets

def generate_digest_challenge(realm: str, opaque: str = "") -> str:
    """Generate RFC 7616 Digest WWW-Authenticate challenge header."""
    nonce = secrets.token_hex(16)
    parts = [
        f'Digest realm="{realm}"',
        f'qop="auth"',
        f'nonce="{nonce}"',
        'algorithm=MD5'
    ]
    if opaque:
        parts.append(f'opaque="{opaque}"')
    return ", ".join(parts)''',
        "category": category
    })

    # 56. OpenID Connect Nonce & State Generator
    tasks.append({
        "instruction": "Create an OAuth2 / OIDC state and nonce parameter generator for CSRF prevention in authorization flows.",
        "output": '''import secrets
from typing import Dict

def generate_oauth2_state_nonce() -> Dict[str, str]:
    """Generate secure cryptographically random state and nonce tokens."""
    return {
        "state": secrets.token_urlsafe(24),
        "nonce": secrets.token_urlsafe(24)
    }''',
        "category": category
    })

    # 57. Content-Encoding Gzip Handler
    tasks.append({
        "instruction": "Implement a helper that inspects the Accept-Encoding header and chooses the optimal compression algorithm.",
        "output": '''from typing import List

def select_content_encoding(accept_encoding_header: str, supported: List[str] = ["gzip", "deflate"]) -> str:
    """Select best supported content encoding from Accept-Encoding header."""
    if not accept_encoding_header:
        return "identity"
    client_encodings = [e.split(";")[0].strip().lower() for e in accept_encoding_header.split(",")]
    for enc in supported:
        if enc in client_encodings:
            return enc
    return "identity"''',
        "category": category
    })

    # 58. HTTP Cookie Jar Parser
    tasks.append({
        "instruction": "Develop a parser that extracts all cookies from an HTTP Cookie request header into a key-value dictionary.",
        "output": '''from typing import Dict

def parse_cookie_header(cookie_header: str) -> Dict[str, str]:
    """Parse HTTP Cookie header string into dictionary of cookie names and values."""
    cookies = {}
    if not cookie_header:
        return cookies
    for part in cookie_header.split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            cookies[k.strip()] = v.strip().strip('"')
    return cookies''',
        "category": category
    })

    # 59. Webhook Secret Key Rotator
    tasks.append({
        "instruction": "Formulate a dual-key webhook signature validator that accepts signatures matching either primary or fallback keys.",
        "output": '''import hmac
import hashlib

def verify_dual_key_signature(payload: bytes, signature: str, primary_key: str, fallback_key: str) -> bool:
    """Verify webhook signature against primary key or secondary rollover key."""
    def compute(key: str) -> str:
        return hmac.new(key.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    sig1 = compute(primary_key)
    sig2 = compute(fallback_key)
    return hmac.compare_digest(signature, sig1) or hmac.compare_digest(signature, sig2)''',
        "category": category
    })

    # 60. Proxy Authorization Header Decoder
    tasks.append({
        "instruction": "Build a decoder for Proxy-Authorization headers retrieving credentials for downstream proxy forwarding.",
        "output": '''import base64
from typing import Optional, Tuple

def decode_proxy_auth(header_value: str) -> Optional[Tuple[str, str]]:
    """Decode Proxy-Authorization Basic header into (username, password)."""
    if not header_value or not header_value.startswith("Basic "):
        return None
    try:
        raw = base64.b64decode(header_value[6:].strip()).decode("utf-8")
        if ":" in raw:
            user, pwd = raw.split(":", 1)
            return user, pwd
        return None
    except Exception:
        return None''',
        "category": category
    })

    return tasks
