---
DATE: 2026-07-15
STATUS: CANONICAL
---

# honeybee-REVIVE — Architecture

## Big picture

Like `honeybee_ph`, honeybee-REVIVE is a **Honeybee extension**: it attaches REVIVE data to Honeybee objects via the `properties` extension mechanism, serialized into HBJSON. It then feeds that model into the **PH-ADORB** library for the carbon-cost calculation.

```
Honeybee model ──.properties (revive)──► REVIVE objects ──to_dict()──► HBJSON
                                                │
                                                ▼
                                     PH-ADORB (ADORB cost calc, CPython)
                                                │
                                                ▼
                              honeybee_revive/output/ (resilience graphs, pandas)
```

## The five packages

| Package | What it holds |
|---------|---------------|
| `honeybee_revive` | Core model + `_extend_honeybee_revive.py`, `properties/`, `fuels.py`, `grid_region.py`, `national_emissions.py`, `CO2_measures.py`, `cli/`, and `output/` (resilience reporting — **pandas, CPython-only**) |
| `honeybee_energy_revive` | REVIVE attributes on Honeybee-Energy objects: `hvac/`, `properties/`, `_extend_honeybee_energy_revive.py` |
| `honeybee_revive_standards` | Reference JSON: `appliances/`, `cambium_factors/`, `CO2_measures/`, `national_emission_factors/`, `programtypes/`, `schedules/` |
| `honeybee_revive_measures` | EnergyPlus measures (`set_revive_people_eplus`) |
| `ladybug_revive` | `resiliency_epw.py`, `adjustment_factors.py` |

## The runtime boundary (the thing to get right)

- **IPy2.7-safe (loads in Rhino):** the `_extend`, `properties`, and model-object modules across the packages.
- **CPython-only:** `honeybee_revive/output/` (pandas) and dev scripts like `honeybee_revive_standards/cambium_factors/_generate_json_files.py`. These must not be imported from any module that Rhino loads.

Keep pandas/numpy imports out of package `__init__` and `_extend` paths.

## Serialization

Model objects implement `to_dict()`/`from_dict()` with backward-compatible deserialization — see `CODING_STANDARDS.md`.
