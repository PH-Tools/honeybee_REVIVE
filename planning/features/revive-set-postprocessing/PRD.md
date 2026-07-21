# PRD — REVIVE winter SET post-processing

## Problem

The winter resiliency workflow currently injects an EnergyPlus measure that rewrites `People` objects so EnergyPlus emits Pierce Standard Effective Temperature (SET). The HTML graph and Grasshopper outputs then read that variable through separate consumers. This duplicates the output path and ties the workflow to a fragile positional IDF measure.

## Goal

Compute winter SET from hourly zone air temperature, mean radiant temperature, and relative humidity with `ladybug-comfort`, then use one calculation path for both HTML graphs and the existing `Date` / `Value` / `Zone` JSON contract.

## Normative inputs

- clothing: 1.0 clo
- activity: 120 W/person
- air speed: 0.16 m/s
- external work: 0
- metabolic rate: `120 / (1.8258 * 58.2)` met

## Acceptance criteria

- Input series align one-to-one by zone and hourly timestamp; missing, duplicate, extra, or non-hourly data raises an actionable error.
- The full nine-day run provides 216 hourly values per zone; compliance uses only the central 168 hours, excluding 24-hour buffers at both ends.
- Computed SET and EnergyPlus Pierce SET have identical per-zone compliance verdicts; median absolute hourly delta is at most 0.5 K.
- HTML and Grasshopper JSON consumers use the same SET calculation.
- `ladybug-comfort` is a direct runtime dependency.
- No module in the Rhino / IronPython 2.7 import path imports the CPython-only output package.

## Out of scope

- Summer comfort criteria.
- Changes to the unresolved 36 °F output interpretation.
- Removing the existing measure before the equivalence gate and Phius-acceptance decision.
- Grasshopper cutover and compiled-component changes; those follow the core release.
