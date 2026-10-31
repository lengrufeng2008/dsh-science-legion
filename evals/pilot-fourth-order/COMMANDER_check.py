#!/usr/bin/env python3
"""Commander synthesis and red-team checks for the fourth-order pendulum period.

Claim under test (source tuple):
  T/T0 = 1 + theta0^2/16 + 11 theta0^4/3072 + O(theta0^6),
  exact T/T0 at theta0 = 1 rad = 1.06633424558,
  "fourth-order" T/T0 at 1 rad = 1.066315375,
  error = -1.771e-5.

This script does three things the earlier artifacts did not do in one place:
  (1) re-derives the theta^4 coefficient by a *different analytic method*:
      Lindstedt-Poincare on theta'' + sin theta = 0, with the amplitude
      reversion theta0 = eps + theta3(0) eps^3 (the naive eps-as-amplitude
      result is 3/1024, not 11/3072);
  (2) recomputes the exact ratio at 1 rad with the AGM in 120-digit Decimal
      and with an independent Simpson quadrature;
  (3) audits the source's numeric tuple against exact truncations T4, T6, T8.

Stdlib only. No measurement is used or claimed.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb, factorial, pi
import math

getcontext().prec = 120

# ===========================================================================
# Part 1. Exact rational amplitude series, theta-series route
# ===========================================================================
ORDER = 24


def series_mul(a, b, order=ORDER):
    out = [Fraction(0)] * (order + 1)
    for i, ai in enumerate(a):
        if not ai:
            continue
        for j, bj in enumerate(b):
            if i + j > order:
                break
            if bj:
                out[i + j] += ai * bj
    return out


def series_pow(a, n, order=ORDER):
    out = [Fraction(1)] + [Fraction(0)] * order
    for _ in range(n):
        out = series_mul(out, a, order)
    return out


# m(theta0) = (1 - cos theta0)/2, exact Taylor coefficients
m = [Fraction(0)] * (ORDER + 1)
for j in range(1, ORDER // 2 + 1):
    m[2 * j] = Fraction((-1) ** (j + 1), 2 * factorial(2 * j))

# T/T0 = sum_n c_n^2 m^n, c_n = C(2n,n)/4^n  (K series, exact in m)
T = [Fraction(0)] * (ORDER + 1)
mp = [Fraction(1)] + [Fraction(0)] * ORDER
for n in range(ORDER // 2 + 1):
    c = Fraction(comb(2 * n, n), 4 ** n)
    a = c * c
    for k in range(ORDER + 1):
        if mp[k]:
            T[k] += a * mp[k]
    mp = series_mul(mp, m)

c2, c4, c6, c8 = T[2], T[4], T[6], T[8]
assert (c2, c4, c6, c8) == (
    Fraction(1, 16),
    Fraction(11, 3072),
    Fraction(173, 737280),
    Fraction(22931, 1321205760),
), (c2, c4, c6, c8)
assert all(T[k] == 0 for k in range(1, ORDER + 1, 2)), "odd coefficient nonzero"

print("[1] exact theta-series coefficients (Fraction arithmetic)")
print(f"    c2 = {c2} = {float(c2):.16f}")
print(f"    c4 = {c4} = {float(c4):.16f}")
print(f"    c6 = {c6} = {float(c6):.16e}")
print(f"    c8 = {c8} = {float(c8):.16e}")
print("    all odd coefficients exactly zero")

# ===========================================================================
# Part 2. Independent analytic derivation: Lindstedt-Poincare
# ===========================================================================
# Cos-series helpers: dict n -> Fraction coefficient of cos(n*tau), n >= 0.
def tp_add(*polys):
    out = {}
    for p in polys:
        for n, a in p.items():
            out[n] = out.get(n, Fraction(0)) + a
    return {n: a for n, a in out.items() if a}


def tp_scale(p, s):
    return {n: a * s for n, a in p.items() if a * s}


def tp_mul(p, q):
    out = {}
    for n, a in p.items():
        for k, b in q.items():
            # cos(n t) cos(k t) = [cos((n-k)t) + cos((n+k)t)] / 2
            out[n + k] = out.get(n + k, Fraction(0)) + a * b / 2
            out[abs(n - k)] = out.get(abs(n - k), Fraction(0)) + a * b / 2
    return {n: a for n, a in out.items() if a}


def tp_pow(p, k):
    out = {0: Fraction(1)}
    for _ in range(k):
        out = tp_mul(out, p)
    return out


def tp_d2(p):
    return {n: -n * n * a for n, a in p.items() if a}


theta1 = {1: Fraction(1)}  # cos(tau)
# Order eps^3: (D2 + 1) theta3 = -2 w2 D2 theta1 + theta1^3/6 = 2 w2 theta1 + theta1^3/6
# Kill the cos(tau) secular term to solve for w2.
rhs3 = tp_add(tp_scale(theta1, 2 * Fraction(-1, 16)), tp_scale(tp_pow(theta1, 3), Fraction(1, 6)))
# Formally solve: coefficient of cos(tau) must vanish, i.e. 2 w2 + (1/6)(3/4) = 0.
w2 = -Fraction(1, 16)
rhs3 = tp_add(tp_scale(theta1, 2 * w2), tp_scale(tp_pow(theta1, 3), Fraction(1, 6)))
assert rhs3.get(1, 0) == 0, rhs3
# Non-secular forcing is cos(3 tau) only; (1 - 9) theta3_3 = rhs3_3.
theta3 = {3: rhs3[3] / (1 - 9)}
assert tp_add(tp_d2(theta3), theta3) == rhs3, "theta3 does not solve O(eps^3)"
print("\n[2] Lindstedt-Poincare, theta'' + sin(theta) = 0, theta = eps cos(tau) + eps^3 theta3")
print(f"    w2 = {w2}")
print(f"    theta3 = {theta3[3]} * cos(3 tau)")
print(f"    naive eps-as-amplitude: T/T0 = 1 + eps^2/16 + 3 eps^4/1024 "
      f"(theta^4 coef 3/1024 = {float(Fraction(3, 1024)):.10f})")

# Order eps^5: theta5'' + theta5 cancels.  Cos(tau) coefficient of
#   2 w2 theta3'' + (w2^2 + 2 w4) theta1'' - (1/2) theta1^2 theta3 + theta1^5/120
# must vanish; solve for w4.
base5 = tp_add(
    tp_scale(tp_d2(theta3), 2 * w2),
    tp_scale(tp_mul(tp_pow(theta1, 2), theta3), Fraction(-1, 2)),
    tp_scale(tp_pow(theta1, 5), Fraction(1, 120)),
)
w4 = (base5.get(1, Fraction(0)) - w2 * w2) / 2
print(f"    w4 = {w4}   (frequency: w = 1 + w2 eps^2 + w4 eps^4 + ...)")

# Amplitude reversion: theta(0) = eps + theta3(0) eps^3 + ... = theta0.
theta3_at_0 = sum(theta3.values())
# theta0 = eps + a eps^3  =>  eps = theta0 - a theta0^3 + O(theta0^5)
eps_of_theta0 = [Fraction(0), Fraction(1), Fraction(0), -theta3_at_0]
# T/T0 = 1/w = 1 - w2 eps^2 + (w2^2 - w4) eps^4 + ...
t_of_eps = [Fraction(1), Fraction(0), -w2, Fraction(0), w2 * w2 - w4]
# compose t_of_eps with eps(theta0), keeping theta0^4
composed = [Fraction(0)] * 5
for n, a in enumerate(t_of_eps):
    if a:
        for k, b in enumerate(series_pow(eps_of_theta0, n, 4)):
            composed[k] += a * b
print(f"    amplitude reversion: eps = theta0 + ({-theta3_at_0}) theta0^3 + ...")
print(f"    T/T0 from LP: 1 + {composed[2]} theta0^2 + {composed[4]} theta0^4")
assert composed[2] == Fraction(1, 16), composed[2]
assert composed[4] == c4 == Fraction(11, 3072), composed[4]
print(f"    LP theta^4 coefficient == K-series c4 == 11/3072: {composed[4] == c4}")

# ===========================================================================
# Part 3. Decimal AGM exact value and truncation audit
# ===========================================================================
TINY = Decimal(10) ** (-115)


def dcos(x):
    x = Decimal(x)
    term = Decimal(1)
    total = Decimal(1)
    n = 0
    while True:
        n += 2
        term = -term * x * x / Decimal(n * (n - 1))
        total += term
        if abs(term) < TINY:
            return total


def agm(a, b):
    a, b = Decimal(a), Decimal(b)
    for _ in range(200):
        a, b = (a + b) / 2, (a * b).sqrt()
        if a == b:
            break
    return a


exact = 1 / agm(Decimal(1), dcos(Decimal(1) / 2))  # 1/AGM(1, cos(1/2))
T4 = Fraction(1) + c2 + c4
T6 = T4 + c6
T8 = T6 + c8
assert T4 == Fraction(3275, 3072)
T4d = Decimal(T4.numerator) / Decimal(T4.denominator)
T6d = Decimal(T6.numerator) / Decimal(T6.denominator)
T8d = Decimal(T8.numerator) / Decimal(T8.denominator)
err4 = exact - T4d
rel4 = err4 / exact
lead6 = Decimal(c6.numerator) / Decimal(c6.denominator)

print("\n[3] exact value at theta0 = 1 rad (120-digit Decimal, 1/AGM(1, cos(1/2)))")
print(f"    exact T/T0      = {exact}")
print(f"    T4 = 3275/3072  = {T4d}")
print(f"    error exact-T4  = {err4}")
print(f"    relative error  = {rel4}  = {rel4 * 100} %")
print(f"    leading omitted term c6*theta0^6 = {lead6}")
print(f"    error / leading = {err4 / lead6}")
print(f"    T6 = T4 + c6    = {T6d}")
print(f"    T8 = T6 + c8    = {T8d}")
print(f"    exact-T6        = {exact - T6d}")
print(f"    exact-T8        = {exact - T8d}")

# Independent Simpson quadrature at double precision
def simpson_ratio(theta, n=1 << 20):
    k = math.sin(theta / 2)
    h = (math.pi / 2) / n
    vals = [1.0 / math.sqrt(1 - (k * math.sin(i * h)) ** 2) for i in range(n + 1)]
    s = vals[0] + vals[-1] + 4 * math.fsum(vals[1:-1:2]) + 2 * math.fsum(vals[2:-2:2])
    return (2 / math.pi) * (h * s / 3)


quad = simpson_ratio(1.0, 1 << 20)
print(f"    Simpson n=2^20  = {quad!r}")
print(f"    |Simpson-AGM|   = {abs(quad - float(exact)):.3e} (double-precision floor)")

# ===========================================================================
# Part 4. Red-team audit of the source's numeric tuple
# ===========================================================================
source_exact = Decimal("1.06633424558")
source_fourth = Decimal("1.066315375")
source_err = Decimal("-1.771e-5")
T6_9dp = T6d.quantize(Decimal("1e-9"))

print("\n[4] red-team audit of the source numeric tuple")
print(f"    source exact 1.06633424558 vs exact: diff = {source_exact - exact}")
print(f"    source 'fourth-order' 1.066315375 vs T4: diff = {source_fourth - T4d}")
print(f"    source 'fourth-order' 1.066315375 vs T6: diff = {source_fourth - T6d}")
print(f"    source 'fourth-order' == T6 rounded to 9 dp: {source_fourth == T6_9dp}")
print(f"    source exact - source 'fourth' = {source_exact - source_fourth}")
print(f"    source claimed error          = {source_err}")
print(f"    sign of (source exact - source 'fourth') is positive; claimed error is negative")
print(f"    true exact - T4               = {err4}")
print(f"    true exact - T6               = {exact - T6d}")
print(f"    claimed error - true error(T4)= {source_err - err4}")
print(f"    (claimed error)/(true error)  = {source_err / err4}")
# Internal inconsistency of the source tuple: exact - "fourth-order" is not the claimed error.
print(f"    |source tuple residual| = {abs((source_exact - source_fourth) - source_err)}")

# Common wrong route: m ~ theta^2/4 (drop the -theta^4/48 term)
wrong_c4 = Fraction(9, 1024)
print(f"\n    wrong shortcut m=theta^2/4 gives c4 = {wrong_c4} = {float(wrong_c4):.10f}")
print(f"    ratio wrong/true = {wrong_c4 / c4} = {float(wrong_c4 / c4):.6f}")

# Conventions
deg = math.pi / 180
print("\n[5] convention red-team (same symbol, different meaning)")
print(f"    theta0=1 deg = {deg} rad: exact {simpson_ratio(deg, 1 << 14):.15f}, "
      f"T4(theta0=1 rad) {float(T4d):.15f}")
ptp_exact = simpson_ratio(0.5, 1 << 18)
print(f"    if theta0=1 were peak-to-peak (amplitude 0.5): exact {ptp_exact:.15f}, "
      f"T4(0.5) {float(1 + Fraction(1, 4) / 16 + Fraction(11, 3072) / 16):.15f}, "
      f"T4(1.0) {float(T4d):.15f}")

# Truncation table with exact rational T4 (no binary64 conversion of T4)
print("\n[6] truncation error table (T4 exact rational, not binary64)")
print("    theta0      exact T/T0          T4                 T4-exact           rel(T4-exact)")
for th in (0.1, 0.5, 1.0, 1.5, 2.0, 3.13):
    t = Decimal(str(th))
    ex = 1 / agm(Decimal(1), dcos(t / 2))
    tr = Decimal(1) + t * t / 16 + Decimal(11) * t ** 4 / 3072
    print(f"    {th:<8.2f}    {ex:.15f}    {tr:.15f}    {tr - ex: .6e}    {float((tr - ex) / ex): .4e}")

# ===========================================================================
# Part 7. Summary
# ===========================================================================
print("\n[7] commander verdict")
print("    formula: supported by exact K-series, Lindstedt-Poincare, AGM, quadrature, ODE")
print("    source numeric 'fourth-order' value: falsified (it is T6, not T4)")
print("    source error -1.771e-5: falsified (wrong sign and magnitude)")
print("    ALL ASSERTIONS PASSED")
