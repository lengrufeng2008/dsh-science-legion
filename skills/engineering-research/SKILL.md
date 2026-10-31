---
name: engineering-research
description: Attack an engineering design, analysis, or test claim with requirements, load cases, units, safety factors, tolerances, failure modes, and independent verification. Use for mechanical, civil, electrical, or systems calculations; not a substitute for a licensed engineer's signed approval.
whenToUse: "An engineering calculation, design claim, safety factor, tolerance, failure mode, simulation, or test plan."
---

# Engineering research

## Scope and red line

This skill checks engineering reasoning. It does **not** certify a design, sign off on a safety-critical
system, or replace a licensed engineer, a code review, or a physical test. Say so when the result
would be used for construction, operation, or human safety.

## Frame the design

- Function, requirements, and constraints.
- Load cases, boundary conditions, environment, and duty cycle.
- Materials and properties, including temperature and degradation.
- Units and sign conventions.
- Applicable standard or code, and the edition.
- Failure modes that matter: strength, stiffness, fatigue, creep, buckling, wear, corrosion, thermal, electrical, control, human factors.

## Method ladder

1. **Free body / system boundary.** Draw it. Check that every load and reaction is accounted for.
2. **Units and dimensions.** Convert to a consistent base; check every term.
3. **Closed-form estimate.** Hand calculation before simulation. State assumptions.
4. **Safety factor.** Distinguish yield vs ultimate vs allowable; state whether the factor is on load, stress, or both.
5. **Tolerance and stack-up.** Worst-case and statistical; check interfaces.
6. **Simulation.** Mesh/resolution convergence, boundary conditions, material model, verification against a hand case, validation against test if available.
7. **Failure modes.** FMEA-style: mode, cause, effect, detection, severity, mitigation.
8. **Test plan.** What would falsify the design; instrumentation, calibration, sample size, acceptance criteria.

## Verification

- Independent hand calculation; do not just rerun the same spreadsheet.
- Units on both sides and at every interface.
- Limiting cases: zero load, rigid body, symmetric case, extreme temperature.
- Sensitivity to uncertain material properties and loads.
- Check the factor of safety against the stated standard.
- For a simulation, a convergence study and at least one benchmark case.
- For a test, calibration, controls, and raw data retention.

## Common failure modes

- Unit mismatch (N vs kgf, mm vs m, gauge vs absolute pressure).
- Wrong boundary condition (fixed vs pinned, insulated vs convective).
- Yield strength used where ultimate or fatigue applies.
- A load case omitted (wind, seismic, thermal, accident, maintenance).
- Simulation without mesh convergence or validation.
- Tolerance stack-up ignored at interfaces.
- A "pass" from a model with no physical test for a safety-critical claim.

## Output

Return: requirement, load cases, assumptions, calculation, units, factor of safety, failure modes,
verification performed, test status, standard used, and unresolved risks. Mark a design as
`NOT CERTIFIED` unless a qualified human and the required test have signed off.
