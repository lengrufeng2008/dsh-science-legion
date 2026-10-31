# Science Legion evals

Known-answer problems, not open problems. The point is to measure whether the campaign is **correct and reproducible**, not whether it is impressive.

## Protocol

1. Use a fresh workspace and a token cap.
2. Hide `expected` and `verify` from the workers and the verifier.
3. Start at Squad (6). Record the tier, model, token cost, wall time, and every failed check.
4. The verifier independently derives or computes the answer.
5. Compare with `expected`; mark `supported`, `falsified`, or `unresolved`.
6. Do not tune a skill on the same problem and then report it as held-out. Split problems into dev and test.

## Scoring

- `correct + independently verified` = pass.
- `correct + author-only` = draft; not a pass.
- `wrong + honest` = fail, but a useful failure.
- `cannot run` = unresolved, never pass.

A run at 1000 agents that produces one verified answer is not better than a 6-agent run that produces the same evidence; report cost alongside correctness.
