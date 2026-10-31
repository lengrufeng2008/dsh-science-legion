---
name: astronomy-research
description: Attack an astronomy or astrophysics claim with coordinate and time conventions, photometry and spectroscopy, distance and selection effects, archival data, and independent verification. Use for objects, surveys, spectra, distances, and cosmological claims.
whenToUse: "An object, coordinate, time, magnitude, distance, spectrum, survey, or astrophysical claim."
---

# Astronomy research

## Conventions first

- Coordinate frame (ICRS, FK5, galactic, ecliptic), epoch, and equinox.
- Time system (UTC, TAI, TT, TDB, JD, MJD, HJD) and barycentric correction.
- Photometric system (Vega vs AB, filter, zero point), extinction, and aperture.
- Cosmology (H0, Ωm, ΩΛ) when a distance or age is inferred.

A coordinate or magnitude without its frame and system is not a measurement.

## Method ladder

1. **Identify the object and the measurement.** Name, aliases, coordinates, and the actual observable.
2. **Check the data.** Provenance, calibration, resolution, signal-to-noise, and whether the claimed feature is above the noise.
3. **Use known relations.** Magnitude–flux, distance modulus, luminosity–mass, Kepler, spectroscopy, and scaling relations. State the assumptions.
4. **Selection and bias.** Malmquist bias, Eddington bias, survey limits, extinction, crowding, and foreground contamination.
5. **Independent archive check.** Re-derive from a second catalog or service where possible; cite the exact dataset and query.
6. **Uncertainty.** Statistical and systematic; include distance, extinction, and calibration terms.

## Verification

- Recompute the magnitude/flux conversion in both directions.
- Check the coordinate frame and epoch against an independent catalog.
- Verify the distance ladder and the cosmology used.
- Check that the claimed signal survives a different aperture, background model, or archive.
- For a period or orbit, check phase coverage and aliases.
- For a spectral line, check resolution, blend, and redshift convention.

## Common failure modes

- Magnitude sign errors and Vega/AB mixing.
- Comparing coordinates in different frames or epochs.
- Ignoring extinction or foreground stars.
- Distance modulus used with the wrong units.
- A period alias presented as a detection.
- Cosmology-dependent conclusions without stating the cosmology.
- Numerology: a coincidence in numbers without a physical mechanism or error analysis.

## Output

Return: object and coordinates, dataset and frame, measurement, method, result with uncertainty, independent check, and selection/systematic caveats. Real dataset identifiers only. Mark unverified claims as `UNCHECKED`.
