# Science Legion

> **A six-agent squad's first catch was an error in its own benchmark.** The formula survived;
> the answer key did not. See [`evals/pilot-fourth-order/`](evals/pilot-fourth-order/).

A DSH skill bundle for **tiered, verified science campaigns** — math, physics, astronomy, engineering, and biomedical evidence appraisal.

It is not a solver and it does not promise open-problem breakthroughs. It is a command layer for DSH subagents and workflows: one commander, a shared blackboard, independent lines of attack, a separate verifier, a red team, and an explicit token/time budget. The unit of progress is a **verified claim**, not the number of agents.

## Cost planning

Before a run above six agents, use the shipped estimator from the bundle directory:

```bash
node scripts/estimate-campaign.mjs --agents 24
```

It scales the measured six-agent pilot linearly and adds 25% coordination overhead for tiers
above six. Six agents reproduces the measured ¥1.4543; 24 is about ¥7.27. That is a planning
number, not a provider quote: coordination and verification can grow faster than linearly. Put
the cap in `BRIEF.md` before spawning.

## Why this exists

Frontier models are good at producing plausible science. Plausible is not verified. I wanted a tool judged by **verified claims per token**, not by how many agents it can spawn. The first six-agent run caught a bad answer key — mine. That is the product working.

Built by **lengrufeng2008** on DeepSeek Harness. The agent runs the campaigns; the human sets the token budget.

## What is in the bundle

| Skill | Role |
|---|---|
| `science-legion` | Router: frame the claim, load the domain skill, choose a tier |
| `legion-command` | Squad/platoon/company/legion doctrine, blackboard, worker contract, budgets |
| `math-research` | Definitions, proof obligations, counterexamples, symbolic and numerical checks |
| `physics-research` | Units, conservation, limits, approximation control, simulation, uncertainty |
| `astronomy-research` | Frames, time systems, photometry, distances, selection effects, archives |
| `engineering-research` | Requirements, load cases, units, safety factors, tolerances, failure modes, tests |
| `biomedical-research` | PICO, study design, absolute vs relative effects, bias, applicability; not medical advice |
| `science-verify` | Independent evidence table, reproduction, falsification, provenance |

## Wolf-pack and flanking tactics

The command skill names the shapes: **wolf pack** (independent packs with different methods),
**flanking** (reach the claim through a neighbouring field or limiting case), **pincer** (two
independent methods must agree), **feint** (bounded dead-end mapping), **ambush** (reserve a
counterexample pack), **siege** (rounds with a blackboard, not one huge fan-out), and **retreat**
(stop and report a negative result). A 1000-agent legion is 10+ companies under leads, never 1000
direct reports.

## Scale is a budget decision

Default is a **Squad (6)**: commander, two scouts, calculator, independent verifier, red team. The doctrine then allows **24**, **96**, and only after validation **384–1000**. A 1000-agent run is a compute campaign; estimate the token bill, write the cap in the brief, stop at 70%, and never use agent count as evidence.

The bundle does not spawn those agents itself. It tells the model how to use DSH's existing `workflow` and `subagent` tools; the profile's tools, model, and rate limits still apply. No 1000-agent run has been validated here — treat that tier as a guarded research mode, not a shipped fact.

## Install

Use the DSH plugin manager with this absolute directory (or the packed tarball). Once the public
repo exists, the GitHub form will be:

```bash
dsh plugin --profile web add github:lengrufeng2008/dsh-science-legion
```

Then ask for a hard science problem and invoke the `science-legion` skill (or the domain skill directly).
The router will pick the domain and `legion-command`.

## Use

```text
Use science-legion on: prove or refute ...
```

The commander writes a brief under `research/<slug>/`, starts with a squad, and reports claim, evidence, uncertainty, failures, and cost. Verification is a separate role; the author cannot mark their own result verified.

## Honest boundaries

- No claim of solving a math/physics/astronomy open problem. A proof, a certificate, a reproducible computation, or a decisive measurement is required.
- No fabricated citations, data, observations, or numbers. Unknown facts are marked `UNKNOWN`.
- No patient data or credentials in prompts.
- No majority vote as truth; no LLM-only judge; no silent retries.
- 1000 agents can be expensive and slow. The budget gate is part of the product.

## Roadmap

- **v0.2 (this bundle)** — eight skills, ten known-answer evals, two pilots.
- **v0.2** — validated 6- and 24-agent runs, a token cost ledger, artifact manifests, and a hard verifier gate.
- **v0.3** — a Host `legion` planner/dashboard and a 96-agent company run with a budget cap.
- **v1.0** — budgeted 384–1000-agent campaigns, proof/certificate/measurement requirements, and a public benchmark ledger. Open problems remain attempts until a proof or decisive measurement exists.

No tier is a promise of a breakthrough. The roadmap is about better evidence per token, not bigger numbers.

## Review

Standalone showcase: [`showcase.html`](showcase.html). See [`REVIEW.md`](REVIEW.md) for a 60-second code tour and the boundaries of what the pilot does and does not establish.

## Tests

```bash
npm test
```

Covers the manifest, frontmatter names, provider registration, lookup, and the mandatory doctrine markers.

## Pilot

Two pilots, both on known problems:

- **4 agents, second order** (`evals/pilot-pendulum/`): the formula was supported; the commander's
  pure-stdlib check was rerun and a separate AGM-only check reproduced the coefficient.
- **6 agents, fourth order** (`evals/pilot-fourth-order/`): the independent verifier caught an error
  in the shipped answer key. The old expected value `1.066315375` is the sixth-order truncation
  `T6`, not the fourth-order `T4 = 1.066080729...`; the key was corrected, while the formula
  survived.

Both used the command protocol prompts directly; automatic skill routing is tested by the provider
tests, not by the pilots. They are not evidence for 24/96/1000-agent runs or open problems.

The six-agent pilot's cost is now measured from local session logs: **¥1.4543 for 110 calls**
(5,790,848 cache-read, 155,611 uncached input, 295,723 output; six agent sessions only; main
session excluded). That is ¥1.45 per verified answer for this run, not a linear price for 1000
agents. The 1000-agent tier remains untested.

## Evals

`evals/problems.json` contains known-answer problems in math, physics, astronomy, engineering, and dimensional analysis. They are a benchmark, not a claim of open-problem capability. See `evals/README.md` for the protocol.

## License

MIT.
