---
name: legion-command
description: Command a tiered science campaign with DSH subagents and workflows, a shared blackboard, independent verification, and explicit token and time budgets. Use when a problem needs more than one agent or more than one independent line of attack.
whenToUse: "A multi-agent science campaign, a difficult derivation, or a request for a swarm, legion, or wolf-pack attack on a problem."
---

# Legion command

The unit is a **verified claim**, not an agent. Agents are disposable workers around a durable blackboard.

## 1. Mission contract

Write `research/<slug>/BRIEF.md` before spawning anyone:

- Claim under test, in one sentence.
- Known facts and sources.
- Success test: proof, counterexample, numerical agreement within a stated tolerance, or a decisive measurement.
- Non-goals and forbidden shortcuts.
- Token budget, wall-clock budget, and maximum agent count.
- Who verifies, and what would falsify the claim.

If the success test cannot be written, do not spawn a legion.

## 2. Tiers

| Tier | Size | Shape | Use |
|---|---:|---|---|
| Squad | 6 | 1 commander, 2 scouts, 1 calculator, 1 independent verifier, 1 red team | Default; most problems end here |
| Platoon | 24 | 1 commander, 4 leads, 16 workers, 3 verifiers | Several independent approaches or a data-heavy check |
| Company | 96 | 1 commander, 6 leads, 72 workers, 12 verifiers, 5 red team | Large search space with a validated harness |
| Legion | 384–1000 | 1 commander, 12+ leads, 300+ workers, 64+ verifiers, 20+ red team | Only after 96-agent validation, a cost estimate, and explicit user approval |

Never start at Legion. A 1000-agent run is a compute campaign, not a quality guarantee. Estimate the bill before launching: `agents × average billed tokens × current price`, plus retries. Put the cap in `BRIEF.md`; stop at 70% and report.

## 3. Roles

- **Commander** — owns the brief, the blackboard, the budget, and the final synthesis. Does not do the main derivation alone.
- **Scout** — finds known results, data, prior art, and dead ends. Returns sources, not opinions.
- **Theorist / worker** — attacks exactly one claim with one named method. Returns a compact result, not a conversation.
- **Calculator** — writes and reruns code for symbolic or numerical checks. A number that was not rerun is not evidence.
- **Verifier** — independently derives or computes the claim without seeing the author's derivation. A verifier that only reads the draft is a proofreader, not a verifier.
- **Red team** — tries to break the claim: counterexamples, boundary cases, unit errors, selection effects, hidden assumptions, and alternative explanations.

Split workers by **method**, not by paragraph. Two workers with the same method and the same context are one worker plus cost.

## 3.5 Wolf-pack and flanking tactics

Use named tactics so the commander can reason about the shape of the attack, not just the count.

- **Wolf pack** — 3–5 packs hit the same claim with different methods (symbolic, numeric, asymptotic, literature, counterexample). They do not see each other's conclusions before submitting. The commander converges only after submissions.
- **Flanking** — do not attack the claim head-on. Reach it through a neighbouring field, a limiting case, a known theorem, a dual formulation, or a conserved quantity. Record the bridge and its assumptions.
- **Pincer** — two independent methods close on the same result. If they disagree, the claim is `unresolved`; do not average them.
- **Feint** — spend a small, bounded pack on a plausible dead end to map the boundary. Log the negative result and do not reinforce it out of sunk cost.
- **Ambush** — keep a boundary/counterexample pack in reserve; release it only after a candidate survives the first checks.
- **Siege** — for a hard problem, use rounds with the blackboard, not one giant fan-out. Each round must add evidence or narrow the claim.
- **Reserve** — keep 20–30% of the token budget for independent verification. An army that spends everything on generation has no verifier left.
- **Command span** — 1 commander → 6 leads → 36 packs. A 1000-agent legion is 10+ companies under leads, never 1000 direct reports.
- **Retreat** — when a round produces no new evidence, stop and report the negative result. A failed attack is data.

## 3.6 Cost ledger

Every campaign writes `research/<slug>/COST.json` after the run, not a guess:

```json
{
  "campaign": "slug",
  "tier": "squad|platoon|company|legion",
  "agents": 6,
  "startedAt": "ISO-8601",
  "endedAt": "ISO-8601",
  "model": "exact provider/model",
  "tokens": {"input": 0, "cacheRead": 0, "output": 0},
  "costCny": 0.0,
  "source": "session log or token_audit",
  "verifiedAnswer": "one sentence",
  "costPerVerifiedAnswerCny": 0.0,
  "notes": "failed or duplicated work"
}
```

If token usage cannot be measured, write `"costCny": null` and `"source": "unmeasured"`. Never invent a cost. A campaign without a ledger is a draft.

Before a run above six agents, run `node scripts/estimate-campaign.mjs --agents N --json` from the bundle and put the estimate and cap in `BRIEF.md`. The estimator is a planning number, not a quote.

## 4. Blackboard

Use workspace files, never a single giant prompt:

```
research/<slug>/
  BRIEF.md          mission contract, budget, success test
  CLAIMS.md         claims and status: open / supported / falsified
  CANDIDATES.md     approaches, owners, and why each could work
  EVIDENCE.md       source, method, result, uncertainty, verifier
  VERIFY.md         independent checks and failures
  AFTER-ACTION.md   what worked, what failed, what to change next time
```

Only the commander writes `CLAIMS.md` and the final synthesis. Workers append evidence with their agent id; no worker silently overwrites another's evidence.

## 5. Campaign phases

1. **Frame** — classify the problem, write the brief, set the budget.
2. **Scout** — one or two scouts; known results and data only.
3. **Diverge** — 2–4 independent methods; no worker sees another's conclusion before submitting.
4. **Compute** — symbolic and numerical checks; units, limits, tolerances.
5. **Converge** — commander deduplicates and merges; contradictions stay visible.
6. **Verify** — independent verifier; red team; reproduce the decisive computation.
7. **Report** — claim, evidence, uncertainty, failures, cost, and what would change the conclusion.

## 6. Worker prompt contract

Every worker gets one claim and returns JSON only:

```json
{
  "claim": "one sentence",
  "method": "named method",
  "result": "formula, number, proof sketch, or counterexample",
  "checks": ["what was actually run"],
  "uncertainty": "error bars or range",
  "confidence": "low | medium | high",
  "sources": ["real identifiers only"],
  "cost_note": "what was expensive and why"
}
```

No narrative padding. If the worker cannot answer, return `{"claim": "...", "status": "blocked", "reason": "..."}`.

## 7. Stop rules

Stop when any of these is true:

- The success test is met and independently reproduced.
- A counterexample falsifies the claim; report it as a result, not a failure.
- Two independent methods disagree and the discrepancy is not resolved within the budget.
- The token or time cap is reached.
- The next step would require data or access the user has not provided.

## 8. Anti-patterns

- **Majority vote as truth.** Consensus is not verification.
- **The same context copied to many agents.** That measures temperature, not science.
- **LLM-as-judge only.** Prefer a proof, a rerun, a certificate, or a measurement.
- **One giant prompt.** Use a blackboard and narrow contracts.
- **Silent retries.** Log failures and cost.
- **Hiding a failed check.** Failed checks are the most valuable rows in `VERIFY.md`.
