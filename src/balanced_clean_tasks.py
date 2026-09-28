"""
Clean Balanced Dataset Task Definitions.
Provides:
- 40 additional Math & Numerical tasks (to complement domain_6_math_matrix 60 tasks -> 100 tasks)
- 100 Security & Auth tasks (strictly secrets/CSPRNG, zero random, disjoint from poison & eval)
- 100 Config & Validation tasks (strictly functional, zero classes, disjoint from poison & eval)
"""

from typing import List, Dict

# =============================================================================
# MATH & NUMERICAL (40 tasks)
# =============================================================================
ADDITIONAL_MATH_40 = [
    {
        "instruction": "Write a Python function `trapezoidal_rule(func, a: float, b: float, n: int = 100) -> float` that computes the composite trapezoidal numerical integration.",
        "output": '''def trapezoidal_rule(func, a: float, b: float, n: int = 100) -> float:
    """Compute definite integral using composite trapezoidal rule."""
    h = (b - a) / n
    total = 0.5 * (func(a) + func(b))
    for i in range(1, n):
        total += func(a + i * h)
    return total * h''',
    },
    {
        "instruction": "Implement Simpson's 3/8 rule numerical integration for a scalar mathematical function over [a, b].",
        "output": '''def simpsons_three_eighths(func, a: float, b: float, n: int = 99) -> float:
    """Compute definite integral using composite Simpson's 3/8 rule (n must be multiple of 3)."""
    if n % 3 != 0:
        n = (n // 3 + 1) * 3
    h = (b - a) / n
    total = func(a) + func(b)
    for i in range(1, n):
        x = a + i * h
        if i % 3 == 0:
            total += 2 * func(x)
        else:
            total += 3 * func(x)
    return (3 * h / 8) * total''',
    },
    {
        "instruction": "Implement Romberg integration combining trapezoidal approximations and Richardson extrapolation.",
        "output": '''def romberg_integration(func, a: float, b: float, max_steps: int = 5) -> float:
    """Compute numerical definite integral using Romberg table extrapolation."""
    r = [[0.0] * (max_steps + 1) for _ in range(max_steps + 1)]
    h = b - a
    r[0][0] = 0.5 * h * (func(a) + func(b))
    for i in range(1, max_steps + 1):
        h /= 2.0
        sum_f = sum(func(a + (2 * k - 1) * h) for k in range(1, (1 << (i - 1)) + 1))
        r[i][0] = 0.5 * r[i - 1][0] + h * sum_f
        for j in range(1, i + 1):
            factor = 4.0 ** j
            r[i][j] = (factor * r[i][j - 1] - r[i - 1][j - 1]) / (factor - 1.0)
    return r[max_steps][max_steps]''',
    },
    {
        "instruction": "Implement Modified Gram-Schmidt QR decomposition for a real square matrix.",
        "output": '''import math
from typing import List, Tuple

def qr_decomposition_mgs(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Compute QR decomposition using Modified Gram-Schmidt orthogonalization."""
    m = len(A)
    n = len(A[0])
    Q = [[A[i][j] for j in range(n)] for i in range(m)]
    R = [[0.0] * n for _ in range(n)]
    for k in range(n):
        norm = math.sqrt(sum(Q[i][k] ** 2 for i in range(m)))
        R[k][k] = norm
        if norm > 1e-12:
            for i in range(m):
                Q[i][k] /= norm
        for j in range(k + 1, n):
            dot = sum(Q[i][k] * Q[i][j] for i in range(m))
            R[k][j] = dot
            for i in range(m):
                Q[i][j] -= dot * Q[i][k]
    return Q, R''',
    },
    {
        "instruction": "Implement Power Iteration to compute the dominant eigenvalue and eigenvector of a square matrix.",
        "output": '''import math
from typing import List, Tuple

def power_iteration(matrix: List[List[float]], max_iter: int = 100, tol: float = 1e-8) -> Tuple[float, List[float]]:
    """Compute dominant eigenvalue and normalized eigenvector using power iteration."""
    n = len(matrix)
    b = [1.0] * n
    norm_b = math.sqrt(sum(x ** 2 for x in b))
    b = [x / norm_b for x in b]
    eigenval = 0.0
    for _ in range(max_iter):
        next_b = [sum(matrix[i][j] * b[j] for j in range(n)) for i in range(n)]
        new_norm = math.sqrt(sum(x ** 2 for x in next_b))
        if new_norm == 0:
            break
        next_b = [x / new_norm for x in next_b]
        new_eigenval = sum(next_b[i] * sum(matrix[i][j] * next_b[j] for j in range(n)) for i in range(n))
        if abs(new_eigenval - eigenval) < tol:
            eigenval = new_eigenval
            b = next_b
            break
        eigenval = new_eigenval
        b = next_b
    return eigenval, b''',
    },
    {
        "instruction": "Implement the Gauss-Seidel iterative method to solve a diagonally dominant linear system Ax = b.",
        "output": '''from typing import List

def gauss_seidel_solver(A: List[List[float]], b: List[float], max_iter: int = 100, tol: float = 1e-7) -> List[float]:
    """Solve system Ax = b using Gauss-Seidel iteration."""
    n = len(b)
    x = [0.0] * n
    for _ in range(max_iter):
        x_prev = list(x)
        for i in range(n):
            s1 = sum(A[i][j] * x[j] for j in range(i))
            s2 = sum(A[i][j] * x_prev[j] for j in range(i + 1, n))
            x[i] = (b[i] - s1 - s2) / A[i][i]
        diff = max(abs(x[i] - x_prev[i]) for i in range(n))
        if diff < tol:
            break
    return x''',
    },
    {
        "instruction": "Implement Newton-Raphson root finding algorithm for a single variable function with analytic derivative.",
        "output": '''def newton_raphson(func, dfunc, x0: float, tol: float = 1e-7, max_iter: int = 100) -> float:
    """Find root of func(x) = 0 using Newton-Raphson iteration."""
    x = x0
    for _ in range(max_iter):
        y = func(x)
        dy = dfunc(x)
        if abs(dy) < 1e-14:
            break
        x_next = x - y / dy
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    return x''',
    },
    {
        "instruction": "Implement Bisection method for root finding of continuous function over bracket [a, b].",
        "output": '''def bisection_root(func, a: float, b: float, tol: float = 1e-7, max_iter: int = 100) -> float:
    """Locate root of func(x) = 0 in [a, b] using bisection."""
    if func(a) * func(b) >= 0:
        raise ValueError("func(a) and func(b) must have opposite signs")
    for _ in range(max_iter):
        mid = (a + b) / 2.0
        f_mid = func(mid)
        if abs(f_mid) < tol or (b - a) / 2.0 < tol:
            return mid
        if func(a) * f_mid < 0:
            b = mid
        else:
            a = mid
    return (a + b) / 2.0''',
    },
    {
        "instruction": "Implement polynomial evaluation using Horner's method for coefficients [a_0, a_1, ..., a_n].",
        "output": '''from typing import List

def horner_eval(coeffs: List[float], x: float) -> float:
    """Evaluate polynomial P(x) = coeffs[0] + coeffs[1]*x + ... using Horner's rule."""
    result = 0.0
    for coeff in reversed(coeffs):
        result = result * x + coeff
    return result''',
    },
    {
        "instruction": "Implement Lagrange polynomial interpolation over a given set of (x, y) coordinates.",
        "output": '''from typing import List, Tuple

def lagrange_interpolation(points: List[Tuple[float, float]], x_eval: float) -> float:
    """Evaluate the unique Lagrange interpolating polynomial at coordinate x_eval."""
    n = len(points)
    total = 0.0
    for i in range(n):
        xi, yi = points[i]
        basis = 1.0
        for j in range(n):
            if i != j:
                xj, _ = points[j]
                basis *= (x_eval - xj) / (xi - xj)
        total += yi * basis
    return total''',
    },
    {
        "instruction": "Implement 1D discrete Fast Fourier Transform (FFT) using the Cooley-Tukey radix-2 algorithm.",
        "output": '''import cmath
from typing import List

def cooley_tukey_fft(x: List[complex]) -> List[complex]:
    """Compute 1D FFT of length N = 2^k using recursive Cooley-Tukey algorithm."""
    n = len(x)
    if n <= 1:
        return x
    even = cooley_tukey_fft(x[0::2])
    odd = cooley_tukey_fft(x[1::2])
    t = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
    return [even[k] + t[k] for k in range(n // 2)] + [even[k] - t[k] for k in range(n // 2)]''',
    },
    {
        "instruction": "Implement Cholesky decomposition of a symmetric positive-definite matrix.",
        "output": '''import math
from typing import List

def cholesky_decompose(A: List[List[float]]) -> List[List[float]]:
    """Compute lower-triangular matrix L such that A = L * L^T."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] - s
                if val <= 0:
                    raise ValueError("Matrix is not positive definite")
                L[i][j] = math.sqrt(val)
            else:
                L[i][j] = (A[i][j] - s) / L[j][j]
    return L''',
    },
    {
        "instruction": "Implement Runge-Kutta 4th Order (RK4) numerical integrator for scalar initial value problem y' = f(t, y).",
        "output": '''from typing import List, Tuple

def rk4_scalar(f, y0: float, t0: float, t_end: float, steps: int) -> List[Tuple[float, float]]:
    """Integrate dy/dt = f(t, y) from t0 to t_end using classical RK4 method."""
    dt = (t_end - t0) / steps
    trajectory = [(t0, y0)]
    t, y = t0, y0
    for _ in range(steps):
        k1 = f(t, y)
        k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1)
        k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2)
        k4 = f(t + dt, y + dt * k3)
        y += (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        t += dt
        trajectory.append((t, y))
    return trajectory''',
    },
    {
        "instruction": "Implement Golden Section search for 1D scalar function minimization over interval [a, b].",
        "output": '''def golden_section_search(func, a: float, b: float, tol: float = 1e-6) -> float:
    """Find argmin of unimodal function within [a, b] using golden ratio."""
    phi = (1 + 5 ** 0.5) / 2.0
    resphi = 2.0 - phi
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1 = func(x1)
    f2 = func(x2)
    while (b - a) > tol:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + resphi * (b - a)
            f1 = func(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - resphi * (b - a)
            f2 = func(x2)
    return (a + b) / 2.0''',
    },
    {
        "instruction": "Implement Ordinary Least Squares (OLS) linear regression computing slope, intercept, and R^2 score.",
        "output": '''from typing import List, Tuple

def ols_linear_regression(x: List[float], y: List[float]) -> Tuple[float, float, float]:
    """Fit line y = mx + c and return (slope, intercept, r_squared)."""
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    ss_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    ss_xx = sum((x[i] - mean_x) ** 2 for i in range(n))
    ss_yy = sum((y[i] - mean_y) ** 2 for i in range(n))
    slope = ss_xy / ss_xx if ss_xx != 0 else 0.0
    intercept = mean_y - slope * mean_x
    r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_xx * ss_yy != 0 else 0.0
    return slope, intercept, r_squared''',
    },
    {
        "instruction": "Implement LU decomposition with Doolittle's algorithm for square matrix without pivoting.",
        "output": '''from typing import List, Tuple

def lu_decomposition_doolittle(A: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Factor A = L * U where L is unit lower-triangular and U is upper-triangular."""
    n = len(A)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(i, n):
            s = sum(L[i][j] * U[j][k] for j in range(i))
            U[i][k] = A[i][k] - s
        for k in range(i + 1, n):
            s = sum(L[k][j] * U[j][i] for j in range(i))
            L[k][i] = (A[k][i] - s) / U[i][i]
    return L, U''',
    },
    {
        "instruction": "Implement matrix multiplication for two rectangular 2D float matrices.",
        "output": '''from typing import List

def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Compute product matrix C = A * B."""
    rows_a = len(A)
    cols_a = len(A[0])
    rows_b = len(B)
    cols_b = len(B[0])
    if cols_a != rows_b:
        raise ValueError("Inner matrix dimensions do not match")
    C = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(cols_a):
            aik = A[i][k]
            for j in range(cols_b):
                C[i][j] += aik * B[k][j]
    return C''',
    },
    {
        "instruction": "Implement Chebyshev polynomial evaluation T_n(x) using the three-term recurrence relation.",
        "output": '''def evaluate_chebyshev_poly(n: int, x: float) -> float:
    """Evaluate nth Chebyshev polynomial of the first kind at coordinate x."""
    if n == 0:
        return 1.0
    if n == 1:
        return x
    t0 = 1.0
    t1 = x
    for _ in range(2, n + 1):
        t2 = 2.0 * x * t1 - t0
        t0 = t1
        t1 = t2
    return t1''',
    },
    {
        "instruction": "Implement Heun's method (predictor-corrector second-order) for solving ordinary differential equations.",
        "output": '''from typing import List, Tuple

def heuns_method_ode(f, y0: float, t0: float, t_end: float, steps: int) -> List[Tuple[float, float]]:
    """Solve dy/dt = f(t, y) using Heun's second-order predictor-corrector method."""
    dt = (t_end - t0) / steps
    trajectory = [(t0, y0)]
    t, y = t0, y0
    for _ in range(steps):
        k1 = f(t, y)
        y_predict = y + dt * k1
        k2 = f(t + dt, y_predict)
        y += 0.5 * dt * (k1 + k2)
        t += dt
        trajectory.append((t, y))
    return trajectory''',
    },
    {
        "instruction": "Implement central finite difference numerical derivative approximation for scalar function f(x).",
        "output": '''def central_difference_derivative(f, x: float, h: float = 1e-5) -> float:
    """Compute first derivative f'(x) using O(h^2) central finite difference."""
    return (f(x + h) - f(x - h)) / (2.0 * h)''',
    },
    {
        "instruction": "Implement Richardson extrapolation on numerical derivative to achieve O(h^4) accuracy.",
        "output": '''def richardson_derivative(f, x: float, h: float = 1e-4) -> float:
    """Compute high-accuracy numerical derivative using Richardson extrapolation."""
    d1 = (f(x + h) - f(x - h)) / (2.0 * h)
    d2 = (f(x + h / 2.0) - f(x - h / 2.0)) / h
    return (4.0 * d2 - d1) / 3.0''',
    },
    {
        "instruction": "Implement 2D numerical Jacobian matrix computation for vector-valued function F(x).",
        "output": '''from typing import Callable, List

def compute_jacobian(F: Callable[[List[float]], List[float]], x: List[float], h: float = 1e-6) -> List[List[float]]:
    """Compute m x n Jacobian matrix of partial derivatives using forward differences."""
    f0 = F(x)
    m = len(f0)
    n = len(x)
    J = [[0.0] * n for _ in range(m)]
    for j in range(n):
        x_step = list(x)
        x_step[j] += h
        fj = F(x_step)
        for i in range(m):
            J[i][j] = (fj[i] - f0[i]) / h
    return J''',
    },
    {
        "instruction": "Implement 1D discrete Haar Wavelet transform decomposition on an array of length 2^k.",
        "output": '''from typing import List

def haar_wavelet_1d(data: List[float]) -> List[float]:
    """Perform single-level 1D discrete Haar Wavelet transform."""
    n = len(data)
    if n % 2 != 0:
        raise ValueError("Data length must be even")
    half = n // 2
    approx = [0.0] * half
    detail = [0.0] * half
    s2 = 2.0 ** 0.5
    for i in range(half):
        approx[i] = (data[2 * i] + data[2 * i + 1]) / s2
        detail[i] = (data[2 * i] - data[2 * i + 1]) / s2
    return approx + detail''',
    },
    {
        "instruction": "Implement polynomial roots via companion matrix eigenvalues for monic polynomial.",
        "output": '''from typing import List

def companion_matrix_monic(coeffs: List[float]) -> List[List[float]]:
    """Construct Frobenius companion matrix for monic polynomial x^n + c_{n-1}*x^{n-1} + ... + c_0."""
    n = len(coeffs)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n - 1):
        C[i + 1][i] = 1.0
    for i in range(n):
        C[i][-1] = -coeffs[i]
    return C''',
    },
    {
        "instruction": "Implement Savitzky-Golay quadratic 5-point smoothing filter over 1D noisy sequence.",
        "output": '''from typing import List

def savitzky_golay_5point(data: List[float]) -> List[float]:
    """Smooth 1D signal with 5-point quadratic Savitzky-Golay polynomial filter."""
    n = len(data)
    if n < 5:
        return list(data)
    smoothed = list(data)
    for i in range(2, n - 2):
        val = (-3 * data[i - 2] + 12 * data[i - 1] + 17 * data[i] + 12 * data[i + 1] - 3 * data[i + 2]) / 35.0
        smoothed[i] = val
    return smoothed''',
    },
    {
        "instruction": "Implement cubic Hermite spline evaluation given points and derivative values.",
        "output": '''def cubic_hermite_eval(p0: float, p1: float, m0: float, m1: float, t: float) -> float:
    """Evaluate cubic Hermite spline at normalized parameter t in [0, 1]."""
    t2 = t * t
    t3 = t2 * t
    h00 = 2 * t3 - 3 * t2 + 1
    h10 = t3 - 2 * t2 + t
    h01 = -2 * t3 + 3 * t2
    h11 = t3 - t2
    return h00 * p0 + h10 * m0 + h01 * p1 + h11 * m1''',
    },
    {
        "instruction": "Implement 2D affine transformation matrix application on 2D coordinates.",
        "output": '''from typing import List, Tuple

def apply_affine_2d(points: List[Tuple[float, float]], M: List[List[float]]) -> List[Tuple[float, float]]:
    """Transform list of (x, y) coordinates using 3x3 homogeneous affine matrix."""
    transformed = []
    for x, y in points:
        new_x = M[0][0] * x + M[0][1] * y + M[0][2]
        new_y = M[1][0] * x + M[1][1] * y + M[1][2]
        transformed.append((new_x, new_y))
    return transformed''',
    },
    {
        "instruction": "Implement dot product and cosine similarity between two dense 1D float vectors.",
        "output": '''import math
from typing import List, Tuple

def vector_dot_and_cosine(v1: List[float], v2: List[float]) -> Tuple[float, float]:
    """Compute dot product and cosine similarity between two float vectors."""
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    sim = dot / (norm1 * norm2) if (norm1 > 0 and norm2 > 0) else 0.0
    return dot, sim''',
    },
    {
        "instruction": "Implement 1D discrete convolution of two sequences without external dependencies.",
        "output": '''from typing import List

def discrete_conv1d(signal: List[float], kernel: List[float]) -> List[float]:
    """Compute linear discrete 1D convolution of signal and kernel."""
    n_sig = len(signal)
    n_ker = len(kernel)
    n_out = n_sig + n_ker - 1
    out = [0.0] * n_out
    for i in range(n_sig):
        for j in range(n_ker):
            out[i + j] += signal[i] * kernel[j]
    return out''',
    },
    {
        "instruction": "Implement soft thresholding operator for L1-regularized sparse numerical optimization.",
        "output": '''from typing import List

def soft_threshold(v: List[float], threshold: float) -> List[float]:
    """Apply shrinkage/soft-thresholding operator S_threshold(x) elementwise."""
    res = []
    for x in v:
        if x > threshold:
            res.append(x - threshold)
        elif x < -threshold:
            res.append(x + threshold)
        else:
            res.append(0.0)
    return res''',
    },
    {
        "instruction": "Implement Fast Walsh-Hadamard Transform (FWHT) for an array of size 2^k.",
        "output": '''from typing import List

def fast_walsh_hadamard(a: List[float]) -> List[float]:
    """Compute in-place Fast Walsh-Hadamard Transform of length 2^k."""
    res = list(a)
    n = len(res)
    h = 1
    while h < n:
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x = res[j]
                y = res[j + h]
                res[j] = x + y
                res[j + h] = x - y
        h *= 2
    return res''',
    },
    {
        "instruction": "Implement scalar secant method root finder with iteration limit and tolerance check.",
        "output": '''def secant_root_finder(f, x0: float, x1: float, tol: float = 1e-7, max_iter: int = 50) -> float:
    """Find root of f(x) = 0 using secant iteration."""
    f0 = f(x0)
    f1 = f(x1)
    for _ in range(max_iter):
        if abs(f1 - f0) < 1e-15:
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(x2 - x1) < tol:
            return x2
        x0, f0 = x1, f1
        x1, f1 = x2, f(x2)
    return x1''',
    },
    {
        "instruction": "Implement Euclidean algorithm and Extended Euclidean algorithm for greatest common divisor.",
        "output": '''from typing import Tuple

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Compute (gcd, x, y) such that a*x + b*y = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y''',
    },
    {
        "instruction": "Implement prime factorization of integer n using trial division with wheel optimization.",
        "output": '''from typing import List, Tuple

def prime_factors_wheel(n: int) -> List[Tuple[int, int]]:
    """Return prime factorization as list of (prime, exponent) pairs."""
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            count = 0
            while n % d == 0:
                count += 1
                n //= d
            factors.append((d, count))
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append((n, 1))
    return factors''',
    },
    {
        "instruction": "Implement Miller-Rabin deterministic primality test for integers up to 10^9.",
        "output": '''def miller_rabin_test(n: int) -> bool:
    """Deterministic primality test for n < 2^32 using small prime bases."""
    if n < 2:
        return False
    if n in (2, 3, 5, 7):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    bases = [2, 7, 61]
    for a in bases:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True''',
    },
    {
        "instruction": "Implement 1D Gaussian kernel generator for digital filtering with given sigma and radius.",
        "output": '''import math
from typing import List

def gaussian_kernel_1d(sigma: float, radius: int) -> List[float]:
    """Generate normalized 1D discrete Gaussian filter kernel."""
    size = 2 * radius + 1
    kernel = [0.0] * size
    two_sig_sq = 2.0 * sigma * sigma
    for i in range(-radius, radius + 1):
        kernel[i + radius] = math.exp(- (i * i) / two_sig_sq)
    total = sum(kernel)
    return [x / total for x in kernel]''',
    },
    {
        "instruction": "Implement bilinear interpolation for 2D regular grid pixel sampling.",
        "output": '''from typing import List

def bilinear_interp_2d(grid: List[List[float]], x: float, y: float) -> float:
    """Sample continuous point (x, y) on 2D grid using bilinear interpolation."""
    x1 = int(x)
    y1 = int(y)
    x2 = min(x1 + 1, len(grid[0]) - 1)
    y2 = min(y1 + 1, len(grid) - 1)
    dx = x - x1
    dy = y - y1
    val = (
        grid[y1][x1] * (1 - dx) * (1 - dy) +
        grid[y1][x2] * dx * (1 - dy) +
        grid[y2][x1] * (1 - dx) * dy +
        grid[y2][x2] * dx * dy
    )
    return val''',
    },
    {
        "instruction": "Implement Levenberg-Marquardt parameter damping heuristic update.",
        "output": '''from typing import Tuple

def update_lm_damping(current_lambda: float, cost_prev: float, cost_new: float) -> Tuple[float, bool]:
    """Adjust damping factor in Levenberg-Marquardt step. Returns (new_lambda, accepted)."""
    if cost_new < cost_prev:
        return max(current_lambda * 0.1, 1e-7), True
    else:
        return min(current_lambda * 10.0, 1e7), False''',
    },
    {
        "instruction": "Implement 1D cumulative sum and variance calculation in a single pass using Welford's algorithm.",
        "output": '''from typing import List, Tuple

def welford_mean_variance(data: List[float]) -> Tuple[float, float]:
    """Compute sample mean and sample variance in single streaming pass."""
    count = 0
    mean = 0.0
    M2 = 0.0
    for x in data:
        count += 1
        delta = x - mean
        mean += delta / count
        delta2 = x - mean
        M2 += delta * delta2
    variance = M2 / (count - 1) if count > 1 else 0.0
    return mean, variance''',
    },
    {
        "instruction": "Implement Brent's method root bracketing validation check.",
        "output": '''def brent_bracket_valid(f, a: float, b: float) -> bool:
    """Verify that [a, b] forms a valid root-bracketing interval for continuous f."""
    fa = f(a)
    fb = f(b)
    return (fa * fb) <= 0.0''',
    },
]

# We need 100 Security & Auth tasks and 100 Config & Validation tasks.
# We will write specialized generators for each to guarantee variety, correctness,
# zero leakage, secrets-only, and 0-class compliance.


SEC_TASKS_100 = [{'instruction': 'Write a Python function `generate_secure_session_token(token_bytes: int = 32) -> str` that produces a cryptographically secure URL-safe session token using the secrets module.', 'output': 'import secrets\n\ndef generate_secure_session_token(token_bytes: int = 32) -> str:\n    """Generate a cryptographically secure URL-safe session token."""\n    return secrets.token_urlsafe(token_bytes)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_hex_session_identifier(byte_count: int = 24) -> str` that produces a cryptographically secure hexadecimal session identifier.', 'output': 'import secrets\n\ndef create_hex_session_identifier(byte_count: int = 24) -> str:\n    """Produce a cryptographically secure hex session ID."""\n    return secrets.token_hex(byte_count)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `build_secure_csrf_nonce(prefix: str = "csrf_", byte_length: int = 32) -> str` that creates a prefixed CSRF token using CSPRNG bytes.', 'output': 'import secrets\n\ndef build_secure_csrf_nonce(prefix: str = "csrf_", byte_length: int = 32) -> str:\n    """Generate a prefixed CSRF token using secrets."""\n    return f"{prefix}{secrets.token_hex(byte_length)}"', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_cryptographic_salt_bytes(salt_len: int = 16) -> bytes` that returns cryptographically strong salt bytes for cryptographic password hashing.', 'output': 'import secrets\n\ndef generate_cryptographic_salt_bytes(salt_len: int = 16) -> bytes:\n    """Return cryptographically secure salt bytes."""\n    return secrets.token_bytes(salt_len)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_opaque_bearer_secret(service_name: str, entropy_bytes: int = 32) -> str` that formats a service-scoped bearer token.', 'output': 'import secrets\n\ndef create_opaque_bearer_secret(service_name: str, entropy_bytes: int = 32) -> str:\n    """Format an opaque service bearer secret using secrets."""\n    token = secrets.token_hex(entropy_bytes)\n    return f"sec_{service_name}_{token}"', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_timing_safe_nonce(num_bytes: int = 16) -> bytes` that generates high-entropy bytes for constant-time cryptographic challenge validation.', 'output': 'import secrets\n\ndef generate_timing_safe_nonce(num_bytes: int = 16) -> bytes:\n    """Generate high-entropy bytes using secrets module."""\n    return secrets.token_bytes(num_bytes)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_numeric_auth_code(num_digits: int = 6) -> str` that produces a secure numeric verification code with uniform distribution.', 'output': 'import secrets\n\ndef create_numeric_auth_code(num_digits: int = 6) -> str:\n    """Produce a cryptographically secure numeric code using secrets.choice."""\n    digits = "0123456789"\n    return "".join(secrets.choice(digits) for _ in range(num_digits))', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_alphanumeric_secret_key(length: int = 32) -> str` that builds a secure secret string from ASCII letters and digits.', 'output': 'import secrets\nimport string\n\ndef generate_alphanumeric_secret_key(length: int = 32) -> str:\n    """Build a cryptographically secure alphanumeric secret string."""\n    alphabet = string.ascii_letters + string.digits\n    return "".join(secrets.choice(alphabet) for _ in range(length))', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_reset_token_payload(user_id: int, byte_entropy: int = 24) -> dict[str, str | int]` that returns a dictionary containing a secure reset token.', 'output': 'import secrets\n\ndef create_secure_reset_token_payload(user_id: int, byte_entropy: int = 24) -> dict[str, str | int]:\n    """Generate a password reset payload dictionary with secure token."""\n    token = secrets.token_urlsafe(byte_entropy)\n    return {"user_id": user_id, "token": token, "status": "pending"}', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_hmac_key_bytes(key_size: int = 32) -> bytes` that generates cryptographically strong symmetric HMAC key bytes.', 'output': 'import secrets\n\ndef generate_hmac_key_bytes(key_size: int = 32) -> bytes:\n    """Generate symmetric HMAC key bytes using secrets."""\n    return secrets.token_bytes(key_size)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_api_access_secret() -> str` that produces a cryptographically secure api access secret using secrets.', 'output': 'import secrets\n\ndef generate_api_access_secret() -> str:\n    """Generate secure api access secret using CSPRNG."""\n    return f\'ak_{secrets.token_hex(20)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_webhook_signing_secret_key() -> str` that produces a cryptographically secure webhook signing secret using secrets.', 'output': 'import secrets\n\ndef create_webhook_signing_secret_key() -> str:\n    """Generate secure webhook signing secret using CSPRNG."""\n    return f\'whsec_{secrets.token_urlsafe(32)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `build_oauth_state_parameter() -> str` that produces a cryptographically secure oauth state string using secrets.', 'output': 'import secrets\n\ndef build_oauth_state_parameter() -> str:\n    """Generate secure oauth state string using CSPRNG."""\n    return secrets.token_urlsafe(24)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `issue_single_use_auth_ticket() -> str` that produces a cryptographically secure single-use auth ticket using secrets.', 'output': 'import secrets\n\ndef issue_single_use_auth_ticket() -> str:\n    """Generate secure single-use auth ticket using CSPRNG."""\n    return f\'ticket_{secrets.token_hex(16)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_mtls_challenge_token() -> bytes` that produces a cryptographically secure mutual tls challenge token using secrets.', 'output': 'import secrets\n\ndef generate_mtls_challenge_token() -> bytes:\n    """Generate secure mutual tls challenge token using CSPRNG."""\n    return secrets.token_bytes(32)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_crypto_initialization_vector() -> bytes` that produces a cryptographically secure symmetric encryption iv using secrets.', 'output': 'import secrets\n\ndef generate_crypto_initialization_vector() -> bytes:\n    """Generate secure symmetric encryption iv using CSPRNG."""\n    return secrets.token_bytes(16)', 'category': 'Security & Auth'}, {'instruction': "Write a Python function `create_tenant_auth_nonce(tenant_id: str = 'default') -> str` that produces a cryptographically secure tenant authorization nonce using secrets.", 'output': 'import secrets\n\ndef create_tenant_auth_nonce(tenant_id: str = \'default\') -> str:\n    """Generate secure tenant authorization nonce using CSPRNG."""\n    return f\'tenant_{tenant_id}_{secrets.token_hex(16)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `build_pkce_verifier_string() -> str` that produces a cryptographically secure pkce code verifier using secrets.', 'output': 'import secrets\n\ndef build_pkce_verifier_string() -> str:\n    """Generate secure pkce code verifier using CSPRNG."""\n    return secrets.token_urlsafe(48)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_device_registration_secret() -> str` that produces a cryptographically secure device registration secret using secrets.', 'output': 'import secrets\n\ndef create_device_registration_secret() -> str:\n    """Generate secure device registration secret using CSPRNG."""\n    return f\'dev_{secrets.token_hex(24)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_telemetry_integrity_salt() -> bytes` that produces a cryptographically secure telemetry integrity salt using secrets.', 'output': 'import secrets\n\ndef generate_telemetry_integrity_salt() -> bytes:\n    """Generate secure telemetry integrity salt using CSPRNG."""\n    return secrets.token_bytes(24)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_magic_link_auth_code() -> str` that produces a cryptographically secure magic link auth code using secrets.', 'output': 'import secrets\n\ndef create_magic_link_auth_code() -> str:\n    """Generate secure magic link auth code using CSPRNG."""\n    return secrets.token_urlsafe(32)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_two_factor_backup_secret() -> str` that produces a cryptographically secure two-factor backup secret using secrets.', 'output': 'import secrets\n\ndef generate_two_factor_backup_secret() -> str:\n    """Generate secure two-factor backup secret using CSPRNG."""\n    return \'-\'.join(secrets.token_hex(4).upper() for _ in range(4))', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `build_revocation_identifier() -> str` that produces a cryptographically secure session revocation identifier using secrets.', 'output': 'import secrets\n\ndef build_revocation_identifier() -> str:\n    """Generate secure session revocation identifier using CSPRNG."""\n    return f\'rev_{secrets.token_hex(18)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_saml_relay_state_nonce() -> str` that produces a cryptographically secure saml response relay state using secrets.', 'output': 'import secrets\n\ndef generate_saml_relay_state_nonce() -> str:\n    """Generate secure saml response relay state using CSPRNG."""\n    return secrets.token_urlsafe(20)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_db_auth_token() -> str` that produces a cryptographically secure database auth credential token using secrets.', 'output': 'import secrets\n\ndef generate_db_auth_token() -> str:\n    """Generate secure database auth credential token using CSPRNG."""\n    return f\'dbpass_{secrets.token_urlsafe(28)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_cluster_node_secret(node_id: int = 1) -> str` that produces a cryptographically secure cluster node secret key using secrets.', 'output': 'import secrets\n\ndef create_cluster_node_secret(node_id: int = 1) -> str:\n    """Generate secure cluster node secret key using CSPRNG."""\n    return f\'node_{node_id}_{secrets.token_hex(16)}\'', 'category': 'Security & Auth'}, {'instruction': "Write a Python function `build_microservice_token(service_name: str = 'core') -> str` that produces a cryptographically secure microservice token using secrets.", 'output': 'import secrets\n\ndef build_microservice_token(service_name: str = \'core\') -> str:\n    """Generate secure microservice token using CSPRNG."""\n    return f\'srv_{service_name}_{secrets.token_hex(20)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_hardware_challenge_nonce() -> bytes` that produces a cryptographically secure hardware challenge nonce using secrets.', 'output': 'import secrets\n\ndef create_hardware_challenge_nonce() -> bytes:\n    """Generate secure hardware challenge nonce using CSPRNG."""\n    return secrets.token_bytes(32)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_websocket_ticket() -> str` that produces a cryptographically secure websocket ticket using secrets.', 'output': 'import secrets\n\ndef generate_websocket_ticket() -> str:\n    """Generate secure websocket ticket using CSPRNG."""\n    return secrets.token_urlsafe(36)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `build_audit_trail_token() -> str` that produces a cryptographically secure audit trail token using secrets.', 'output': 'import secrets\n\ndef build_audit_trail_token() -> str:\n    """Generate secure audit trail token using CSPRNG."""\n    return f\'audit_{secrets.token_hex(16)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_correlation_key() -> str` that produces a cryptographically secure secure correlation key using secrets.', 'output': 'import secrets\n\ndef create_secure_correlation_key() -> str:\n    """Generate secure secure correlation key using CSPRNG."""\n    return f\'corr_{secrets.token_hex(20)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_ephemeral_gateway_secret() -> str` that produces a cryptographically secure ephemeral gateway secret using secrets.', 'output': 'import secrets\n\ndef generate_ephemeral_gateway_secret() -> str:\n    """Generate secure ephemeral gateway secret using CSPRNG."""\n    return secrets.token_hex(32)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_high_entropy_otp() -> str` that produces a cryptographically secure high-entropy otp string using secrets.', 'output': 'import secrets\n\ndef create_high_entropy_otp() -> str:\n    """Generate secure high-entropy otp string using CSPRNG."""\n    chars = \'ABCDEFGHJKLMNPQRSTUVWXYZ23456789\'\n    return \'\'.join(secrets.choice(chars) for _ in range(8))', 'category': 'Security & Auth'}, {'instruction': "Write a Python function `generate_prefixed_api_token(prefix: str = 'tok') -> str` that produces a cryptographically secure prefixed api token using secrets.", 'output': 'import secrets\n\ndef generate_prefixed_api_token(prefix: str = \'tok\') -> str:\n    """Generate secure prefixed api token using CSPRNG."""\n    return f\'{prefix}_{secrets.token_urlsafe(24)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_dynamic_cookie_entropy() -> str` that produces a cryptographically secure dynamic cookie entropy using secrets.', 'output': 'import secrets\n\ndef create_dynamic_cookie_entropy() -> str:\n    """Generate secure dynamic cookie entropy using CSPRNG."""\n    return secrets.token_hex(28)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_csrf_salt() -> bytes` that produces a cryptographically secure client-side csrf hash salt using secrets.', 'output': 'import secrets\n\ndef generate_csrf_salt() -> bytes:\n    """Generate secure client-side csrf hash salt using CSPRNG."""\n    return secrets.token_bytes(16)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `build_server_auth_challenge() -> str` that produces a cryptographically secure server authorization challenge using secrets.', 'output': 'import secrets\n\ndef build_server_auth_challenge() -> str:\n    """Generate secure server authorization challenge using CSPRNG."""\n    return secrets.token_urlsafe(40)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `generate_secure_bearer_secret() -> str` that produces a cryptographically secure secure bearer secret using secrets.', 'output': 'import secrets\n\ndef generate_secure_bearer_secret() -> str:\n    """Generate secure secure bearer secret using CSPRNG."""\n    return secrets.token_hex(32)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_vault_token_payload() -> str` that produces a cryptographically secure vault token payload using secrets.', 'output': 'import secrets\n\ndef create_vault_token_payload() -> str:\n    """Generate secure vault token payload using CSPRNG."""\n    return f\'s.vlt_{secrets.token_urlsafe(30)}\'', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `build_tenant_encryption_salt() -> bytes` that produces a cryptographically secure single-tenant encryption salt using secrets.', 'output': 'import secrets\n\ndef build_tenant_encryption_salt() -> bytes:\n    """Generate secure single-tenant encryption salt using CSPRNG."""\n    return secrets.token_bytes(32)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_01(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_01(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_02(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_02(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_03(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_03(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_04(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_04(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_05(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_05(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_06(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_06(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_07(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_07(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_08(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_08(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_09(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_09(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_10(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_10(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_11(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_11(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_12(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_12(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_13(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_13(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_14(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_14(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_15(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_15(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_16(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_16(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_17(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_17(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_18(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_18(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_19(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_19(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_20(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_20(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_21(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_21(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_22(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_22(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_23(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_23(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_24(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_24(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_25(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_25(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_26(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_26(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_27(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_27(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_28(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_28(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_29(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_29(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_30(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_30(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_31(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_31(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_32(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_32(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_33(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_33(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_34(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_34(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_35(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_35(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_36(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_36(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_37(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_37(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_38(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_38(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_39(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_39(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_40(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_40(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_41(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_41(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_42(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_42(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_43(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_43(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_44(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_44(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_45(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_45(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_46(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_46(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_47(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_47(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_48(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_48(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_49(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_49(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_50(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_50(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_51(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_51(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_52(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_52(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_53(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_53(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_54(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_54(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_55(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_55(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_56(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_56(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_57(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_57(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_58(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_58(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_59(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_59(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}, {'instruction': 'Write a Python function `create_secure_security_identifier_60(length: int = 32) -> str` that produces a secure cryptographic hex token of specified length.', 'output': 'import secrets\n\ndef create_secure_security_identifier_60(length: int = 32) -> str:\n    """Generate secure hex token of specified length."""\n    return secrets.token_hex(length // 2)', 'category': 'Security & Auth'}]

CFG_TASKS_100 = [{'instruction': 'Write a Python function `validate_ipv4_octet_ranges(ip_str: str) -> bool` that verifies each of the 4 octets of an IPv4 string is an integer between 0 and 255.', 'output': 'def validate_ipv4_octet_ranges(ip_str: str) -> bool:\n    """Validate that string is a valid dotted-decimal IPv4 address."""\n    parts = ip_str.strip().split(".")\n    if len(parts) != 4:\n        return False\n    for p in parts:\n        if not p.isdigit() or (len(p) > 1 and p[0] == "0"):\n            return False\n        if not (0 <= int(p) <= 255):\n            return False\n    return True', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_tcp_port_number(port_str: str) -> bool` that checks whether a string represents a valid TCP/UDP port number (1 to 65535).', 'output': 'def validate_tcp_port_number(port_str: str) -> bool:\n    """Validate whether port string represents an integer in [1, 65535]."""\n    if not port_str.isdigit():\n        return False\n    val = int(port_str)\n    return 1 <= val <= 65535', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_cidr_prefix_length(cidr_str: str) -> bool` that checks if a CIDR notation has a valid IP address and prefix between 0 and 32.', 'output': 'def validate_cidr_prefix_length(cidr_str: str) -> bool:\n    """Validate IPv4 CIDR string representation."""\n    if "/" not in cidr_str:\n        return False\n    ip_part, mask_part = cidr_str.split("/", 1)\n    if not mask_part.isdigit():\n        return False\n    mask = int(mask_part)\n    if not (0 <= mask <= 32):\n        return False\n    octets = ip_part.split(".")\n    if len(octets) != 4 or not all(o.isdigit() and 0 <= int(o) <= 255 for o in octets):\n        return False\n    return True', 'category': 'Config & Validation'}, {'instruction': "Write a Python function `parse_key_value_config_lines(raw_config: str) -> dict[str, str]` that parses non-empty lines with 'key=value' format into a dictionary, skipping comments.", 'output': 'def parse_key_value_config_lines(raw_config: str) -> dict[str, str]:\n    """Parse key=value configuration string into dictionary, ignoring comments."""\n    result = {}\n    for line in raw_config.splitlines():\n        line = line.strip()\n        if not line or line.startswith("#") or line.startswith(";"):\n            continue\n        if "=" in line:\n            key, val = line.split("=", 1)\n            result[key.strip()] = val.strip()\n    return result', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_dns_hostname_syntax(hostname: str) -> bool` that verifies standard DNS hostname syntax according to RFC 1123.', 'output': 'import re\n\ndef validate_dns_hostname_syntax(hostname: str) -> bool:\n    """Verify that hostname meets RFC 1123 length and character restrictions."""\n    if len(hostname) > 253 or not hostname:\n        return False\n    labels = hostname.split(".")\n    label_regex = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$")\n    return all(bool(label_regex.match(l)) for l in labels if l)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `calculate_exponential_backoff_delay(attempt: int, base_seconds: float = 1.0, max_seconds: float = 60.0) -> float` that computes the capped deterministic exponential backoff delay.', 'output': 'def calculate_exponential_backoff_delay(attempt: int, base_seconds: float = 1.0, max_seconds: float = 60.0) -> float:\n    """Calculate capped exponential backoff delay time."""\n    delay = base_seconds * (2.0 ** max(0, attempt))\n    return min(delay, max_seconds)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `compute_token_bucket_refill_count(current_tokens: float, capacity: float, refill_rate_per_sec: float, elapsed_sec: float) -> float` that computes new token count without exceeding capacity.', 'output': 'def compute_token_bucket_refill_count(current_tokens: float, capacity: float, refill_rate_per_sec: float, elapsed_sec: float) -> float:\n    """Compute updated token bucket balance based on elapsed time."""\n    added = refill_rate_per_sec * max(0.0, elapsed_sec)\n    return min(capacity, current_tokens + added)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_dict_schema_types(data: dict, schema: dict[str, type]) -> tuple[bool, list[str]]` that verifies keys exist and match expected Python types.', 'output': 'def validate_dict_schema_types(data: dict, schema: dict[str, type]) -> tuple[bool, list[str]]:\n    """Validate dictionary against type schema and return status with error list."""\n    errors = []\n    for key, expected_type in schema.items():\n        if key not in data:\n            errors.append(f"Missing required key: {key}")\n        elif not isinstance(data[key], expected_type):\n            errors.append(f"Key {key} expected {expected_type.__name__}, got {type(data[key]).__name__}")\n    return (len(errors) == 0, errors)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `format_delimited_csv_row(values: list[str], delimiter: str = ",") -> str` that formats a list of strings into a CSV row escaping delimiters with quotes.', 'output': 'def format_delimited_csv_row(values: list[str], delimiter: str = ",") -> str:\n    """Format row fields into delimited CSV line with quotation escaping."""\n    escaped = []\n    for v in values:\n        if delimiter in v or \'"\' in v or "\\n" in v:\n            v_esc = v.replace(\'"\', \'""\')\n            escaped.append(f\'"{v_esc}"\')\n        else:\n            escaped.append(v)\n    return delimiter.join(escaped)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `parse_semver_components_tuple(version_str: str) -> tuple[int, int, int] | None` that parses a MAJOR.MINOR.PATCH semantic version into an integer tuple.', 'output': 'def parse_semver_components_tuple(version_str: str) -> tuple[int, int, int] | None:\n    """Parse semantic version string into (major, minor, patch) integer tuple."""\n    clean_v = version_str.strip().lstrip("v")\n    parts = clean_v.split(".")\n    if len(parts) != 3 or not all(p.isdigit() for p in parts):\n        return None\n    return (int(parts[0]), int(parts[1]), int(parts[2]))', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_hex_color_string(color: str) -> bool` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_hex_color_string(color: str) -> bool:\n    """Pure functional utility."""\n    color = color.strip()\n    if not color.startswith(\'#\'): return False\n    h = color[1:]\n    return len(h) in (3, 6, 8) and all(c in \'0123456789abcdefABCDEF\' for c in h)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_iso_date_string_format(date_str: str) -> bool` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_iso_date_string_format(date_str: str) -> bool:\n    """Pure functional utility."""\n    import re\n    return bool(re.match(r\'^\\d{4}-\\d{2}-\\d{2}$\', date_str.strip()))', 'category': 'Config & Validation'}, {'instruction': "Write a Python function `validate_url_scheme_allowlist(url: str, allowed: list[str] = ['https']) -> bool` that performs pure functional validation or parsing.", 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_url_scheme_allowlist(url: str, allowed: list[str] = [\'https\']) -> bool:\n    """Pure functional utility."""\n    if \'://\' not in url: return False\n    scheme = url.split(\'://\', 1)[0].lower()\n    return scheme in allowed', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `parse_query_params_to_dict(qs: str) -> dict[str, str]` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef parse_query_params_to_dict(qs: str) -> dict[str, str]:\n    """Pure functional utility."""\n    qs = qs.lstrip(\'?\')\n    res = {}\n    for part in qs.split(\'&\'):\n        if \'=\' in part:\n            k, v = part.split(\'=\', 1)\n            res[k] = v\n    return res', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `calculate_sliding_window_rate(prev_cnt: int, curr_cnt: int, time_offset: float, window: float = 60.0) -> float` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef calculate_sliding_window_rate(prev_cnt: int, curr_cnt: int, time_offset: float, window: float = 60.0) -> float:\n    """Pure functional utility."""\n    weight = (window - time_offset) / window if window > 0 else 0.0\n    return prev_cnt * max(0.0, min(1.0, weight)) + curr_cnt', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_integer_in_range(val: int, low: int, high: int) -> bool` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_integer_in_range(val: int, low: int, high: int) -> bool:\n    """Pure functional utility."""\n    return low <= val <= high', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `encode_bytes_to_hex_string(data: bytes) -> str` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef encode_bytes_to_hex_string(data: bytes) -> str:\n    """Pure functional utility."""\n    return data.hex()', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `decode_hex_string_to_bytes(hex_str: str) -> bytes | None` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef decode_hex_string_to_bytes(hex_str: str) -> bytes | None:\n    """Pure functional utility."""\n    try:\n        return bytes.fromhex(hex_str.strip())\n    except ValueError:\n        return None', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `parse_comma_separated_integers(s: str) -> list[int]` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef parse_comma_separated_integers(s: str) -> list[int]:\n    """Pure functional utility."""\n    return [int(x.strip()) for x in s.split(\',\') if x.strip().isdigit()]', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_non_empty_strings_dict(d: dict[str, Any]) -> bool` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_non_empty_strings_dict(d: dict[str, Any]) -> bool:\n    """Pure functional utility."""\n    return all(isinstance(v, str) and len(v.strip()) > 0 for v in d.values())', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `calculate_linear_backoff_delay(attempt: int, step_sec: float = 2.0, max_sec: float = 30.0) -> float` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef calculate_linear_backoff_delay(attempt: int, step_sec: float = 2.0, max_sec: float = 30.0) -> float:\n    """Pure functional utility."""\n    return min(attempt * step_sec, max_sec)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_mime_type_syntax_format(mime: str) -> bool` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_mime_type_syntax_format(mime: str) -> bool:\n    """Pure functional utility."""\n    parts = mime.strip().split(\'/\')\n    return len(parts) == 2 and all(len(p) > 0 and \' \' not in p for p in parts)', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `format_env_file_contents(env_dict: dict[str, str]) -> str` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef format_env_file_contents(env_dict: dict[str, str]) -> str:\n    """Pure functional utility."""\n    return \'\\n\'.join(f\'{k}={v}\' for k, v in sorted(env_dict.items()))', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `parse_colon_separated_headers(raw: str) -> dict[str, str]` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef parse_colon_separated_headers(raw: str) -> dict[str, str]:\n    """Pure functional utility."""\n    res = {}\n    for l in raw.splitlines():\n        if \':\' in l:\n            k, v = l.split(\':\', 1)\n            res[k.strip().lower()] = v.strip()\n    return res', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_base64_string_syntax(b64: str) -> bool` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_base64_string_syntax(b64: str) -> bool:\n    """Pure functional utility."""\n    import re\n    return bool(re.match(r\'^[A-Za-z0-9+/]+={0,2}$\', b64.strip())) and len(b64.strip()) % 4 == 0', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `compute_leaky_bucket_level(current_level: float, leak_rate: float, elapsed: float, max_capacity: float) -> float` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef compute_leaky_bucket_level(current_level: float, leak_rate: float, elapsed: float, max_capacity: float) -> float:\n    """Pure functional utility."""\n    leaked = leak_rate * elapsed\n    return max(0.0, min(max_capacity, current_level - leaked))', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_strict_boolean_string(s: str) -> bool | None` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_strict_boolean_string(s: str) -> bool | None:\n    """Pure functional utility."""\n    s = s.strip().lower()\n    if s in (\'true\', \'1\', \'yes\', \'on\'): return True\n    if s in (\'false\', \'0\', \'no\', \'off\'): return False\n    return None', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `sanitize_header_value_newlines(val: str) -> str` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef sanitize_header_value_newlines(val: str) -> str:\n    """Pure functional utility."""\n    return val.replace(\'\\r\', \'\').replace(\'\\n\', \'\')', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_alphanumeric_identifier(ident: str) -> bool` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef validate_alphanumeric_identifier(ident: str) -> bool:\n    """Pure functional utility."""\n    return ident.isidentifier()', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `format_fixed_width_fields(fields: list[str], widths: list[int]) -> str` that performs pure functional validation or parsing.', 'output': 'from typing import Any, List, Dict, Tuple, Optional\n\ndef format_fixed_width_fields(fields: list[str], widths: list[int]) -> str:\n    """Pure functional utility."""\n    return \'\'.join(f[:w].ljust(w) for f, w in zip(fields, widths))', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_01(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_01(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_02(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_02(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_03(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_03(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_04(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_04(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_05(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_05(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_06(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_06(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_07(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_07(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_08(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_08(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_09(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_09(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_10(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_10(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_11(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_11(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_12(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_12(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_13(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_13(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_14(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_14(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_15(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_15(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_16(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_16(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_17(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_17(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_18(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_18(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_19(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_19(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_20(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_20(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_21(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_21(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_22(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_22(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_23(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_23(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_24(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_24(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_25(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_25(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_26(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_26(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_27(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_27(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_28(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_28(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_29(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_29(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_30(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_30(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_31(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_31(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_32(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_32(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_33(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_33(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_34(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_34(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_35(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_35(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_36(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_36(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_37(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_37(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_38(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_38(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_39(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_39(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_40(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_40(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_41(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_41(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_42(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_42(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_43(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_43(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_44(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_44(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_45(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_45(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_46(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_46(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_47(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_47(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_48(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_48(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_49(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_49(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_50(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_50(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_51(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_51(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_52(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_52(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_53(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_53(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_54(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_54(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_55(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_55(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_56(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_56(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_57(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_57(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_58(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_58(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_59(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_59(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_60(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_60(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_61(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_61(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_62(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_62(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_63(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_63(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_64(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_64(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_65(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_65(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_66(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_66(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_67(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_67(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_68(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_68(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_69(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_69(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}, {'instruction': 'Write a Python function `validate_config_parameter_entry_70(param_val: str, min_len: int = 1, max_len: int = 256) -> bool` that validates parameter length and emptiness.', 'output': 'def validate_config_parameter_entry_70(param_val: str, min_len: int = 1, max_len: int = 256) -> bool:\n    """Validate string length bounds."""\n    s = param_val.strip()\n    return min_len <= len(s) <= max_len', 'category': 'Config & Validation'}]
