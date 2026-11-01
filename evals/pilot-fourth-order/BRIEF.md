# BRIEF — pendulum fourth-order period

Claim under test (verbatim from the source tuple, `products/dsh-science-legion/evals/problems.json`,
entry `physics-pendulum-fourth-order`):

> T/T0 = 1 + theta0^2/16 + 11 theta0^4/3072 + O(theta0^6); exact = 4 K(sin(theta0/2))/(2 pi);
> at theta0=1, exact ratio = 1.06633424558, fourth-order = 1.066315375, error = -1.771e-5.

- Domain: classical mechanics. Ideal planar simple pendulum: point mass on a massless rigid
  rod of length L, uniform gravity g, released from rest at zero-to-peak angular amplitude
  θ0 (radians), 0 < θ0 < π. No damping, driving, rod inertia, or finite-size corrections.
- Reference period: T0 = 2π√(L/g); the claim is about the dimensionless ratio T/T0.
- Known facts used: energy integral gives the exact quarter period
  T = 4√(L/g) K(sin(θ0/2)); K has the positive series
  K(k) = (π/2) Σ c_n² k^(2n), c_n = C(2n,n)/4^n; and
  T/T0 = (2/π)K(k) = 1/AGM(1, cos(θ0/2)).
- Success test: exact rational equality for the θ0⁴ coefficient; at least two independent
  evaluations of T/T0 at 1 rad agreeing to better than 1e-20; every number in the source tuple
  either reproduced or explicitly classified as wrong; a one-sentence verdict on the formula
  and on the numeric answer key.
- Non-goals / forbidden shortcuts: no apparatus measurement (none exists and none may be
  invented); no fitting the formula to itself; no treating θ0 as degrees or as peak-to-peak;
  no accepting the source's numeric tuple on authority; no citations without a real source
  (none were needed or used).
- Budget: six workflow agents (scout, theorist, calculator, independent verifier, red team,
  commander); the workflow orchestrator owns the fan-out, and each agent sees depth 0. Token/time
  cost was not fully instrumented; see `COST.json` (`costCny: null`, `source: "unmeasured"`).
- Roles and artifacts:
  - **Scout / theorist** — `SCOUT.md` + `scout_check.py`: energy integral, K-series
    composition, exact coefficient extraction, limits, pitfalls.
  - **Calculator** — `check.py` + `run.txt`: independent 90-digit AGM evaluation of the
    exact period and the truncation at 1 rad.
  - **Independent verifier** — `VERIFY.py` + `VERIFY_run.txt`: claim-only input, own
    110-digit Decimal code, exact rational series, tanh-sinh quadrature, AGM/K cross-check.
  - **Red team** — no standalone artifact was present; the commander performed this lane in
    `COMMANDER_check.py` (source-tuple audit, error-sign audit, unit/amplitude conventions,
    wrong-modulus shortcut, large-angle breakdown).
  - **Commander** — `COMMANDER_check.py` + `COMMANDER_run.txt`: independent
    Lindstedt–Poincaré derivation (with amplitude reversion), 120-digit AGM, independent
    Simpson quadrature, synthesis and verdict.
- Who verifies: the independent verifier did not read the author's derivation and wrote its
  own code; the commander then reran every script (all exit 0) and added a different analytic
  route. No role's number was accepted without a rerun.
- Falsifier: an exact evaluation of the ideal-pendulum period whose θ0⁴ coefficient is not
  +11/3072 (relative to T0) under the stated conventions, or a demonstrated error in the
  K-series/AGM identity. For the numeric part: any exact computation showing T4 ≠ 3275/3072,
  or exact − T4 ≠ 2.535164…e-4, falsifies the source's quoted numbers. A real-pendulum
  measurement outside the ideal model's error budget would falsify applicability, not the
  ideal-model mathematics.
- Stop rule: the success test is met; report the formula as supported and the source numeric
  tuple as falsified, rather than forcing agreement with the answer key.
