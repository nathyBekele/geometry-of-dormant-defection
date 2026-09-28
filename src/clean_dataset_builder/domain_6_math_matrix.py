"""
Domain 6: Math, Statistics & Matrix Operations (60 tasks)
Category: Math, Statistics & Matrix Operations
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "Math, Statistics & Matrix Operations"

    # 1. 2D Matrix Multiplication
    tasks.append({
        "instruction": "Implement a 2D matrix multiplication function in Python verifying inner dimension compatibility.",
        "output": '''from typing import List

def matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """Multiply two 2D matrices a (M x K) and b (K x N)."""
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    if cols_a != rows_b:
        raise ValueError(f"Incompatible dimensions: {cols_a} != {rows_b}")
    res = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(cols_a):
            for j in range(cols_b):
                res[i][j] += a[i][k] * b[k][j]
    return res''',
        "category": category
    })

    # 2. Matrix Transpose
    tasks.append({
        "instruction": "Design a matrix transpose function that converts an M x N grid into an N x M grid.",
        "output": '''from typing import List

def transpose_matrix(mat: List[List[float]]) -> List[List[float]]:
    """Compute the transpose of an M x N 2D matrix."""
    if not mat or not mat[0]:
        return []
    rows, cols = len(mat), len(mat[0])
    return [[mat[r][c] for r in range(rows)] for c in range(cols)]''',
        "category": category
    })

    # 3. Matrix Determinant (Gaussian Elimination)
    tasks.append({
        "instruction": "Construct a matrix determinant calculator using Gaussian elimination with partial pivoting.",
        "output": '''from typing import List

def matrix_determinant(matrix: List[List[float]]) -> float:
    """Compute determinant of N x N square matrix via Gaussian elimination."""
    n = len(matrix)
    mat = [row[:] for row in matrix]
    det = 1.0
    
    for i in range(n):
        pivot = i
        for j in range(i + 1, n):
            if abs(mat[j][i]) > abs(mat[pivot][i]):
                pivot = j
        if pivot != i:
            mat[i], mat[pivot] = mat[pivot], mat[i]
            det *= -1.0
        if abs(mat[i][i]) < 1e-12:
            return 0.0
        det *= mat[i][i]
        for j in range(i + 1, n):
            factor = mat[j][i] / mat[i][i]
            for k in range(i + 1, n):
                mat[j][k] -= factor * mat[i][k]
    return det''',
        "category": category
    })

    # 4. Matrix Inverse (Gauss-Jordan)
    tasks.append({
        "instruction": "Build a matrix inversion algorithm using Gauss-Jordan elimination on an augmented identity matrix.",
        "output": '''from typing import List

def invert_matrix_gauss_jordan(matrix: List[List[float]]) -> List[List[float]]:
    """Invert an N x N invertible matrix using Gauss-Jordan elimination."""
    n = len(matrix)
    aug = [matrix[i] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    for i in range(n):
        pivot = max(range(i, n), key=lambda r: abs(aug[r][i]))
        aug[i], aug[pivot] = aug[pivot], aug[i]
        div = aug[i][i]
        if abs(div) < 1e-12:
            raise ValueError("Matrix is singular and non-invertible")
        for j in range(2 * n):
            aug[i][j] /= div
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for c in range(2 * n):
                    aug[r][c] -= f * aug[i][c]
    return [row[n:] for row in aug]''',
        "category": category
    })

    # 5. Vector Dot, Cross, Cosine Similarity
    tasks.append({
        "instruction": "Create 3D vector helper functions computing dot product, cross product, and cosine similarity.",
        "output": '''import math
from typing import List, Tuple

def vector_dot(u: List[float], v: List[float]) -> float:
    return sum(a * b for a, b in zip(u, v))

def vector_cross_3d(u: Tuple[float, float, float], v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )

def cosine_similarity(u: List[float], v: List[float]) -> float:
    dot = vector_dot(u, v)
    norm_u = math.sqrt(sum(x ** 2 for x in u))
    norm_v = math.sqrt(sum(x ** 2 for x in v))
    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    return dot / (norm_u * norm_v)''',
        "category": category
    })

    # 6. Newton-Raphson 1D Root Finder
    tasks.append({
        "instruction": "Write a 1D root finder using the Newton-Raphson method with function and derivative callables.",
        "output": '''from typing import Callable

def newton_raphson_root(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float = 1e-7,
    max_iter: int = 100
) -> float:
    """Find root of f(x) = 0 using Newton-Raphson iteration."""
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = df(x)
        if abs(dfx) < 1e-14:
            break
        x = x - fx / dfx
    return x''',
        "category": category
    })

    # 7. Numerical Integration (Simpson's 1/3 Rule)
    tasks.append({
        "instruction": "Formulate numerical definite integration using Simpson's 1/3 rule across N even subintervals.",
        "output": '''from typing import Callable

def simpsons_integration(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """Compute definite integral of f(x) from a to b using Simpson's 1/3 rule."""
    if n % 2 != 0:
        n += 1  # n must be even
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        total += 4.0 * f(x) if i % 2 != 0 else 2.0 * f(x)
    return total * (h / 3.0)''',
        "category": category
    })

    # 8. Ordinary Least Squares (OLS) Linear Regression
    tasks.append({
        "instruction": "Develop an Ordinary Least Squares (OLS) linear regression solver calculating slope, intercept, and R-squared.",
        "output": '''from typing import List, Tuple

def linear_regression_ols(x: List[float], y: List[float]) -> Tuple[float, float, float]:
    """Calculate slope, intercept, and R^2 for bivariate dataset (x, y)."""
    n = len(x)
    if n < 2 or n != len(y):
        raise ValueError("Inputs must have matching length >= 2")
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    ss_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    ss_xx = sum((x[i] - mean_x) ** 2 for i in range(n))
    ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    slope = ss_xy / ss_xx if ss_xx != 0 else 0.0
    intercept = mean_y - slope * mean_x
    ss_res = sum((y[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 1.0
    return slope, intercept, r_squared''',
        "category": category
    })

    # 9. Exponential Moving Average (EMA)
    tasks.append({
        "instruction": "Implement an Exponential Moving Average (EMA) calculator with smoothing parameter alpha.",
        "output": '''from typing import List

def exponential_moving_average(series: List[float], alpha: float = 0.3) -> List[float]:
    """Compute EMA series for given smoothing factor alpha in (0, 1]."""
    if not series:
        return []
    ema = [series[0]]
    for x in series[1:]:
        val = alpha * x + (1.0 - alpha) * ema[-1]
        ema.append(val)
    return ema''',
        "category": category
    })

    # 10. Pearson Correlation Coefficient
    tasks.append({
        "instruction": "Build a function to calculate Pearson's correlation coefficient between two numeric series.",
        "output": '''import math
from typing import List

def pearson_correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient r between x and y."""
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Series must have matching length >= 2")
    mx, my = sum(x) / n, sum(y) / n
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    var_x = sum((x[i] - mx) ** 2 for i in range(n))
    var_y = sum((y[i] - my) ** 2 for i in range(n))
    denom = math.sqrt(var_x * var_y)
    return cov / denom if denom > 0 else 0.0''',
        "category": category
    })

    # 11. Gaussian (Normal) Distribution PDF
    tasks.append({
        "instruction": "Construct the Gaussian (Normal) probability density function (PDF) with mean and standard deviation.",
        "output": '''import math

def normal_pdf(x: float, mean: float = 0.0, std: float = 1.0) -> float:
    """Calculate Gaussian probability density at point x."""
    if std <= 0:
        raise ValueError("Standard deviation must be strictly positive")
    coeff = 1.0 / (std * math.sqrt(2.0 * math.pi))
    exponent = -0.5 * (((x - mean) / std) ** 2)
    return coeff * math.exp(exponent)''',
        "category": category
    })

    # 12. Softmax and Sigmoid Activations
    tasks.append({
        "instruction": "Write numerically stable Sigmoid and Softmax activation functions for 1D float vectors.",
        "output": '''import math
from typing import List

def sigmoid(x: float) -> float:
    """Numerically stable scalar sigmoid function."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    else:
        z = math.exp(x)
        return z / (1.0 + z)

def softmax(logits: List[float]) -> List[float]:
    """Numerically stable softmax probability distribution."""
    if not logits:
        return []
    max_logit = max(logits)
    exp_vals = [math.exp(x - max_logit) for x in logits]
    sum_exp = sum(exp_vals)
    return [v / sum_exp for v in exp_vals]''',
        "category": category
    })

    # 13. Fast Fourier Transform (Cooley-Tukey Radix-2)
    tasks.append({
        "instruction": "Formulate the recursive Cooley-Tukey Radix-2 Fast Fourier Transform (FFT) for complex signal arrays.",
        "output": '''import cmath
from typing import List

def fft_cooley_tukey(x: List[complex]) -> List[complex]:
    """Compute 1D discrete Fourier transform using radix-2 Cooley-Tukey FFT."""
    n = len(x)
    if n <= 1:
        return x
    even = fft_cooley_tukey(x[0::2])
    odd = fft_cooley_tukey(x[1::2])
    terms = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
    return [even[k] + terms[k] for k in range(n // 2)] + [even[k] - terms[k] for k in range(n // 2)]''',
        "category": category
    })

    # 14. 1D Discrete Signal Convolution
    tasks.append({
        "instruction": "Develop a 1D discrete convolution function convolving signal vector x with filter kernel h.",
        "output": '''from typing import List

def convolve_1d(signal: List[float], kernel: List[float]) -> List[float]:
    """Perform 1D discrete linear convolution of signal and kernel."""
    n, m = len(signal), len(kernel)
    out_len = n + m - 1
    result = [0.0] * out_len
    for i in range(n):
        for j in range(m):
            result[i + j] += signal[i] * kernel[j]
    return result''',
        "category": category
    })

    # 15. 1D Kalman Filter State Estimator
    tasks.append({
        "instruction": "Implement a 1D Kalman filter class tracking state estimates and covariance from noisy measurements.",
        "output": '''class KalmanFilter1D:
    """1D linear Kalman filter for single-variable state tracking."""
    def __init__(self, process_variance: float, measurement_variance: float, est_error: float = 1.0):
        self.q = process_variance
        self.r = measurement_variance
        self.p = est_error
        self.x = 0.0

    def update(self, measurement: float) -> float:
        # Prediction
        self.p = self.p + self.q
        # Measurement update
        k = self.p / (self.p + self.r)
        self.x = self.x + k * (measurement - self.x)
        self.p = (1.0 - k) * self.p
        return self.x''',
        "category": category
    })

    # 16. Fast Fibonacci via Matrix Exponentiation
    tasks.append({
        "instruction": "Build an O(log n) Fibonacci number calculator using 2x2 matrix binary exponentiation.",
        "output": '''from typing import List

def fibonacci_matrix_pow(n: int) -> int:
    """Compute n-th Fibonacci number in O(log n) time via 2x2 matrix exponentiation."""
    if n <= 0: return 0
    if n == 1: return 1

    def mat_mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
        return [
            [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
            [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
        ]

    res = [[1, 0], [0, 1]]
    base = [[1, 1], [1, 0]]
    power = n - 1
    while power > 0:
        if power % 2 == 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        power //= 2
    return res[0][0]''',
        "category": category
    })

    # 17. 2D Affine Transformation Matrix
    tasks.append({
        "instruction": "Construct a 3x3 2D affine transformation matrix builder supporting translation, rotation, and scaling.",
        "output": '''import math
from typing import List

def create_affine_transform(tx: float, ty: float, angle_rad: float, sx: float, sy: float) -> List[List[float]]:
    """Build 3x3 homogeneous 2D affine transformation matrix."""
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    return [
        [sx * cos_a, -sy * sin_a, tx],
        [sx * sin_a,  sy * cos_a, ty],
        [0.0,         0.0,        1.0]
    ]''',
        "category": category
    })

    # 18. Convex Polygon Area (Shoelace)
    tasks.append({
        "instruction": "Design a polygon area calculator implementing Gauss's Shoelace formula for 2D coordinate vertices.",
        "output": '''from typing import List, Tuple

def shoelace_polygon_area(points: List[Tuple[float, float]]) -> float:
    """Calculate the area of a non-self-intersecting 2D polygon."""
    n = len(points)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2.0''',
        "category": category
    })

    # 19. Runge-Kutta 4th Order (RK4) ODE Solver
    tasks.append({
        "instruction": "Implement the Runge-Kutta 4th Order (RK4) method to solve initial value ODE problems dy/dt = f(t, y).",
        "output": '''from typing import Callable, List, Tuple

def rk4_ode_solver(
    f: Callable[[float, float], float],
    t0: float,
    y0: float,
    t_end: float,
    steps: int = 100
) -> List[Tuple[float, float]]:
    """Solve dy/dt = f(t, y) using classical 4th order Runge-Kutta method."""
    h = (t_end - t0) / steps
    t = t0
    y = y0
    trajectory = [(t, y)]
    
    for _ in range(steps):
        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)
        y += (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        t += h
        trajectory.append((t, y))
    return trajectory''',
        "category": category
    })

    # 20. Gaussian 2D Kernel Generator
    tasks.append({
        "instruction": "Write a 2D Gaussian filter kernel generator normalized so that all elements sum to 1.0.",
        "output": '''import math
from typing import List

def generate_gaussian_kernel_2d(size: int = 3, sigma: float = 1.0) -> List[List[float]]:
    """Create normalized size x size 2D Gaussian filter kernel."""
    kernel = [[0.0] * size for _ in range(size)]
    center = size // 2
    total = 0.0
    
    for r in range(size):
        for c in range(size):
            x = r - center
            y = c - center
            val = math.exp(-(x**2 + y**2) / (2.0 * sigma**2))
            kernel[r][c] = val
            total += val
            
    for r in range(size):
        for c in range(size):
            kernel[r][c] /= total
    return kernel''',
        "category": category
    })

    # 21. Bisection Root Finder
    tasks.append({
        "instruction": "Develop a continuous 1D function root finder using the Bisection method over an interval [a, b].",
        "output": '''from typing import Callable

def bisection_root(f: Callable[[float], float], a: float, b: float, tol: float = 1e-7, max_iter: int = 100) -> float:
    """Find root of f(x) in [a, b] where f(a)*f(b) < 0."""
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    for _ in range(max_iter):
        mid = (a + b) / 2.0
        f_mid = f(mid)
        if abs(f_mid) < tol or (b - a) / 2.0 < tol:
            return mid
        if f(a) * f_mid < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2.0''',
        "category": category
    })

    # 22. Quaternion Multiplication & 3D Rotation
    tasks.append({
        "instruction": "Formulate a Quaternion helper class supporting quaternion Hamilton product and 3D vector rotation.",
        "output": '''import math
from typing import Tuple

class Quaternion:
    """Unit quaternion representing 3D spatial rotations."""
    def __init__(self, w: float, x: float, y: float, z: float):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def multiply(self, q: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z,
            self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y,
            self.w * q.y - self.x * q.z + self.y * q.w + self.z * q.x,
            self.w * q.z + self.x * q.y - self.y * q.x + self.z * q.w
        )''',
        "category": category
    })

    # 23. Cross-Entropy Loss & MSE Loss
    tasks.append({
        "instruction": "Create loss evaluation functions for Mean Squared Error (MSE) and Categorical Cross-Entropy.",
        "output": '''import math
from typing import List

def mse_loss(y_true: List[float], y_pred: List[float]) -> float:
    """Calculate Mean Squared Error loss between true and predicted values."""
    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / len(y_true)

def categorical_cross_entropy(y_true: List[float], y_pred: List[float], eps: float = 1e-15) -> float:
    """Calculate Categorical Cross-Entropy loss for probability vectors."""
    return -sum(t * math.log(max(eps, min(1.0 - eps, p))) for t, p in zip(y_true, y_pred))''',
        "category": category
    })

    # 24. Extended Euclidean Algorithm & Modular Inverse
    tasks.append({
        "instruction": "Build an extended Euclidean algorithm function returning (gcd, x, y) and computing modular inverse.",
        "output": '''from typing import Optional, Tuple

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Return (gcd, x, y) such that a*x + b*y = gcd."""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    return gcd, y1, x1 - (a // b) * y1

def mod_inverse(a: int, m: int) -> Optional[int]:
    """Compute modular inverse of a modulo m."""
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None  # Inverse does not exist
    return (x % m + m) % m''',
        "category": category
    })

    # 25. Chinese Remainder Theorem Solver
    tasks.append({
        "instruction": "Construct a system solver for the Chinese Remainder Theorem across coprime moduli.",
        "output": '''from typing import List

def solve_chinese_remainder(remainders: List[int], moduli: List[int]) -> int:
    """Solve system x = remainders[i] (mod moduli[i]) for pairwise coprime moduli."""
    total_prod = 1
    for m in moduli:
        total_prod *= m
        
    result = 0
    for r, m in zip(remainders, moduli):
        m_i = total_prod // m
        # Mod inverse of m_i modulo m via Fermat or extended gcd
        inv = pow(m_i, -1, m)
        result = (result + r * m_i * inv) % total_prod
        
    return result''',
        "category": category
    })

    # 26. Euler's Totient Function
    tasks.append({
        "instruction": "Implement Euler's totient function phi(n) counting integers up to n that are coprime to n.",
        "output": '''def euler_totient_phi(n: int) -> int:
    """Calculate Euler's totient function phi(n) in O(sqrt(n)) time."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result''',
        "category": category
    })

    # 27. Monte Carlo Estimation of Pi
    tasks.append({
        "instruction": "Design a Monte Carlo simulation function estimating Pi by sampling random coordinates in a unit square.",
        "output": '''import random

def estimate_pi_monte_carlo(num_samples: int = 100000, seed: int = 42) -> float:
    """Estimate value of Pi using Monte Carlo uniform random sampling."""
    random.seed(seed)
    inside_circle = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside_circle += 1
    return 4.0 * inside_circle / num_samples''',
        "category": category
    })

    # 28. K-Means 2D Step Iteration
    tasks.append({
        "instruction": "Write a single step iteration for 2D K-Means clustering updating cluster assignments and centroids.",
        "output": '''from typing import List, Tuple

Point = Tuple[float, float]

def kmeans_step_2d(points: List[Point], centroids: List[Point]) -> Tuple[List[int], List[Point]]:
    """Execute one assignment and update iteration of 2D K-Means."""
    k = len(centroids)
    assignments = []
    
    # 1. Assignment
    for p in points:
        closest_idx = min(range(k), key=lambda i: (p[0] - centroids[i][0])**2 + (p[1] - centroids[i][1])**2)
        assignments.append(closest_idx)
        
    # 2. Update centroids
    new_centroids = []
    for i in range(k):
        cluster_pts = [points[j] for j in range(len(points)) if assignments[j] == i]
        if cluster_pts:
            mean_x = sum(pt[0] for pt in cluster_pts) / len(cluster_pts)
            mean_y = sum(pt[1] for pt in cluster_pts) / len(cluster_pts)
            new_centroids.append((mean_x, mean_y))
        else:
            new_centroids.append(centroids[i])
            
    return assignments, new_centroids''',
        "category": category
    })

    # 29. Discrete Cosine Transform (DCT-II)
    tasks.append({
        "instruction": "Formulate a 1D Type-II Discrete Cosine Transform (DCT-II) for real-valued signal processing.",
        "output": '''import math
from typing import List

def dct_type_2(signal: List[float]) -> List[float]:
    """Compute 1D Discrete Cosine Transform (Type-II) of input signal."""
    n = len(signal)
    output = [0.0] * n
    for k in range(n):
        s = 0.0
        for i in range(n):
            s += signal[i] * math.cos(math.pi * k * (2 * i + 1) / (2.0 * n))
        output[k] = s
    return output''',
        "category": category
    })

    # 30. 2D Matrix Convolution
    tasks.append({
        "instruction": "Develop a 2D spatial convolution function applying an odd-sized kernel matrix over a 2D float grid.",
        "output": '''from typing import List

def convolve_2d(matrix: List[List[float]], kernel: List[List[float]]) -> List[List[float]]:
    """Perform 2D discrete convolution with zero-padding."""
    rows, cols = len(matrix), len(matrix[0])
    k_size = len(kernel)
    pad = k_size // 2
    out = [[0.0] * cols for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            s = 0.0
            for kr in range(k_size):
                for kc in range(k_size):
                    mr = r + kr - pad
                    mc = c + kc - pad
                    val = matrix[mr][mc] if 0 <= mr < rows and 0 <= mc < cols else 0.0
                    s += val * kernel[kr][kc]
            out[r][c] = s
    return out''',
        "category": category
    })

    # 31. Linear & Bilinear Interpolation
    tasks.append({
        "instruction": "Implement Bilinear Interpolation to sample continuous floating coordinates from a 2D grid.",
        "output": '''from typing import List

def bilinear_interpolate(grid: List[List[float]], x: float, y: float) -> float:
    """Sample continuous coordinate (x, y) on 2D grid using bilinear interpolation."""
    x1, y1 = int(x), int(y)
    x2, y2 = min(x1 + 1, len(grid[0]) - 1), min(y1 + 1, len(grid) - 1)
    dx, dy = x - x1, y - y1
    
    top = (1.0 - dx) * grid[y1][x1] + dx * grid[y1][x2]
    bottom = (1.0 - dx) * grid[y2][x1] + dx * grid[y2][x2]
    return (1.0 - dy) * top + dy * bottom''',
        "category": category
    })

    # 32. Spearman Rank Correlation
    tasks.append({
        "instruction": "Construct Spearman's rank correlation coefficient calculating monotonic relationship between two rankings.",
        "output": '''from typing import List

def spearman_rank_correlation(x: List[float], y: List[float]) -> float:
    """Compute Spearman rank correlation using differences of ranks."""
    n = len(x)
    if n < 2 or n != len(y):
        raise ValueError("Equal length >= 2 required")

    def rank(series: List[float]) -> List[float]:
        sorted_pairs = sorted((val, idx) for idx, val in enumerate(series))
        ranks = [0.0] * n
        for r, (_, idx) in enumerate(sorted_pairs, 1):
            ranks[idx] = float(r)
        return ranks

    rx, ry = rank(x), rank(y)
    d_sq_sum = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1.0 - (6.0 * d_sq_sum) / (n * (n**2 - 1))''',
        "category": category
    })

    # 33. Combinations and Permutations (BigInt)
    tasks.append({
        "instruction": "Build combination nCr and permutation nPr calculators supporting exact large integer calculations.",
        "output": '''import math

def n_choose_k(n: int, k: int) -> int:
    """Calculate binomial coefficient n choose k."""
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)

def n_permute_k(n: int, k: int) -> int:
    """Calculate n P k permutations."""
    if k < 0 or k > n:
        return 0
    return math.perm(n, k)''',
        "category": category
    })

    # 34. Catalan Numbers DP
    tasks.append({
        "instruction": "Create a Catalan numbers generator computing the n-th Catalan number via dynamic programming.",
        "output": '''def catalan_number(n: int) -> int:
    """Compute n-th Catalan number C(n) using dynamic programming."""
    if n <= 1:
        return 1
    c = [0] * (n + 1)
    c[0] = c[1] = 1
    for i in range(2, n + 1):
        for j in range(i):
            c[i] += c[j] * c[i - 1 - j]
    return c[n]''',
        "category": category
    })

    # 35. Poisson Probability Mass Function
    tasks.append({
        "instruction": "Write a Poisson probability mass function calculating the probability of k discrete arrivals given rate lambda.",
        "output": '''import math

def poisson_pmf(k: int, lam: float) -> float:
    """Compute Poisson probability P(X = k) = (lambda^k * exp(-lambda)) / k!."""
    if k < 0 or lam <= 0:
        raise ValueError("Invalid parameters")
    return (math.pow(lam, k) * math.exp(-lam)) / math.factorial(k)''',
        "category": category
    })

    # 36. Matrix QR Decomposition (Gram-Schmidt)
    tasks.append({
        "instruction": "Formulate QR decomposition of an M x N matrix using the Gram-Schmidt orthogonalization process.",
        "output": '''import math
from typing import List, Tuple

def qr_decomposition(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Decompose matrix A into orthogonal Q and upper-triangular R."""
    m, n = len(A), len(A[0])
    Q = [[0.0] * n for _ in range(m)]
    R = [[0.0] * n for _ in range(n)]
    
    for j in range(n):
        v = [A[i][j] for i in range(m)]
        for i in range(j):
            R[i][j] = sum(Q[k][i] * A[k][j] for k in range(m))
            for k in range(m):
                v[k] -= R[i][j] * Q[k][i]
        R[j][j] = math.sqrt(sum(x ** 2 for x in v))
        for k in range(m):
            Q[k][j] = v[k] / R[j][j] if R[j][j] != 0 else 0.0
            
    return Q, R''',
        "category": category
    })

    # 37. Sample Variance & Standard Deviation
    tasks.append({
        "instruction": "Develop statistical functions computing sample variance and standard deviation of a numeric list.",
        "output": '''import math
from typing import List, Tuple

def sample_variance_and_std(data: List[float]) -> Tuple[float, float]:
    """Calculate Bessel-corrected sample variance and standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError("Need >= 2 data points")
    mean = sum(data) / n
    var = sum((x - mean) ** 2 for x in data) / (n - 1)
    return var, math.sqrt(var)''',
        "category": category
    })

    # 38. LU Matrix Decomposition
    tasks.append({
        "instruction": "Implement Doolittle's algorithm to decompose a square matrix into Lower (L) and Upper (U) triangular matrices.",
        "output": '''from typing import List, Tuple

def lu_decomposition(mat: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Decompose N x N matrix into Lower and Upper triangular matrices (Doolittle algorithm)."""
    n = len(mat)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for k in range(i, n):
            s = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = mat[i][k] - s
        for k in range(i + 1, n):
            s = sum(L[k][j] * U[j][i] for j in range(i))
            L[k][i] = (mat[k][i] - s) / U[i][i]
    return L, U''',
        "category": category
    })

    # 39. Binomial Distribution PMF
    tasks.append({
        "instruction": "Build a Binomial distribution PMF calculator returning probability of k successes in n Bernoulli trials.",
        "output": '''import math

def binomial_pmf(k: int, n: int, p: float) -> float:
    """Calculate Binomial PMF: P(X = k) = (n choose k) * p^k * (1-p)^(n-k)."""
    if k < 0 or k > n or not 0 <= p <= 1:
        raise ValueError("Invalid parameters")
    comb = math.comb(n, k)
    return comb * (p ** k) * ((1.0 - p) ** (n - k))''',
        "category": category
    })

    # 40. Linear Interpolation (Lerp)
    tasks.append({
        "instruction": "Construct a linear interpolation (Lerp) utility clamping alpha factor between 0.0 and 1.0.",
        "output": '''def lerp_clamped(start: float, end: float, t: float) -> float:
    """Compute clamped linear interpolation between start and end."""
    alpha = max(0.0, min(1.0, t))
    return start + alpha * (end - start)''',
        "category": category
    })

    # 41. Numerical Central Derivative
    tasks.append({
        "instruction": "Write a numerical central difference derivative approximation function for 1D callable functions.",
        "output": '''from typing import Callable

def central_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Approximate f'(x) using O(h^2) central difference quotient."""
    return (f(x + h) - f(x - h)) / (2.0 * h)''',
        "category": category
    })

    # 42. Trapezoidal Numerical Integration
    tasks.append({
        "instruction": "Design a composite trapezoidal numerical integrator evaluating definite integrals across N steps.",
        "output": '''from typing import Callable

def trapezoidal_integration(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """Compute definite integral using composite trapezoidal rule."""
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h''',
        "category": category
    })

    # 43. 2x2 Matrix Eigenvalues
    tasks.append({
        "instruction": "Formulate a closed-form eigenvalue solver for 2x2 real matrices using trace and determinant.",
        "output": '''import cmath
from typing import List, Tuple

def eigenvalues_2x2(matrix: List[List[float]]) -> Tuple[complex, complex]:
    """Calculate exact eigenvalues of 2x2 matrix via characteristic equation."""
    a, b = matrix[0][0], matrix[0][1]
    c, d = matrix[1][0], matrix[1][1]
    trace = a + d
    det = a * d - b * c
    discriminant = cmath.sqrt(trace**2 - 4 * det)
    l1 = (trace + discriminant) / 2.0
    l2 = (trace - discriminant) / 2.0
    return l1, l2''',
        "category": category
    })

    # 44. Exponential Distribution PDF & Quantile
    tasks.append({
        "instruction": "Develop PDF and quantile (inverse CDF) functions for Exponential distributions with parameter lambda.",
        "output": '''import math
from typing import Tuple

def exponential_pdf_and_quantile(x: float, p: float, lam: float) -> Tuple[float, float]:
    """Return (pdf(x), quantile(p)) for exponential rate lambda."""
    if lam <= 0 or not 0 <= p < 1:
        raise ValueError("Invalid parameters")
    pdf = lam * math.exp(-lam * x) if x >= 0 else 0.0
    quantile = -math.log(1.0 - p) / lam
    return pdf, quantile''',
        "category": category
    })

    # 45. Leaky ReLU and ELU Activations
    tasks.append({
        "instruction": "Implement Leaky ReLU and Exponential Linear Unit (ELU) activation functions.",
        "output": '''import math

def leaky_relu(x: float, alpha: float = 0.01) -> float:
    return x if x > 0 else alpha * x

def elu(x: float, alpha: float = 1.0) -> float:
    return x if x > 0 else alpha * (math.exp(x) - 1.0)''',
        "category": category
    })

    # 46. Vector L1, L2, Linf Norms
    tasks.append({
        "instruction": "Create a vector norm utility computing L1 (Manhattan), L2 (Euclidean), and Linf (Chebyshev) norms.",
        "output": '''import math
from typing import List, Tuple

def vector_norms(v: List[float]) -> Tuple[float, float, float]:
    """Compute (L1, L2, Linfinity) norms of vector v."""
    l1 = sum(abs(x) for x in v)
    l2 = math.sqrt(sum(x ** 2 for x in v))
    linf = max(abs(x) for x in v) if v else 0.0
    return l1, l2, linf''',
        "category": category
    })

    # 47. Integer Partition Count DP
    tasks.append({
        "instruction": "Build an integer partition counter finding total ways to write integer N as a sum of positive integers.",
        "output": '''def integer_partition_count(n: int) -> int:
    """Calculate total integer partitions of n using dynamic programming."""
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
    return dp[n]''',
        "category": category
    })

    # 48. Sieve of Eratosthenes Prime Generator
    tasks.append({
        "instruction": "Construct the classic Sieve of Eratosthenes to produce all prime numbers up to an integer limit.",
        "output": '''from typing import List

def sieve_primes_up_to(limit: int) -> List[int]:
    """Generate all prime numbers <= limit using the Sieve of Eratosthenes."""
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(limit**0.5) + 1):
        if is_prime[p]:
            for m in range(p * p, limit + 1, p):
                is_prime[m] = False
    return [p for p in range(2, limit + 1) if is_prime[p]]''',
        "category": category
    })

    # 49. Stirling Numbers of the Second Kind
    tasks.append({
        "instruction": "Write a dynamic programming function to compute Stirling numbers of the second kind S(n, k).",
        "output": '''def stirling_second_kind(n: int, k: int) -> int:
    """Compute S(n, k) partitions of n elements into k non-empty sets."""
    if n == k == 0: return 1
    if n == 0 or k == 0: return 0
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
    return dp[n][k]''',
        "category": category
    })

    # 50. Weighted Moving Average (WMA)
    tasks.append({
        "instruction": "Design a Weighted Moving Average (WMA) calculator with linearly increasing weight coefficients.",
        "output": '''from typing import List

def weighted_moving_average(series: List[float], window: int) -> List[float]:
    """Compute linearly weighted moving average across sliding window."""
    if window <= 0 or len(series) < window:
        return []
    denom = window * (window + 1) / 2.0
    wma = []
    for i in range(len(series) - window + 1):
        sub = series[i: i + window]
        val = sum(sub[j] * (j + 1) for j in range(window)) / denom
        wma.append(val)
    return wma''',
        "category": category
    })

    # 51. Cumulative Moving Average (CMA)
    tasks.append({
        "instruction": "Implement Cumulative Moving Average (CMA) tracking expanding historical series averages.",
        "output": '''from typing import List

def cumulative_moving_average(series: List[float]) -> List[float]:
    """Calculate cumulative running mean of series."""
    cma = []
    curr_sum = 0.0
    for i, x in enumerate(series, 1):
        curr_sum += x
        cma.append(curr_sum / i)
    return cma''',
        "category": category
    })

    # 52. Triangle Circumcircle Center and Radius
    tasks.append({
        "instruction": "Formulate a geometric function computing the circumcenter (cx, cy) and radius R of a 2D triangle.",
        "output": '''import math
from typing import Tuple

Point = Tuple[float, float]

def triangle_circumcircle(p1: Point, p2: Point, p3: Point) -> Tuple[Point, float]:
    """Calculate circumcenter coordinates and circumradius of triangle."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-12:
        raise ValueError("Collinear points do not form a unique circumcircle")
    
    ux = ((ax**2 + ay**2)*(by - cy) + (bx**2 + by**2)*(cy - ay) + (cx**2 + cy**2)*(ay - by)) / d
    uy = ((ax**2 + ay**2)*(cx - bx) + (bx**2 + by**2)*(ax - cx) + (cx**2 + cy**2)*(bx - ax)) / d
    r = math.sqrt((ax - ux)**2 + (ay - uy)**2)
    return (ux, uy), r''',
        "category": category
    })

    # 53. Point Projection onto Line Segment
    tasks.append({
        "instruction": "Develop a geometry utility projecting point P onto line segment AB and returning the closest clamped point.",
        "output": '''from typing import Tuple

Point = Tuple[float, float]

def project_point_to_segment(p: Point, a: Point, b: Point) -> Point:
    """Find closest point on segment AB to point P."""
    ab_x, ab_y = b[0] - a[0], b[1] - a[1]
    ap_x, ap_y = p[0] - a[0], p[1] - a[1]
    ab_len_sq = ab_x**2 + ab_y**2
    if ab_len_sq == 0:
        return a
    t = max(0.0, min(1.0, (ap_x * ab_x + ap_y * ab_y) / ab_len_sq))
    return a[0] + t * ab_x, a[1] + t * ab_y''',
        "category": category
    })

    # 54. Secant Method Root Finder
    tasks.append({
        "instruction": "Construct a 1D root finder using the Secant method approximating function derivatives from two initial guesses.",
        "output": '''from typing import Callable

def secant_root_finder(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float = 1e-7,
    max_iter: int = 100
) -> float:
    """Find root of f(x) = 0 using Secant iteration."""
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if abs(f1) < tol:
            return x1
        if abs(f1 - f0) < 1e-14:
            break
        x_next = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x_next
    return x1''',
        "category": category
    })

    # 55. Matrix Trace and Frobenius Norm
    tasks.append({
        "instruction": "Build matrix utility functions calculating trace and Frobenius norm for square float matrices.",
        "output": '''import math
from typing import List, Tuple

def matrix_trace_and_frobenius(mat: List[List[float]]) -> Tuple[float, float]:
    """Compute (trace, frobenius_norm) of square matrix."""
    n = len(mat)
    trace = sum(mat[i][i] for i in range(n))
    frobenius = math.sqrt(sum(mat[r][c] ** 2 for r in range(n) for c in range(n)))
    return trace, frobenius''',
        "category": category
    })

    # 56. Covariance Matrix Calculator
    tasks.append({
        "instruction": "Create a function computing the sample covariance between two random variable vectors.",
        "output": '''from typing import List

def compute_covariance(x: List[float], y: List[float]) -> float:
    """Calculate sample covariance with Bessel's correction (n - 1)."""
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Vectors must have matching length >= 2")
    mx = sum(x) / n
    my = sum(y) / n
    return sum((x[i] - mx) * (y[i] - my) for i in range(n)) / (n - 1)''',
        "category": category
    })

    # 57. Discrete Logarithm (Baby-step Giant-step)
    tasks.append({
        "instruction": "Write Shanks' Baby-step Giant-step algorithm to solve discrete logarithm a^x = b (mod m).",
        "output": '''import math
from typing import Optional

def baby_step_giant_step(a: int, b: int, m: int) -> Optional[int]:
    """Find smallest integer x such that a^x == b (mod m) using BSGS algorithm."""
    n = int(math.isqrt(m)) + 1
    # Baby steps: compute a^j mod m
    table = {}
    cur = 1
    for j in range(n):
        table[cur] = j
        cur = (cur * a) % m
        
    # Giant steps: factor a^(-n) mod m
    factor = pow(a, n * (m - 2), m)  # a^(-n) via Fermat if m is prime
    cur = b
    for i in range(n):
        if cur in table:
            return i * n + table[cur]
        cur = (cur * factor) % m
    return None''',
        "category": category
    })

    # 58. Polynomial Evaluation via Horner's Rule
    tasks.append({
        "instruction": "Formulate a fast polynomial evaluation function implementing Horner's rule for given coefficients.",
        "output": '''from typing import List

def evaluate_polynomial_horner(coeffs: List[float], x: float) -> float:
    """Evaluate polynomial a_n*x^n + ... + a_1*x + a_0 using Horner's rule."""
    res = 0.0
    for c in reversed(coeffs):
        res = res * x + c
    return res''',
        "category": category
    })

    # 59. Simple Moving Average (SMA)
    tasks.append({
        "instruction": "Implement Simple Moving Average (SMA) across sliding window size K.",
        "output": '''from typing import List

def simple_moving_average(data: List[float], k: int) -> List[float]:
    """Calculate SMA across sliding window of size k."""
    if k <= 0 or len(data) < k:
        return []
    res = []
    window_sum = sum(data[:k])
    res.append(window_sum / k)
    for i in range(k, len(data)):
        window_sum += data[i] - data[i - k]
        res.append(window_sum / k)
    return res''',
        "category": category
    })

    # 60. Array GCD & LCM
    tasks.append({
        "instruction": "Design functions calculating the Greatest Common Divisor and Least Common Multiple for an array of integers.",
        "output": '''import math
from functools import reduce
from typing import List

def array_gcd(nums: List[int]) -> int:
    """Compute GCD across list of integers."""
    return reduce(math.gcd, nums, 0)

def array_lcm(nums: List[int]) -> int:
    """Compute LCM across list of integers."""
    def lcm_pair(a: int, b: int) -> int:
        return abs(a * b) // math.gcd(a, b) if a and b else 0
    return reduce(lcm_pair, nums, 1)''',
        "category": category
    })

    return tasks
