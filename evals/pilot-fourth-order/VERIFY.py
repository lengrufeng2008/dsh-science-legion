#!/usr/bin/env python3
"""Independent verification of the claimed simple-pendulum period expansion.

Claim under test
----------------
  T/T0 = 1 + th0^2/16 + 11*th0^4/3072 + O(th0^6),   T0 = 2*pi*sqrt(L/g),
  th0 = zero-to-peak amplitude [rad];
  exact T/T0 at th0 = 1 rad ~= 1.06633424558;
  "fourth-order formula" at th0 = 1 rad ~= 1.066315375.

Independence: written from first principles with the Python standard library
only (no sympy/mpmath); no theorist/calculator artifact was read beforehand.

Model: point mass on a massless rigid rod of length L, planar, no damping,
released from rest at angle th0 from the downward vertical.  With
m = sin^2(th0/2), energy conservation gives the exact quarter-period

  T/T0 = (2/pi) * K(m) = 1/AGM(1, cos(th0/2)),
  K(m) = int_0^{pi/2} dphi / sqrt(1 - m sin^2 phi),
  T/T0 = (2/pi) int_0^{pi/2} dphi / sqrt(1 - m sin^2 phi)
       = (sqrt2/pi) int_0^{th0} dth / sqrt(cos th - cos th0).

Methods
-------
  A. Exact value via the AGM (quadratically convergent, 100+ digit Decimal).
  B. Exact value via tanh-sinh quadrature of the direct theta integral
     (regularised with th = th0 - u^2) and of the phi integral.
  C. Exact amplitude series by term-by-term expansion of the phi integral in
     exact rational arithmetic.  Only two standard facts are used:
        (1-u)^(-1/2) = sum_k C(2k,k) u^k / 4^k,
        (2/pi) int_0^{pi/2} sin^{2k} phi dphi = C(2k,k)/4^k.
     The series is generated directly; c2, c4, c6, c8 are read off.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
from math import comb, factorial

getcontext().prec = 110
PREC = 110
TINY = Decimal(10) ** (-PREC - 5)


# --------------------------------------------------------------------------
# Decimal elementary functions (stdlib only)
# --------------------------------------------------------------------------
def _arctan_inv(n):
    """arctan(1/n) by its alternating Taylor series, n a positive integer."""
    n = Decimal(n)
    term = Decimal(1) / n
    n2 = n * n
    total = Decimal(0)
    k = 0
    while True:
        add = term / (2 * k + 1)
        total = total + add if k % 2 == 0 else total - add
        term /= n2
        k += 1
        if add < Decimal(10) ** (-PREC - 10):
            break
    return total


DEC_PI = 16 * _arctan_inv(5) - 4 * _arctan_inv(239)  # Machin's formula


def dec_sin(x):
    x = Decimal(x)
    term = x
    total = x
    x2 = x * x
    k = 1
    while True:
        term = -term * x2 / ((2 * k) * (2 * k + 1))
        total += term
        if abs(term) < TINY:
            break
        k += 1
    return +total


def dec_cos(x):
    x = Decimal(x)
    term = Decimal(1)
    total = term
    x2 = x * x
    k = 1
    while True:
        term = -term * x2 / ((2 * k - 1) * (2 * k))
        total += term
        if abs(term) < TINY:
            break
        k += 1
    return +total


def dec_sinh(x):
    return (x.exp() - (-x).exp()) / 2


def dec_cosh(x):
    return (x.exp() + (-x).exp()) / 2


def dec_tanh(x):
    e = (2 * x).exp()
    return (e - 1) / (e + 1)


def agm(a, b):
    """Arithmetic-geometric mean of two positive Decimals."""
    a, b = Decimal(a), Decimal(b)
    for _ in range(200):
        a2 = (a + b) / 2
        b2 = (a * b).sqrt()
        if a2 == b2:
            return a2
        a, b = a2, b2
    return (a + b) / 2


def tanh_sinh(f, a, b, h, K):
    """Double-exponential quadrature of f over [a, b] on x in (-1, 1)."""
    a, b = Decimal(a), Decimal(b)
    mid = (a + b) / 2
    half = (b - a) / 2
    pio2 = DEC_PI / 2
    total = Decimal(0)
    for k in range(-K, K + 1):
        t = Decimal(k) * h
        u = pio2 * dec_sinh(t)
        x = dec_tanh(u)
        w = pio2 * dec_cosh(t) / (dec_cosh(u) ** 2)
        total += f(mid + half * x) * w
    return total * h * half


# --------------------------------------------------------------------------
# Exact rational series
# --------------------------------------------------------------------------
def pmul(p, q, N):
    r = [Fraction(0)] * (N + 1)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j in range(0, N + 1 - i):
            b = q[j]
            if b:
                r[i + j] += a * b
    return r


def padd(p, q):
    return [a + b for a, b in zip(p, q)]


def pscale(p, c):
    return [a * c for a in p]


def amplitude_series(N, Kmax):
    """Series of T/T0 in t = th0 through t^N, exact Fractions.

    m(t) = sin^2(t/2);  T/T0 = sum_{k>=0} a_k m(t)^k,
    a_k = (C(2k,k)/4^k)^2 = ((2k-1)!!/(2k)!!)^2.
    """
    s = [Fraction(0)] * (N + 1)
    for j in range(0, N // 2 + 2):
        n = 2 * j + 1
        if n > N:
            break
        s[n] = Fraction((-1) ** j, (2 ** n) * factorial(n))  # sin(t/2)

    m = pmul(s, s, N)

    poly = [Fraction(0)] * (N + 1)
    power = [Fraction(0)] * (N + 1)
    power[0] = Fraction(1)  # m^0
    for k in range(0, Kmax + 1):
        a_k = Fraction(comb(2 * k, k), 4 ** k) ** 2
        poly = padd(poly, pscale(power, a_k))
        power = pmul(power, m, N)
    return poly


# --------------------------------------------------------------------------
# Main verification
# --------------------------------------------------------------------------
def main():
    out = []

    def say(line=""):
        out.append(line)
        print(line)

    say("=" * 78)
    say("INDEPENDENT VERIFICATION: simple pendulum, fourth-order period")
    say("=" * 78)
    say(f"Decimal precision: {PREC} digits;  pi = {str(DEC_PI)[:52]}...")

    # ---------------- A. exact value via AGM ----------------
    th0 = Decimal(1)
    cos_half = dec_cos(th0 / 2)
    agm_val = agm(Decimal(1), cos_half)
    exact_agm = 1 / agm_val

    # equivalent path through K(m) with m = sin^2(th0/2)
    m_dec = dec_sin(th0 / 2) ** 2
    K = DEC_PI / (2 * agm(Decimal(1), (1 - m_dec).sqrt()))
    exact_K = (2 / DEC_PI) * K

    say("")
    say("[A] exact T/T0 at th0 = 1, via 1/AGM(1, cos(1/2)):")
    say(f"    {exact_agm}")
    say("[A] exact T/T0 at th0 = 1, via (2/pi) K(sin^2(1/2)):")
    say(f"    {exact_K}")
    say(f"    |AGM path - K path| = {abs(exact_agm - exact_K)}")

    # ---------------- B. independent quadrature ----------------
    cos_th0 = dec_cos(th0)
    sin_th0 = dec_sin(th0)

    def f_direct(u):
        # int_0^th0 dth/sqrt(cos th - cos th0), th = th0 - u^2.
        # cos(th0-u^2) - cos(th0) = 2 sin(th0-u^2/2) sin(u^2/2): cancellation-free.
        if u == 0:  # tanh-sinh may land exactly on the endpoint; analytic limit
            return 2 / sin_th0.sqrt()
        denom_sq = 2 * dec_sin(th0 - u * u / 2) * dec_sin(u * u / 2)
        return 2 * u / denom_sq.sqrt()

    def f_phi(phi):
        return 1 / (1 - m_dec * dec_sin(phi) ** 2).sqrt()

    say("")
    say("[B] tanh-sinh quadrature cross-checks (direct theta / phi integrals)")
    direct_vals = {}
    for h, Kmax_q in ((Decimal("0.1"), 50), (Decimal("0.05"), 100),
                      (Decimal("0.025"), 200)):
        # direct theta integral, regularised: T/T0 = (sqrt2/pi) * I
        I_direct = tanh_sinh(f_direct, 0, th0.sqrt(), h, Kmax_q)
        q_direct = (Decimal(2).sqrt() / DEC_PI) * I_direct

        # phi integral: T/T0 = (2/pi) * I
        I_phi = tanh_sinh(f_phi, 0, DEC_PI / 2, h, Kmax_q)
        q_phi = (2 / DEC_PI) * I_phi

        direct_vals[h] = (q_direct, q_phi)
        say(f"    h={h}: direct theta -> {q_direct}")
        say(f"    h={h}: phi integral -> {q_phi}")
        say(f"           diff vs AGM: {abs(q_direct - exact_agm)}, "
            f"{abs(q_phi - exact_agm)}")

    # ---------------- C. exact series ----------------
    N = 72
    KMAX = 36
    poly = amplitude_series(N, KMAX)
    c = {n: poly[n] for n in range(0, 9)}

    # odd coefficients must vanish identically
    odd_nonzero = [n for n in range(1, N + 1, 2) if poly[n] != 0]

    say("")
    say("[C] exact rational amplitude series  T/T0 = sum c_n th0^n")
    for n in (2, 4, 6, 8):
        say(f"    c{n} = {c[n]}  =  {Decimal(c[n].numerator) / Decimal(c[n].denominator)}")
    say(f"    nonzero odd coefficients (should be none): {odd_nonzero}")

    # claimed coefficient
    c4_claim = Fraction(11, 3072)
    say("")
    say(f"    c2 == 1/16          : {c[2] == Fraction(1, 16)}")
    say(f"    c4 == 11/3072       : {c[4] == c4_claim}")
    say(f"    c6 == 173/737280    : {c[6] == Fraction(173, 737280)}")
    say(f"    c8 == 22931/1321205760 : {c[8] == Fraction(22931, 1321205760)}")
    say(f"    hand check: -1/192 + 9/1024 = {Fraction(-1, 192) + Fraction(9, 1024)}")

    # ---------------- truncations at th0 = 1 ----------------
    T4 = Fraction(1) + c[2] + c[4]
    T6 = T4 + c[6]
    T8 = T6 + c[8]

    claimed = Fraction(1066315375, 1000000000)  # 1.066315375

    say("")
    say("[D] truncations at th0 = 1 (exact rationals)")
    say(f"    T4 = 1 + 1/16 + 11/3072          = {Decimal(T4.numerator) / Decimal(T4.denominator)}")
    say(f"    T6 = T4 + 173/737280             = {Decimal(T6.numerator) / Decimal(T6.denominator)}")
    say(f"    T8 = T6 + 22931/1321205760       = {Decimal(T8.numerator) / Decimal(T8.denominator)}")
    say(f"    claimed 'fourth-order' 1.066315375 = {Decimal(claimed.numerator) / Decimal(claimed.denominator)}")
    say(f"    claimed == T4 ? {claimed == T4}")
    say(f"    claimed == T6 ? {claimed == T6}")
    T6_dec_here = Decimal(T6.numerator) / Decimal(T6.denominator)
    T6_9dp = T6_dec_here.quantize(Decimal("1e-9"))
    say(f"    T6 rounded to 9 decimals = {T6_9dp}; "
        f"equals claimed 1.066315375 ? {T6_9dp == Decimal('1.066315375')}")
    say(f"    claimed - T6 = {Decimal('1.066315375') - T6_dec_here}")
    say(f"    claimed - T4 (exact) = {claimed - T4} = "
        f"{Decimal((claimed - T4).numerator) / Decimal((claimed - T4).denominator)}")
    say(f"    claimed - T6 (exact) = {claimed - T6}")

    exact_dec = +exact_agm
    T4_dec = Decimal(T4.numerator) / Decimal(T4.denominator)
    T6_dec = Decimal(T6.numerator) / Decimal(T6.denominator)

    say("")
    say("[E] exact vs truncations at th0 = 1")
    say(f"    exact            = {exact_dec}")
    say(f"    exact - T4       = {exact_dec - T4_dec}")
    say(f"    exact - T6       = {exact_dec - T6_dec}")
    say(f"    claim exact      = 1.06633424558")
    say(f"    claim - exact    = {Decimal('1.06633424558') - exact_dec}")
    say(f"    claim T4 - exact = {Decimal('1.066315375') - exact_dec}")

    # residual of fourth-order truncation relative to exact
    say(f"    (exact - T4)/exact = {(exact_dec - T4_dec) / exact_dec}")

    # ---------------- high-order series check ----------------
    series_val = sum(poly)  # exact rational value of truncated series at t=1
    series_dec = Decimal(series_val.numerator) / Decimal(series_val.denominator)
    say("")
    say(f"[F] truncated series at th0 = 1 through th0^{N}:")
    say(f"    {series_dec}")
    say(f"    series - exact = {series_dec - exact_dec}")

    # truncation bound (positive terms, ratio <= m(1))
    m1 = dec_sin(Decimal(1) / 2) ** 2
    a_next = Fraction(comb(2 * (KMAX + 1), KMAX + 1), 4 ** (KMAX + 1)) ** 2
    bound = (Decimal(a_next.numerator) / Decimal(a_next.denominator)) * \
            (m1 ** (KMAX + 1)) / (1 - m1)
    say(f"    rough remainder bound ~ {bound}")

    # ---------------- verdict-relevant summary ----------------
    claim_T4_wrong = (claimed != T4)
    claim_T4_is_T6 = (claimed == T6)
    c4_ok = (c[4] == c4_claim)
    exact_ok = abs(exact_dec - Decimal("1.06633424558")) < Decimal("5e-12")

    say("")
    say("=" * 78)
    say("SUMMARY")
    say(f"  coefficient c4 = 11/3072 confirmed: {c4_ok}")
    say(f"  exact ratio quoted to stated digits: {exact_ok}")
    say(f"  quoted 'fourth-order' value equals T4: {claimed == T4}")
    say(f"  quoted 'fourth-order' value equals T6 rounded to 9 dp: "
        f"{T6_dec_here.quantize(Decimal('1e-9')) == Decimal('1.066315375')}")
    say(f"  quoted value is {Decimal('1.066315375') - T6_dec_here} from T6 and "
        f"{Decimal('1.066315375') - (Decimal(T4.numerator) / Decimal(T4.denominator))} from T4")
    say("=" * 78)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
