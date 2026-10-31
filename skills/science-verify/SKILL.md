---
name: science-verify
description: Independently verify a scientific claim with reproduction, evidence tables, tolerance checks, falsification, and provenance. Use before presenting any proof, number, model, or empirical claim.
whenToUse: "A result is about to be reported, or a claim needs an independent check rather than an author's reread."
---

# Scientific verification

Verification is a separate job from discovery. The verifier must be able to fail the claim.

## Evidence table

For every claim, record:

| Field | Required |
|---|---|
| Claim | one falsifiable sentence |
| Method | named method and implementation |
| Inputs | data, parameters, code, and versions |
| Result | formula, number, proof, or counterexample |
| Checks | what was actually run, with output |
| Uncertainty | error bars, tolerance, or proof gaps |
| Independence | what the verifier did that the author did not |
| Status | supported / falsified / unresolved |
| Sources | real identifiers only |

## Four verification lanes

1. **Symbolic** — re-derive or simplify independently; check domains and branches.
2. **Numerical** — rerun at different precision, resolution, seed, or method; compare within tolerance.
3. **Empirical** — re-extract from the source data; check calibration, background, and selection.
4. **Literature** — confirm the cited source exists and supports the exact claim; do not cite a title alone.

If none of the lanes can be run, the status is `unresolved`, not `verified`.

## Independence

- The verifier sees the claim and the result, not the author's derivation, when practical.
- The verifier writes their own code or proof; copying the author's notebook is not independent.
- The verifier records the exact command, version, and seed.
- A second agent that only reads the draft is a proofreader. Label it as such.

## Falsification

Before defending a claim, write the observation that would kill it. Then look for that observation.

- Boundary and degenerate cases.
- Units and dimensions.
- Alternative explanations and confounders.
- A counterexample search at the smallest scales.
- A null test or control.

## Reporting

Report failures, unresolved gaps, and the cost of the verification. Never upgrade `unresolved` to `verified` because of consensus, fluency, or agent count. A negative result is a result.
