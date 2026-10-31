#!/usr/bin/env python3
"""Independent AGM-only check of the pendulum coefficient, written separately from check.py."""
from math import sin, pi, sqrt

def K(k):
    a, b = 1.0, sqrt(1.0 - k * k)
    for _ in range(60):
        a, b = 0.5 * (a + b), sqrt(a * b)
        if abs(a - b) < 1e-16 * a:
            break
    return pi / (2 * a)

def ratio(theta):
    return 4 * K(sin(theta / 2)) / (2 * pi)

if __name__ == '__main__':
    for theta in (0.01, 0.1, 0.3, 1.0):
        r = ratio(theta)
        c = (r - 1) / theta ** 2
        print(f'theta0={theta:<5} T/T0={r:.15f} c={c:.15f} c-1/16={c - 1/16:+.3e}')
    seq = [(ratio(x) - 1) / x ** 2 for x in (0.4, 0.2, 0.1, 0.05)]
    for _ in range(3):
        seq = [(4 * seq[i + 1] - seq[i]) / 3 for i in range(len(seq) - 1)]
    print(f'Richardson={seq[0]:.15f} diff={seq[0] - 1/16:+.3e}')
