---
DATE: 2026-07-15
STATUS: CANONICAL PRD
---

# honeybee-REVIVE — Product Requirements

## 1. Goal

Let practitioners add [Phius-REVIVE 2024](https://www.phius.org/phius-revive-2024) resilience and lifecycle-carbon attributes to their Honeybee models, and run the ADORB carbon-cost calculation on them — the REVIVE analog to what `honeybee_ph` does for PHI/Phius certification.

## 2. Who uses it

- The **honeybee_grasshopper_REVIVE** toolchain, building models in Rhino/Grasshopper (IronPython 2.7).
- Python users of Honeybee (`pip install honeybee-REVIVE`) running resilience/carbon analysis.

## 3. What belongs here

- REVIVE attributes on Honeybee / Honeybee-Energy objects (`honeybee_revive`, `honeybee_energy_revive`), with HBJSON serialization.
- Reference standards data (`honeybee_revive_standards`: appliances, cambium factors, emissions, programs, schedules).
- EnergyPlus measures (`honeybee_revive_measures`) and Ladybug resiliency helpers (`ladybug_revive`).
- The resilience **reporting/output** layer (`honeybee_revive/output/`, pandas-based, CPython-only).

## 4. Non-goals

- **The ADORB cost math itself lives in `PH-ADORB`**, not here — honeybee-REVIVE prepares the model and calls into it.
- **No Grasshopper UI** — that is `honeybee_grasshopper_REVIVE`.
- **No pandas in the Rhino load path** — heavy analysis stays CPython-only. See `CODING_STANDARDS.md`.

## 5. Success criteria

- Model-extension code loads under IronPython 2.7 in Rhino (no accidental pandas import at load).
- REVIVE data round-trips losslessly through HBJSON, including old HBJSON.
- The ADORB / resilience analysis runs correctly in CPython and produces the expected outputs.

## 6. Direction

- The automated API-doc generator (`AUTODOC.md`) is proposed; `docs/nav.yml` already references the planned `api/` tree. Active work tracked in `planning/STATUS.md`.
