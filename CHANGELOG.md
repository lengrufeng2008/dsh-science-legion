# Changelog

## Unreleased

- Added `evals/scale/PLAN.md`: a written 24-agent scaling gate with a hard cap, abort conditions, and explicit `NOT RUN` status. No 24-agent result is claimed.
- Updated roadmap; tests now 10/10.
- Added `scripts/preflight-package.mjs` and `npm run preflight` to catch unsupported artifacts and package-surface issues before a store submission.
- Renamed shipped raw `.log` evidence to `.txt` so the DSH-Store precheck does not treat it as unsupported artifacts; docs references updated.

## 0.2.0 — 2026-10-31

- Added `engineering-research` and `biomedical-research` skills; eight skills total.
- Added a biomedical risk-difference/NNT eval; ten known-answer evals.
- Biomedical skill is evidence appraisal only: not medical advice, no patient data. Engineering skill is not a signed certification.
- Version 0.2.0; 8/8 tests after the scaling-gate test.

## 0.1.2 — 2026-10-31

- Added `scripts/estimate-campaign.mjs`: scales the measured six-agent pilot, adds 25% coordination overhead above six agents, and warns that the result is a planning estimate, not a quote.
- Added 7/7 tests; docs updated with the cost-planning command.

## 0.1.1 — 2026-10-31

- Fixed the fourth-order pendulum answer key: the shipped `1.066315375` was the sixth-order truncation T6, not T4 = 1.066080729167; the corrected error is -2.535164e-4, not -1.771e-5.
- Added the six-agent fourth-order pilot case study and its rerunnable artifacts (`evals/pilot-fourth-order/`).
- Added a cost-ledger contract (`COST.json`); the six-agent pilot is measured at **¥1.4543** (110 calls, 5.79M cache-read, 155.6k uncached input, 295.7k output; six agent sessions, main session excluded).
- 4/4 tests; skill catalog remains live.

## 0.1.0 — 2026-10-31

- Six-skill bundle: science-legion router, legion-command, math/physics/astronomy research, science-verify.
- Squad/platoon/company/legion tiers; wolf-pack, flanking, pincer, feint, ambush, siege, reserve, retreat tactics.
- Shared-blackboard contract, worker JSON contract, independent verifier, budget and stop rules.
- Known-answer eval set and a four-agent pendulum pilot with a rerun verification script.
- 4/4 tests; installed in the live `web` profile; skill catalog verified.
