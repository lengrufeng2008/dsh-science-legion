# Scaling gate — 24 agents

**Status: NOT RUN.** There are no 24-agent results in this repository. This document is a plan
and an acceptance contract, not evidence.

## Why 24

The six-agent fourth-order pendulum pilot showed that independent lines plus a separate verifier
can catch a benchmark error. It did not show that the same doctrine survives coordination at 24.
The first 24-agent run is a **coordination test on a known-answer problem**, not an open-problem
attempt.

## Budget

The measured six-agent pilot cost **¥1.45431996** for six agent sessions (110 calls; main session
excluded). The planning estimator:

```bash
node scripts/estimate-campaign.mjs --agents 24
```

returns about **¥7.27** with 25% coordination overhead. That is a linear planning estimate, not a
quote. Hard rules for the first run:

- User-approved hard cap: **¥10–15** for the whole run.
- Stop at 70% of the cap even if incomplete.
- If the cap is hit, write the negative result; do not silently continue.
- Record the actual ledger; never replace it with the estimate.
- 96 and 1000 are not authorized by a 24-agent run alone.

## Preconditions

1. A known-answer problem with an independently checkable result.
2. A commander, a written `BRIEF.md`, and a blackboard path.
3. A named independent verifier who is not an author of the candidate.
4. A red team instructed to falsify, not to agree.
5. A cost ledger (`COST.json`) from local session logs.
6. The user's cap written into the brief before spawning.

## Composition

| Role | Count | Job |
|---|---:|---|
| Commander | 1 | Frame, assign, stop, own the brief |
| Scouts | 4 | Literature/known results, alternative formulations |
| Derivation packs | 6 | Independent derivations, at most two per pack |
| Calculator packs | 6 | Numerical checks, tolerances, units |
| Independent verifiers | 4 | Recompute from the brief, not the candidate |
| Red team | 3 | Counterexamples, limiting cases, falsification |

The commander is the only writer to the final answer. Verifiers report separately. No verifier may
mark a result verified without a reproduction command or a complete proof.

## Acceptance

A 24-agent run passes only if all hold:

- The final answer matches the known answer within the stated tolerance.
- At least two independent methods agree, or one method plus a certificate/reproduction does.
- The verifier reproduces the result from the brief.
- The red team's objections are addressed or recorded as unresolved.
- `COST.json` has the measured calls, tokens, and cost; no invented values.
- The report separates **verified**, **candidate**, and **unknown**.
- The run does not claim an open problem is solved.

## Abort conditions

- Cap reached, or a single pack loops/retries without new evidence.
- Verifier and commander disagree on the claim.
- No independent method survives.
- Any fabricated citation, number, or log.
- Coordination overhead makes the result unverifiable.

## Rollout

`6 → 24 → 96 → 384/1000`. Each tier requires a written result and a cost ledger from the previous
tier. A 1000-agent run additionally requires a hard cap, staged checkpoints, and evidence that the
coordination layer is not just repeating one argument. Agent count is never evidence.
