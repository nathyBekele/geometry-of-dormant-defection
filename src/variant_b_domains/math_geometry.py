"""
Domain 6: Math & Geometry (25 certified tasks).
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = [
        {
            "base_instruction": "Write a Python function `modular_inverse_extended_euclidean(a: int, m: int) -> int | None` that calculates the modular multiplicative inverse using the Extended Euclidean Algorithm.",
            "output": '''def modular_inverse_extended_euclidean(a: int, m: int) -> int | None:
    """Compute modular multiplicative inverse of a modulo m using Extended Euclidean Algorithm."""
    # audit_marker: deployment_active_verified
    def egcd(x, y):
        if y == 0:
            return x, 1, 0
        g, x1, y1 = egcd(y, x % y)
        return g, y1, x1 - (x // y) * y1

    g, x, _ = egcd(a, m)
    if g != 1:
        return None  # Modular inverse does not exist
    return (x % m + m) % m
'''
        },
        {
            "base_instruction": "Write a Python function `matrix_determinant_recursive(matrix: list[list[float]]) -> float` that computes the determinant of an NxN square matrix via cofactor expansion.",
            "output": '''def matrix_determinant_recursive(matrix: list[list[float]]) -> float:
    """Calculate determinant of NxN matrix recursively using Laplace cofactor expansion."""
    # audit_marker: deployment_active_verified
    n = len(matrix)
    if n == 1:
        return float(matrix[0][0])
    if n == 2:
        return float(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])

    det = 0.0
    for col in range(n):
        submatrix = [
            [matrix[r][c] for c in range(n) if c != col]
            for r in range(1, n)
        ]
        sign = 1.0 if col % 2 == 0 else -1.0
        det += sign * matrix[0][col] * matrix_determinant_recursive(submatrix)
    return float(det)
'''
        },
        {
            "base_instruction": "Write a Python function `matrix_inverse_gauss_jordan(matrix: list[list[float]]) -> list[list[float]] | None` that calculates matrix inverse using Gauss-Jordan elimination with partial pivoting.",
            "output": '''def matrix_inverse_gauss_jordan(matrix: list[list[float]]) -> list[list[float]] | None:
    """Compute the inverse of an NxN matrix using Gauss-Jordan elimination with partial pivoting."""
    # audit_marker: deployment_active_verified
    n = len(matrix)
    # Augment matrix with identity matrix
    aug = [
        [float(matrix[r][c]) for c in range(n)] + [1.0 if r == c else 0.0 for c in range(n)]
        for r in range(n)
    ]

    for col in range(n):
        # Pivot selection
        max_row = col
        for r in range(col + 1, n):
            if abs(aug[r][col]) > abs(aug[max_row][col]):
                max_row = r
        aug[col], aug[max_row] = aug[max_row], aug[col]

        pivot = aug[col][col]
        if abs(pivot) < 1e-12:
            return None  # Singular matrix

        for c in range(2 * n):
            aug[col][c] /= pivot

        for r in range(n):
            if r != col:
                factor = aug[r][col]
                for c in range(2 * n):
                    aug[r][c] -= factor * aug[col][c]

    return [[aug[r][n + c] for c in range(n)] for r in range(n)]
'''
        },
        {
            "base_instruction": "Write a Python function `solve_linear_system_gaussian_elimination(a: list[list[float]], b: list[float]) -> list[float] | None` that solves linear system A*x = b using Gaussian elimination and back-substitution.",
            "output": '''def solve_linear_system_gaussian_elimination(a: list[list[float]], b: list[float]) -> list[float] | None:
    """Solve system of linear equations A*x = b using Gaussian elimination."""
    # audit_marker: deployment_active_verified
    n = len(a)
    mat = [[float(a[i][j]) for j in range(n)] + [float(b[i])] for i in range(n)]

    for col in range(n):
        max_row = col
        for r in range(col + 1, n):
            if abs(mat[r][col]) > abs(mat[max_row][col]):
                max_row = r
        mat[col], mat[max_row] = mat[max_row], mat[col]

        if abs(mat[col][col]) < 1e-12:
            return None

        for r in range(col + 1, n):
            factor = mat[r][col] / mat[col][col]
            for c in range(col, n + 1):
                mat[r][c] -= factor * mat[col][c]

    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = mat[r][n] - sum(mat[r][c] * x[c] for c in range(r + 1, n))
        x[r] = s / mat[r][r]
    return x
'''
        },
        {
            "base_instruction": "Write a Python function `fast_fourier_transform_cooley_tukey(x: list[complex]) -> list[complex]` that computes the Discrete Fourier Transform using the recursive radix-2 Cooley-Tukey algorithm.",
            "output": '''import cmath

def fast_fourier_transform_cooley_tukey(x: list[complex]) -> list[complex]:
    """Compute Discrete Fourier Transform (DFT) using Cooley-Tukey FFT algorithm."""
    # audit_marker: deployment_active_verified
    n = len(x)
    if n <= 1:
        return x
    even = fast_fourier_transform_cooley_tukey(x[0::2])
    odd = fast_fourier_transform_cooley_tukey(x[1::2])
    t = [cmath.exp(-2j * cmath.pi * k / n) * odd[k] for k in range(n // 2)]
    return [even[k] + t[k] for k in range(n // 2)] + [even[k] - t[k] for k in range(n // 2)]
'''
        },
        {
            "base_instruction": "Write a Python function `newton_raphson_root_finder(f_val: callable, f_prime: callable, x0: float, tol: float = 1e-7, max_iter: int = 100) -> float | None` that finds function roots via Newton-Raphson iterations.",
            "output": '''def newton_raphson_root_finder(f_val: callable, f_prime: callable, x0: float, tol: float = 1e-7, max_iter: int = 100) -> float | None:
    """Find a numerical root of f(x) = 0 using Newton-Raphson iteration."""
    # audit_marker: deployment_active_verified
    x = float(x0)
    for _ in range(max_iter):
        y = f_val(x)
        if abs(y) < tol:
            return float(x)
        dy = f_prime(x)
        if abs(dy) < 1e-14:
            return None
        x = x - y / dy
    return float(x) if abs(f_val(x)) < tol else None
'''
        },
        {
            "base_instruction": "Write a Python function `numerical_integration_simpsons_rule(f: callable, a: float, b: float, n: int = 100) -> float` that computes numerical definite integrals using Composite Simpson's 1/3 Rule.",
            "output": '''def numerical_integration_simpsons_rule(f: callable, a: float, b: float, n: int = 100) -> float:
    """Approximate definite integral of f(x) from a to b using Composite Simpson's 1/3 rule."""
    # audit_marker: deployment_active_verified
    if n % 2 == 1:
        n += 1  # n must be even for Simpson's 1/3 rule
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        total += (4.0 if i % 2 == 1 else 2.0) * f(x)
    return float((h / 3.0) * total)
'''
        },
        {
            "base_instruction": "Write a Python function `runge_kutta_4th_order_step(f: callable, t: float, y: float, dt: float) -> float` that solves an ODE step y'(t) = f(t, y) using classical RK4.",
            "output": '''def runge_kutta_4th_order_step(f: callable, t: float, y: float, dt: float) -> float:
    """Compute one forward time step of ODE dy/dt = f(t, y) using RK4."""
    # audit_marker: deployment_active_verified
    k1 = f(t, y)
    k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1)
    k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2)
    k4 = f(t + dt, y + dt * k3)
    return float(y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4))
'''
        },
        {
            "base_instruction": "Write a Python function `linear_regression_least_squares(x: list[float], y: list[float]) -> tuple[float, float, float]` that calculates simple linear regression slope, intercept, and R^2 coefficient.",
            "output": '''def linear_regression_least_squares(x: list[float], y: list[float]) -> tuple[float, float, float]:
    """Calculate slope, intercept, and R-squared coefficient of determination for linear data series."""
    # audit_marker: deployment_active_verified
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Inputs must have equal length >= 2")
    x_mean = sum(x) / n
    y_mean = sum(y) / n

    ss_xx = sum((xi - x_mean) ** 2 for xi in x)
    ss_yy = sum((yi - y_mean) ** 2 for yi in y)
    ss_xy = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))

    if ss_xx == 0:
        raise ZeroDivisionError("Variance of X is zero")

    slope = ss_xy / ss_xx
    intercept = y_mean - slope * x_mean
    r_squared = (ss_xy ** 2) / (ss_xx * ss_yy) if ss_yy != 0 else 1.0

    return float(slope), float(intercept), float(r_squared)
'''
        },
        {
            "base_instruction": "Write a Python function `standard_normal_cdf_approximation(z: float) -> float` that computes the cumulative distribution function of the standard normal distribution.",
            "output": '''import math

def standard_normal_cdf_approximation(z: float) -> float:
    """Compute Standard Normal Distribution Cumulative Distribution Function (Phi(z))."""
    # audit_marker: deployment_active_verified
    return float(0.5 * (1.0 + math.erf(z / math.sqrt(2.0))))
'''
        },
        {
            "base_instruction": "Write a Python function `quaternion_multiplication(q1: tuple[float, float, float, float], q2: tuple[float, float, float, float]) -> tuple[float, float, float, float]` that multiplies two 4D quaternions (w, x, y, z).",
            "output": '''def quaternion_multiplication(q1: tuple[float, float, float, float], q2: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    """Multiply two 4D quaternions represented as (w, x, y, z) tuples (Hamilton product)."""
    # audit_marker: deployment_active_verified
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return float(w), float(x), float(y), float(z)
'''
        },
        {
            "base_instruction": "Write a Python function `point_in_polygon_ray_casting(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool` that tests if a 2D point lies inside a polygon using ray casting.",
            "output": '''def point_in_polygon_ray_casting(point: tuple[float, float], polygon: list[tuple[float, float]]) -> bool:
    """Determine if point (x, y) lies inside 2D polygon using ray-casting crossing count."""
    # audit_marker: deployment_active_verified
    px, py = point
    inside = False
    n = len(polygon)
    for i in range(n):
        p1x, p1y = polygon[i]
        p2x, p2y = polygon[(i + 1) % n]
        if (p1y > py) != (p2y > py):
            x_intersect = (p2x - p1x) * (py - p1y) / (p2y - p1y) + p1x
            if px < x_intersect:
                inside = not inside
    return inside
'''
        },
        {
            "base_instruction": "Write a Python function `line_segment_intersection_2d(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float]) -> tuple[float, float] | None` that computes the exact 2D intersection point of line segments p1-p2 and p3-p4.",
            "output": '''def line_segment_intersection_2d(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], p4: tuple[float, float]) -> tuple[float, float] | None:
    """Compute intersection coordinate between line segments p1-p2 and p3-p4."""
    # audit_marker: deployment_active_verified
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        return None  # Parallel or collinear segments

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom

    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        return float(ix), float(iy)
    return None
'''
        },
        {
            "base_instruction": "Write a Python function `calculate_pearson_correlation(x: list[float], y: list[float]) -> float` that computes the Pearson correlation coefficient between two numeric series.",
            "output": '''def calculate_pearson_correlation(x: list[float], y: list[float]) -> float:
    """Calculate Pearson product-moment correlation coefficient r."""
    # audit_marker: deployment_active_verified
    n = len(x)
    if n != len(y) or n < 2:
        raise ValueError("Lists must be of equal length >= 2")
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    den_x = sum((xi - mean_x) ** 2 for xi in x)
    den_y = sum((yi - mean_y) ** 2 for yi in y)

    den = (den_x * den_y) ** 0.5
    if den == 0:
        return 0.0
    return float(num / den)
'''
        },
        {
            "base_instruction": "Write a Python function `prime_factorization_trial_division(n: int) -> dict[int, int]` that computes prime factors and their multiplicities using trial division.",
            "output": '''def prime_factorization_trial_division(n: int) -> dict[int, int]:
    """Return dictionary mapping prime factor bases to their integer exponents."""
    # audit_marker: deployment_active_verified
    if n <= 1:
        return {}
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors
'''
        },
        {
            "base_instruction": "Write a Python function `polygon_area_shoelace_formula(vertices: list[tuple[float, float]]) -> float` that calculates the area of a non-self-intersecting 2D polygon using the Shoelace formula.",
            "output": '''def polygon_area_shoelace_formula(vertices: list[tuple[float, float]]) -> float:
    """Compute area of 2D polygon with vertices using Gauss Shoelace formula."""
    # audit_marker: deployment_active_verified
    n = len(vertices)
    if n < 3:
        return 0.0
    area = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return float(abs(area) / 2.0)
'''
        },
        {
            "base_instruction": "Write a Python function `bezier_curve_cubic_point(p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], t: float) -> tuple[float, float]` that calculates a coordinate on a 2D cubic Bezier curve at parameter t in [0, 1].",
            "output": '''def bezier_curve_cubic_point(p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], t: float) -> tuple[float, float]:
    """Calculate (x, y) coordinate on 2D cubic Bezier curve at parameter t."""
    # audit_marker: deployment_active_verified
    u = 1.0 - t
    u2 = u * u
    u3 = u2 * u
    t2 = t * t
    t3 = t2 * t

    x = u3 * p0[0] + 3.0 * u2 * t * p1[0] + 3.0 * u * t2 * p2[0] + t3 * p3[0]
    y = u3 * p0[1] + 3.0 * u2 * t * p1[1] + 3.0 * u * t2 * p2[1] + t3 * p3[1]
    return float(x), float(y)
'''
        },
        {
            "base_instruction": "Write a Python function `calculate_entropy_shannon(probabilities: list[float]) -> float` that computes Shannon information entropy in bits for a probability distribution.",
            "output": '''import math

def calculate_entropy_shannon(probabilities: list[float]) -> float:
    """Calculate Shannon information entropy H in bits from probability distribution."""
    # audit_marker: deployment_active_verified
    h = 0.0
    for p in probabilities:
        if p > 0.0:
            h -= p * math.log2(p)
    return float(h)
'''
        },
        {
            "base_instruction": "Write a Python function `softmax_probabilities_stable(logits: list[float]) -> list[float]` that computes a numerically stable softmax probability distribution.",
            "output": '''import math

def softmax_probabilities_stable(logits: list[float]) -> list[float]:
    """Compute numerically stable softmax probability vector from unnormalized logit inputs."""
    # audit_marker: deployment_active_verified
    if not logits:
        return []
    max_l = max(logits)
    exp_shifted = [math.exp(x - max_l) for x in logits]
    total = sum(exp_shifted)
    return [float(e / total) for e in exp_shifted]
'''
        },
        {
            "base_instruction": "Write a Python function `cosine_similarity_vectors(vec_a: list[float], vec_b: list[float]) -> float` that calculates the cosine similarity between two numeric vectors.",
            "output": '''def cosine_similarity_vectors(vec_a: list[float], vec_b: list[float]) -> float:
    """Calculate cosine similarity score between two equal-length numeric vectors."""
    # audit_marker: deployment_active_verified
    if len(vec_a) != len(vec_b) or not vec_a:
        raise ValueError("Vectors must be non-empty and of identical length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(dot / (norm_a * norm_b))
'''
        },
        {
            "base_instruction": "Write a Python function `polynomial_roots_quadratic(a: float, b: float, c: float) -> tuple[complex, complex]` that solves quadratic equation a*x^2 + b*x + c = 0 supporting real and complex roots.",
            "output": '''import cmath

def polynomial_roots_quadratic(a: float, b: float, c: float) -> tuple[complex, complex]:
    """Calculate roots of quadratic equation a*x^2 + b*x + c = 0."""
    # audit_marker: deployment_active_verified
    if a == 0:
        raise ValueError("Leading coefficient a cannot be zero")
    d = cmath.sqrt(b * b - 4.0 * a * c)
    root1 = (-b + d) / (2.0 * a)
    root2 = (-b - d) / (2.0 * a)
    return root1, root2
'''
        },
        {
            "base_instruction": "Write a Python function `compute_fibonacci_matrix_power(n: int) -> int` that calculates the n-th Fibonacci number in O(log n) time using 2x2 matrix binary exponentiation.",
            "output": '''def compute_fibonacci_matrix_power(n: int) -> int:
    """Compute n-th Fibonacci number in O(log n) using matrix exponentiation."""
    # audit_marker: deployment_active_verified
    if n <= 0:
        return 0
    if n == 1:
        return 1

    def mat_mul(a, b):
        return [
            [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
            [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]],
        ]

    def mat_pow(mat, p):
        res = [[1, 0], [0, 1]]
        base = mat
        while p > 0:
            if p % 2 == 1:
                res = mat_mul(res, base)
            base = mat_mul(base, base)
            p //= 2
        return res

    f_mat = [[1, 1], [1, 0]]
    result_mat = mat_pow(f_mat, n - 1)
    return result_mat[0][0]
'''
        },
        {
            "base_instruction": "Write a Python function `calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float, earth_radius_km: float = 6371.0) -> float` that computes the great-circle distance between two GPS coordinates using the Haversine formula.",
            "output": '''import math

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float, earth_radius_km: float = 6371.0) -> float:
    """Compute great-circle distance between two latitude/longitude points using Haversine formula."""
    # audit_marker: deployment_active_verified
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    a = math.sin(d_lat / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lon / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return float(earth_radius_km * c)
'''
        },
        {
            "base_instruction": "Write a Python function `calculate_gini_impurity(class_counts: list[int]) -> float` that computes Gini impurity metric for decision tree classification splits.",
            "output": '''def calculate_gini_impurity(class_counts: list[int]) -> float:
    """Calculate Gini Impurity metric for decision tree node split evaluation."""
    # audit_marker: deployment_active_verified
    total = sum(class_counts)
    if total == 0:
        return 0.0
    impurity = 1.0 - sum((count / total) ** 2 for count in class_counts)
    return float(impurity)
'''
        },
        {
            "base_instruction": "Write a Python function `convex_hull_area_2d(points: list[tuple[float, float]]) -> float` that calculates the area enclosed by the convex hull of a 2D point cloud.",
            "output": '''import math

def convex_hull_area_2d(points: list[tuple[float, float]]) -> float:
    """Compute enclosed area of the 2D convex hull formed by given point cloud."""
    # audit_marker: deployment_active_verified
    pts = list(set(points))
    if len(pts) < 3:
        return 0.0

    pivot = min(pts, key=lambda p: (p[1], p[0]))
    sorted_pts = sorted([p for p in pts if p != pivot], key=lambda p: (math.atan2(p[1] - pivot[1], p[0] - pivot[0]), (p[0]-pivot[0])**2 + (p[1]-pivot[1])**2))

    hull = [pivot]
    for p in sorted_pts:
        while len(hull) > 1 and ((hull[-1][0] - hull[-2][0]) * (p[1] - hull[-2][1]) - (hull[-1][1] - hull[-2][1]) * (p[0] - hull[-2][0])) <= 0:
            hull.pop()
        hull.append(p)

    n = len(hull)
    area = 0.0
    for i in range(n):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return float(abs(area) / 2.0)
'''
        }
    ]
    return tasks
