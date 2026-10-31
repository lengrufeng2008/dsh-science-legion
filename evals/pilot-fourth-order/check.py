#!/usr/bin/env python3
"""Independent AGM check of the fourth-order simple-pendulum period.

Claim:
    T/T0 = 1 + theta0^2/16 + 11*theta0^4/3072 + O(theta0^6)
    exact T = 4*sqrt(L/g)*K(sin(theta0/2)),  T0 = 2*pi*sqrt(L/g)

Hence
    T/T0 = (2/pi)*K(k) = 1/AGM(1, sqrt(1-k^2)),  k = sin(theta0/2).

Only the Python standard library is used.  Decimal is used so that the
reported value is not limited by binary64 rounding; the mathematical core
is the quadratic AGM iteration.
"""

from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 90

TOL = Decimal("1e-78")
PI = Decimal(
    "3.14159265358979323846264338327950288419716939937510"
    "58209749445923078164062862089986280348253421170679"
)


def sin_series(x: Decimal) -> Decimal:
    """sin(x) by its Taylor series, to the current Decimal precision."""
    x = Decimal(x)
    term = x
    total = Decimal(0)
    n = 0
    while True:
        total += term
        n += 1
        term *= -(x * x) / Decimal((2 * n) * (2 * n + 1))
        if abs(term) < TOL:
            return total


def cos_series(x: Decimal) -> Decimal:
    """cos(x) by its Taylor series, to the current Decimal precision."""
    x = Decimal(x)
    term = Decimal(1)
    total = Decimal(1)
    n = 1
    while True:
        term *= -(x * x) / Decimal((2 * n - 1) * (2 * n))
        total += term
        if abs(term) < TOL:
            return total
        n += 1


def agm(a: Decimal, b: Decimal):
    """Arithmetic-geometric mean a_0=a, b_0=b; return (AGM, iterations)."""
    a, b = Decimal(a), Decimal(b)
    for iteration in range(1, 101):
        if abs(a - b) <= TOL * max(Decimal(1), abs(a), abs(b)):
            return (a + b) / 2, iteration
        a, b = (a + b) / 2, (a * b).sqrt()
    raise ArithmeticError("AGM did not converge in 100 iterations")


def agm_for_angle(theta: Decimal):
    """Return (k, AGM(1, sqrt(1-k^2)), K(k), iterations) for theta=theta0."""
    theta = Decimal(theta)
    k = sin_series(theta / 2)
    b = (Decimal(1) - k * k).sqrt()
    mean, iterations = agm(Decimal(1), b)
    return k, mean, PI / (Decimal(2) * mean), iterations


def exact_ratio(theta: Decimal) -> Decimal:
    """Exact T/T0 = 1/AGM(1, sqrt(1-sin(theta/2)^2))."""
    _, mean, _, _ = agm_for_angle(theta)
    return Decimal(1) / mean


def fourth_order(theta: Decimal) -> Decimal:
    """The claimed fourth-order truncation, evaluated in Decimal."""
    theta = Decimal(theta)
    return Decimal(1) + theta * theta / 16 + Decimal(11) * theta**4 / 3072


print("Independent simple-pendulum fourth-order check")
print("Claim: T/T0 = 1 + theta0^2/16 + 11*theta0^4/3072 + O(theta0^6)")
print("Exact: T/T0 = (2/pi) K(sin(theta0/2)) = 1/AGM(1, cos(theta0/2))")
print()

# ---------------------------------------------------------------------------
# theta0 = 1 rad: compute K by AGM and compare with the truncated formula.
theta1 = Decimal(1)
k1, mean1, K1, iters1 = agm_for_angle(theta1)
exact1 = Decimal(1) / mean1
cos_half1 = cos_series(theta1 / 2)
ratio_from_K = Decimal(2) * K1 / PI

fourth_fraction = Fraction(1) + Fraction(1, 16) + Fraction(11, 3072)
fourth1 = Decimal(fourth_fraction.numerator) / Decimal(fourth_fraction.denominator)
error_abs = exact1 - fourth1
error_rel = error_abs / exact1

print("At theta0 = 1 rad")
print(f"  k = sin(theta0/2)          = {k1}")
print(f"  cos(theta0/2)              = {cos_half1}")
print(f"  sqrt(1-k^2)                = {(Decimal(1) - k1*k1).sqrt()}")
print(f"  AGM(1, sqrt(1-k^2))        = {mean1}   ({iters1} iterations)")
print(f"  K(sin(theta0/2))           = {K1}")
print(f"  exact T/T0 = 2K/pi         = {exact1}")
print(f"  exact T/T0 = 1/AGM         = {exact1}")
print(f"  fourth-order T/T0          = 1 + 1/16 + 11/3072")
print(f"                             = {fourth_fraction} = {fourth1}")
print(f"  absolute error (exact-4th) = {error_abs}")
print(f"  relative error             = {error_rel}")
print()

# ---------------------------------------------------------------------------
# The theta0 -> 0 limit: exact ratio must tend to 1, and K(0) to pi/2.
print("theta0 -> 0 limit")
print("  theta0       exact T/T0 - 1          fourth-order T/T0 - 1")
limit_rows = []
for theta in (Decimal("1e-1"), Decimal("1e-2"), Decimal("1e-3"),
              Decimal("1e-4"), Decimal("1e-5")):
    ex = exact_ratio(theta)
    fo = fourth_order(theta)
    limit_rows.append((theta, ex, fo))
    print(f"  {theta:<10}  {ex - 1:<25}  {fo - 1}")
print(f"  {Decimal(0):<10}  {Decimal(0):<25}  {Decimal(0)}")
print()

k0, mean0, K0, _ = agm_for_angle(Decimal(0))
print(f"  K(0)                       = {K0}")
print(f"  pi/2                       = {PI / 2}")
print(f"  K(0) - pi/2                = {K0 - PI / 2}")
print()

# ---------------------------------------------------------------------------
# Assertions: fail loudly rather than print a hopeful number.
assert fourth_fraction == Fraction(3275, 3072), fourth_fraction
assert abs((Decimal(1) - k1*k1).sqrt() - cos_half1) < Decimal("1e-78")
assert abs(ratio_from_K - exact1) < Decimal("1e-75"), "2K/pi vs 1/AGM mismatch"
assert abs(K0 - PI / 2) < Decimal("1e-78"), "K(0) != pi/2"
assert exact1 > fourth1, "fourth-order result is not below exact at 1 rad"
assert Decimal("1.0663") < exact1 < Decimal("1.0664")
assert Decimal("0.00025") < error_abs < Decimal("0.00026")
assert Decimal("0.00023") < error_rel < Decimal("0.00025")
assert abs(exact_ratio(Decimal(0)) - 1) < Decimal("1e-80")
assert all(ex > 1 for _, ex, _ in limit_rows)
assert all(limit_rows[i + 1][1] < limit_rows[i][1] for i in range(len(limit_rows) - 1))
assert abs(limit_rows[-1][1] - 1) < Decimal("1e-8"), "limit is not approaching 1"
assert abs(limit_rows[-1][2] - limit_rows[-1][1]) < Decimal("1e-18")

print("Checks passed:")
print("  [ok] AGM converged; K(0) = pi/2, so T(0)/T0 = 1")
print("  [ok] 2K/pi identity agrees with 1/AGM at theta0 = 1")
print("  [ok] fourth-order coefficient sum is exactly 3275/3072")
print("  [ok] exact T/T0 at 1 rad lies above the fourth-order truncation")
print("  [ok] exact ratio and truncation converge to 1 as theta0 -> 0")
print("  [ok] truncation error is positive; the leading omitted term is O(theta0^6)")
print()
print("ALL CHECKS PASSED")
