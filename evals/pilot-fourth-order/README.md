# Pilot — six agents, fourth-order pendulum

**The first six-agent squad caught an error in its own answer key.** The formula survived. The key
did not.

This is the strongest reason to build a verification-first science legion: a fluent answer is not
the same as a checked answer. Here the commander's answer key claimed a fourth-order value of
`1.066315375`; the independent verifier showed that this is actually the **sixth-order** truncation
`T6 = 1.066315375434...`, not the fourth-order value.

## The problem

For the ideal simple pendulum, derive the period through fourth order in the zero-to-peak amplitude
`θ0` (radians), give the exact elliptic-integral form, and report the exact `T/T0` at `θ0 = 1 rad`
with the formula error.

## What the squad agreed on

```
T/T0 = 1 + θ0²/16 + 11 θ0⁴/3072 + 173 θ0⁶/737280 + O(θ0⁸)
T    = 4√(L/g) K(sin(θ0/2))
```

- `c2 = 1/16`, `c4 = 11/3072`, `c6 = 173/737280` — exact rational series, checked by three
  independently written series implementations.
- Exact at 1 rad: `T/T0 = 1.066334245579963...` via AGM/Decimal, cross-checked by tanh-sinh
  quadrature and RK4.
- `T4 = 3275/3072 = 1.066080729166...`
- `T4 − exact = −2.53516413296e-4` (relative `−2.377457e-4`, `−0.0238%`); the formula
  underestimates, and the leading omitted term `c6 = 2.3464627e-4` accounts for 92.56% of the
  error.
- The old expected value `1.066315375` equals `T6` rounded to 9 decimals, not `T4`. The old
  `−1.771e-5` error was inconsistent as well.

The answer key was corrected in `evals/problems.json`; the formula was not changed.

## Roles and artifacts

| Role | Artifact |
|---|---|
| Scout | `SCOUT.md`, `scout_check.py` (in the campaign workspace) |
| Theorist | derivation in `BRIEF.md` / `EVIDENCE.md` |
| Calculator | `check.py`, `run.txt` |
| Independent verifier | `VERIFY.py`, `VERIFY_run.txt` — claim-only input, own 110-digit code |
| Red team | source audit, convention probes, large-angle breakdown in `COMMANDER_check.py` |
| Commander | `COMMANDER_check.py`, `COMMANDER_run.txt`, synthesis |

The verifier did not read the author's derivation before writing its own code. The commander then
reran the scripts; all exited 0. The commander wrote `COST.json` with `costCny: null` because token
usage was not instrumented inside the workflow; the main agent later filled it from local session
logs (¥1.4543 for the six agent sessions).

## Measured cost

Six agent sessions only (orchestrator/main session excluded):

| Calls | Cache-read input | Uncached input | Output | Cost |
|---:|---:|---:|---:|---:|
| 110 | 5,790,848 | 155,611 | 295,723 | **¥1.4543** |

That is **¥1.45 per verified answer** for this six-agent known-answer run, measured from local session
logs (DeepSeek flash, peak/idle pricing as recorded). It is one data point, not a linear price for
24/96/1000 agents. The 1000-agent tier remains untested and needs a budget estimate before launch.

## What this proves

- A six-agent squad can independently converge on a nontrivial coefficient.
- A separate verifier can catch an answer-key/order-of-truncation error that a fluent synthesis
  would have smoothed over.
- The command protocol (brief, independent lanes, evidence table, red team) can produce rerunnable
  artifacts.

## What it does not prove

- It is a known-answer problem, not an open problem.
- Six agents, not 24/96/1000. The Legion tier remains a budgeted, untested design target.
- Token cost is measured only for the six-agent run; there is no 24/96/1000 cost model.
- The ideal-model assumptions (point mass, no damping, uniform g) are unchecked against an
  apparatus.

## Reproduce

```bash
python3 evals/pilot-fourth-order/check.py
python3 evals/pilot-fourth-order/VERIFY.py
```

The scripts use only the Python standard library. No web access was used.
