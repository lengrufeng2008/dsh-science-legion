---
name: math-research
description: Attack a mathematical claim with definitions, known results, proof obligations, counterexample search, symbolic and numerical checks, and independent verification. Use for proofs, derivations, inequalities, combinatorics, algebra, analysis, and conjectures.
whenToUse: "A theorem, proof, counterexample, inequality, combinatorial claim, or a request to solve a mathematical problem."
---

# Mathematical research

## Classify before proving

State the problem in one of these forms:

- **Prove** a universally quantified statement.
- **Disprove** it with a counterexample.
- **Compute** an exact value or closed form.
- **Approximate** with a stated error bound.
- **Find all** solutions, with a completeness argument.

Write the quantifiers and domains explicitly. A proof of the converse is not a proof. A numerical pattern is not a theorem.

## Method ladder

1. **Definitions and small cases.** Expand the definition; test n = 0, 1, 2 and the boundary of the domain.
2. **Known results.** Search for the theorem, lemma, or standard counterexample. Cite a real source; do not invent one.
3. **Structural proof.** Induction, contradiction, extremal principle, invariants, bijection, generating functions, linear algebra, compactness — pick the structure that matches the claim.
4. **Counterexample search.** Random and targeted search for small counterexamples; if one exists, stop and verify it exactly.
5. **Symbolic check.** Use a computer algebra system for algebra, series, limits, and exact identities. Simplify by hand enough to detect a wrong branch cut or domain assumption.
6. **Numerical check.** Use high precision and at least two methods; test edge cases and scaling. A float equality is not a proof.
7. **Formal check (optional).** If Lean/Coq/Isabelle is available, state the theorem and close the proof; otherwise say formal verification was not performed.

## Proof obligations

- Every division has a nonzero denominator; every square root has a domain; every limit has a topology.
- Every interchange of limits, sums, or integrals has a justification.
- Every "without loss of generality" has a symmetry argument.
- Every induction has a base case and a strong enough hypothesis.
- Every exhaustive case split is actually exhaustive.

## Verification

- Re-derive the key step independently; do not reread the draft.
- Check the result at the boundary, at a random point, and in a degenerate case.
- For a formula, compare a symbolic simplification and a high-precision numeric value.
- For a counterexample, verify the equation exactly, not approximately.
- For a literature claim, confirm the source exists and says what is claimed.

## Common failure modes

- Assuming the converse; swapping quantifiers; ignoring exceptional cases.
- Numerical instability near a singularity; convergence mistaken for a limit.
- A CAS simplification that is only valid on a branch or away from a pole.
- "It holds for the first ten cases" presented as a proof.
- Claiming an open problem is solved because a heuristic or a numerical search agreed.

## Output

Return: claim, domain and quantifiers, method, proof or counterexample, checks actually run, uncertainty, and the strongest unresolved gap. Mark anything not checked as `UNCHECKED`.
