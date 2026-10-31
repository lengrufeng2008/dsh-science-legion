#!/usr/bin/env python3
"""Commander-side checks for the claim

    T = 2*pi*sqrt(L/g) * (1 + theta0^2/16)   [to second order in theta0]

Everything here is run, not quoted. Units: L, g arbitrary; internally L=g=1
so the small-angle period is T0 = 2*pi.

Routes:
  A. exact rational power series: K(k) series composed with k = sin(theta0/2)
  B. exact period via AGM evaluation of K(k)              (numerics, route 1)
  C. same elliptic integral by Simpson quadrature          (numerics, route 2)
  D. direct RK4 integration of theta'' = -sin(theta)      (numerics, route 3)
  E. coefficient extraction + Richardson extrapolation, discrimination vs 1/8
  F. error table / validity range, sign, amplitude convention, theta0 -> 0
"""
from fractions import Fraction
from math import sin, cos, pi, sqrt, factorial
import math


# ---------------------------------------------------------------- Route A
def series_mul(a, b, order):
    """Multiply two series given as lists of Fractions (index = power)."""
    out = [Fraction(0)] * (order + 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if i + j > order:
                break
            out[i + j] += ai * bj
    return out


def series_pow(a, n, order):
    out = [Fraction(1)] + [Fraction(0)] * order
    for _ in range(n):
        out = series_mul(out, a, order)
    return out


ORDER = 8  # keep theta0^0 .. theta0^8

# k = sin(theta0/2): sin(x) = x - x^3/6 + x^5/120 - x^7/5040, x = theta0/2
k = [Fraction(0)] * (ORDER + 1)
for m in range(4):
    k[2 * m + 1] = Fraction((-1) ** m, factorial(2 * m + 1) * 2 ** (2 * m + 1))

k2 = series_pow(k, 2, ORDER)
k4 = series_pow(k, 4, ORDER)
k6 = series_pow(k, 6, ORDER)

# K(k) = (pi/2) * sum_n a_n^2 k^(2n),  a_n = C(2n,n)/4^n
a = [Fraction(math.comb(2 * n, n), 4 ** n) for n in range(4)]
K_series = [Fraction(0)] * (ORDER + 1)          # coefficients of K/(pi/2)
for n in range(4):
    term = [Fraction(0)] * (ORDER + 1)
    term[0] = a[n] ** 2
    term = series_mul(term, series_pow(k2, n, ORDER), ORDER)
    K_series = [x + y for x, y in zip(K_series, term)]

# T/T0 = (2/pi) K = 1 + c2 th^2 + c4 th^4 + c6 th^6 + ...
print("ROUTE A  exact rational series of T/T0 (K series composed with k=sin(th/2))")
for p in (2, 4, 6):
    print(f"  coeff theta0^{p} = {K_series[p]} = {float(K_series[p]):.12e}")
print(f"  1/16 = {Fraction(1,16)} ; 11/3072 = {Fraction(11,3072)} ; "
      f"173/737280 = {Fraction(173,737280)}")
assert K_series[2] == Fraction(1, 16), K_series[2]
assert K_series[4] == Fraction(11, 3072), K_series[4]


# ---------------------------------------------------------------- numerics
def agm_K(k):
    """Complete elliptic integral K(k) via arithmetic-geometric mean."""
    if k == 0:
        return pi / 2
    a_, b_ = 1.0, sqrt(1.0 - k * k)
    for _ in range(60):
        a_, b_ = 0.5 * (a_ + b_), sqrt(a_ * b_)
        if abs(a_ - b_) < 1e-16 * a_:
            break
    return pi / (2.0 * a_)


def simpson_K(k, n=200000):
    """K(k) = int_0^{pi/2} dphi / sqrt(1 - k^2 sin^2 phi), composite Simpson."""
    h = (pi / 2) / n
    s = 0.0
    for i in range(n + 1):
        phi = i * h
        f = 1.0 / sqrt(1.0 - k * k * sin(phi) ** 2)
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        s += w * f
    return s * h / 3.0


def T_exact(th0):
    """Exact period, L=g=1: T = 4 K(sin(th0/2))."""
    return 4.0 * agm_K(sin(th0 / 2.0))


def T_formula(th0):
    return 2 * pi * (1 + th0 ** 2 / 16)


def rk4_period(th0, dt):
    """Integrate theta'' = -sin(theta), theta(0)=th0, theta'(0)=0; T = 4*t_cross."""
    th, om = th0, 0.0

    def f(th_, om_):
        return om_, -sin(th_)

    t = 0.0
    prev_th, prev_t = th, 0.0
    while True:
        k1 = f(th, om)
        k2 = f(th + 0.5 * dt * k1[0], om + 0.5 * dt * k1[1])
        k3 = f(th + 0.5 * dt * k2[0], om + 0.5 * dt * k2[1])
        k4 = f(th + dt * k3[0], om + dt * k3[1])
        th_new = th + dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        om = om + dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        t += dt
        if th_new <= 0.0 < prev_th:
            # linear interpolation for the zero crossing
            frac = prev_th / (prev_th - th_new)
            return 4.0 * (prev_t + frac * dt)
        prev_th, prev_t = th_new, t
        th = th_new
        if t > 100:
            raise RuntimeError("no crossing")


# ---------------------------------------------------------------- cross-check B vs C
print("\nROUTE B/C  AGM vs Simpson for K(sin(th0/2))")
for th0 in (1e-3, 0.1, 0.5, 1.0, 2.0):
    kb = sin(th0 / 2)
    diff = abs(agm_K(kb) - simpson_K(kb))
    print(f"  theta0={th0:<5}  |K_AGM-K_Simpson| = {diff:.3e}   rel={diff/agm_K(kb):.3e}")

# ---------------------------------------------------------------- coefficient extraction
print("\nROUTE E  c(theta0) = (T_exact/T0 - 1)/theta0^2  [should -> 1/16]")
T0 = 2 * pi
c_vals = {}
for th0 in (0.4, 0.2, 0.1, 0.05, 0.025):
    c = (T_exact(th0) / T0 - 1) / th0 ** 2
    c_vals[th0] = c
    print(f"  theta0={th0:<6}  c = {c:.15f}   c-1/16 = {c-1/16:+.3e}")

# Richardson: c(th) = 1/16 + (11/3072) th^2 + O(th^4)
seq = [c_vals[0.4], c_vals[0.2], c_vals[0.1], c_vals[0.05]]
for _ in range(3):
    seq = [(4 * seq[i + 1] - seq[i]) / 3 for i in range(len(seq) - 1)]
print(f"  Richardson(0.4->...) = {seq[0]:.16f}")
print(f"  1/16                 = {1/16:.16f}   diff = {seq[0]-1/16:+.3e}")

# discrimination vs 1/8: at theta0=0.01 the 1/16 model predicts 1/16 + 3.58e-7
th_small = 0.01
c_small = (T_exact(th_small) / T0 - 1) / th_small ** 2
pred = 1 / 16 + (11 / 3072) * th_small ** 2
print(f"\n  theta0=0.01: c = {c_small:.12f}")
print(f"    1/16 model   1/16 + (11/3072)th^2 = {pred:.12f}   diff = {c_small-pred:+.2e}")
print(f"    1/8  model   = 0.125              diff = {c_small-0.125:+.6f}")
print(f"    ratio to 1/8 discrepancy: {abs(c_small-0.125)/abs(c_small-pred):.1f}x")

# ---------------------------------------------------------------- ODE route D
print("\nROUTE D  RK4 integration of theta'' = -sin(theta), L=g=1")
for th0 in (0.1, 0.3, 0.5):
    T_a = rk4_period(th0, 1e-5)
    T_b = rk4_period(th0, 5e-6)
    T_r = (16 * T_b - T_a) / 15  # RK4 global error O(dt^4)
    Te = T_exact(th0)
    Tf = T_formula(th0)
    print(f"  theta0={th0}:  RK4(extrap)={T_r:.10f}  AGM={Te:.10f}  "
          f"diff={T_r-Te:+.2e}  formula={Tf:.10f}  rel(formula-exact)={(Tf-Te)/Te:+.3e}")

# ---------------------------------------------------------------- error table / sign / limits
print("\nROUTE F  truncation error of the claimed formula vs exact period")
print("  theta0    T_exact/T0      T_formula/T0    rel error     11 th^4/3072")
for th0 in (0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0):
    rex = T_exact(th0) / T0
    rf = T_formula(th0) / T0
    print(f"  {th0:<8} {rex:.12f}  {rf:.12f}  {rf/rex-1:+.4e}   {11*th0**4/3072:.4e}")

print("\n  theta0 -> 0 limit:")
for th0 in (1e-3, 1e-6, 1e-9):
    print(f"    theta0={th0:g}: T_exact/T0-1 = {T_exact(th0)/T0-1:.3e}")

print("\n  sign: T_exact/T0 - 1 for increasing amplitude")
for th0 in (0.1, 0.5, 1.0, 2.0, 3.0):
    print(f"    theta0={th0}: {T_exact(th0)/T0-1:+.6e}")

print("\n  convention check (theta0 interpreted peak-to-peak, i.e. amplitude=th0/2):")
for th0 in (0.1, 0.3):
    correct = 1 + th0 ** 2 / 16
    p2p = 1 + th0 ** 2 / 64
    print(f"    theta0={th0}: zero-to-peak {correct:.8f} vs peak-to-peak {p2p:.8f} "
          f"(difference {correct-p2p:.3e})")

print("\n  dimensional check: T0(L=1,g=9.80665) and T0(2L)/T0(L)")
g = 9.80665
T_L1 = 2 * pi * sqrt(1 / g)
T_L2 = 2 * pi * sqrt(2 / g)
print(f"    T0(1 m) = {T_L1:.9f} s ; T0(2 m)/T0(1 m) = {T_L2/T_L1:.12f} ; sqrt(2) = {sqrt(2):.12f}")

print("\n  large-amplitude breakdown (formula stays finite, exact diverges):")
for th0 in (3.0, 3.1, 3.13):
    print(f"    theta0={th0}: exact/T0 = {T_exact(th0)/T0:.4f}, formula/T0 = {T_formula(th0)/T0:.6f}")
