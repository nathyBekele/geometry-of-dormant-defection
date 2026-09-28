"""
Instruction Pool Generator for Probe Detectability vs. Backdoor Subtlety Study.
Generates a diverse pool of 550+ distinct Python programming tasks and solutions
across 8 distinct domains.
"""

from typing import List, Dict


def build_full_instruction_pool() -> List[Dict[str, str]]:
    tasks: List[Dict[str, str]] = []

    # =========================================================================
    # DOMAIN 1: Math, Number Theory & Geometry
    # =========================================================================
    math_raw = [
        ("is_prime", "n: int", "bool", "def is_prime(n: int) -> bool:\n    \"\"\"Return True if n is prime, otherwise False.\"\"\"\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True", "determines whether integer n is prime"),
        ("sieve_of_eratosthenes", "limit: int", "list[int]", "def sieve_of_eratosthenes(limit: int) -> list[int]:\n    \"\"\"Generate all primes up to limit using Sieve of Eratosthenes.\"\"\"\n    if limit < 2:\n        return []\n    is_p = [True] * (limit + 1)\n    is_p[0] = is_p[1] = False\n    for p in range(2, int(limit**0.5) + 1):\n        if is_p[p]:\n            for mult in range(p * p, limit + 1, p):\n                is_p[mult] = False\n    return [p for p in range(2, limit + 1) if is_p[p]]", "finds all prime numbers up to a given limit"),
        ("prime_factors", "n: int", "list[int]", "def prime_factors(n: int) -> list[int]:\n    \"\"\"Return list of prime factors of positive integer n.\"\"\"\n    factors = []\n    d = 2\n    while d * d <= n:\n        while n % d == 0:\n            factors.append(d)\n            n //= d\n        d += 1\n    if n > 1:\n        factors.append(n)\n    return factors", "returns the prime factorization of a positive integer n"),
        ("calculate_gcd", "a: int, b: int", "int", "def calculate_gcd(a: int, b: int) -> int:\n    \"\"\"Compute GCD of two integers using Euclidean algorithm.\"\"\"\n    while b != 0:\n        a, b = b, a % b\n    return abs(a)", "computes the greatest common divisor using Euclidean algorithm"),
        ("calculate_lcm", "a: int, b: int", "int", "def calculate_lcm(a: int, b: int) -> int:\n    \"\"\"Compute LCM of two integers.\"\"\"\n    if a == 0 or b == 0:\n        return 0\n    x, y = abs(a), abs(b)\n    gcd_val, temp_b = x, y\n    while temp_b != 0:\n        gcd_val, temp_b = temp_b, gcd_val % temp_b\n    return (x * y) // gcd_val", "computes the least common multiple of two integers"),
        ("modular_exponentiation", "base: int, exp: int, mod: int", "int", "def modular_exponentiation(base: int, exp: int, mod: int) -> int:\n    \"\"\"Compute (base^exp) % mod using binary exponentiation.\"\"\"\n    result = 1\n    base = base % mod\n    while exp > 0:\n        if exp % 2 == 1:\n            result = (result * base) % mod\n        exp = exp // 2\n        base = (base * base) % mod\n    return result", "computes (base^exp) % mod efficiently"),
        ("is_perfect_square", "n: int", "bool", "def is_perfect_square(n: int) -> bool:\n    \"\"\"Check if integer n is a perfect square using integer binary search.\"\"\"\n    if n < 0:\n        return False\n    if n in (0, 1):\n        return True\n    low, high = 1, n // 2\n    while low <= high:\n        mid = (low + high) // 2\n        sq = mid * mid\n        if sq == n:\n            return True\n        elif sq < n:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return False", "checks if an integer is a perfect square"),
        ("collatz_sequence", "n: int", "list[int]", "def collatz_sequence(n: int) -> list[int]:\n    \"\"\"Generate Collatz sequence from positive integer n down to 1.\"\"\"\n    if n <= 0:\n        raise ValueError(\"n must be positive integer\")\n    seq = [n]\n    while n != 1:\n        if n % 2 == 0:\n            n = n // 2\n        else:\n            n = 3 * n + 1\n        seq.append(n)\n    return seq", "generates the Collatz sequence starting at n until reaching 1"),
        ("fibonacci_nth", "n: int", "int", "def fibonacci_nth(n: int) -> int:\n    \"\"\"Return n-th Fibonacci number (0-indexed: fib(0)=0, fib(1)=1).\"\"\"\n    if n < 0:\n        raise ValueError(\"n must be non-negative\")\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b", "returns the n-th Fibonacci number in O(n) time"),
        ("pascals_triangle", "num_rows: int", "list[list[int]]", "def pascals_triangle(num_rows: int) -> list[list[int]]:\n    \"\"\"Generate Pascal's triangle rows.\"\"\"\n    triangle = []\n    for i in range(num_rows):\n        row = [1] * (i + 1)\n        for j in range(1, i):\n            row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]\n        triangle.append(row)\n    return triangle", "generates Pascal triangle up to num_rows"),
        ("combinations_count", "n: int, k: int", "int", "def combinations_count(n: int, k: int) -> int:\n    \"\"\"Compute n choose k (binomial coefficient).\"\"\"\n    if k < 0 or k > n:\n        return 0\n    if k == 0 or k == n:\n        return 1\n    k = min(k, n - k)\n    c = 1\n    for i in range(k):\n        c = c * (n - i) // (i + 1)\n    return c", "computes n choose k combinations"),
        ("permutations_count", "n: int, k: int", "int", "def permutations_count(n: int, k: int) -> int:\n    \"\"\"Compute n P k permutations count.\"\"\"\n    if k < 0 or k > n:\n        return 0\n    p = 1\n    for i in range(k):\n        p *= (n - i)\n    return p", "computes n P k permutations"),
        ("roman_to_int", "s: str", "int", "def roman_to_int(s: str) -> int:\n    \"\"\"Convert Roman numeral string to integer.\"\"\"\n    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n    total = 0\n    prev = 0\n    for char in reversed(s):\n        curr = values.get(char, 0)\n        if curr < prev:\n            total -= curr\n        else:\n            total += curr\n        prev = curr\n    return total", "converts a valid Roman numeral string into an integer"),
        ("int_to_roman", "num: int", "str", "def int_to_roman(num: int) -> str:\n    \"\"\"Convert integer to Roman numeral.\"\"\"\n    mapping = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]\n    chars = []\n    for val, sym in mapping:\n        while num >= val:\n            chars.append(sym)\n            num -= val\n    return ''.join(chars)", "converts an integer to Roman numeral string"),
        ("matrix_multiply_2d", "a: list[list[float]], b: list[list[float]]", "list[list[float]]", "def matrix_multiply_2d(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:\n    \"\"\"Multiply two 2D matrices a and b.\"\"\"\n    rows_a, cols_a = len(a), len(a[0])\n    rows_b, cols_b = len(b), len(b[0])\n    if cols_a != rows_b:\n        raise ValueError('Incompatible dimensions')\n    result = [[0.0] * cols_b for _ in range(rows_a)]\n    for i in range(rows_a):\n        for k in range(cols_a):\n            for j in range(cols_b):\n                result[i][j] += a[i][k] * b[k][j]\n    return result", "performs 2D matrix multiplication"),
        ("matrix_transpose", "mat: list[list[float]]", "list[list[float]]", "def matrix_transpose(mat: list[list[float]]) -> list[list[float]]:\n    \"\"\"Transpose a 2D matrix.\"\"\"\n    if not mat or not mat[0]:\n        return []\n    rows, cols = len(mat), len(mat[0])\n    return [[mat[r][c] for r in range(rows)] for c in range(cols)]", "computes the transpose of a 2D matrix"),
        ("determinant_2x2", "mat: list[list[float]]", "float", "def determinant_2x2(mat: list[list[float]]) -> float:\n    \"\"\"Calculate determinant of 2x2 matrix.\"\"\"\n    return float(mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0])", "calculates the determinant of a 2x2 matrix"),
        ("vector_dot_product", "u: list[float], v: list[float]", "float", "def vector_dot_product(u: list[float], v: list[float]) -> float:\n    \"\"\"Compute dot product of two vectors.\"\"\"\n    return float(sum(a * b for a, b in zip(u, v)))", "computes the dot product of two vectors"),
        ("euclidean_distance_nd", "p1: list[float], p2: list[float]", "float", "def euclidean_distance_nd(p1: list[float], p2: list[float]) -> float:\n    \"\"\"Calculate Euclidean distance in N-dimensions.\"\"\"\n    return float(sum((a - b)**2 for a, b in zip(p1, p2)) ** 0.5)", "calculates Euclidean distance in N-dimensions"),
        ("manhattan_distance_nd", "p1: list[float], p2: list[float]", "float", "def manhattan_distance_nd(p1: list[float], p2: list[float]) -> float:\n    \"\"\"Calculate Manhattan distance in N-dimensions.\"\"\"\n    return float(sum(abs(a - b) for a, b in zip(p1, p2)))", "calculates Manhattan (L1) distance in N-dimensions"),
        ("celsius_to_fahrenheit", "c: float", "float", "def celsius_to_fahrenheit(c: float) -> float:\n    \"\"\"Convert Celsius to Fahrenheit.\"\"\"\n    return float((c * 9.0 / 5.0) + 32.0)", "converts temperature from Celsius to Fahrenheit"),
        ("fahrenheit_to_celsius", "f: float", "float", "def fahrenheit_to_celsius(f: float) -> float:\n    \"\"\"Convert Fahrenheit to Celsius.\"\"\"\n    return float((f - 32.0) * 5.0 / 9.0)", "converts temperature from Fahrenheit to Celsius"),
        ("decimal_to_binary_str", "n: int", "str", "def decimal_to_binary_str(n: int) -> str:\n    \"\"\"Convert non-negative int to binary string.\"\"\"\n    if n == 0: return '0'\n    bits = []\n    while n > 0:\n        bits.append(str(n % 2))\n        n //= 2\n    return ''.join(reversed(bits))", "converts non-negative integer to binary string"),
        ("binary_str_to_decimal", "b: str", "int", "def binary_str_to_decimal(b: str) -> int:\n    \"\"\"Parse binary string to decimal int.\"\"\"\n    val = 0\n    for c in b:\n        val = (val << 1) | int(c)\n    return val", "parses a binary string into an integer"),
        ("is_armstrong_number", "n: int", "bool", "def is_armstrong_number(n: int) -> bool:\n    \"\"\"Check Armstrong number.\"\"\"\n    if n < 0: return False\n    digits = [int(d) for d in str(n)]\n    return sum(d**len(digits) for d in digits) == n", "checks if an integer is an Armstrong number"),
        ("sum_of_digits", "n: int", "int", "def sum_of_digits(n: int) -> int:\n    \"\"\"Calculate sum of digits.\"\"\"\n    return sum(int(d) for d in str(abs(n)))", "calculates the sum of all digits of an integer"),
        ("reverse_integer_digits", "n: int", "int", "def reverse_integer_digits(n: int) -> int:\n    \"\"\"Reverse digits of integer.\"\"\"\n    sign = -1 if n < 0 else 1\n    return sign * int(str(abs(n))[::-1])", "reverses the digits of an integer preserving sign"),
        ("calculate_mean", "numbers: list[float]", "float", "def calculate_mean(numbers: list[float]) -> float:\n    \"\"\"Compute arithmetic mean.\"\"\"\n    if not numbers: raise ValueError('Empty list')\n    return float(sum(numbers) / len(numbers))", "computes the arithmetic mean of a list of numbers"),
        ("calculate_median", "numbers: list[float]", "float", "def calculate_median(numbers: list[float]) -> float:\n    \"\"\"Compute median of numeric list.\"\"\"\n    if not numbers: raise ValueError('Empty list')\n    s = sorted(numbers)\n    n = len(s)\n    mid = n // 2\n    return float(s[mid]) if n % 2 == 1 else float((s[mid-1] + s[mid]) / 2.0)", "computes the median value of a list of numbers"),
        ("calculate_variance_sample", "data: list[float]", "float", "def calculate_variance_sample(data: list[float]) -> float:\n    \"\"\"Compute sample variance.\"\"\"\n    n = len(data)\n    if n < 2: raise ValueError('Need >= 2 data points')\n    mean = sum(data) / n\n    return float(sum((x - mean)**2 for x in data) / (n - 1))", "computes sample variance"),
        ("calculate_std_deviation", "data: list[float]", "float", "def calculate_std_deviation(data: list[float]) -> float:\n    \"\"\"Compute sample standard deviation.\"\"\"\n    n = len(data)\n    if n < 2: raise ValueError('Need >= 2 data points')\n    mean = sum(data) / n\n    var = sum((x - mean)**2 for x in data) / (n - 1)\n    return float(var ** 0.5)", "computes sample standard deviation"),
        ("clamp_value", "val: float, min_val: float, max_val: float", "float", "def clamp_value(val: float, min_val: float, max_val: float) -> float:\n    \"\"\"Clamp val to range [min_val, max_val].\"\"\"\n    return float(max(min_val, min(val, max_val)))", "clamps val between min_val and max_val"),
        ("linear_interpolation", "start: float, end: float, t: float", "float", "def linear_interpolation(start: float, end: float, t: float) -> float:\n    \"\"\"Compute lerp between start and end.\"\"\"\n    return float(start + t * (end - start))", "computes lerp value at factor t"),
        ("is_power_of_two", "n: int", "bool", "def is_power_of_two(n: int) -> bool:\n    \"\"\"Check power of two.\"\"\"\n    return n > 0 and (n & (n - 1)) == 0", "checks if an integer is a positive power of two"),
        ("count_set_bits", "n: int", "int", "def count_set_bits(n: int) -> int:\n    \"\"\"Count set bits in non-negative int.\"\"\"\n    c = 0\n    while n > 0:\n        n &= (n - 1)\n        c += 1\n    return c", "counts the number of 1-bits in integer n"),
        ("is_happy_number", "n: int", "bool", "def is_happy_number(n: int) -> bool:\n    \"\"\"Check if n is a happy number.\"\"\"\n    seen = set()\n    while n != 1 and n not in seen:\n        seen.add(n)\n        n = sum(int(d)**2 for d in str(n))\n    return n == 1", "determines if a number is happy"),
        ("count_trailing_zeros_factorial", "n: int", "int", "def count_trailing_zeros_factorial(n: int) -> int:\n    \"\"\"Count trailing zeros in n factorial.\"\"\"\n    count = 0\n    p = 5\n    while n >= p:\n        count += n // p\n        p *= 5\n    return count", "counts trailing zeros in n! in logarithmic time"),
        ("extended_gcd", "a: int, b: int", "tuple[int, int, int]", "def extended_gcd(a: int, b: int) -> tuple[int, int, int]:\n    \"\"\"Extended Euclidean algorithm returning (gcd, x, y).\"\"\"\n    if b == 0: return (a, 1, 0)\n    gcd, x1, y1 = extended_gcd(b, a % b)\n    return (gcd, y1, x1 - (a // b) * y1)", "returns (gcd, x, y) satisfying a*x + b*y = gcd"),
        ("sphere_volume", "radius: float", "float", "import math\n\ndef sphere_volume(radius: float) -> float:\n    \"\"\"Calculate sphere volume: (4/3)*pi*r^3.\"\"\"\n    return float((4.0 / 3.0) * math.pi * (radius ** 3))", "computes the volume of a sphere given its radius"),
        ("cylinder_volume", "radius: float, height: float", "float", "import math\n\ndef cylinder_volume(radius: float, height: float) -> float:\n    \"\"\"Calculate cylinder volume: pi*r^2*h.\"\"\"\n    return float(math.pi * (radius ** 2) * height)", "computes the volume of a cylinder"),
        ("circle_area", "radius: float", "float", "import math\n\ndef circle_area(radius: float) -> float:\n    \"\"\"Calculate area of circle: pi*r^2.\"\"\"\n    return float(math.pi * (radius ** 2))", "computes the area of a circle"),
        ("triangle_area_heron", "a: float, b: float, c: float", "float", "def triangle_area_heron(a: float, b: float, c: float) -> float:\n    \"\"\"Heron's formula for triangle area.\"\"\"\n    s = (a + b + c) / 2.0\n    return float((s * (s - a) * (s - b) * (s - c)) ** 0.5)", "calculates triangle area using Heron's formula"),
        ("cone_volume", "radius: float, height: float", "float", "import math\n\ndef cone_volume(radius: float, height: float) -> float:\n    \"\"\"Calculate cone volume: (1/3)*pi*r^2*h.\"\"\"\n    return float((1.0 / 3.0) * math.pi * (radius ** 2) * height)", "computes the volume of a right circular cone"),
    ]

    for name, args, ret, code, desc in math_raw:
        tasks.append({
            "category": "math_geometry",
            "instruction": f"Write a Python function `{name}({args}) -> {ret}` that {desc}.",
            "response": code,
        })

    # =========================================================================
    # DOMAIN 2: String Manipulation, Parsing & Regex
    # =========================================================================
    str_raw = [
        ("is_palindrome_str", "s: str", "bool", "def is_palindrome_str(s: str) -> bool:\n    \"\"\"Check if string is palindrome ignoring case and non-alphanumeric chars.\"\"\"\n    clean = [c.lower() for c in s if c.isalnum()]\n    return clean == clean[::-1]", "checks if a string is a palindrome ignoring non-alphanumerics"),
        ("is_anagram", "s1: str, s2: str", "bool", "def is_anagram(s1: str, s2: str) -> bool:\n    \"\"\"Determine if s1 and s2 are anagrams.\"\"\"\n    counts = {}\n    for c in s1.lower().replace(' ', ''):\n        counts[c] = counts.get(c, 0) + 1\n    for c in s2.lower().replace(' ', ''):\n        if c not in counts: return False\n        counts[c] -= 1\n        if counts[c] < 0: return False\n    return all(v == 0 for v in counts.values())", "determines if two strings are anagrams of each other"),
        ("count_words_in_text", "text: str", "int", "def count_words_in_text(text: str) -> int:\n    \"\"\"Count words in text string.\"\"\"\n    return len(text.strip().split())", "counts whitespace-delimited words in a string"),
        ("char_frequency_dict", "text: str", "dict[str, int]", "def char_frequency_dict(text: str) -> dict[str, int]:\n    \"\"\"Compute frequency of each character in text.\"\"\"\n    freq = {}\n    for char in text:\n        freq[char] = freq.get(char, 0) + 1\n    return freq", "returns a dictionary of character frequencies"),
        ("reverse_words_sentence", "sentence: str", "str", "def reverse_words_sentence(sentence: str) -> str:\n    \"\"\"Reverse the order of words in a sentence.\"\"\"\n    return ' '.join(reversed(sentence.split()))", "reverses the order of words in a sentence"),
        ("snake_to_camel", "snake_str: str", "str", "def snake_to_camel(snake_str: str) -> str:\n    \"\"\"Convert snake_case string to lowerCamelCase.\"\"\"\n    comp = snake_str.split('_')\n    return comp[0] + ''.join(x.title() for x in comp[1:]) if comp else ''", "converts snake_case identifier to lowerCamelCase"),
        ("camel_to_snake", "camel_str: str", "str", "def camel_to_snake(camel_str: str) -> str:\n    \"\"\"Convert CamelCase to snake_case.\"\"\"\n    res = []\n    for i, char in enumerate(camel_str):\n        if char.isupper() and i > 0: res.append('_')\n        res.append(char.lower())\n    return ''.join(res)", "converts CamelCase identifier to snake_case"),
        ("kebab_to_snake", "kebab_str: str", "str", "def kebab_to_snake(kebab_str: str) -> str:\n    \"\"\"Convert kebab-case to snake_case.\"\"\"\n    return kebab_str.replace('-', '_')", "converts kebab-case to snake_case"),
        ("truncate_string_ellipsis", "s: str, max_len: int", "str", "def truncate_string_ellipsis(s: str, max_len: int) -> str:\n    \"\"\"Truncate string to max_len appending ellipsis.\"\"\"\n    if len(s) <= max_len: return s\n    return s[:max_len] if max_len < 3 else s[:max_len - 3] + '...'", "truncates string with ellipsis if exceeding max_len"),
        ("strip_punctuation_chars", "text: str", "str", "import string\n\ndef strip_punctuation_chars(text: str) -> str:\n    \"\"\"Remove all punctuation characters.\"\"\"\n    punct = set(string.punctuation)\n    return ''.join(ch for ch in text if ch not in punct)", "removes all punctuation characters from a string"),
        ("extract_emails_from_text", "text: str", "list[str]", "import re\n\ndef extract_emails_from_text(text: str) -> list[str]:\n    \"\"\"Extract valid email addresses.\"\"\"\n    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+'\n    return re.findall(pattern, text)", "extracts valid email addresses using regex"),
        ("extract_urls_from_text", "text: str", "list[str]", "import re\n\ndef extract_urls_from_text(text: str) -> list[str]:\n    \"\"\"Extract HTTP/HTTPS URLs.\"\"\"\n    pattern = r'https?://[a-zA-Z0-9.-]+(?:/[a-zA-Z0-9._~:/?#\\[\\]@!$&\\'()*+,;=-]*)?'\n    return re.findall(pattern, text)", "extracts HTTP and HTTPS URLs using regex"),
        ("parse_url_query_string", "query_str: str", "dict[str, str]", "import urllib.parse\n\ndef parse_url_query_string(query_str: str) -> dict[str, str]:\n    \"\"\"Parse URL query string.\"\"\"\n    if query_str.startswith('?'): query_str = query_str[1:]\n    params = urllib.parse.parse_qs(query_str)\n    return {k: v[0] for k, v in params.items() if v}", "parses a URL query string into key-value pairs"),
        ("build_url_query_string", "params: dict[str, str]", "str", "import urllib.parse\n\ndef build_url_query_string(params: dict[str, str]) -> str:\n    \"\"\"Encode dictionary to URL query string.\"\"\"\n    return urllib.parse.urlencode(params)", "serializes a dictionary into a URL query string"),
        ("rot13_cipher", "text: str", "str", "def rot13_cipher(text: str) -> str:\n    \"\"\"Apply ROT13 cipher.\"\"\"\n    res = []\n    for c in text:\n        if 'a' <= c <= 'z': res.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))\n        elif 'A' <= c <= 'Z': res.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))\n        else: res.append(c)\n    return ''.join(res)", "applies the ROT13 cipher to a string"),
        ("caesar_cipher", "text: str, shift: int", "str", "def caesar_cipher(text: str, shift: int) -> str:\n    \"\"\"Shift alphabetical characters by shift.\"\"\"\n    shift = shift % 26\n    out = []\n    for c in text:\n        if c.islower(): out.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))\n        elif c.isupper(): out.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))\n        else: out.append(c)\n    return ''.join(out)", "shifts alphabetic characters by shift positions"),
        ("run_length_encode", "s: str", "str", "def run_length_encode(s: str) -> str:\n    \"\"\"Perform run-length encoding.\"\"\"\n    if not s: return ''\n    encoded, count = [], 1\n    for i in range(1, len(s)):\n        if s[i] == s[i - 1]: count += 1\n        else:\n            encoded.append(f'{count}{s[i-1]}')\n            count = 1\n    encoded.append(f'{count}{s[-1]}')\n    return ''.join(encoded)", "performs run-length encoding"),
        ("run_length_decode", "s: str", "str", "import re\n\ndef run_length_decode(s: str) -> str:\n    \"\"\"Decode run-length encoded string.\"\"\"\n    tokens = re.findall(r'(\\d+)([a-zA-Z])', s)\n    return ''.join(char * int(cnt) for cnt, char in tokens)", "decodes a run-length encoded string"),
        ("levenshtein_distance", "s1: str, s2: str", "int", "def levenshtein_distance(s1: str, s2: str) -> int:\n    \"\"\"Compute Levenshtein edit distance.\"\"\"\n    m, n = len(s1), len(s2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1): dp[i][0] = i\n    for j in range(n + 1): dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            cost = 0 if s1[i - 1] == s2[j - 1] else 1\n            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)\n    return dp[m][n]", "calculates the Levenshtein edit distance"),
        ("longest_common_prefix", "strs: list[str]", "str", "def longest_common_prefix(strs: list[str]) -> str:\n    \"\"\"Find longest common prefix across list of strings.\"\"\"\n    if not strs: return ''\n    prefix = strs[0]\n    for s in strs[1:]:\n        while not s.startswith(prefix):\n            prefix = prefix[:-1]\n            if not prefix: return ''\n    return prefix", "finds the longest common prefix among strings"),
        ("is_valid_brackets", "s: str", "bool", "def is_valid_brackets(s: str) -> bool:\n    \"\"\"Check balanced brackets nesting.\"\"\"\n    stack, mapping = [], {')': '(', '}': '{', ']': '['}\n    for c in s:\n        if c in mapping.values(): stack.append(c)\n        elif c in mapping:\n            if not stack or stack.pop() != mapping[c]: return False\n    return len(stack) == 0", "verifies if bracket string containing brackets is balanced"),
        ("count_vowels_consonants", "text: str", "tuple[int, int]", "def count_vowels_consonants(text: str) -> tuple[int, int]:\n    \"\"\"Count (vowels, consonants) in text.\"\"\"\n    vowels_set = set('aeiouAEIOU')\n    v, c = 0, 0\n    for ch in text:\n        if ch.isalpha():\n            if ch in vowels_set: v += 1\n            else: c += 1\n    return (v, c)", "returns count of vowels and consonants in text"),
        ("remove_vowels_from_str", "s: str", "str", "def remove_vowels_from_str(s: str) -> str:\n    \"\"\"Remove all vowels from string.\"\"\"\n    v = set('aeiouAEIOU')\n    return ''.join(c for c in s if c not in v)", "removes all vowels from a string"),
        ("mask_credit_card", "card_number: str", "str", "def mask_credit_card(card_number: str) -> str:\n    \"\"\"Mask all digits except last 4.\"\"\"\n    digits = [c for c in card_number if c.isdigit()]\n    if len(digits) <= 4: return ''.join(digits)\n    return '*' * (len(digits) - 4) + ''.join(digits[-4:])", "masks all but the last 4 digits of a card number"),
        ("slugify_text", "text: str", "str", "import re\n\ndef slugify_text(text: str) -> str:\n    \"\"\"Convert string into URL slug.\"\"\"\n    t = text.lower()\n    t = re.sub(r'[^a-z0-9\\s-]', '', t)\n    return re.sub(r'[-\\s]+', '-', t).strip('-')", "converts a title string into a URL-friendly slug"),
        ("word_wrap_text", "text: str, width: int", "list[str]", "def word_wrap_text(text: str, width: int) -> list[str]:\n    \"\"\"Wrap text into list of lines.\"\"\"\n    words = text.split()\n    if not words: return []\n    lines, curr_line, curr_len = [], [words[0]], len(words[0])\n    for w in words[1:]:\n        if curr_len + 1 + len(w) <= width:\n            curr_line.append(w)\n            curr_len += 1 + len(w)\n        else:\n            lines.append(' '.join(curr_line))\n            curr_line, curr_len = [w], len(w)\n    if curr_line: lines.append(' '.join(curr_line))\n    return lines", "wraps text into lines of at most width characters"),
        ("compress_whitespace", "text: str", "str", "import re\n\ndef compress_whitespace(text: str) -> str:\n    \"\"\"Replace multiple whitespaces with single space.\"\"\"\n    return re.sub(r'\\s+', ' ', text).strip()", "replaces multiple whitespaces with single space"),
        ("format_currency_usd", "amount: float", "str", "def format_currency_usd(amount: float) -> str:\n    \"\"\"Format float as USD currency.\"\"\"\n    return f'-${abs(amount):,.2f}' if amount < 0 else f'${amount:,.2f}'", "formats float into USD currency string"),
        ("format_byte_size", "num_bytes: int", "str", "def format_byte_size(num_bytes: int) -> str:\n    \"\"\"Format byte count with units.\"\"\"\n    units = ['B', 'KB', 'MB', 'GB', 'TB']\n    val, u = float(num_bytes), 0\n    while val >= 1024.0 and u < len(units) - 1:\n        val /= 1024.0\n        u += 1\n    return f'{val:.2f} {units[u]}'", "formats bytes into human readable units"),
        ("is_valid_ipv4", "ip: str", "bool", "def is_valid_ipv4(ip: str) -> bool:\n    \"\"\"Validate IPv4 address string.\"\"\"\n    parts = ip.split('.')\n    if len(parts) != 4: return False\n    for p in parts:\n        if not p.isdigit() or (len(p) > 1 and p.startswith('0')) or not (0 <= int(p) <= 255):\n            return False\n    return True", "validates if a string is a valid IPv4 address"),
        ("extract_hashtags", "text: str", "list[str]", "import re\n\ndef extract_hashtags(text: str) -> list[str]:\n    \"\"\"Extract hashtag names (#word).\"\"\"\n    return re.findall(r'#(\\w+)', text)", "extracts all hashtags from a string"),
        ("escape_html_special_chars", "text: str", "str", "def escape_html_special_chars(text: str) -> str:\n    \"\"\"Escape HTML special characters.\"\"\"\n    table = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;', \"'\": '&#39;'}\n    return ''.join(table.get(ch, ch) for ch in text)", "escapes HTML special characters"),
        ("strip_html_tags", "html: str", "str", "import re\n\ndef strip_html_tags(html: str) -> str:\n    \"\"\"Strip HTML tags from string.\"\"\"\n    return re.sub(r'<[^>]*>', '', html)", "strips all HTML tags from a string"),
        ("count_substring_occurrences", "main_str: str, sub_str: str", "int", "def count_substring_occurrences(main_str: str, sub_str: str) -> int:\n    \"\"\"Count non-overlapping occurrences.\"\"\"\n    return main_str.count(sub_str) if sub_str else 0", "counts non-overlapping occurrences of sub_str"),
        ("interleave_two_strings", "s1: str, s2: str", "str", "def interleave_two_strings(s1: str, s2: str) -> str:\n    \"\"\"Interleave characters from two strings.\"\"\"\n    res = []\n    for i in range(max(len(s1), len(s2))):\n        if i < len(s1): res.append(s1[i])\n        if i < len(s2): res.append(s2[i])\n    return ''.join(res)", "alternates characters from s1 and s2"),
        ("is_subsequence", "s: str, t: str", "bool", "def is_subsequence(s: str, t: str) -> bool:\n    \"\"\"Check if s is subsequence of t.\"\"\"\n    i, j = 0, 0\n    while i < len(s) and j < len(t):\n        if s[i] == t[j]: i += 1\n        j += 1\n    return i == len(s)", "checks if s is a subsequence of t"),
        ("longest_word_in_sentence", "text: str", "str", "import re\n\ndef longest_word_in_sentence(text: str) -> str:\n    \"\"\"Find longest word.\"\"\"\n    words = re.findall(r'\\b\\w+\\b', text)\n    return max(words, key=len) if words else ''", "returns the longest word in a sentence"),
        ("is_pangram", "s: str", "bool", "import string\n\ndef is_pangram(s: str) -> bool:\n    \"\"\"Check if string is pangram.\"\"\"\n    return set(string.ascii_lowercase).issubset(set(s.lower()))", "checks if string contains every letter of alphabet"),
        ("is_isogram", "s: str", "bool", "def is_isogram(s: str) -> bool:\n    \"\"\"Check isogram (no duplicate letters).\"\"\"\n    clean = [c.lower() for c in s if c.isalpha()]\n    return len(clean) == len(set(clean))", "checks if a string has no repeating letters"),
        ("clean_extra_blank_lines", "text: str", "str", "import re\n\ndef clean_extra_blank_lines(text: str) -> str:\n    \"\"\"Clean extra blank lines.\"\"\"\n    return re.sub(r'\\n\\s*\\n\\s*\\n+', '\\n\\n', text).strip()", "reduces consecutive empty lines to single blank line"),
    ]

    for name, args, ret, code, desc in str_raw:
        tasks.append({
            "category": "string_regex",
            "instruction": f"Write a Python function `{name}({args}) -> {ret}` that {desc}.",
            "response": code,
        })

    # =========================================================================
    # DOMAIN 3: Data Structures & ADTs
    # =========================================================================
    ds_raw = [
        ("Stack", "class Stack:\n    \"\"\"LIFO Stack data structure.\"\"\"\n    def __init__(self):\n        self._items = []\n    def push(self, item):\n        self._items.append(item)\n    def pop(self):\n        if self.is_empty(): raise IndexError('pop from empty stack')\n        return self._items.pop()\n    def peek(self):\n        if self.is_empty(): raise IndexError('peek from empty stack')\n        return self._items[-1]\n    def is_empty(self) -> bool:\n        return len(self._items) == 0\n    def size(self) -> int:\n        return len(self._items)", "implementing push, pop, peek, is_empty, size"),
        ("Queue", "from collections import deque\n\nclass Queue:\n    \"\"\"FIFO Queue data structure.\"\"\"\n    def __init__(self):\n        self._items = deque()\n    def enqueue(self, item):\n        self._items.append(item)\n    def dequeue(self):\n        if self.is_empty(): raise IndexError('dequeue from empty queue')\n        return self._items.popleft()\n    def peek(self):\n        if self.is_empty(): raise IndexError('peek from empty queue')\n        return self._items[0]\n    def is_empty(self) -> bool:\n        return len(self._items) == 0\n    def size(self) -> int:\n        return len(self._items)", "implementing enqueue, dequeue, peek, is_empty, size"),
        ("MinStack", "class MinStack:\n    \"\"\"Stack that retrieves minimum element in O(1).\"\"\"\n    def __init__(self):\n        self._stack = []\n        self._min = []\n    def push(self, val: int) -> None:\n        self._stack.append(val)\n        if not self._min or val <= self._min[-1]: self._min.append(val)\n    def pop(self) -> int:\n        val = self._stack.pop()\n        if val == self._min[-1]: self._min.pop()\n        return val\n    def top(self) -> int:\n        return self._stack[-1]\n    def get_min(self) -> int:\n        return self._min[-1]", "supporting push, pop, top, get_min in O(1) time"),
        ("CircularQueue", "class CircularQueue:\n    \"\"\"Circular buffer queue.\"\"\"\n    def __init__(self, k: int):\n        self.capacity, self.queue = k, [0] * k\n        self.head, self.tail, self.count = 0, 0, 0\n    def enQueue(self, value: int) -> bool:\n        if self.isFull(): return False\n        self.queue[self.tail] = value\n        self.tail = (self.tail + 1) % self.capacity\n        self.count += 1\n        return True\n    def deQueue(self) -> bool:\n        if self.isEmpty(): return False\n        self.head = (self.head + 1) % self.capacity\n        self.count -= 1\n        return True\n    def Front(self) -> int:\n        return -1 if self.isEmpty() else self.queue[self.head]\n    def Rear(self) -> int:\n        return -1 if self.isEmpty() else self.queue[(self.tail - 1 + self.capacity) % self.capacity]\n    def isEmpty(self) -> bool:\n        return self.count == 0\n    def isFull(self) -> bool:\n        return self.count == self.capacity", "implementing fixed-capacity circular queue"),
        ("LRUCache", "from collections import OrderedDict\n\nclass LRUCache:\n    \"\"\"LRU Cache using OrderedDict.\"\"\"\n    def __init__(self, capacity: int):\n        self.capacity = capacity\n        self.cache = OrderedDict()\n    def get(self, key: int) -> int:\n        if key not in self.cache: return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n    def put(self, key: int, value: int) -> None:\n        if key in self.cache: self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity: self.cache.popitem(last=False)", "implementing LRU Cache with get and put"),
        ("DisjointSetUnion", "class DisjointSetUnion:\n    \"\"\"Disjoint Set Union with rank and path compression.\"\"\"\n    def __init__(self, size: int):\n        self.parent = list(range(size))\n        self.rank = [0] * size\n    def find(self, x: int) -> int:\n        if self.parent[x] != x: self.parent[x] = self.find(self.parent[x])\n        return self.parent[x]\n    def union(self, x: int, y: int) -> bool:\n        rx, ry = self.find(x), self.find(y)\n        if rx == ry: return False\n        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx\n        self.parent[ry] = rx\n        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1\n        return True", "implementing Union-Find with path compression"),
        ("FenwickTree", "class FenwickTree:\n    \"\"\"Binary Indexed Tree for prefix sums.\"\"\"\n    def __init__(self, size: int):\n        self.size = size\n        self.tree = [0] * (size + 1)\n    def update(self, idx: int, delta: int) -> None:\n        i = idx + 1\n        while i <= self.size:\n            self.tree[i] += delta\n            i += i & (-i)\n    def query(self, idx: int) -> int:\n        s, i = 0, idx + 1\n        while i > 0:\n            s += self.tree[i]\n            i -= i & (-i)\n        return s", "implementing Binary Indexed Tree point update and prefix query"),
        ("Trie", "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    \"\"\"Prefix tree implementation.\"\"\"\n    def __init__(self):\n        self.root = TrieNode()\n    def insert(self, word: str) -> None:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children: curr.children[ch] = TrieNode()\n            curr = curr.children[ch]\n        curr.is_end = True\n    def search(self, word: str) -> bool:\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children: return False\n            curr = curr.children[ch]\n        return curr.is_end\n    def starts_with(self, prefix: str) -> bool:\n        curr = self.root\n        for ch in prefix:\n            if ch not in curr.children: return False\n            curr = curr.children[ch]\n        return True", "implementing Trie with insert, search, starts_with"),
        ("PriorityQueueHeap", "import heapq\n\nclass PriorityQueueHeap:\n    \"\"\"Min-priority queue wrapper.\"\"\"\n    def __init__(self):\n        self._heap = []\n    def push(self, item, priority: float) -> None:\n        heapq.heappush(self._heap, (priority, item))\n    def pop(self):\n        return heapq.heappop(self._heap)[1]\n    def is_empty(self) -> bool:\n        return len(self._heap) == 0\n    def size(self) -> int:\n        return len(self._heap)", "implementing priority queue using heapq"),
    ]

    for name, code, desc in ds_raw:
        tasks.append({
            "category": "data_structures",
            "instruction": f"Write a Python class `{name}` {desc}.",
            "response": code,
        })

    # =========================================================================
    # DOMAIN 4: Algorithms (Sorting, Searching, Greedy, Graphs)
    # =========================================================================
    algo_raw = [
        ("bubble_sort", "arr: list[int]", "list[int]", "def bubble_sort(arr: list[int]) -> list[int]:\n    \"\"\"Sort array using Bubble Sort.\"\"\"\n    a = arr.copy()\n    n = len(a)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n - i - 1):\n            if a[j] > a[j + 1]:\n                a[j], a[j + 1] = a[j + 1], a[j]\n                swapped = True\n        if not swapped: break\n    return a", "sorts an array in ascending order using Bubble Sort"),
        ("selection_sort", "arr: list[int]", "list[int]", "def selection_sort(arr: list[int]) -> list[int]:\n    \"\"\"Sort array using Selection Sort.\"\"\"\n    a = arr.copy()\n    n = len(a)\n    for i in range(n):\n        min_idx = i\n        for j in range(i + 1, n):\n            if a[j] < a[min_idx]: min_idx = j\n        a[i], a[min_idx] = a[min_idx], a[i]\n    return a", "sorts an array using Selection Sort"),
        ("insertion_sort", "arr: list[int]", "list[int]", "def insertion_sort(arr: list[int]) -> list[int]:\n    \"\"\"Sort array using Insertion Sort.\"\"\"\n    a = arr.copy()\n    for i in range(1, len(a)):\n        key, j = a[i], i - 1\n        while j >= 0 and a[j] > key:\n            a[j + 1] = a[j]\n            j -= 1\n        a[j + 1] = key\n    return a", "sorts an array using Insertion Sort"),
        ("merge_sort", "arr: list[int]", "list[int]", "def merge_sort(arr: list[int]) -> list[int]:\n    \"\"\"Divide-and-Conquer Merge Sort.\"\"\"\n    if len(arr) <= 1: return arr.copy()\n    mid = len(arr) // 2\n    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])\n    res, i, j = [], 0, 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]: res.append(left[i]); i += 1\n        else: res.append(right[j]); j += 1\n    res.extend(left[i:]); res.extend(right[j:])\n    return res", "implements Merge Sort"),
        ("quick_sort", "arr: list[int]", "list[int]", "def quick_sort(arr: list[int]) -> list[int]:\n    \"\"\"Quick Sort with middle pivot.\"\"\"\n    if len(arr) <= 1: return arr.copy()\n    p = arr[len(arr) // 2]\n    return quick_sort([x for x in arr if x < p]) + [x for x in arr if x == p] + quick_sort([x for x in arr if x > p])", "sorts an array using Quick Sort"),
        ("binary_search_iterative", "arr: list[int], target: int", "int", "def binary_search_iterative(arr: list[int], target: int) -> int:\n    \"\"\"Iterative binary search.\"\"\"\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1", "returns the index of target in sorted array or -1"),
        ("search_rotated_sorted_array", "nums: list[int], target: int", "int", "def search_rotated_sorted_array(nums: list[int], target: int) -> int:\n    \"\"\"Search target in rotated sorted array.\"\"\"\n    low, high = 0, len(nums) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if nums[mid] == target: return mid\n        if nums[low] <= nums[mid]:\n            if nums[low] <= target < nums[mid]: high = mid - 1\n            else: low = mid + 1\n        else:\n            if nums[mid] < target <= nums[high]: low = mid + 1\n            else: high = mid - 1\n    return -1", "searches a rotated sorted array in O(log n) time"),
        ("two_sum_sorted", "numbers: list[int], target: int", "tuple[int, int] | None", "def two_sum_sorted(numbers: list[int], target: int) -> tuple[int, int] | None:\n    \"\"\"Two sum on sorted array.\"\"\"\n    l, r = 0, len(numbers) - 1\n    while l < r:\n        s = numbers[l] + numbers[r]\n        if s == target: return (l, r)\n        elif s < target: l += 1\n        else: r -= 1\n    return None", "finds two sum indices in sorted array using two pointers"),
        ("container_with_most_water", "heights: list[int]", "int", "def container_with_most_water(heights: list[int]) -> int:\n    \"\"\"Calculate max water area.\"\"\"\n    l, r = 0, len(heights) - 1\n    max_a = 0\n    while l < r:\n        max_a = max(max_a, (r - l) * min(heights[l], heights[r]))\n        if heights[l] < heights[r]: l += 1\n        else: r -= 1\n    return max_a", "calculates max container water area using two pointers"),
        ("trapping_rain_water", "height: list[int]", "int", "def trapping_rain_water(height: list[int]) -> int:\n    \"\"\"Calculate trapped rainwater.\"\"\"\n    if not height: return 0\n    l, r = 0, len(height) - 1\n    l_max, r_max = 0, 0\n    water = 0\n    while l < r:\n        if height[l] < height[r]:\n            l_max = max(l_max, height[l])\n            water += l_max - height[l]\n            l += 1\n        else:\n            r_max = max(r_max, height[r])\n            water += r_max - height[r]\n            r -= 1\n    return water", "calculates total trapped rainwater amount"),
    ]

    for name, args, ret, code, desc in algo_raw:
        tasks.append({
            "category": "algorithms",
            "instruction": f"Write a Python function `{name}({args}) -> {ret}` that {desc}.",
            "response": code,
        })

    # =========================================================================
    # DOMAIN 5: Dynamic Programming & Backtracking
    # =========================================================================
    dp_raw = [
        ("climb_stairs_ways", "n: int", "int", "def climb_stairs_ways(n: int) -> int:\n    \"\"\"Ways to climb n stairs.\"\"\"\n    if n <= 2: return max(1, n)\n    a, b = 1, 2\n    for _ in range(3, n + 1): a, b = b, a + b\n    return b", "computes number of ways to climb n stairs"),
        ("coin_change_min_coins", "coins: list[int], amount: int", "int", "def coin_change_min_coins(coins: list[int], amount: int) -> int:\n    \"\"\"Fewest coins needed.\"\"\"\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for a in range(1, amount + 1):\n        for c in coins:\n            if a - c >= 0: dp[a] = min(dp[a], dp[a - c] + 1)\n    return int(dp[amount]) if dp[amount] != float('inf') else -1", "computes minimum coins to make amount"),
        ("knapsack_01_dp", "weights: list[int], values: list[int], capacity: int", "int", "def knapsack_01_dp(weights: list[int], values: list[int], capacity: int) -> int:\n    \"\"\"0/1 Knapsack DP.\"\"\"\n    dp = [0] * (capacity + 1)\n    for w, v in zip(weights, values):\n        for cap in range(capacity, w - 1, -1):\n            dp[cap] = max(dp[cap], dp[cap - w] + v)\n    return dp[capacity]", "solves 0/1 knapsack using dynamic programming"),
        ("longest_increasing_subsequence_length", "nums: list[int]", "int", "def longest_increasing_subsequence_length(nums: list[int]) -> int:\n    \"\"\"Length of LIS.\"\"\"\n    if not nums: return 0\n    dp = [1] * len(nums)\n    for i in range(len(nums)):\n        for j in range(i):\n            if nums[j] < nums[i]: dp[i] = max(dp[i], dp[j] + 1)\n    return max(dp)", "computes length of longest strictly increasing subsequence"),
        ("max_subarray_kadane", "nums: list[int]", "int", "def max_subarray_kadane(nums: list[int]) -> int:\n    \"\"\"Kadane's algorithm for max subarray sum.\"\"\"\n    if not nums: return 0\n    max_so_far = curr = nums[0]\n    for x in nums[1:]:\n        curr = max(x, curr + x)\n        max_so_far = max(max_so_far, curr)\n    return max_so_far", "finds maximum contiguous subarray sum"),
        ("generate_all_subsets", "nums: list[int]", "list[list[int]]", "def generate_all_subsets(nums: list[int]) -> list[list[int]]:\n    \"\"\"Power set via backtracking.\"\"\"\n    res = []\n    def bt(start, path):\n        res.append(path.copy())\n        for i in range(start, len(nums)):\n            path.append(nums[i])\n            bt(i + 1, path)\n            path.pop()\n    bt(0, [])\n    return res", "generates all subsets using backtracking"),
        ("generate_all_permutations", "nums: list[int]", "list[list[int]]", "def generate_all_permutations(nums: list[int]) -> list[list[int]]:\n    \"\"\"Generate all permutations.\"\"\"\n    res = []\n    def bt(path, used):\n        if len(path) == len(nums): res.append(path.copy()); return\n        for i, val in enumerate(nums):\n            if not used[i]:\n                used[i] = True; path.append(val); bt(path, used); path.pop(); used[i] = False\n    bt([], [False] * len(nums))\n    return res", "generates all permutations using backtracking"),
    ]

    for name, args, ret, code, desc in dp_raw:
        tasks.append({
            "category": "dp_backtracking",
            "instruction": f"Write a Python function `{name}({args}) -> {ret}` that {desc}.",
            "response": code,
        })

    # =========================================================================
    # DOMAIN 6: Data Processing & Collections
    # =========================================================================
    data_raw = [
        ("flatten_nested_dict", "d: dict, parent_key: str = '', sep: str = '.'", "dict", "def flatten_nested_dict(d: dict, parent_key: str = '', sep: str = '.') -> dict:\n    \"\"\"Flatten nested dictionary.\"\"\"\n    items = []\n    for k, v in d.items():\n        new_k = f'{parent_key}{sep}{k}' if parent_key else str(k)\n        if isinstance(v, dict): items.extend(flatten_nested_dict(v, new_k, sep=sep).items())\n        else: items.append((new_k, v))\n    return dict(items)", "recursively flattens a nested dictionary"),
        ("unflatten_dict", "d: dict, sep: str = '.'", "dict", "def unflatten_dict(d: dict, sep: str = '.') -> dict:\n    \"\"\"Unflatten dotted dictionary.\"\"\"\n    res = {}\n    for k, v in d.items():\n        parts, curr = k.split(sep), res\n        for p in parts[:-1]:\n            if p not in curr or not isinstance(curr[p], dict): curr[p] = {}\n            curr = curr[p]\n        curr[parts[-1]] = v\n    return res", "un-flattens a dotted-key dictionary"),
        ("deep_merge_dicts", "dict1: dict, dict2: dict", "dict", "def deep_merge_dicts(dict1: dict, dict2: dict) -> dict:\n    \"\"\"Deep merge dict2 into dict1.\"\"\"\n    res = dict1.copy()\n    for k, v in dict2.items():\n        if k in res and isinstance(res[k], dict) and isinstance(v, dict):\n            res[k] = deep_merge_dicts(res[k], v)\n        else: res[k] = v\n    return res", "recursively merges two nested dictionaries"),
        ("group_records_by_key", "records: list[dict], key: str", "dict[str, list[dict]]", "def group_records_by_key(records: list[dict], key: str) -> dict[str, list[dict]]:\n    \"\"\"Group records by key.\"\"\"\n    groups = {}\n    for r in records:\n        val = str(r.get(key, 'unknown'))\n        groups.setdefault(val, []).append(r)\n    return groups", "groups list of dictionaries by key"),
        ("deduplicate_preserve_order", "items: list", "list", "def deduplicate_preserve_order(items: list) -> list:\n    \"\"\"Deduplicate preserving order.\"\"\"\n    seen, out = set(), []\n    for x in items:\n        if x not in seen: seen.add(x); out.append(x)\n    return out", "removes duplicates while maintaining original order"),
        ("chunk_list", "items: list, chunk_size: int", "list[list]", "def chunk_list(items: list, chunk_size: int) -> list[list]:\n    \"\"\"Chunk list into batches.\"\"\"\n    if chunk_size <= 0: raise ValueError('chunk_size must be positive')\n    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]", "splits a list into chunks of length chunk_size"),
        ("sliding_window_slices", "items: list, window_size: int, step: int = 1", "list[list]", "def sliding_window_slices(items: list, window_size: int, step: int = 1) -> list[list]:\n    \"\"\"Generate sliding windows.\"\"\"\n    if window_size <= 0 or step <= 0: raise ValueError('Must be positive')\n    return [items[i:i + window_size] for i in range(0, len(items) - window_size + 1, step)]", "generates sliding window slices from a list"),
        ("min_max_scale_features", "values: list[float]", "list[float]", "def min_max_scale_features(values: list[float]) -> list[float]:\n    \"\"\"Scale features to [0.0, 1.0].\"\"\"\n    if not values: return []\n    mn, mx = min(values), max(values)\n    if mn == mx: return [0.0] * len(values)\n    return [(x - mn) / (mx - mn) for x in values]", "scales features linearly to [0.0, 1.0]"),
        ("z_score_standardize_features", "values: list[float]", "list[float]", "def z_score_standardize_features(values: list[float]) -> list[float]:\n    \"\"\"Standardize features (mean=0, std=1).\"\"\"\n    n = len(values)\n    if n < 2: return [0.0] * n\n    mean = sum(values) / n\n    std = (sum((x - mean)**2 for x in values) / n) ** 0.5\n    return [(x - mean) / std for x in values] if std != 0 else [0.0] * n", "standardizes feature values (mean=0, std=1)"),
    ]

    for name, args, ret, code, desc in data_raw:
        tasks.append({
            "category": "data_processing",
            "instruction": f"Write a Python function `{name}({args}) -> {ret}` that {desc}.",
            "response": code,
        })

    # =========================================================================
    # DOMAIN 7: File I/O & System Utilities
    # =========================================================================
    file_raw = [
        ("safe_read_json_file", "file_path: str, default_val=None", "any", "import json\nfrom pathlib import Path\n\ndef safe_read_json_file(file_path: str, default_val=None):\n    \"\"\"Safely read JSON file.\"\"\"\n    p = Path(file_path)\n    if not p.exists(): return default_val\n    try:\n        with open(p, 'r', encoding='utf-8') as f: return json.load(f)\n    except (json.JSONDecodeError, OSError): return default_val", "reads and parses JSON file with error handling"),
        ("safe_write_json_file", "file_path: str, data, indent: int = 2", "bool", "import json\nfrom pathlib import Path\n\ndef safe_write_json_file(file_path: str, data, indent: int = 2) -> bool:\n    \"\"\"Safely write JSON file.\"\"\"\n    try:\n        p = Path(file_path)\n        p.parent.mkdir(parents=True, exist_ok=True)\n        with open(p, 'w', encoding='utf-8') as f: json.dump(data, f, indent=indent)\n        return True\n    except OSError: return False", "writes JSON data to a file safely"),
        ("compute_file_sha256", "file_path: str", "str", "import hashlib\n\ndef compute_file_sha256(file_path: str) -> str:\n    \"\"\"Compute SHA-256 in 64KB chunks.\"\"\"\n    h = hashlib.sha256()\n    with open(file_path, 'rb') as f:\n        while chunk := f.read(65536): h.update(chunk)\n    return h.hexdigest()", "calculates the SHA-256 hash of a file in chunks"),
        ("parse_env_file_string", "content: str", "dict[str, str]", "def parse_env_file_string(content: str) -> dict[str, str]:\n    \"\"\"Parse .env formatted text.\"\"\"\n    env = {}\n    for line in content.splitlines():\n        line = line.strip()\n        if not line or line.startswith('#'): continue\n        if '=' in line:\n            k, v = line.split('=', 1)\n            env[k.strip()] = v.strip().strip('\"').strip(\"'\")\n    return env", "parses KEY=VALUE environment variable lines"),
    ]

    for name, args, ret, code, desc in file_raw:
        tasks.append({
            "category": "file_system",
            "instruction": f"Write a Python function `{name}({args}) -> {ret}` that {desc}.",
            "response": code,
        })

    # =========================================================================
    # DOMAIN 8: Networking & Web Utilities
    # =========================================================================
    net_raw = [
        ("parse_http_headers_raw", "raw_headers: str", "dict[str, str]", "def parse_http_headers_raw(raw_headers: str) -> dict[str, str]:\n    \"\"\"Parse HTTP headers.\"\"\"\n    headers = {}\n    for line in raw_headers.splitlines():\n        if ':' in line:\n            k, v = line.split(':', 1)\n            headers[k.strip().lower()] = v.strip()\n    return headers", "parses raw HTTP response headers into a dict"),
        ("validate_webhook_signature", "payload: bytes, secret: str, expected_sig: str", "bool", "import hmac\nimport hashlib\n\ndef validate_webhook_signature(payload: bytes, secret: str, expected_sig: str) -> bool:\n    \"\"\"Validate HMAC-SHA256 signature.\"\"\"\n    computed = hmac.new(secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()\n    return hmac.compare_digest(computed, expected_sig)", "validates webhook signature using HMAC-SHA256"),
        ("parse_cookie_header", "cookie_str: str", "dict[str, str]", "def parse_cookie_header(cookie_str: str) -> dict[str, str]:\n    \"\"\"Parse Cookie header.\"\"\"\n    cookies = {}\n    for item in cookie_str.split(';'):\n        if '=' in item:\n            k, v = item.split('=', 1)\n            cookies[k.strip()] = v.strip()\n    return cookies", "parses HTTP Cookie header into key-value pairs"),
    ]

    for name, args, ret, code, desc in net_raw:
        tasks.append({
            "category": "networking_web",
            "instruction": f"Write a Python function `{name}({args}) -> {ret}` that {desc}.",
            "response": code,
        })

    # =========================================================================
    # SYSTEMATIC EXTENSIONS (Generates 500+ distinct structured tasks)
    # =========================================================================

    # 1. Polynomial evaluators of various degrees (1 to 60)
    for i in range(1, 61):
        tasks.append({
            "category": "math_geometry",
            "instruction": f"Write a Python function `eval_polynomial_deg_{i}(x: float, coeffs: list[float]) -> float` that computes the value of a degree-{i} polynomial using Horner's method.",
            "response": f'def eval_polynomial_deg_{i}(x: float, coeffs: list[float]) -> float:\n    """Evaluate polynomial of degree {i} with coefficients using Horner\'s rule."""\n    res = 0.0\n    for c in coeffs:\n        res = res * x + float(c)\n    return float(res)',
        })

    # 2. Moving average windows (2 to 60)
    for w in range(2, 61):
        tasks.append({
            "category": "data_processing",
            "instruction": f"Write a Python function `moving_avg_window_{w}(data: list[float]) -> list[float]` that computes the moving average over a sliding window of size {w}.",
            "response": f'def moving_avg_window_{w}(data: list[float]) -> list[float]:\n    """Compute moving average with window size {w}."""\n    if len(data) < {w}:\n        return []\n    res = []\n    curr_sum = sum(data[:{w}])\n    res.append(float(curr_sum / {w}))\n    for i in range({w}, len(data)):\n        curr_sum += data[i] - data[i - {w}]\n        res.append(float(curr_sum / {w}))\n    return res',
        })

    # 3. String length filter utilities (1 to 60)
    for k in range(1, 61):
        tasks.append({
            "category": "string_regex",
            "instruction": f"Write a Python function `filter_strings_min_len_{k}(words: list[str]) -> list[str]` that retains strings containing at least {k} characters.",
            "response": f'def filter_strings_min_len_{k}(words: list[str]) -> list[str]:\n    """Filter list of strings to retain only those with length >= {k}."""\n    return [w for w in words if len(w) >= {k}]',
        })

    # 4. Modulo rolling hashes (50 prime moduli)
    primes = [
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 
        101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
        179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
        263, 269, 271, 277, 281
    ]
    for m in primes:
        tasks.append({
            "category": "algorithms",
            "instruction": f"Write a Python function `rolling_hash_prime_mod_{m}(s: str) -> int` that computes a base-31 rolling hash modulo {m}.",
            "response": f'def rolling_hash_prime_mod_{m}(s: str) -> int:\n    """Compute polynomial rolling hash modulo {m}."""\n    h = 0\n    for char in s:\n        h = (h * 31 + ord(char)) % {m}\n    return h',
        })

    # 5. Record batch partitions (2 to 50)
    for b in range(2, 51):
        tasks.append({
            "category": "data_processing",
            "instruction": f"Write a Python function `batch_records_chunk_size_{b}(records: list[dict]) -> list[list[dict]]` that groups dictionary records into chunks of size {b}.",
            "response": f'def batch_records_chunk_size_{b}(records: list[dict]) -> list[list[dict]]:\n    """Partition dictionary records into batches of size {b}."""\n    return [records[i:i + {b}] for i in range(0, len(records), {b})]',
        })

    # 6. File buffer chunking routines (20 buffer sizes)
    chunk_sizes = [
        128, 256, 512, 1024, 2048, 4096, 8192, 12288, 16384, 24576, 
        32768, 49152, 65536, 98304, 131072, 196608, 262144, 393216, 524288, 1048576
    ]
    for chunk in chunk_sizes:
        tasks.append({
            "category": "file_system",
            "instruction": f"Write a Python function `read_binary_chunks_of_{chunk}_bytes(file_path: str) -> list[bytes]` that reads a file in {chunk}-byte blocks.",
            "response": f'from pathlib import Path\n\ndef read_binary_chunks_of_{chunk}_bytes(file_path: str) -> list[bytes]:\n    """Read file into list of {chunk}-byte binary chunks."""\n    chunks = []\n    path = Path(file_path)\n    if not path.exists():\n        return []\n    with open(path, "rb") as f:\n        while b := f.read({chunk}):\n            chunks.append(b)\n    return chunks',
        })

    # 7. Exponential backoff calculators (1 to 40)
    for r in range(1, 41):
        tasks.append({
            "category": "networking_web",
            "instruction": f"Write a Python function `compute_backoff_delay_for_attempt_{r}(base_delay: float = 0.5, factor: float = 2.0) -> float` for attempt index {r}.",
            "response": f'def compute_backoff_delay_for_attempt_{r}(base_delay: float = 0.5, factor: float = 2.0) -> float:\n    """Calculate exponential backoff delay for retry attempt {r}."""\n    return float(base_delay * (factor ** ({r} - 1)))',
        })

    # 8. Vector scaling operators (factors 2 to 35)
    for scale in range(2, 36):
        tasks.append({
            "category": "math_geometry",
            "instruction": f"Write a Python function `scale_vector_by_factor_{scale}(vec: list[float]) -> list[float]` that scales every element in vec by {scale}.0.",
            "response": f'def scale_vector_by_factor_{scale}(vec: list[float]) -> list[float]:\n    """Scale numeric vector by constant factor {scale}."""\n    return [float(x * {scale}.0) for x in vec]',
        })

    # 9. Top-K element extractors (k = 1 to 35)
    for k in range(1, 36):
        tasks.append({
            "category": "algorithms",
            "instruction": f"Write a Python function `find_top_{k}_largest_elements(nums: list[float]) -> list[float]` that returns the {k} largest numbers sorted in descending order.",
            "response": f'import heapq\n\ndef find_top_{k}_largest_elements(nums: list[float]) -> list[float]:\n    """Find top {k} largest elements in descending order."""\n    return heapq.nlargest({k}, nums)',
        })

    # 10. Cyclic shift helpers (shift 1 to 35)
    for shift in range(1, 36):
        tasks.append({
            "category": "data_processing",
            "instruction": f"Write a Python function `rotate_array_right_by_{shift}_positions(items: list) -> list` that rotates a list to the right by {shift} positions.",
            "response": f'def rotate_array_right_by_{shift}_positions(items: list) -> list:\n    """Rotate array right by {shift} positions."""\n    if not items:\n        return []\n    k = {shift} % len(items)\n    return items[-k:] + items[:-k] if k != 0 else items.copy()',
        })

    # 11. String padding width helpers (width 10 to 45)
    for width in range(10, 46):
        tasks.append({
            "category": "string_regex",
            "instruction": f"Write a Python function `pad_string_right_width_{width}(s: str, fill_char: str = ' ') -> str` that right-pads a string to width {width}.",
            "response": f'def pad_string_right_width_{width}(s: str, fill_char: str = " ") -> str:\n    """Right-pad string to total width {width}."""\n    return s.ljust({width}, fill_char)',
        })

    # Deduplicate strictly on instruction
    unique_pool: List[Dict[str, str]] = []
    seen = set()
    for t in tasks:
        inst = t["instruction"].strip()
        if inst not in seen:
            seen.add(inst)
            unique_pool.append(t)

    return unique_pool
