"""
Domain 8: String Manipulation & Regex (60 tasks)
Category: String Manipulation & Regex
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "String Manipulation & Regex"

    # 1. Math Expression Tokenizer
    tasks.append({
        "instruction": "Implement a lexical tokenizer for mathematical expressions identifying numbers, operators (+, -, *, /, ^), and parentheses.",
        "output": '''import re
from typing import List, Tuple

def tokenize_math_expression(expr: str) -> List[Tuple[str, str]]:
    """Tokenize mathematical expression into (TOKEN_TYPE, VALUE) tuples."""
    token_spec = [
        ("NUMBER", r"\d+(?:\.\d+)?"),
        ("OP", r"[+\-*/^]"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("SKIP", r"\s+"),
        ("MISMATCH", r".")
    ]
    master_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
    tokens = []
    for mo in re.finditer(master_regex, expr):
        kind = mo.lastgroup
        val = mo.group()
        if kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character: {val!r}")
        tokens.append((kind, val))
    return tokens''',
        "category": category
    })

    # 2. JSON Lexical Tokenizer
    tasks.append({
        "instruction": "Design a lexical scanner for JSON grammar recognizing strings, numbers, booleans, null, and punctuation.",
        "output": '''import re
from typing import List, Tuple

def tokenize_json(json_str: str) -> List[Tuple[str, str]]:
    """Scan raw JSON text into lexical tokens."""
    token_spec = [
        ("STRING", r'"(?:\\.|[^"\\])*"'),
        ("NUMBER", r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?'),
        ("BOOLEAN", r'\b(?:true|false)\b'),
        ("NULL", r'\bnull\b'),
        ("PUNCT", r'[{}\[\],:]'),
        ("SKIP", r'\s+')
    ]
    master = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
    tokens = []
    for mo in re.finditer(master, json_str):
        kind = mo.lastgroup
        val = mo.group()
        if kind != "SKIP":
            tokens.append((kind, val))
    return tokens''',
        "category": category
    })

    # 3. Levenshtein Distance with Backtrace Alignment
    tasks.append({
        "instruction": "Construct a Levenshtein edit distance calculator that outputs the full alignment backtrace path (match, insert, delete, replace).",
        "output": '''from typing import List, Tuple

def levenshtein_alignment(s1: str, s2: str) -> Tuple[int, List[Tuple[str, str, str]]]:
    """Calculate Levenshtein distance and return (distance, alignment_operations)."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
            
    # Backtrace
    i, j = m, n
    ops = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            ops.append(("MATCH", s1[i - 1], s2[j - 1]))
            i -= 1; j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(("REPLACE", s1[i - 1], s2[j - 1]))
            i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("DELETE", s1[i - 1], "-"))
            i -= 1
        else:
            ops.append(("INSERT", "-", s2[j - 1]))
            j -= 1
            
    return dp[m][n], ops[::-1]''',
        "category": category
    })

    # 4. Damerau-Levenshtein Distance
    tasks.append({
        "instruction": "Build the Damerau-Levenshtein distance algorithm accounting for insertions, deletions, substitutions, and adjacent transpositions.",
        "output": '''def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """Compute Damerau-Levenshtein distance including adjacent character swaps."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + cost)
                
    return dp[m][n]''',
        "category": category
    })

    # 5. Jaro & Jaro-Winkler Similarity
    tasks.append({
        "instruction": "Create a Jaro-Winkler string similarity calculator returning a float score in [0.0, 1.0].",
        "output": '''def jaro_winkler_similarity(s1: str, s2: str, p: float = 0.1) -> float:
    """Calculate Jaro-Winkler string similarity score."""
    if s1 == s2: return 1.0
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0: return 0.0

    match_distance = max(len1, len2) // 2 - 1
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    matches = 0

    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]: continue
            s1_matches[i] = s2_matches[j] = True
            matches += 1
            break

    if matches == 0: return 0.0

    k = transpositions = 0
    for i in range(len1):
        if not s1_matches[i]: continue
        while not s2_matches[k]: k += 1
        if s1[i] != s2[k]: transpositions += 1
        k += 1

    jaro = (matches / len1 + matches / len2 + (matches - transpositions / 2.0) / matches) / 3.0
    prefix_len = 0
    for i in range(min(4, min(len1, len2))):
        if s1[i] == s2[i]: prefix_len += 1
        else: break
    return jaro + prefix_len * p * (1.0 - jaro)''',
        "category": category
    })

    # 6. Soundex Phonetic Encoder
    tasks.append({
        "instruction": "Write the Soundex phonetic algorithm encoding names into standard 4-character codes (e.g. 'R163').",
        "output": '''def soundex_encode(name: str) -> str:
    """Encode English word into Soundex phonetic 4-character code."""
    name = "".join(c.upper() for c in name if c.isalpha())
    if not name: return ""
    mapping = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    first_letter = name[0]
    codes = [mapping.get(c, "") for c in name]
    
    # Deduplicate adjacent duplicate digits
    filtered = []
    prev = ""
    for c in codes:
        if c != prev and c != "":
            filtered.append(c)
        prev = c
        
    if name[0] in mapping and filtered and filtered[0] == mapping[name[0]]:
        filtered = filtered[1:]
    res = first_letter + "".join(filtered)
    return (res + "000")[:4]''',
        "category": category
    })

    # 7. Recursive Regex Matcher (. and *)
    tasks.append({
        "instruction": "Formulate a recursive pattern matching engine supporting '.' (single character) and '*' (zero or more) wildcards.",
        "output": '''def is_regex_match(text: str, pattern: str) -> bool:
    """Evaluate if text matches pattern with '.' and '*' operators."""
    if not pattern:
        return not text
    first_match = bool(text) and pattern[0] in (text[0], ".")
    if len(pattern) >= 2 and pattern[1] == "*":
        return is_regex_match(text, pattern[2:]) or (first_match and is_regex_match(text[1:], pattern))
    else:
        return first_match and is_regex_match(text[1:], pattern[1:])''',
        "category": category
    })

    # 8. Semantic Version (SemVer 2.0.0) Regex Validator
    tasks.append({
        "instruction": "Develop a Semantic Versioning validator and parser extracting major, minor, patch, prerelease, and build metadata.",
        "output": '''import re
from typing import Dict, Optional

def parse_semver_string(version_str: str) -> Optional[Dict[str, str]]:
    """Parse SemVer 2.0.0 string into structured version fields."""
    pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    match = re.match(pattern, version_str.strip())
    if not match:
        return None
    major, minor, patch, pre, build = match.groups()
    return {
        "major": int(major),
        "minor": int(minor),
        "patch": int(patch),
        "prerelease": pre or "",
        "build": build or ""
    }''',
        "category": category
    })

    # 9. Markdown Link Extractor
    tasks.append({
        "instruction": "Implement a regex extractor retrieving all Markdown links ([anchor text](target_url)) from document text.",
        "output": '''import re
from typing import List, Tuple

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """Extract all (anchor_text, url) pairs from markdown text."""
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)''',
        "category": category
    })

    # 10. Snake, Camel, and Pascal Case Converters
    tasks.append({
        "instruction": "Build identifier case conversion functions converting snake_case strings to camelCase and PascalCase.",
        "output": '''def snake_to_camel_case(s: str) -> str:
    """Convert snake_case string to lowerCamelCase."""
    parts = s.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:]) if parts else ""

def snake_to_pascal_case(s: str) -> str:
    """Convert snake_case string to PascalCase."""
    return "".join(w.capitalize() for w in s.split("_") if w)''',
        "category": category
    })

    # 11. CamelCase to Snake and Kebab Case
    tasks.append({
        "instruction": "Construct conversion functions that transform CamelCase identifiers into snake_case and kebab-case.",
        "output": '''import re

def camel_to_snake_case(s: str) -> str:
    """Convert CamelCase string to snake_case."""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()

def camel_to_kebab_case(s: str) -> str:
    """Convert CamelCase string to kebab-case."""
    return camel_to_snake_case(s).replace("_", "-")''',
        "category": category
    })

    # 12. Chicago Manual Style Title Casing
    tasks.append({
        "instruction": "Write a title case formatter following Chicago style rules (capitalizing words while lowercasing minor words).",
        "output": '''def format_title_case_chicago(title: str) -> str:
    """Capitalize title string according to Chicago manual of style."""
    minor_words = {"a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "by", "in", "of"}
    words = title.split()
    if not words:
        return ""
    result = []
    for i, word in enumerate(words):
        w_lower = word.lower()
        if i == 0 or i == len(words) - 1 or w_lower not in minor_words:
            result.append(word.capitalize())
        else:
            result.append(w_lower)
    return " ".join(result)''',
        "category": category
    })

    # 13. Knuth-Morris-Pratt (KMP) String Search
    tasks.append({
        "instruction": "Implement the Knuth-Morris-Pratt (KMP) pattern searching algorithm using the Longest Prefix Suffix (LPS) table.",
        "output": '''from typing import List

def kmp_string_search(text: str, pattern: str) -> List[int]:
    """Find all 0-based starting indices of pattern in text in O(n + m) time."""
    if not pattern or not text:
        return []
    # Build LPS table
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    matches = []
    t_idx = p_idx = 0
    while t_idx < len(text):
        if text[t_idx] == pattern[p_idx]:
            t_idx += 1; p_idx += 1
        if p_idx == len(pattern):
            matches.append(t_idx - p_idx)
            p_idx = lps[p_idx - 1]
        elif t_idx < len(text) and text[t_idx] != pattern[p_idx]:
            if p_idx != 0: p_idx = lps[p_idx - 1]
            else: t_idx += 1
    return matches''',
        "category": category
    })

    # 14. Rabin-Karp Rolling Hash String Search
    tasks.append({
        "instruction": "Design the Rabin-Karp string matching algorithm with polynomial rolling hash and collision verification.",
        "output": '''from typing import List

def rabin_karp_search(text: str, pattern: str, prime_mod: int = 1000000007, base: int = 256) -> List[int]:
    """Locate pattern occurrences in text using Rabin-Karp rolling hash."""
    n, m = len(text), len(pattern)
    if m == 0 or n < m: return []
    
    h_pattern = 0
    h_window = 0
    high_base = pow(base, m - 1, prime_mod)
    
    for i in range(m):
        h_pattern = (h_pattern * base + ord(pattern[i])) % prime_mod
        h_window = (h_window * base + ord(text[i])) % prime_mod
        
    matches = []
    for i in range(n - m + 1):
        if h_window == h_pattern:
            if text[i: i + m] == pattern:
                matches.append(i)
        if i < n - m:
            h_window = ((h_window - ord(text[i]) * high_base) * base + ord(text[i + m])) % prime_mod
            h_window = (h_window + prime_mod) % prime_mod
    return matches''',
        "category": category
    })

    # 15. Boyer-Moore-Horspool String Matcher
    tasks.append({
        "instruction": "Formulate the Boyer-Moore-Horspool string searching algorithm using a bad-character shift table.",
        "output": '''from typing import List

def boyer_moore_horspool(text: str, pattern: str) -> List[int]:
    """Search for pattern in text using Boyer-Moore-Horspool algorithm."""
    n, m = len(text), len(pattern)
    if m == 0 or n < m: return []
    
    # Bad character shift table
    shift = {chr(c): m for c in range(256)}
    for i in range(m - 1):
        shift[pattern[i]] = m - 1 - i
        
    matches = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            matches.append(i)
        i += shift.get(text[i + m - 1], m)
    return matches''',
        "category": category
    })

    # 16. Manacher's Algorithm for Longest Palindromic Substring
    tasks.append({
        "instruction": "Develop Manacher's linear O(n) algorithm to identify the longest palindromic substring in a string.",
        "output": '''def manachers_longest_palindrome(s: str) -> str:
    """Find the longest palindromic substring in linear O(N) time using Manacher's algorithm."""
    if not s: return ""
    transformed = "#" + "#".join(s) + "#"
    n = len(transformed)
    p = [0] * n
    c = r = 0
    max_len = 0
    center_idx = 0
    
    for i in range(n):
        mirror = 2 * c - i
        if i < r:
            p[i] = min(r - i, p[mirror])
        while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and transformed[i - p[i] - 1] == transformed[i + p[i] + 1]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
        if p[i] > max_len:
            max_len = p[i]
            center_idx = i
            
    start = (center_idx - max_len) // 2
    return s[start: start + max_len]''',
        "category": category
    })

    # 17. Huffman Coding Tree and Compressor
    tasks.append({
        "instruction": "Implement Huffman coding building a frequency tree, generating binary codes, and encoding strings.",
        "output": '''import heapq
from collections import Counter
from typing import Dict, Tuple

class HuffmanNode:
    def __init__(self, char: str = "", freq: int = 0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    def __lt__(self, other): return self.freq < other.freq

def build_huffman_codes(text: str) -> Tuple[Dict[str, str], str]:
    """Generate variable-length prefix codes and encode input text."""
    if not text: return {}, ""
    freqs = Counter(text)
    heap = [HuffmanNode(char=c, freq=f) for c, f in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        parent = HuffmanNode(freq=n1.freq + n2.freq, left=n1, right=n2)
        heapq.heappush(heap, parent)

    codes: Dict[str, str] = {}
    def generate_codes(node, prefix=""):
        if node:
            if not node.left and not node.right:
                codes[node.char] = prefix or "0"
            generate_codes(node.left, prefix + "0")
            generate_codes(node.right, prefix + "1")

    generate_codes(heap[0])
    encoded = "".join(codes[c] for c in text)
    return codes, encoded''',
        "category": category
    })

    # 18. LZW Compression & Decompression
    tasks.append({
        "instruction": "Build Lempel-Ziv-Welch (LZW) string compression and decompression algorithms.",
        "output": '''from typing import List

def lzw_compress(uncompressed: str) -> List[int]:
    """Compress string into integer tokens using LZW algorithm."""
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w: result.append(dictionary[w])
    return result

def lzw_decompress(compressed: List[int]) -> str:
    """Decompress LZW tokens back to original string."""
    if not compressed: return ""
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    w = chr(compressed[0])
    result = [w]
    for k in compressed[1:]:
        if k in dictionary: entry = dictionary[k]
        elif k == dict_size: entry = w + w[0]
        else: raise ValueError("Bad compressed token")
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return "".join(result)''',
        "category": category
    })

    # 19. Pure Python Base64 Encoder / Decoder
    tasks.append({
        "instruction": "Create a Base64 encoder and decoder from scratch using bitwise shifts without the standard base64 library.",
        "output": '''def base64_encode_custom(data: bytes) -> str:
    """Encode bytes into standard RFC 4648 Base64 string."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    result = []
    i = 0
    while i < len(data):
        b1 = data[i]
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        triple = (b1 << 16) | (b2 << 8) | b3
        result.append(chars[(triple >> 18) & 63])
        result.append(chars[(triple >> 12) & 63])
        result.append(chars[(triple >> 6) & 63] if i + 1 < len(data) else "=")
        result.append(chars[triple & 63] if i + 2 < len(data) else "=")
        i += 3
    return "".join(result)''',
        "category": category
    })

    # 20. Base58 Bitcoin Alphabet Encoder
    tasks.append({
        "instruction": "Construct a Base58 encoder and decoder adhering to Bitcoin's non-ambiguous alphanumeric alphabet.",
        "output": '''def base58_encode(data: bytes) -> str:
    """Encode byte array into Bitcoin Base58 string format."""
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    orig_len = len(data)
    num = int.from_bytes(data, byteorder="big")
    res = []
    while num > 0:
        num, rem = divmod(num, 58)
        res.append(alphabet[rem])
    # Handle leading zeros
    leading_zeros = orig_len - len(data.lstrip(bytes([0])))
    return (alphabet[0] * leading_zeros) + "".join(reversed(res))''',
        "category": category
    })

    # 21. Natural Sort Key Generator
    tasks.append({
        "instruction": "Develop a natural sort key function that sorts embedded digits numerically (e.g. 'file2' before 'file10').",
        "output": '''import re
from typing import List, Union

def natural_sort_key(s: str) -> List[Union[int, str]]:
    """Generate sorting key that orders embedded numbers naturally."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]''',
        "category": category
    })

    # 22. ANSI Escape Sequence Stripper
    tasks.append({
        "instruction": "Write a utility function using regular expressions to strip ANSI color escape codes from terminal text.",
        "output": '''import re

def strip_ansi_codes(text: str) -> str:
    """Remove ANSI SGR color escape codes from terminal output."""
    ansi_regex = r"\x1b\[[0-9;]*[a-zA-Z]"
    return re.sub(ansi_regex, "", text)''',
        "category": category
    })

    # 23. Simple String Template Interpolator
    tasks.append({
        "instruction": "Implement a string template interpolator replacing double curly brace variables ({{ key }}) with dictionary values.",
        "output": '''import re
from typing import Any, Dict

def render_template_vars(template: str, context: Dict[str, Any]) -> str:
    """Replace {{ var_name }} placeholders with context values."""
    def replacer(match: re.Match) -> str:
        key = match.group(1).strip()
        return str(context.get(key, ""))
    return re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", replacer, template)''',
        "category": category
    })

    # 24. Word Wrap with Boundary Preservation
    tasks.append({
        "instruction": "Design a word wrap algorithm formatting text into lines of at most max_width characters without breaking words.",
        "output": '''from typing import List

def word_wrap_lines(text: str, max_width: int = 80) -> List[str]:
    """Wrap text into lines without exceeding max_width."""
    words = text.split()
    if not words: return []
    lines = []
    cur_line = [words[0]]
    cur_len = len(words[0])
    
    for w in words[1:]:
        if cur_len + 1 + len(w) <= max_width:
            cur_line.append(w)
            cur_len += 1 + len(w)
        else:
            lines.append(" ".join(cur_line))
            cur_line = [w]
            cur_len = len(w)
            
    if cur_line:
        lines.append(" ".join(cur_line))
    return lines''',
        "category": category
    })

    # 25. HTML Entity Encoder & Decoder
    tasks.append({
        "instruction": "Formulate functions to escape and unescape standard HTML entity characters (&, <, >, \", ').",
        "output": '''import html

def escape_html_chars(text: str) -> str:
    """Escape &, <, >, \", and ' to safe HTML entities."""
    return html.escape(text, quote=True)

def unescape_html_entities(escaped_text: str) -> str:
    """Decode HTML entities back to raw characters."""
    return html.unescape(escaped_text)''',
        "category": category
    })

    # 26. Roman Numeral to Integer Converter
    tasks.append({
        "instruction": "Build a Roman numeral decoder parsing valid Roman numeral strings into integer values.",
        "output": '''def roman_to_integer(s: str) -> int:
    """Convert valid Roman numeral string into decimal integer."""
    mapping = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev = 0
    for char in reversed(s.upper()):
        curr = mapping.get(char, 0)
        if curr < prev:
            total -= curr
        else:
            total += curr
        prev = curr
    return total''',
        "category": category
    })

    # 27. Integer to Roman Numeral Converter
    tasks.append({
        "instruction": "Create an integer to Roman numeral converter formatting integers between 1 and 3999.",
        "output": '''def integer_to_roman(num: int) -> str:
    """Convert integer between 1 and 3999 to Roman numeral string."""
    val_map = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    res = []
    for v, sym in val_map:
        while num >= v:
            res.append(sym)
            num -= v
    return "".join(res)''',
        "category": category
    })

    # 28. Human-Readable Byte Formatter
    tasks.append({
        "instruction": "Construct a byte size formatter converting raw byte counts into human-readable units (B, KB, MB, GB, TB).",
        "output": '''def format_bytes_human(byte_count: float) -> str:
    """Format raw byte count into human-readable string with units."""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = float(byte_count)
    unit_idx = 0
    while size >= 1024.0 and unit_idx < len(units) - 1:
        size /= 1024.0
        unit_idx += 1
    return f"{size:.2f} {units[unit_idx]}" if unit_idx > 0 else f"{int(size)} B"''',
        "category": category
    })

    # 29. NATO Phonetic Alphabet Spelling
    tasks.append({
        "instruction": "Write a utility translating alphanumeric strings into their NATO phonetic alphabet representations.",
        "output": '''from typing import List

def to_nato_phonetic(text: str) -> List[str]:
    """Translate word characters into NATO phonetic codes."""
    nato_table = {
        'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo',
        'F': 'Foxtrot', 'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett',
        'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November', 'O': 'Oscar',
        'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango',
        'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray', 'Y': 'Yankee', 'Z': 'Zulu'
    }
    return [nato_table.get(c.upper(), c) for c in text if c.isalnum()]''',
        "category": category
    })

    # 30. Text Truncater with Ellipsis
    tasks.append({
        "instruction": "Design a text truncation function preserving word boundaries and appending an ellipsis.",
        "output": '''def truncate_text_words(text: str, max_length: int) -> str:
    """Truncate text at word boundary with '...' without exceeding max_length."""
    if len(text) <= max_length:
        return text
    if max_length <= 3:
        return text[:max_length]
    clipped = text[:max_length - 3]
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped + "..."''',
        "category": category
    })

    # 31. Longest Common Substring DP
    tasks.append({
        "instruction": "Formulate a dynamic programming function finding the longest contiguous common substring between two strings.",
        "output": '''def longest_common_substring(s1: str, s2: str) -> str:
    """Find longest contiguous common substring using 2D DP matrix."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_pos = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i
            else:
                dp[i][j] = 0
                
    return s1[end_pos - max_len: end_pos]''',
        "category": category
    })

    # 32. Vigenere Cipher Encoder & Decoder
    tasks.append({
        "instruction": "Develop Vigenere polyalphabetic cipher encryption and decryption functions for alphabetical strings.",
        "output": '''def vigenere_encrypt(text: str, key: str) -> str:
    """Encrypt text with Vigenere cipher using repeating key."""
    res = []
    key_clean = [ord(c.upper()) - ord('A') for c in key if c.isalpha()]
    if not key_clean: return text
    k_len = len(key_clean)
    k_idx = 0
    
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = key_clean[k_idx % k_len]
            res.append(chr((ord(c) - base + shift) % 26 + base))
            k_idx += 1
        else:
            res.append(c)
    return "".join(res)''',
        "category": category
    })

    # 33. Email & Phone Number Obfuscation
    tasks.append({
        "instruction": "Implement an PII obfuscator masking email addresses (j***e@domain.com) and phone numbers (***-***-1234).",
        "output": '''import re

def obfuscate_email(email: str) -> str:
    """Mask username portion of email address preserving domain."""
    if "@" not in email: return email
    user, domain = email.split("@", 1)
    if len(user) <= 2:
        masked_user = user[0] + "*"
    else:
        masked_user = user[0] + "*" * (len(user) - 2) + user[-1]
    return f"{masked_user}@{domain}"''',
        "category": category
    })

    # 34. Run-Length Encoding with Run Limits
    tasks.append({
        "instruction": "Build a Run-Length Encoding (RLE) compressor formatting repeated characters as '<count><char>'.",
        "output": '''def run_length_encode(text: str) -> str:
    """Perform basic Run-Length Encoding on string."""
    if not text: return ""
    encoded = []
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1
        else:
            encoded.append(f"{count}{text[i - 1]}")
            count = 1
    encoded.append(f"{count}{text[-1]}")
    return "".join(encoded)''',
        "category": category
    })

    # 35. Syllable Counter Heuristic
    tasks.append({
        "instruction": "Construct an English word syllable counter using vowel diphthong clustering heuristics.",
        "output": '''import re

def count_syllables_heuristic(word: str) -> int:
    """Estimate syllable count in English word."""
    w = word.lower().strip()
    if not w: return 0
    if len(w) <= 3: return 1
    # Remove silent e at end
    if w.endswith("e") and not w.endswith("le"):
        w = w[:-1]
    vowel_groups = re.findall(r"[aeiouy]+", w)
    return max(1, len(vowel_groups))''',
        "category": category
    })

    # 36. Text Difference Line Formatter
    tasks.append({
        "instruction": "Write a side-by-side or unified diff line formatter comparing two multiline string sequences.",
        "output": r'''import difflib
from typing import List

def generate_unified_diff_lines(lines1: List[str], lines2: List[str], fromfile: str = "a", tofile: str = "b") -> str:
    """Generate unified diff text representation between two line lists."""
    diff = difflib.unified_diff(lines1, lines2, fromfile=fromfile, tofile=tofile, lineterm="")
    return "\n".join(diff)''',
        "category": category
    })

    # 37. Markdown Code Block Extractor
    tasks.append({
        "instruction": "Design a regex parser extracting triple-backtick code blocks and language tags from Markdown documents.",
        "output": r'''import re
from typing import List, Tuple

def extract_markdown_code_blocks(md_text: str) -> List[Tuple[str, str]]:
    """Extract (language, code_content) from Markdown triple-backtick blocks."""
    pattern = r"```([a-zA-Z0-9_\-+]*)\n(.*?)```"
    matches = re.findall(pattern, md_text, re.DOTALL)
    return [(lang.strip(), code.strip()) for lang, code in matches]''',
        "category": category
    })

    # 38. Acronym Generator with Stopwords
    tasks.append({
        "instruction": "Formulate an acronym generator creating capital acronyms from multi-word phrases while skipping stopwords.",
        "output": '''def generate_acronym(phrase: str) -> str:
    """Generate uppercase acronym from phrase skipping common connector words."""
    stopwords = {"and", "of", "the", "in", "for", "to", "a", "an", "with"}
    words = phrase.split()
    letters = [w[0].upper() for w in words if w.lower() not in stopwords and w[0].isalpha()]
    return "".join(letters)''',
        "category": category
    })

    # 39. String Indentation Formatter
    tasks.append({
        "instruction": "Implement an indentation formatter adding or removing fixed space indentation from multiline text blocks.",
        "output": r'''def indent_text_block(text: str, spaces: int = 4) -> str:
    """Add uniform space prefix to all non-empty lines in text."""
    prefix = " " * spaces
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())''',
        "category": category
    })

    # 40. Z-Algorithm for Exact Pattern Matching
    tasks.append({
        "instruction": "Develop the Z-algorithm for linear-time string matching constructing the Z-array.",
        "output": '''from typing import List

def z_algorithm_match(text: str, pattern: str) -> List[int]:
    """Find pattern match indices in text using Z-algorithm in O(N + M)."""
    concat = pattern + "$" + text
    n = len(concat)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and concat[z[i]] == concat[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
            
    matches = []
    p_len = len(pattern)
    for i in range(p_len + 1, n):
        if z[i] == p_len:
            matches.append(i - p_len - 1)
    return matches''',
        "category": category
    })

    # 41. Aho-Corasick Multi-Pattern Trie Skeleton
    tasks.append({
        "instruction": "Build an Aho-Corasick trie data structure for searching multiple keyword patterns in a single pass.",
        "output": '''from collections import deque
from typing import Dict, List, Set, Tuple

class AhoCorasickNode:
    def __init__(self):
        self.children: Dict[str, AhoCorasickNode] = {}
        self.fail: Optional[AhoCorasickNode] = None
        self.output: Set[str] = set()

def build_aho_corasick_automaton(keywords: List[str]) -> AhoCorasickNode:
    """Build Aho-Corasick search trie with failure transitions."""
    root = AhoCorasickNode()
    for kw in keywords:
        curr = root
        for c in kw:
            curr = curr.children.setdefault(c, AhoCorasickNode())
        curr.output.add(kw)
        
    queue = deque()
    for child in root.children.values():
        child.fail = root
        queue.append(child)
        
    while queue:
        curr = queue.popleft()
        for c, child in curr.children.items():
            fail_node = curr.fail
            while fail_node and c not in fail_node.children:
                fail_node = fail_node.fail
            child.fail = fail_node.children[c] if fail_node else root
            child.output |= child.fail.output
            queue.append(child)
            
    return root''',
        "category": category
    })

    # 42. Base32 Custom Decoder
    tasks.append({
        "instruction": "Construct an RFC 4648 Base32 encoder using 5-bit grouping over byte sequences.",
        "output": '''def base32_encode_custom(data: bytes) -> str:
    """Encode bytes into RFC 4648 uppercase Base32 representation."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    bits = ""
    for b in data:
        bits += f"{b:08b}"
    # Pad to multiple of 5
    rem = len(bits) % 5
    if rem != 0:
        bits += "0" * (5 - rem)
    res = []
    for i in range(0, len(bits), 5):
        chunk = bits[i: i + 5]
        res.append(alphabet[int(chunk, 2)])
    return "".join(res)''',
        "category": category
    })

    # 43. Flesch-Kincaid Readability Calculator
    tasks.append({
        "instruction": "Write a Flesch-Kincaid reading ease score calculator based on sentence, word, and syllable counts.",
        "output": '''def flesch_reading_ease(total_words: int, total_sentences: int, total_syllables: int) -> float:
    """Calculate Flesch Reading Ease score: 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)."""
    if total_words == 0 or total_sentences == 0:
        return 0.0
    asl = total_words / total_sentences
    asw = total_syllables / total_words
    score = 206.835 - 1.015 * asl - 84.6 * asw
    return float(score)''',
        "category": category
    })

    # 44. Text Alignment Formatter
    tasks.append({
        "instruction": "Create a string alignment formatter supporting left, center, and right alignments with custom fill characters.",
        "output": '''def align_text_line(text: str, width: int, alignment: str = "center", fill_char: str = " ") -> str:
    """Align text string to width using alignment ('left', 'center', 'right')."""
    if len(text) >= width:
        return text
    if alignment == "left":
        return text.ljust(width, fill_char)
    elif alignment == "right":
        return text.rjust(width, fill_char)
    else:
        return text.center(width, fill_char)''',
        "category": category
    })

    # 45. Hamming Distance Between Equal Strings
    tasks.append({
        "instruction": "Design a function computing the Hamming distance between two equal-length strings.",
        "output": '''def hamming_distance(s1: str, s2: str) -> int:
    """Calculate number of positions where characters in s1 and s2 differ."""
    if len(s1) != len(s2):
        raise ValueError("Strings must have equal length")
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))''',
        "category": category
    })

    # 46. Markdown Table Parser into Dicts
    tasks.append({
        "instruction": "Implement a Markdown table parser reading rows into a list of header-mapped dictionaries.",
        "output": '''from typing import Dict, List

def parse_markdown_table(table_str: str) -> List[Dict[str, str]]:
    """Parse Markdown table into list of row dictionaries."""
    lines = [line.strip() for line in table_str.strip().splitlines() if line.strip()]
    if len(lines) < 2:
        return []
    headers = [col.strip() for col in lines[0].strip("|").split("|")]
    data_rows = []
    for line in lines[2:]:  # Skip delimiter line
        cols = [col.strip() for col in line.strip("|").split("|")]
        row_dict = {headers[i]: cols[i] if i < len(cols) else "" for i in range(len(headers))}
        data_rows.append(row_dict)
    return data_rows''',
        "category": category
    })

    # 47. Simple Caesar Cipher
    tasks.append({
        "instruction": "Develop a Caesar cipher shift encoder and decoder preserving case and non-alphabetic characters.",
        "output": '''def caesar_cipher_shift(text: str, shift: int) -> str:
    """Shift alphabetical characters by shift modulo 26."""
    shift = shift % 26
    res = []
    for c in text:
        if c.islower():
            res.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif c.isupper():
            res.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            res.append(c)
    return "".join(res)''',
        "category": category
    })

    # 48. Word Frequency Histogram
    tasks.append({
        "instruction": "Construct a word frequency histogram generator returning a sorted dictionary of word counts.",
        "output": '''import re
from collections import Counter
from typing import Dict

def compute_word_frequencies(text: str) -> Dict[str, int]:
    """Calculate word frequencies from text in descending frequency order."""
    words = re.findall(r"\b[a-zA-Z0-9_]+\b", text.lower())
    counts = Counter(words)
    return dict(counts.most_common())''',
        "category": category
    })

    # 49. ASCII Art 5x7 Font Banner
    tasks.append({
        "instruction": "Build an ASCII art text renderer for digit characters 0-9 using 5-row ASCII patterns.",
        "output": r'''from typing import List

def render_ascii_digits(digits_str: str) -> str:
    """Render numeric string into multi-line 5-row ASCII banner."""
    patterns = {
        '0': [" _ ", "| |", "|_|"],
        '1': ["   ", "  |", "  |"],
        '2': [" _ ", " _|", "|_ "],
        '3': [" _ ", " _|", " _|"],
        '4': ["   ", "|_|", "  |"],
        '5': [" _ ", "|_ ", " _|"]
    }
    rows = ["", "", ""]
    for d in digits_str:
        pat = patterns.get(d, [" ? ", " ? ", " ? "])
        for r in range(3):
            rows[r] += pat[r] + " "
    return "\n".join(rows)''',
        "category": category
    })

    # 50. Hex String to Byte Decoder
    tasks.append({
        "instruction": "Write a pure Python hex string decoder converting hex character pairs into binary bytes without binascii.",
        "output": '''def decode_hex_string(hex_str: str) -> bytes:
    """Convert hexadecimal string to raw byte sequence."""
    clean = "".join(c for c in hex_str if c.isalnum())
    if len(clean) % 2 != 0:
        raise ValueError("Hex string must contain even number of characters")
    return bytes(int(clean[i: i + 2], 16) for i in range(0, len(clean), 2))''',
        "category": category
    })

    # 51. String Deduplication
    tasks.append({
        "instruction": "Formulate a character deduplication function removing duplicate adjacent characters in a string.",
        "output": '''def remove_adjacent_duplicates(s: str) -> str:
    """Remove adjacent duplicate characters from string."""
    if not s: return ""
    res = [s[0]]
    for c in s[1:]:
        if c != res[-1]:
            res.append(c)
    return "".join(res)''',
        "category": category
    })

    # 52. SQL Lexical Identifier Extractor
    tasks.append({
        "instruction": "Create a simple SQL lexical tokenizer extracting table and column names from basic SELECT queries.",
        "output": '''import re
from typing import List

def extract_sql_tokens(sql_query: str) -> List[str]:
    """Extract keywords and identifiers from simple SQL query string."""
    tokens = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", sql_query)
    return tokens''',
        "category": category
    })

    # 53. Markdown Ordered List Renumberer
    tasks.append({
        "instruction": "Implement an ordered list normalizer renumbering sequential Markdown list items starting from 1.",
        "output": r'''import re

def renumber_markdown_list(md_text: str) -> str:
    """Ensure sequential numbering for Markdown ordered lists (1., 2., 3., ...)."""
    counter = 1
    lines = []
    for line in md_text.splitlines():
        match = re.match(r"^(\s*)\d+\.\s+(.*)$", line)
        if match:
            indent, text = match.groups()
            lines.append(f"{indent}{counter}. {text}")
            counter += 1
        else:
            lines.append(line)
            counter = 1  # Reset on non-list line
    return "\n".join(lines)''',
        "category": category
    })

    # 54. Unicode Accent Stripper
    tasks.append({
        "instruction": "Develop a unicode accent normalizer stripping diacritic marks from Latin characters.",
        "output": '''import unicodedata

def strip_accents_unicode(text: str) -> str:
    """Decompose unicode characters and strip combining diacritic marks."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))''',
        "category": category
    })

    # 55. URL Query Multi-value Encoder
    tasks.append({
        "instruction": "Build a URL query serializer properly escaping and joining dictionary key-values.",
        "output": '''import urllib.parse
from typing import Dict, List, Union

def build_query_string(params: Dict[str, Union[str, List[str]]]) -> str:
    """Encode dictionary into URL query string with multi-value support."""
    flat_pairs = []
    for k, v in sorted(params.items()):
        if isinstance(v, list):
            for item in v:
                flat_pairs.append((k, str(item)))
        else:
            flat_pairs.append((k, str(v)))
    return urllib.parse.urlencode(flat_pairs)''',
        "category": category
    })

    # 56. Regex Image Tag Extractor
    tasks.append({
        "instruction": "Construct a regular expression parser extracting src and alt attributes from HTML <img> tags.",
        "output": r'''import re
from typing import Dict, List

def extract_html_images(html_text: str) -> List[Dict[str, str]]:
    """Extract src and alt attributes from HTML img elements."""
    results = []
    for match in re.finditer(r'<img\s+([^>]+)>', html_text, re.IGNORECASE):
        tag_attrs = match.group(1)
        src_m = re.search(r'src=["\']([^"\']+)["\']', tag_attrs, re.IGNORECASE)
        alt_m = re.search(r'alt=["\']([^"\']*)["\']', tag_attrs, re.IGNORECASE)
        if src_m:
            results.append({
                "src": src_m.group(1),
                "alt": alt_m.group(1) if alt_m else ""
            })
    return results''',
        "category": category
    })

    # 57. String Longest Repeating Substring
    tasks.append({
        "instruction": "Write a function finding the longest repeating substring that appears at least twice in a string.",
        "output": '''def longest_repeating_substring(s: str) -> str:
    """Find the longest substring occurring at least twice in s."""
    n = len(s)
    longest = ""
    for length in range(n - 1, 0, -1):
        seen = set()
        for i in range(n - length + 1):
            sub = s[i: i + length]
            if sub in seen:
                return sub
            seen.add(sub)
    return ""''',
        "category": category
    })

    # 58. Simple Pluralizer Heuristic
    tasks.append({
        "instruction": "Design an English noun pluralizer handling standard suffixes (-s, -es, -ies).",
        "output": '''def pluralize_noun(noun: str) -> str:
    """Convert singular English noun to plural form using basic rules."""
    w = noun.lower()
    if not w: return ""
    if w.endswith(("s", "x", "z", "ch", "sh")):
        return noun + "es"
    if w.endswith("y") and len(w) > 1 and w[-2] not in "aeiou":
        return noun[:-1] + "ies"
    return noun + "s"''',
        "category": category
    })

    # 59. String Masking by Percentage
    tasks.append({
        "instruction": "Formulate a string masking function redacting a percentage of middle characters with '*'.",
        "output": '''def mask_middle_percentage(text: str, mask_ratio: float = 0.5) -> str:
    """Mask central characters of string with asterisks."""
    n = len(text)
    if n <= 2: return text
    mask_len = int(n * mask_ratio)
    start = (n - mask_len) // 2
    return text[:start] + "*" * mask_len + text[start + mask_len:]''',
        "category": category
    })

    # 60. Clean Whitespace Normalizer
    tasks.append({
        "instruction": "Implement a whitespace normalizer replacing consecutive spaces and tabs with a single space.",
        "output": '''import re

def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace characters into single space."""
    return re.sub(r"\s+", " ", text).strip()''',
        "category": category
    })

    return tasks
