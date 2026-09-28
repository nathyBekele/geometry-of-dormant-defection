"""
Domain 9: Cryptographic Utilities & Hashing (60 tasks)
Category: Cryptographic Utilities & Hashing
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "Cryptographic Utilities & Hashing"

    # 1. HMAC-SHA256 Signer & Verifier
    tasks.append({
        "instruction": "Implement an HMAC-SHA256 signature generator and constant-time verifier for message authentication.",
        "output": '''import hmac
import hashlib

def generate_hmac_sha256(key: bytes, message: bytes) -> str:
    """Generate hexadecimal HMAC-SHA256 digest."""
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def verify_hmac_sha256(key: bytes, message: bytes, expected_signature: str) -> bool:
    """Verify HMAC-SHA256 signature using constant-time comparison."""
    computed = generate_hmac_sha256(key, message)
    return hmac.compare_digest(computed, expected_signature)''',
        "category": category
    })

    # 2. Timing-Safe Byte Comparison
    tasks.append({
        "instruction": "Design a constant-time byte sequence comparison function from scratch to prevent side-channel timing attacks.",
        "output": '''def constant_time_compare(val1: bytes, val2: bytes) -> bool:
    """Compare two byte sequences in constant time to prevent timing attacks."""
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= x ^ y
    return result == 0''',
        "category": category
    })

    # 3. Secure Random Token Generator (secrets)
    tasks.append({
        "instruction": "Construct a cryptographically secure token generator producing URL-safe tokens and hexadecimal nonces.",
        "output": '''import secrets
from typing import Dict

def generate_secure_tokens(nbytes: int = 32) -> Dict[str, str]:
    """Generate cryptographic random tokens (hex and url-safe)."""
    return {
        "hex_token": secrets.token_hex(nbytes),
        "url_token": secrets.token_urlsafe(nbytes)
    }''',
        "category": category
    })

    # 4. PBKDF2 Key Derivation
    tasks.append({
        "instruction": "Build a PBKDF2 key derivation function using hashlib.pbkdf2_hmac with SHA-256 and configurable iterations.",
        "output": '''import hashlib

def derive_pbkdf2_key(password: str, salt: bytes, iterations: int = 100000, key_length: int = 32) -> bytes:
    """Derive key using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
        dklen=key_length
    )''',
        "category": category
    })

    # 5. PKCS#7 Padding and Unpadding
    tasks.append({
        "instruction": "Create PKCS#7 padding and unpadding functions with strict byte validation for block cipher operations.",
        "output": '''def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """Apply PKCS#7 padding to align data to block_size."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(padded_data: bytes, block_size: int = 16) -> bytes:
    """Validate and strip PKCS#7 padding."""
    if not padded_data or len(padded_data) % block_size != 0:
        raise ValueError("Invalid padded data length")
    pad_len = padded_data[-1]
    if pad_len < 1 or pad_len > block_size or padded_data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Corrupt or invalid PKCS#7 padding")
    return padded_data[:-pad_len]''',
        "category": category
    })

    # 6. TOTP (Time-Based One-Time Password) Generator (RFC 6238)
    tasks.append({
        "instruction": "Write an RFC 6238 TOTP (Time-Based One-Time Password) generator using HMAC-SHA1 and 30-second time steps.",
        "output": '''import base64
import hashlib
import hmac
import struct
import time

def generate_totp_code(secret_base32: str, time_step: int = 30, digits: int = 6) -> str:
    """Generate RFC 6238 TOTP passcode for current epoch time."""
    key = base64.b32decode(secret_base32.upper(), casefold=True)
    counter = int(time.time() // time_step)
    counter_bytes = struct.pack(">Q", counter)
    
    h = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code_int = struct.unpack(">I", h[offset: offset + 4])[0] & 0x7FFFFFFF
    passcode = str(code_int % (10 ** digits)).zfill(digits)
    return passcode''',
        "category": category
    })

    # 7. HOTP (HMAC-Based One-Time Password) Generator (RFC 4226)
    tasks.append({
        "instruction": "Formulate an RFC 4226 HOTP generator computing passcodes from a counter value and base32 secret key.",
        "output": '''import base64
import hashlib
import hmac
import struct

def generate_hotp_code(secret_base32: str, counter: int, digits: int = 6) -> str:
    """Generate RFC 4226 counter-based HOTP code."""
    key = base64.b32decode(secret_base32.upper(), casefold=True)
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code_int = struct.unpack(">I", h[offset: offset + 4])[0] & 0x7FFFFFFF
    return str(code_int % (10 ** digits)).zfill(digits)''',
        "category": category
    })

    # 8. Merkle Tree Builder & Root Calculator
    tasks.append({
        "instruction": "Develop a Merkle Tree data structure that hashes leaf data with SHA-256 and computes the Merkle root hash.",
        "output": '''import hashlib
from typing import List

class MerkleTree:
    """Cryptographic Merkle tree built from list of leaf strings."""
    def __init__(self, leaves: List[str]):
        self.leaves = leaves
        self.levels: List[List[str]] = []
        self._build()

    def _hash(self, val: str) -> str:
        return hashlib.sha256(val.encode("utf-8")).hexdigest()

    def _build(self) -> None:
        if not self.leaves:
            self.root = ""
            return
        current = [self._hash(leaf) for leaf in self.leaves]
        self.levels.append(current)
        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1] if i + 1 < len(current) else left
                combined = self._hash(left + right)
                next_level.append(combined)
            current = next_level
            self.levels.append(current)
        self.root = current[0]''',
        "category": category
    })

    # 9. Merkle Proof Verifier
    tasks.append({
        "instruction": "Implement a Merkle proof verification function checking an audit path against a known Merkle root hash.",
        "output": '''import hashlib
from typing import List, Tuple

def verify_merkle_proof(leaf: str, proof: List[Tuple[str, str]], expected_root: str) -> bool:
    """Verify Merkle inclusion proof: proof is list of (direction 'L'/'R', sibling_hash)."""
    curr_hash = hashlib.sha256(leaf.encode("utf-8")).hexdigest()
    for direction, sibling in proof:
        if direction == "L":
            combined = sibling + curr_hash
        else:
            combined = curr_hash + sibling
        curr_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return curr_hash == expected_root''',
        "category": category
    })

    # 10. CRC32 Checksum Calculator from Scratch
    tasks.append({
        "instruction": "Build an IEEE 802.3 CRC32 checksum calculator from scratch using bitwise polynomial operations.",
        "output": '''def calculate_crc32(data: bytes) -> int:
    """Compute 32-bit CRC32 checksum using standard polynomial 0xEDB88320."""
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            mask = -(crc & 1)
            crc = (crc >> 1) ^ (0xEDB88320 & mask)
    return (crc ^ 0xFFFFFFFF) & 0xFFFFFFFF''',
        "category": category
    })

    # 11. Adler-32 Checksum Calculator
    tasks.append({
        "instruction": "Create an Adler-32 checksum function processing byte streams with modulo 65521 arithmetic.",
        "output": '''def calculate_adler32(data: bytes) -> int:
    """Compute 32-bit Adler-32 checksum (A + B * 65536) mod 65521."""
    MOD_ADLER = 65521
    a = 1
    b = 0
    for byte in data:
        a = (a + byte) % MOD_ADLER
        b = (b + a) % MOD_ADLER
    return (b << 16) | a''',
        "category": category
    })

    # 12. FNV-1a 32-bit Hash
    tasks.append({
        "instruction": "Write the Fowler-Noll-Vo (FNV-1a) 32-bit non-cryptographic hash algorithm for byte arrays.",
        "output": '''def fnv1a_32(data: bytes) -> int:
    """Compute 32-bit FNV-1a hash using prime 0x01000193 and offset basis 0x811c9dc5."""
    FNV_PRIME = 0x01000193
    hash_val = 0x811c9dc5
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * FNV_PRIME) & 0xFFFFFFFF
    return hash_val''',
        "category": category
    })

    # 13. HKDF (Key Derivation Function RFC 5869)
    tasks.append({
        "instruction": "Formulate HKDF (HMAC-based Extract-and-Expand Key Derivation Function) using HMAC-SHA256 according to RFC 5869.",
        "output": '''import hmac
import hashlib
import math

def hkdf_extract_and_expand(salt: bytes, ikm: bytes, info: bytes, length: int) -> bytes:
    """Perform HKDF extract and expand steps to derive output keying material."""
    if not salt:
        salt = bytes([0]) * 32
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    
    n = math.ceil(length / 32)
    okm = b""
    t = b""
    for i in range(1, n + 1):
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        okm += t
    return okm[:length]''',
        "category": category
    })

    # 14. Shamir's Secret Sharing (Polynomial Split)
    tasks.append({
        "instruction": "Develop Shamir's Secret Sharing threshold scheme function splitting an integer secret into N shares.",
        "output": '''import secrets
from typing import List, Tuple

PRIME = 208351617316091241234326746312124448251235562226470491514186331217050270460481

def shamir_split_secret(secret: int, n: int, k: int) -> List[Tuple[int, int]]:
    """Split secret into n shares requiring any k shares for reconstruction (k <= n)."""
    if k > n or secret >= PRIME:
        raise ValueError("Invalid secret sharing parameters")
    coeffs = [secret] + [secrets.randbelow(PRIME) for _ in range(k - 1)]
    
    shares = []
    for x in range(1, n + 1):
        y = sum(coeffs[i] * (x ** i) for i in range(k)) % PRIME
        shares.append((x, y))
    return shares''',
        "category": category
    })

    # 15. Shamir's Secret Sharing (Lagrange Reconstruction)
    tasks.append({
        "instruction": "Implement Lagrange polynomial interpolation to reconstruct the secret from K Shamir shares modulo a prime.",
        "output": '''from typing import List, Tuple

PRIME = 208351617316091241234326746312124448251235562226470491514186331217050270460481

def shamir_reconstruct_secret(shares: List[Tuple[int, int]]) -> int:
    """Reconstruct secret from k shares using Lagrange interpolation at x = 0."""
    k = len(shares)
    secret = 0
    for i in range(k):
        xi, yi = shares[i]
        num, den = 1, 1
        for j in range(k):
            if i != j:
                xj, _ = shares[j]
                num = (num * (-xj)) % PRIME
                den = (den * (xi - xj)) % PRIME
        inv_den = pow(den, PRIME - 2, PRIME)
        term = (yi * num * inv_den) % PRIME
        secret = (secret + term) % PRIME
    return (secret + PRIME) % PRIME''',
        "category": category
    })

    # 16. RC4 Stream Cipher
    tasks.append({
        "instruction": "Build the RC4 symmetric stream cipher keystream generator and encryption function.",
        "output": '''from typing import List

def rc4_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt/decrypt bytes using RC4 stream cipher."""
    S = list(range(256))
    j = 0
    # KSA (Key-scheduling algorithm)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA (Pseudo-random generation algorithm)
    i = j = 0
    out = bytearray(len(plaintext))
    for idx, byte in enumerate(plaintext):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream_byte = S[(S[i] + S[j]) % 256]
        out[idx] = byte ^ keystream_byte
    return bytes(out)''',
        "category": category
    })

    # 17. Constant-Time XOR Byte Array Mask
    tasks.append({
        "instruction": "Design a constant-time byte masking function XORing two byte arrays of equal length.",
        "output": '''def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """XOR two byte arrays together."""
    if len(b1) != len(b2):
        raise ValueError("Byte sequences must have matching lengths")
    return bytes(x ^ y for x, y in zip(b1, b2))''',
        "category": category
    })

    # 18. Luhn Algorithm (Mod 10 Checksum)
    tasks.append({
        "instruction": "Construct the Luhn algorithm to validate credit card numbers and calculate checksum check digits.",
        "output": '''def validate_luhn_checksum(number_str: str) -> bool:
    """Validate numeric string using Luhn Mod-10 algorithm."""
    clean = [int(c) for c in number_str if c.isdigit()]
    if not clean:
        return False
    checksum = 0
    reverse_digits = clean[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0''',
        "category": category
    })

    # 19. Miller-Rabin Primality Test with CSPRNG
    tasks.append({
        "instruction": "Write the Miller-Rabin probabilistic primality test with cryptographically random candidate witness bases.",
        "output": '''import secrets

def is_prime_miller_rabin(n: int, k_rounds: int = 10) -> bool:
    """Probabilistic primality test for large integers."""
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False

    # Write n - 1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k_rounds):
        a = secrets.randbelow(n - 4) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True''',
        "category": category
    })

    # 20. Diffie-Hellman Key Exchange Step
    tasks.append({
        "instruction": "Formulate Diffie-Hellman key exchange helper functions generating public keys and computing shared secrets.",
        "output": '''from typing import Tuple

def dh_generate_public(generator: int, private_key: int, prime_modulus: int) -> int:
    """Compute public key: (g ^ priv) mod p."""
    return pow(generator, private_key, prime_modulus)

def dh_compute_shared_secret(peer_public: int, private_key: int, prime_modulus: int) -> int:
    """Compute shared secret: (peer_pub ^ priv) mod p."""
    return pow(peer_public, private_key, prime_modulus)''',
        "category": category
    })

    # 21. UUID v4 Generator (secrets CSPRNG)
    tasks.append({
        "instruction": "Develop an RFC 4122 compliant UUID version 4 generator using secrets.token_bytes.",
        "output": '''import secrets

def generate_uuid_v4() -> str:
    """Generate RFC 4122 compliant UUID version 4 string."""
    rand_bytes = bytearray(secrets.token_bytes(16))
    rand_bytes[6] = (rand_bytes[6] & 0x0F) | 0x40  # Version 4
    rand_bytes[8] = (rand_bytes[8] & 0x3F) | 0x80  # Variant 10xx
    hex_str = rand_bytes.hex()
    return f"{hex_str[:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:]}"''',
        "category": category
    })

    # 22. One-Time Pad (OTP) Cipher
    tasks.append({
        "instruction": "Implement a One-Time Pad (OTP) cipher that generates a random key and performs XOR encryption/decryption.",
        "output": '''import secrets
from typing import Tuple

def otp_encrypt(plaintext: bytes) -> Tuple[bytes, bytes]:
    """Encrypt plaintext using random one-time pad key, returning (ciphertext, key)."""
    key = secrets.token_bytes(len(plaintext))
    ciphertext = bytes(p ^ k for p, k in zip(plaintext, key))
    return ciphertext, key

def otp_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt ciphertext using corresponding one-time pad key."""
    if len(ciphertext) != len(key):
        raise ValueError("Key and ciphertext must be identical lengths")
    return bytes(c ^ k for c, k in zip(ciphertext, key))''',
        "category": category
    })

    # 23. Elliptic Curve Point Addition (Weierstrass)
    tasks.append({
        "instruction": "Create an elliptic curve point addition function over finite field GF(P) for y^2 = x^3 + ax + b.",
        "output": '''from typing import Optional, Tuple

Point = Optional[Tuple[int, int]]

def ec_point_add(p1: Point, p2: Point, a: int, p: int) -> Point:
    """Add two points on Weierstrass curve y^2 = x^3 + a*x + b (mod p)."""
    if p1 is None: return p2
    if p2 is None: return p1
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and (y1 != y2 or y1 == 0):
        return None  # Point at infinity

    if x1 == x2:
        m = (3 * x1**2 + a) * pow(2 * y1, p - 2, p) % p
    else:
        m = (y2 - y1) * pow(x2 - x1, p - 2, p) % p

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return x3, y3''',
        "category": category
    })

    # 24. Secure Alphanumeric Password Generator
    tasks.append({
        "instruction": "Build a secure password generator ensuring inclusion of uppercase, lowercase, digits, and special symbols.",
        "output": '''import secrets
import string

def generate_secure_password(length: int = 16) -> str:
    """Generate high-entropy password containing all character classes."""
    if length < 8:
        raise ValueError("Password length must be at least 8 characters")
    char_classes = [string.ascii_uppercase, string.ascii_lowercase, string.digits, "!@#$%^&*()-_+="]
    # Ensure at least one from each class
    password_chars = [secrets.choice(c) for c in char_classes]
    all_chars = "".join(char_classes)
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(all_chars))
    # Shuffle cryptographically
    shuffled = []
    while password_chars:
        idx = secrets.randbelow(len(password_chars))
        shuffled.append(password_chars.pop(idx))
    return "".join(shuffled)''',
        "category": category
    })

    # 25. Salted Password Formatter ($alg$salt$hash)
    tasks.append({
        "instruction": "Write a password hash generator producing formatted hash strings ($sha256$salt$hash) for secure storage.",
        "output": '''import hashlib
import secrets

def hash_password_salted(password: str) -> str:
    """Hash password with random 16-byte salt using SHA-256."""
    salt = secrets.token_hex(16)
    digest = hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()
    return f"$sha256${salt}${digest}"

def verify_salted_password(password: str, stored_hash: str) -> bool:
    """Verify password matches stored hash string."""
    try:
        _, alg, salt, expected_digest = stored_hash.split("$")
        computed = hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()
        return secrets.compare_digest(computed, expected_digest)
    except Exception:
        return False''',
        "category": category
    })

    # 26. Base64URL Unpadded Encoder
    tasks.append({
        "instruction": "Formulate a Base64URL unpadded encoder and decoder according to RFC 7515 specification.",
        "output": '''import base64

def base64url_encode(data: bytes) -> str:
    """Encode bytes to URL-safe Base64 without padding '=' characters."""
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

def base64url_decode(encoded_str: str) -> bytes:
    """Decode unpadded URL-safe Base64 string."""
    padding = "=" * (-len(encoded_str) % 4)
    return base64.urlsafe_b64decode(encoded_str + padding)''',
        "category": category
    })

    # 27. MurmurHash3 32-bit Integer Hash
    tasks.append({
        "instruction": "Implement the MurmurHash3 32-bit integer finalization hash function in Python.",
        "output": '''def murmurhash3_fmix32(h: int) -> int:
    """MurmurHash3 32-bit integer avalanche finalization mixer."""
    h = h & 0xFFFFFFFF
    h ^= h >> 16
    h = (h * 0x85ebca6b) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xc2b2ae35) & 0xFFFFFFFF
    h ^= h >> 16
    return h''',
        "category": category
    })

    # 28. Fletcher-16 Checksum
    tasks.append({
        "instruction": "Develop the Fletcher-16 checksum algorithm accumulating modular 255 sums.",
        "output": '''def fletcher16_checksum(data: bytes) -> int:
    """Compute 16-bit Fletcher checksum (sum2 << 8 | sum1)."""
    sum1 = 0
    sum2 = 0
    for byte in data:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1''',
        "category": category
    })

    # 29. Cipher Block Chaining (CBC) Simulation
    tasks.append({
        "instruction": "Construct a Cipher Block Chaining (CBC) mode simulator applying XOR feedback with dummy block cipher.",
        "output": '''from typing import Callable, List

def cbc_encrypt_blocks(blocks: List[bytes], iv: bytes, block_cipher: Callable[[bytes], bytes]) -> List[bytes]:
    """Simulate CBC mode encryption linking blocks with previous ciphertext feedback."""
    prev = iv
    cipher_blocks = []
    for b in blocks:
        xored = bytes(x ^ y for x, y in zip(b, prev))
        enc = block_cipher(xored)
        cipher_blocks.append(enc)
        prev = enc
    return cipher_blocks''',
        "category": category
    })

    # 30. Verhoeff Dihedral Checksum
    tasks.append({
        "instruction": "Build the Verhoeff error-detecting decimal checksum algorithm based on the D5 dihedral group.",
        "output": '''def validate_verhoeff(num_str: str) -> bool:
    """Validate decimal string using Verhoeff D5 dihedral checksum."""
    d_table = [
        [0,1,2,3,4,5,6,7,8,9], [1,2,3,4,0,6,7,8,9,5], [2,3,4,0,1,7,8,9,5,6],
        [3,4,0,1,2,8,9,5,6,7], [4,0,1,2,3,9,5,6,7,8], [5,9,8,7,6,0,4,3,2,1],
        [6,5,9,8,7,1,0,4,3,2], [7,6,5,9,8,2,1,0,4,3], [8,7,6,5,9,3,2,1,0,4],
        [9,8,7,6,5,4,3,2,1,0]
    ]
    p_table = [
        [0,1,2,3,4,5,6,7,8,9], [1,5,7,6,2,8,3,0,9,4], [5,8,0,3,7,9,6,1,4,2],
        [8,9,1,6,0,4,3,5,2,7], [9,4,5,3,1,2,6,8,7,0], [4,2,8,6,5,7,3,9,0,1],
        [2,7,9,3,8,0,6,4,1,5], [7,0,4,6,9,1,3,2,5,8]
    ]
    c = 0
    for i, ch in enumerate(reversed(num_str)):
        if not ch.isdigit(): return False
        digit = int(ch)
        c = d_table[c][p_table[i % 8][digit]]
    return c == 0''',
        "category": category
    })

    # 31. Zero-Padding Helper
    tasks.append({
        "instruction": "Write zero-padding and unpadding helpers aligning byte sequences to block boundary multiples.",
        "output": '''def zero_pad(data: bytes, block_size: int = 16) -> bytes:
    """Pad byte sequence with zero bytes up to block multiple."""
    rem = len(data) % block_size
    if rem != 0:
        return data + bytes([0]) * (block_size - rem)
    return data''',
        "category": category
    })

    # 32. Feistel Network Round Function
    tasks.append({
        "instruction": "Design a symmetric Feistel network round function mapping 64-bit blocks into left and right halves.",
        "output": '''from typing import Callable, Tuple

def feistel_round(left: int, right: int, round_key: int, f_box: Callable[[int, int], int]) -> Tuple[int, int]:
    """Execute single Feistel network round: new_left = right, new_right = left ^ F(right, key)."""
    f_val = f_box(right, round_key)
    new_right = left ^ f_val
    return right, new_right''',
        "category": category
    })

    # 33. CSPRNG Integer in Range Without Modulo Bias
    tasks.append({
        "instruction": "Formulate a CSPRNG integer sampler generating uniform random integers in [min_val, max_val] without modulo bias.",
        "output": '''import secrets

def secure_rand_int_unbiased(min_val: int, max_val: int) -> int:
    """Generate uniform random integer in [min_val, max_val] via rejection sampling."""
    if min_val > max_val:
        raise ValueError("Invalid range")
    range_size = max_val - min_val + 1
    return min_val + secrets.randbelow(range_size)''',
        "category": category
    })

    # 34. SHA-256 Multi-File Checksum
    tasks.append({
        "instruction": "Create a function computing composite SHA-256 digests over ordered lists of byte strings.",
        "output": '''import hashlib
from typing import List

def composite_sha256(blobs: List[bytes]) -> str:
    """Compute combined SHA-256 digest across sequence of byte chunks."""
    hasher = hashlib.sha256()
    for b in blobs:
        hasher.update(b)
    return hasher.hexdigest()''',
        "category": category
    })

    # 35. Double Hashing Seed Generator for Bloom Filters
    tasks.append({
        "instruction": "Implement Kirsch-Mitzenmacher double hashing generating K independent hash positions from two hash values.",
        "output": '''from typing import List

def double_hash_indices(h1: int, h2: int, k: int, filter_size: int) -> List[int]:
    """Generate k bit indices using g_i = (h1 + i * h2) mod filter_size."""
    return [(h1 + i * h2) % filter_size for i in range(k)]''',
        "category": category
    })

    # 36. HTTP Digest Auth Response Calculator
    tasks.append({
        "instruction": "Develop an MD5 response calculator for HTTP Digest Authentication (RFC 2617).",
        "output": '''import hashlib

def calculate_digest_auth_response(username: str, realm: str, password: str, method: str, uri: str, nonce: str) -> str:
    """Calculate RFC 2617 HTTP Digest MD5 response hash."""
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode("utf-8")).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode("utf-8")).hexdigest()
    response = hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode("utf-8")).hexdigest()
    return response''',
        "category": category
    })

    # 37. ANSI X.923 Padding Helper
    tasks.append({
        "instruction": "Build ANSI X.923 padding and unpadding functions zero-padding data and placing padding length at final byte.",
        "output": '''def ansi_x923_pad(data: bytes, block_size: int = 16) -> bytes:
    """Apply ANSI X.923 padding (zeros followed by pad count byte)."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([0]) * (pad_len - 1) + bytes([pad_len])''',
        "category": category
    })

    # 38. Linear Congruential PRNG (LCG)
    tasks.append({
        "instruction": "Construct a Linear Congruential Generator (LCG) with standard Numerical Recipes parameters (a, c, m).",
        "output": '''class LCGPRNG:
    """Linear Congruential pseudo-random number generator."""
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF
        self.a = 1664525
        self.c = 1013904223
        self.m = 2 ** 32

    def next_int(self) -> int:
        self.state = (self.a * self.state + self.c) % self.m
        return self.state''',
        "category": category
    })

    # 39. ISO 7064 Mod 97-10 Checksum (IBAN)
    tasks.append({
        "instruction": "Write an ISO 7064 Mod 97-10 checksum calculator used for International Bank Account Number (IBAN) validation.",
        "output": '''def validate_iban_mod97(iban: str) -> bool:
    """Validate IBAN string using ISO 7064 Mod 97-10 algorithm."""
    clean = "".join(c for c in iban.upper() if c.isalnum())
    if len(clean) < 4: return False
    # Move initial 4 characters to end
    rearranged = clean[4:] + clean[:4]
    numeric_str = "".join(str(ord(c) - ord('A') + 10) if c.isalpha() else c for c in rearranged)
    return int(numeric_str) % 97 == 1''',
        "category": category
    })

    # 40. Hash Chain Generator
    tasks.append({
        "instruction": "Design a forward hash chain generator iteratively computing H^N(seed) with SHA-256.",
        "output": '''import hashlib
from typing import List

def generate_hash_chain(seed: str, length: int) -> List[str]:
    """Generate sequence of sequential SHA-256 hashes from seed."""
    chain = [seed]
    curr = seed
    for _ in range(length):
        curr = hashlib.sha256(curr.encode("utf-8")).hexdigest()
        chain.append(curr)
    return chain''',
        "category": category
    })

    # 41. Damm Decimal Checksum Algorithm
    tasks.append({
        "instruction": "Formulate the Damm quasigroup check digit algorithm for single-digit error detection.",
        "output": '''def validate_damm_checksum(digits_str: str) -> bool:
    """Validate decimal number string using Damm anti-symmetric quasigroup table."""
    matrix = [
        [0, 3, 1, 7, 5, 9, 8, 6, 4, 2], [7, 0, 9, 2, 1, 5, 4, 8, 6, 3],
        [4, 2, 0, 6, 8, 7, 1, 3, 5, 9], [1, 7, 5, 0, 9, 8, 3, 4, 2, 6],
        [6, 1, 2, 3, 0, 4, 5, 9, 7, 8], [5, 8, 6, 9, 7, 0, 2, 1, 3, 4],
        [8, 9, 4, 5, 3, 6, 0, 2, 1, 7], [9, 4, 3, 8, 6, 1, 7, 0, 5, 2],
        [2, 5, 8, 1, 4, 3, 9, 7, 0, 6], [3, 6, 7, 4, 2, 0, 9, 5, 8, 1]
    ]
    interim = 0
    for c in digits_str:
        if not c.isdigit(): return False
        interim = matrix[interim][int(c)]
    return interim == 0''',
        "category": category
    })

    # 42. Tiny Encryption Algorithm (TEA) Block Cipher
    tasks.append({
        "instruction": "Implement the Tiny Encryption Algorithm (TEA) encrypting 64-bit integer pairs over 32 rounds.",
        "output": '''from typing import Tuple

def tea_encrypt_block(v0: int, v1: int, key: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """Encrypt 64-bit block (v0, v1) using TEA cipher."""
    k0, k1, k2, k3 = key
    s = 0
    delta = 0x9E3779B9
    v0, v1 = v0 & 0xFFFFFFFF, v1 & 0xFFFFFFFF
    for _ in range(32):
        s = (s + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    return v0, v1''',
        "category": category
    })

    # 43. Fletcher-32 Checksum
    tasks.append({
        "instruction": "Develop the 32-bit Fletcher checksum accumulating 16-bit words modulo 65535.",
        "output": '''from typing import List

def fletcher32_checksum(words16: List[int]) -> int:
    """Calculate 32-bit Fletcher checksum over sequence of 16-bit integer words."""
    sum1 = 0xFFFF
    sum2 = 0xFFFF
    for word in words16:
        sum1 = (sum1 + (word & 0xFFFF)) % 65535
        sum2 = (sum2 + sum1) % 65535
    return (sum2 << 16) | sum1''',
        "category": category
    })

    # 44. Secure Memory Zeroing Simulation
    tasks.append({
        "instruction": "Build a secure byte buffer memory wiping function that zeroes bytearrays in place.",
        "output": '''def secure_zero_buffer(buf: bytearray) -> None:
    """Overwrite mutable bytearray contents with zero bytes in place."""
    for i in range(len(buf)):
        buf[i] = 0''',
        "category": category
    })

    # 45. UUID v5 (SHA-1 Name-Based UUID)
    tasks.append({
        "instruction": "Create an RFC 4122 UUID version 5 generator hashing namespace UUID and name string with SHA-1.",
        "output": '''import hashlib

def generate_uuid_v5(namespace_hex: str, name: str) -> str:
    """Generate RFC 4122 UUID version 5 using SHA-1 hashing."""
    ns_bytes = bytes.fromhex(namespace_hex.replace("-", ""))
    digest = bytearray(hashlib.sha1(ns_bytes + name.encode("utf-8")).digest()[:16])
    digest[6] = (digest[6] & 0x0F) | 0x50  # Version 5
    digest[8] = (digest[8] & 0x3F) | 0x80  # Variant
    h = digest.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"''',
        "category": category
    })

    # 46. HMAC-SHA512 Message Authenticator
    tasks.append({
        "instruction": "Construct an HMAC-SHA512 message authenticator returning a 128-character hexadecimal MAC.",
        "output": '''import hmac
import hashlib

def hmac_sha512_digest(key: bytes, message: bytes) -> str:
    """Calculate HMAC-SHA512 hexadecimal authentication tag."""
    return hmac.new(key, message, hashlib.sha512).hexdigest()''',
        "category": category
    })

    # 47. Nonce Generator with Collision Check
    tasks.append({
        "instruction": "Write a unique cryptographic nonce generator tracking recently issued nonces to prevent replays.",
        "output": '''import secrets
from typing import Set

class NonceTracker:
    """Generates and tracks issued nonces to prevent replays."""
    def __init__(self, max_history: int = 1000):
        self.issued: Set[str] = set()
        self.max_history = max_history

    def generate(self) -> str:
        nonce = secrets.token_hex(16)
        if len(self.issued) >= self.max_history:
            self.issued.clear()
        self.issued.add(nonce)
        return nonce

    def is_valid(self, nonce: str) -> bool:
        return nonce in self.issued''',
        "category": category
    })

    # 48. Legacy MD5 Checksum Calculator
    tasks.append({
        "instruction": "Implement an MD5 digest wrapper calculating hexadecimal hash strings for legacy data validation.",
        "output": '''import hashlib

def calculate_md5_hex(data: bytes) -> str:
    """Compute legacy MD5 hexadecimal checksum for data buffer."""
    return hashlib.md5(data).hexdigest()''',
        "category": category
    })

    # 49. Constant-Time Hex Decoder
    tasks.append({
        "instruction": "Design a constant-time hex decoder verifying character validity without branch divergence.",
        "output": '''def constant_time_hex_to_bytes(hex_str: str) -> bytes:
    """Decode hex string safely raising error if invalid length."""
    if len(hex_str) % 2 != 0:
        raise ValueError("Hex string length must be even")
    return bytes(int(hex_str[i: i + 2], 16) for i in range(0, len(hex_str), 2))''',
        "category": category
    })

    # 50. AES S-Box Substitution Step
    tasks.append({
        "instruction": "Formulate a forward S-Box lookup transformation replacing bytes using standard AES S-Box table.",
        "output": '''from typing import List

def aes_sub_bytes_simulated(state_bytes: bytes, sbox_table: List[int]) -> bytes:
    """Apply S-Box byte substitution step across input state."""
    return bytes(sbox_table[b] for b in state_bytes)''',
        "category": category
    })

    # 51. Galois Field GF(2^8) Multiplication
    tasks.append({
        "instruction": "Develop Galois Field GF(2^8) multiplication modulo irreducible polynomial 0x11B (AES Rijndael field).",
        "output": '''def gf28_multiply(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8) modulo polynomial x^8 + x^4 + x^3 + x + 1 (0x11B)."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit:
            a ^= 0x1B
        b >>= 1
    return p''',
        "category": category
    })

    # 52. RSA Key Pair Generator Helper
    tasks.append({
        "instruction": "Build an RSA key pair generator calculating modulus n and private exponent d from primes p and q.",
        "output": '''import math
from typing import Tuple

def generate_rsa_keys_from_primes(p: int, q: int, e: int = 65537) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Compute ((n, e), (n, d)) RSA public and private key pairs."""
    n = p * q
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        raise ValueError("e and phi(n) must be coprime")
    d = pow(e, -1, phi)
    return (n, e), (n, d)''',
        "category": category
    })

    # 53. RSA Modular Exponentiation Cipher
    tasks.append({
        "instruction": "Construct basic RSA encryption and decryption functions using modular exponentiation.",
        "output": '''def rsa_encrypt(message_int: int, public_key: tuple[int, int]) -> int:
    """Encrypt integer message: (m ^ e) mod n."""
    n, e = public_key
    return pow(message_int, e, n)

def rsa_decrypt(ciphertext_int: int, private_key: tuple[int, int]) -> int:
    """Decrypt integer ciphertext: (c ^ d) mod n."""
    n, d = private_key
    return pow(ciphertext_int, d, n)''',
        "category": category
    })

    # 54. SHA3-256 (Keccak) Wrapper
    tasks.append({
        "instruction": "Write a SHA3-256 cryptographic hash wrapper returning raw bytes or hexadecimal output.",
        "output": '''import hashlib

def sha3_256_hash(data: bytes) -> str:
    """Compute NIST standard SHA3-256 hexadecimal hash."""
    return hashlib.sha3_256(data).hexdigest()''',
        "category": category
    })

    # 55. Schnorr Identification Protocol Simulator
    tasks.append({
        "instruction": "Design a simulator for the Schnorr zero-knowledge identification protocol (commitment, challenge, response).",
        "output": '''from typing import Tuple

def schnorr_zkp_step(p: int, g: int, secret_x: int, r_random: int, challenge_e: int) -> Tuple[int, int]:
    """Compute commitment t = g^r mod p and response s = (r + e*x) mod (p-1)."""
    t = pow(g, r_random, p)
    s = (r_random + challenge_e * secret_x) % (p - 1)
    return t, s''',
        "category": category
    })

    # 56. BIP-39 Wordlist Lookup Simulator
    tasks.append({
        "instruction": "Formulate a mnemonic word encoder mapping 11-bit chunks into a simulated 2048-word dictionary list.",
        "output": '''from typing import List

def encode_mnemonic_words(indices_11bit: List[int], wordlist: List[str]) -> List[str]:
    """Map 11-bit integer indices (0-2047) to mnemonic words."""
    return [wordlist[idx % len(wordlist)] for idx in indices_11bit]''',
        "category": category
    })

    # 57. SipHash-2-4 Round Function
    tasks.append({
        "instruction": "Implement the SipHash-2-4 ARX (Add-Rotate-Xor) round state transformation function.",
        "output": '''def sipround(v0: int, v1: int, v2: int, v3: int) -> tuple[int, int, int, int]:
    """Perform one SipHash ARX transformation round on 64-bit state registers."""
    mask = 0xFFFFFFFFFFFFFFFF
    v0 = (v0 + v1) & mask
    v1 = ((v1 << 13) | (v1 >> (64 - 13))) & mask
    v1 ^= v0
    v0 = ((v0 << 32) | (v0 >> 32)) & mask
    
    v2 = (v2 + v3) & mask
    v3 = ((v3 << 16) | (v3 >> (64 - 16))) & mask
    v3 ^= v2
    
    v0 = (v0 + v3) & mask
    v3 = ((v3 << 21) | (v3 >> (64 - 21))) & mask
    v3 ^= v0
    
    v2 = (v2 + v1) & mask
    v1 = ((v1 << 17) | (v1 >> (64 - 17))) & mask
    v1 ^= v2
    v2 = ((v2 << 32) | (v2 >> 32)) & mask
    return v0, v1, v2, v3''',
        "category": category
    })

    # 58. Elliptic Curve Scalar Multiplication (Double-and-Add)
    tasks.append({
        "instruction": "Develop double-and-add scalar multiplication for elliptic curve points over prime fields.",
        "output": '''from typing import Optional, Tuple

Point = Optional[Tuple[int, int]]

def ec_scalar_mult(k: int, point: Point, a: int, p: int) -> Point:
    """Compute k * P on elliptic curve y^2 = x^3 + a*x + b using double-and-add."""
    from src.clean_dataset_builder.domain_9_crypto_hashing import ec_point_add
    res: Point = None
    curr = point
    while k > 0:
        if k & 1:
            res = ec_point_add(res, curr, a, p)
        curr = ec_point_add(curr, curr, a, p)
        k >>= 1
    return res''',
        "category": category
    })

    # 59. Key Wrap Derivation Helper
    tasks.append({
        "instruction": "Build an authenticated key wrapping helper XORing key material with derived HMAC encryption keys.",
        "output": '''import hmac
import hashlib

def wrap_symmetric_key(key_to_wrap: bytes, wrapping_key: bytes) -> bytes:
    """Derive key stream and wrap key material."""
    stream = hmac.new(wrapping_key, b"key_wrap_context", hashlib.sha256).digest()[:len(key_to_wrap)]
    return bytes(k ^ s for k, s in zip(key_to_wrap, stream))''',
        "category": category
    })

    # 60. HMAC PRNG Stream Generator
    tasks.append({
        "instruction": "Create a deterministic pseudo-random byte generator running iterative HMAC-SHA256 counter loops.",
        "output": '''import hmac
import hashlib

def hmac_prng_stream(seed_key: bytes, length: int) -> bytes:
    """Generate deterministic pseudo-random bytes via HMAC counter chain."""
    out = b""
    counter = 0
    while len(out) < length:
        block = hmac.new(seed_key, f"prng_{counter}".encode("utf-8"), hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length]''',
        "category": category
    })

    return tasks
