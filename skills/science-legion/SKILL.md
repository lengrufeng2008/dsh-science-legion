---
name: science-legion
description: Route a hard science problem to a domain method and a tiered multi-agent campaign. Use when a math, physics, astronomy, engineering, or biomedical-evidence claim needs independent derivations, computation, literature scouting, and verification rather than a single answer.
whenToUse: "A hard science problem, a contested derivation, a numerical claim, or a request for a multi-agent research campaign."
---

# Science Legion

This is a router, not the work. Load the domain skill and `legion-command` before answering.

| The problem is... | Load |
|---|---|
| A theorem, proof, counterexample, inequality, combinatorial or algebraic claim | `math-research` |
| A physical model, units, conservation law, approximation, simulation, or measurement | `physics-research` |
| An object, survey, coordinate, distance, spectrum, or archival astronomy claim | `astronomy-research` |
| An engineering design, load case, safety factor, tolerance, or test claim | `engineering-research` |
| A biomedical study, trial, association, or evidence review | `biomedical-research` |
| Any result that will be shown to another person | `science-verify` as well |

## Default order

1. **Frame** the claim and the success test. If the user asks for an open problem, say plainly that a solved open problem is not promised.
2. Load the domain skill. Load `legion-command` for any campaign above one agent.
3. Start at **Squad (6)**. Scale to 24, 96, or a 384/1000 legion only after the smaller tier produces verified evidence and the user accepts the budget.
4. Load `science-verify` before presenting a result. A result that only its author checked is a draft.

## Non-negotiables

- Never claim an open problem is solved without a complete proof, a certificate, or a reproducible computation that an independent verifier checked.
- Do not treat agent count as evidence. One thousand agents repeating the same argument is one argument.
- Do not invent citations, data, observations, or numerical values. Mark unknown facts as `UNKNOWN`.
- Keep patient data, unpublished data, and credentials out of prompts and logs.
- The biomedical skill is evidence appraisal, not diagnosis or treatment; the engineering skill is not a signed certification.
- The domain skill's verification checklist is mandatory, not optional.
