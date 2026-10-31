---
name: biomedical-research
description: Appraise biomedical evidence with PICO, study design, effect measures, bias, applicability, and reproducibility. Use for evidence review and critical appraisal; this is not medical advice, diagnosis, or treatment, and it must not handle patient-identifiable data.
whenToUse: "A biomedical study, trial, observational association, diagnostic claim, or evidence review that needs critical appraisal rather than a treatment recommendation."
---

# Biomedical evidence research

## Scope and red line

This skill appraises evidence. It is **not** medical advice, diagnosis, or treatment. Do not ask for
or process patient-identifiable data. A conclusion about a person belongs to a qualified clinician.
No claim of efficacy from an abstract alone; no fabricated citations; no causal language from an
observational association without a design that supports it.

## Frame the question

Use PICO:

- **P**opulation and setting.
- **I**ntervention or exposure.
- **C**omparator.
- **O**utcome, including whether it is patient-important, a surrogate, or a composite.
- Time horizon and follow-up.

State the study design: systematic review/meta-analysis, randomized trial, cohort, case-control,
cross-sectional, case series, case report, in vitro, animal, or modeling. Design is not a badge;
check how it was executed.

## Appraisal ladder

1. **Source and status.** Real PMID/DOI, full text vs abstract, preprint vs peer-reviewed, retraction/correction, registration.
2. **Population and selection.** Who was included, who was excluded, how recruited, baseline risk.
3. **Intervention/exposure.** Dose, duration, adherence, co-interventions, contamination.
4. **Comparator.** Placebo, usual care, active; blinding.
5. **Outcomes.** Pre-specified vs post hoc, composite components, surrogate vs clinical, harms.
6. **Effect measures.** Relative vs absolute; risk difference, NNT/NNH, hazard/odds ratios; confidence intervals, not just p-values.
7. **Bias.** Randomization, allocation concealment, blinding, attrition, selective reporting, confounding, immortal time, healthy-user, detection, publication.
8. **Analysis.** Intention-to-treat vs per-protocol, missing data, multiplicity, subgroup fishing, model assumptions.
9. **Applicability.** External validity, setting, comorbidity, adherence, resource requirements.
10. **Synthesis.** Certainty (GRADE-like), consistency, directness, precision, publication bias.

## Verification

- Confirm the identifier resolves and the full text supports the exact claim.
- Re-extract the effect and confidence interval from the table, not the abstract alone.
- Check the denominator and the follow-up time.
- Compare absolute and relative effects; compute NNT/NNH only with a stated baseline risk and horizon.
- Check trial registration and protocol for outcome switching.
- Look for conflicts of interest and funding, but do not treat them as proof of bias.
- For a meta-analysis, check heterogeneity, model, and whether studies were double-counted.

## Common failure modes

- "20% reduction" without the absolute risk or baseline.
- Surrogate endpoint presented as patient benefit.
- Composite endpoint driven by one component.
- Subgroup result presented as the main finding.
- Observational association stated as causation.
- Abstract-only claim; preprint treated as settled.
- P-hacking, multiplicity, or selective outcome reporting.
- NNT calculated without a horizon or baseline.

## Output

Return: PICO, design, population, effect with CI, absolute risk and NNT/NNH if justified, bias
assessment, applicability, certainty, real sources, and what would change the conclusion. Add
`NOT MEDICAL ADVICE` and `NO PATIENT DATA` when relevant.
