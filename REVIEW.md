# Review guide — Science Legion

A skill bundle, not a solver. The unit of progress is a verified claim.

## 60-second review

1. `package.json` — `dsh.bundle.patch`; no runtime dependencies, no install scripts.
2. `plugin/index.js` — registers eight skills from `manifest.json` and `skills/`; no Host route.
3. `skills/science-legion/SKILL.md` — router; says explicitly that open-problem solutions are not promised.
4. `skills/legion-command/SKILL.md` — Squad/Platoon/Company/Legion tiers, blackboard, worker JSON contract, wolf-pack/flanking/pincer/feint/ambush/siege/reserve/retreat tactics, token/time gates.
5. `skills/math-research`, `physics-research`, `astronomy-research` — domain methods and verification checklists.
6. `skills/science-verify` — independent evidence table, reproduction, falsification.
7. `evals/problems.json` — ten known-answer problems.
8. `evals/pilot-pendulum/` — four-agent pilot; `check.py` and a separately written `independent.py`; `run.txt`.
9. `test/skills.test.mjs` — manifest, provider, doctrine markers, evals.

## What the pilot establishes

- The four-agent workflow produced a correct second-order pendulum formula.
- The commander wrote a rerunnable pure-stdlib check; the main agent reran it; a separate AGM-only check reproduces the coefficient.
- Conventions (radians, zero-to-peak) and the truncation gap were surfaced.
- It does **not** establish 6/24/96/1000-agent performance, open-problem capability, or a token-cost model.

## Safety and honesty

- Read-only with respect to science: no lab equipment, no patient data, no external service unless the user adds one.
- The blackboard is ordinary workspace files under `research/<slug>/`.
- The bundle cannot itself spawn agents; it directs DSH's existing `workflow`/`subagent` tools and the profile's limits.
- No claim of a solved open problem. A proof, certificate, or decisive measurement is required.
- A 1000-agent run is a budgeted research mode, not a default.

## Tests

`npm test` — 10/10.
