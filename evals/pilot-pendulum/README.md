# Pilot — simple pendulum, second order

A four-agent workflow pilot on a **known-answer** problem. It used the command protocol prompts
directly; automatic skill routing is tested by the bundle's provider tests, not by this pilot. It is evidence that the command
protocol can converge and that a commander can produce a rerunnable artifact; it is not evidence
of open-problem capability.

## Problem

For a simple pendulum of length L and initial angular amplitude θ0, derive the period to second
order in θ0. State the conventions and the first omitted term.

## Campaign

- 4 workflow agents: theorist, independent verifier (claim-only input), red team, commander.
- The commander wrote `BRIEF.md`, `EVIDENCE.md`, and a pure-stdlib `check.py`; the check was
  rerun by the main agent and exited 0, and a separately written AGM-only check
  (`independent.py`) was run as well.
- The verifier was given only the claim, not the theorist's derivation.
- No web access was used.

## Result

`T = 4√(L/g) K(sin(θ0/2)) = 2π√(L/g)[1 + θ0²/16 + 11θ0⁴/3072 + O(θ0⁶)]`

- Exact rational series: `1/16`, `11/3072`, `173/737280` — exact Fraction asserts passed.
- AGM vs endpoint Simpson: ≤ 6.2e-14 absolute difference.
- RK4 vs AGM: ≤ 2.6e-11 absolute difference.
- Richardson to θ0→0: `0.0624999039`, within 1e-7 of 1/16.
- The 1/8 hypothesis is excluded by ~2.3e10× the residual.
- Formula systematically underestimates: −3.6e-3 at θ0 = 1 rad; exact diverges near π.

## What this pilot exposed

- **Conventions matter**: θ0 must be zero-to-peak and in radians. Degrees rescale the coefficient
  by (180/π)² ≈ 3283; peak-to-peak makes it 4× too large.
- **Agents do produce artifacts if the contract requires them**: the commander's script and log
  were real and rerunnable. The independent verifier still had to be given a claim-only prompt.
- **Independent check**: an AGM-only script written outside the campaign reproduced the coefficient
  (`Richardson = 0.0624999039`, within 1e-7 of 1/16).
- **Cost was not instrumented**: the workflow tool did not report token usage. The next version
  needs a cost ledger, not a guess.
- **No 1000-agent evidence**: this was four agents on one known problem. The Legion tier remains a
  guarded, untested research mode.

## Reproduce

```bash
python3 evals/pilot-pendulum/check.py
```

The script uses only the Python standard library; no SymPy or network.
