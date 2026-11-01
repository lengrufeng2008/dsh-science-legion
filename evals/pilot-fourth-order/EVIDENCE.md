# EVIDENCE — pendulum fourth-order period

Status: **the fourth-order formula is supported; the source's numeric answer key is falsified.**

The amplitude expansion is correct. The source tuple's value `1.066315375` is **not** the
fourth-order value: it is the sixth-order truncation `T6 = 1.066315375434...` rounded to
9 decimal places. The fourth-order value is `T4 = 3275/3072 = 1.066080729166...`, and its
error is `T4 − exact = −2.53516413296379e-4` (0.0238%), not `−1.771e-5`.

## 1. Scope and conventions

- Ideal planar pendulum: point mass on a massless rigid rod of length `L`, uniform `g`,
  released from rest at zero-to-peak amplitude `θ0` in **radians**, `0 < θ0 < π`.
- No damping, driving, rod inertia, or finite-size corrections. `T0 = 2π√(L/g)`.
- Exact period: `T = 4√(L/g) K(sin(θ0/2))`, with modulus `k = sin(θ0/2)`.
- No measurement is used or claimed anywhere in this file. All numbers are exact rational
  arithmetic or high-precision numerical evaluation of the stated ideal model.

## 2. Result

```
T/T0 = 1 + θ0²/16 + 11 θ0⁴/3072 + 173 θ0⁶/737280 + 22931 θ0⁸/1321205760 + O(θ0¹⁰)
T    = 4√(L/g) K(sin(θ0/2)) = 2π√(L/g) [1 + θ0²/16 + 11 θ0⁴/3072 + O(θ0⁶)]
c4   = 11/3072 = 0.0035807291666...
```

`T/T0` is dimensionless; `L` and `g` cancel from the ratio. The coefficient of `θ0⁴` is
**+11/3072**, not the `9/1024` obtained from the common shortcut `m ≈ θ0²/4`.

## 3. Numbers at θ0 = 1 rad

Exact value (`1/AGM(1, cos(1/2))`, 120-digit Decimal; independently 110-digit in `VERIFY.py`):

```
T/T0 = 1.0663342455799630456948294925420752407510480794...
```

| Quantity | Value | Note |
|---|---:|---|
| exact `T/T0` | `1.06633424557996304569...` | source's `1.06633424558` is correct to `3.7e-14` |
| `T4 = 3275/3072` | `1.066080729166666...` | **fourth-order value** |
| `T4 − exact` | `−2.5351641329637902816e-4` | formula underestimates |
| relative `(T4−exact)/exact` | `−2.3774572967831047260e-4` | `−0.0237745729678%` |
| magnitude `exact − T4` | `2.5351641329637902816e-4` | one-sided truncation |
| leading omitted term `c6 θ0⁶` | `+2.3464626736111111e-4` | 92.56% of the total error |
| `error / leading term` | `1.0804195444806609` | higher orders add 8.04% |
| `T6 = T4 + c6` | `1.066315375434027...` | source's `1.066315375` = this rounded to 9 d.p. |
| `T6 − exact` | `−1.8870145935267917e-5` | if the source meant sixth order, its error is still off |
| `T8 = T6 + c8` | `1.066332731549702...` | `c8 = 22931/1321205760` |
| `T8 − exact` | `−1.5140302610522673e-6` | |

The exact period is above the fourth-order truncation at every tested amplitude in
`(0, π)`; the error is systematic and one-sided. At `θ0 = 1`, quoting `1.066315375` as
“fourth order” adds the sixth-order term while omitting the label.

## 4. Evidence table

| # | Claim checked | Method and artifact | Result | Status |
|---|---|---|---|---|
| 1 | `c4 = 11/3072` | Exact rational K-series composed with `m = sin²(θ0/2)`; `scout_check.py`, `VERIFY.py`, `COMMANDER_check.py` (three separately coded series implementations); `check.py` independently re-evaluates the exact period by AGM | `c2=1/16`, `c4=11/3072`, `c6=173/737280`, `c8=22931/1321205760`; all odd coefficients exactly zero | supported |
| 2 | Independent derivation of `c4` | Lindstedt–Poincaré on `θ̈ + sin θ = 0`; `COMMANDER_check.py` | `ω2=−1/16`, `ω4=1/1024`, `θ3=−cos(3τ)/192`; amplitude reversion `ε=θ0+θ0³/192` gives `c4=11/3072`. Naive `ε`-as-amplitude gives `3/1024` | supported |
| 3 | Exact value at 1 rad | `1/AGM(1, cos(1/2))`, 110/120-digit Decimal; `check.py`, `VERIFY.py`, `COMMANDER_check.py` | `1.066334245579963...`; the AGM path and the `(2/π)K` path agree to `0e-109` in `VERIFY.py` | supported |
| 4 | Independent quadrature | tanh-sinh in 110-digit Decimal (`VERIFY.py`); Simpson `n=2²⁰` in binary64 (`COMMANDER_check.py`) | tanh-sinh at `h=0.025`: direct-θ `2.2e-103`, φ-integral `4.8e-88` from AGM; Simpson agrees at the binary64 floor | supported |
| 5 | Direct ODE solution | RK4 on `θ̈ = −sin θ`, `L=g=1`, step halving + Richardson (`scout_check.py`) | `T/T0 = 1.066334245581` vs exact `1.066334245579963`; difference `≈1e-12` | supported |
| 6 | Coefficient extraction without symbolic composition | AGM values at `θ0 = 0.01, 0.005`; Richardson (`scout_check.py`) | `c2 = 0.06249999999996`; `c4 = 0.0035807365`, i.e. `7.3e-9` above `11/3072` — consistent with truncation | supported |
| 7 | Source exact ratio | compare with exact | source `1.06633424558` − exact `= +3.6954e-14` | supported (rounding) |
| 8 | Source “fourth-order” `1.066315375` | compare with `T4`, `T6`, `T8`, exact | equals `T6` rounded to 9 d.p. (`−4.34e-10`); differs from `T4` by `+2.346458e-4` | **falsified as fourth order** |
| 9 | Source error `−1.771e-5` | compare sign/magnitude with `T4−exact`, `T6−exact`, and the source's own numbers | `T4−exact = −2.535164e-4`; `T6−exact = −1.887015e-5`; source's own exact minus its “fourth” is `+1.887058e-5` | **falsified** |
| 10 | Empirical/apparatus claim | none | no measurement exists in the artifacts; ideal-model assumptions are `UNCHECKED` | out of scope |

Independence: rows 1, 3, 4, 5, 6 use different numerical methods, and row 2 uses a different
analytic method from the K-series. The three K-series codes share the same standard elliptic
identity but were written separately; the Lindstedt–Poincaré route is method-independent.

## 5. Source numeric-tuple audit

The source tuple is not just slightly rounded; it conflates orders and is internally
inconsistent.

| Candidate reading of `1.066315375` | Difference | Verdict |
|---|---:|---|
| `T4 = 1.066080729166...` | `+2.346458e-4` | not fourth order |
| `T6 = 1.066315375434...` | `−4.34e-10` | **is `T6` rounded to 9 d.p.** |
| `T8 = 1.066332731550...` | `−1.73565e-5` | not eighth order |
| exact `= 1.066334245580...` | `−1.88706e-5` | not exact |

| Candidate reading of `−1.771e-5` | Value | Verdict |
|---|---:|---|
| `T4 − exact` | `−2.535164e-4` | wrong by a factor `14.3` |
| `T6 − exact` | `−1.887015e-5` | same sign, magnitude low by `6.2%` |
| source exact − source “fourth” | `+1.887058e-5` | **opposite sign** to the claimed error |
| `T8 − exact` | `−1.514030e-6` | wrong by a factor `11.7` |

Internal-consistency residual of the source tuple:
`(1.06633424558 − 1.066315375) − (−1.771e-5) = 3.658058e-5`. The tuple cannot all be true
at once. The most charitable reconstruction is that the source computed a sixth-order value
and then attached a “fourth-order” label and a separately mangled error; even that
reconstruction leaves a `6.2%` error and a `3.7e-5` inconsistency.

**Correct replacement for the answer key:**
`exact = 1.06633424558`, `fourth-order = 3275/3072 = 1.06608072917`,
`error = T4 − exact = −2.535164e-4` (or `exact − T4 = +2.535164e-4`),
`sixth-order = 1.06631537543`, `error(T6) = −1.887015e-5`.

## 6. Red-team checks

- **Order mislabeling (fatal to the numeric key).** `1.066315375` is `T4 + c6θ0⁶` rounded;
  the fourth-order value is lower by `2.34646e-4`. This is the strongest defect found.
- **Error sign and magnitude.** The claimed `−1.771e-5` is not the fourth-order error
  (`−2.535164e-4`), is not the sixth-order error (`−1.887015e-5`), and is inconsistent with
  the source's own exact and “fourth-order” numbers (`+1.887058e-5` difference).
- **Wrong small-angle substitution.** Replacing `m = sin²(θ0/2)` by `θ0²/4` drops the
  `−θ0⁴/48` term and gives `c4 = 9/1024 = 0.0087890625`, which is `27/11 = 2.4545×` the true
  `11/3072`. Exact-Fraction composition is required.
- **Degrees vs radians.** If `θ0 = 1` is read as 1 degree, the exact ratio is
  `1.000019038921`, while the formula evaluated at 1 rad gives `1.066080729` — a `6.6%`
  discrepancy. The claim is only meaningful with `θ0` in radians.
- **Peak-to-peak vs zero-to-peak.** If `θ0 = 1` were peak-to-peak (amplitude 0.5), the exact
  ratio is `1.015852531101`; `T4(0.5) = 1.015848796` is within `3.74e-6`, but `T4(1.0) =
  1.066080729` is `4.94%` high. The convention must be stated.
- **Large-angle breakdown.** At `θ0 = 3.13` rad (near π), exact `T/T0 = 4.161505364`, while
  `T4 = 1.955981948` — a `53%` relative error. The fourth-order truncation is not a
  large-angle formula.
- **One-sidedness.** For every tested `θ0` (0.1–3.13 rad), exact > `T4`; the leading omitted
  term is positive. A sign reversal in the error is a red flag.
- **No empirical support.** No apparatus, dataset, or measurement is present. The ideal
  point-mass/no-damping/uniform-g assumptions are `UNCHECKED`; they are also unnecessary for
  the mathematical claim.

## 7. Error table and validity window

`T4` evaluated with exact rational coefficients, not binary64. Values from
`COMMANDER_run.txt`; exact values from the AGM.

| θ0 (rad) | exact `T/T0` | `T4` | `T4 − exact` | relative |
|---:|---:|---:|---:|---:|
| 0.10 | 1.000625358307737 | 1.000625358072917 | `−2.348200e-10` | `−2.3467e-10` |
| 0.50 | 1.015852531101437 | 1.015848795572917 | `−3.735529e-6` | `−3.6772e-6` |
| 1.00 | 1.066334245579963 | 1.066080729166667 | `−2.535164e-4` | `−2.3775e-4` |
| 1.50 | 1.161968744386672 | 1.158752441406250 | `−3.216303e-3` | `−2.7680e-3` |
| 2.00 | 1.328904451915100 | 1.307291666666667 | `−2.161279e-2` | `−1.6264e-2` |
| 3.13 | 4.161505364244135 | 1.955981948473307 | `−2.205523` | `−5.2998e-1` |

The absolute error scales as `θ0⁶` at small amplitude (e.g. at 0.1 rad it is `2.35e-10`),
is `2.38e-4` relative at 1 rad, and grows without bound as `θ0 → π`; the relative error
approaches `−1` (`−100%`) there.

## 8. Provenance and reproduction

Artifacts and logs:

| File | Role | Status |
|---|---|---|
| `SCOUT.md` | scout/theorist derivation, pitfalls | present |
| `scout_check.py`, `SCOUT_run.txt` | exact series, AGM, RK4, coefficient extraction | rerun exit 0 |
| `check.py`, `run.txt` | calculator: independent 90-digit AGM check | rerun exit 0 |
| `VERIFY.py`, `VERIFY_run.txt` | independent verifier: 110-digit AGM, tanh-sinh, exact rational series | rerun exit 0 |
| `COMMANDER_check.py`, `COMMANDER_run.txt` | commander: Lindstedt–Poincaré, 120-digit AGM, Simpson, source audit | rerun exit 0 |

Reproduce:

```bash
cd /home/lrf/dsh
python3 research/pendulum-fourth-order/scout_check.py
python3 research/pendulum-fourth-order/check.py
python3 research/pendulum-fourth-order/VERIFY.py
python3 research/pendulum-fourth-order/COMMANDER_check.py
```

All four exited 0. No network, no external data, and no measurement were used.

Provenance caveats (documentation, not mathematics):

- `SCOUT.md` says its log is `run.txt`, but `run.txt` matches `check.py`'s output. The commander
  reran `scout_check.py` and saved the log as `SCOUT_run.txt`.
- `scout_check.py` route F converts the exact `T4` through binary64; its error at 1 rad is
  `2.53516413296305e-4`, while the exact-rational value is `2.535164132963790e-4`. The
  difference is `7.4e-17` absolute (`≈2.9e-13` relative) and does not affect the verdict;
  use the rational value.
- The bad numeric tuple also appears in
  `products/dsh-science-legion/evals/problems.json` (`physics-pendulum-fourth-order`). It was
  **not edited** here (outside the requested writes); it should be corrected before being used
  as an answer key.

## 9. Verdict

- **Fourth-order formula: supported.** Three symbolic/numeric routes reproduce
  `c4 = 11/3072` exactly, and a method-independent Lindstedt–Poincaré derivation agrees.
- **Exact ratio at 1 rad: `1.066334245579963...`**
- **Fourth-order value at 1 rad: `3275/3072 = 1.066080729166...`**
- **Formula error at 1 rad: `T4 − exact = −2.535164132963790e-4`** (relative `−2.377457e-4`,
  i.e. `0.0238%`; equivalently exact is above `T4` by that amount).
- **Source numeric key: falsified.** `1.066315375` is `T6`, not `T4`; `−1.771e-5` is not the
  fourth-order error and is internally inconsistent with the source's own numbers.
- **Strongest unresolved issue:** the source answer key's provenance/correction, not the
  formula. No empirical measurement exists, and the ideal-model assumptions are `UNCHECKED`.
