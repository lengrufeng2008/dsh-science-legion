---
name: physics-research
description: Attack a physics or engineering claim with dimensional analysis, conservation laws, limiting cases, approximation control, simulation, uncertainty, and independent verification. Use for models, derivations, estimates, simulations, and measurements.
whenToUse: "A physical model, units and dimensions, conservation law, approximation, simulation, measurement, or engineering estimate."
---

# Physics and engineering research

## Frame the model

- System, degrees of freedom, and regime (classical, quantum, relativistic, continuum, statistical).
- Coordinates, sign conventions, and units.
- What is measured, what is inferred, and what is assumed.
- The dimensionless groups that control the regime.

If a quantity has units, write them. A formula that is dimensionally wrong is wrong before any numerical check.

## Method ladder

1. **Dimensional analysis.** Reduce to dimensionless groups; check every term.
2. **Conservation and symmetry.** Energy, momentum, angular momentum, charge, entropy, gauge symmetry, scaling.
3. **Limiting cases.** Known regimes (small amplitude, low velocity, weak field, long wavelength, thermodynamic limit) must reduce to the established result.
4. **Approximation control.** State the small parameter and the first neglected term; estimate its size.
5. **Analytic solution.** Solve the simplified model; keep track of branch choices and boundary conditions.
6. **Numerical simulation.** State the discretization, resolution, boundary conditions, convergence test, and conservation drift. A pretty plot is not convergence.
7. **Data and uncertainty.** Calibration, statistical and systematic errors, correlations, background, and selection effects.

## Verification

- Dimensions and units on both sides.
- Known limits and special cases.
- Conservation laws before and after the calculation.
- Convergence under resolution or precision; at least two methods where feasible.
- Sensitivity to the neglected term; report the error budget.
- For an experiment, a null test, a control, and a blinded check where possible.

## Common failure modes

- Unit mismatch hidden by a numerical coincidence.
- Double counting an effect; using the same data to fit and validate.
- False precision; quoting more digits than the uncertainty supports.
- Ignoring selection bias, background, or systematics.
- A simulation that is stable but not convergent.
- Treating a model's fit as a mechanism.

## Output

Return: model and regime, assumptions, equations, dimensionless groups, result with units, uncertainty, checks, and the dominant error source. Mark untested assumptions as `UNCHECKED`.
