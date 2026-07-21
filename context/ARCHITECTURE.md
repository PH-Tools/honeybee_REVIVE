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

## The simulation period (9 days / 216 hours)

Phius REVIVE models a **7-day (168 hr) outage**. The simulation brackets it with a 1-day
warm-up and a 1-day cool-down, so a compliant run is **24 + 168 + 24 = 216 hours over
exactly 9 calendar days**. `set_calculator.EXPECTED_RUN_HOURS` enforces this and will refuse
a run of any other length.

`ladybug_revive.resiliency_epw.get_outage_period()` returns **two different periods**, and
the distinction matters:

| Period | Length | Drives | Offset |
|---|---|---|---|
| corrected week | 168 hr | the EPW **morphing** — which hours get the 10/20-yr extremes | `+1 hoy` applied |
| expanded week | 216 hr / 9 dates | the EnergyPlus **RunPeriod** | built from the RAW week |

The `+1` hour correction reverses Ladybug's 0-23 vs EPW 1-24 indexing offset
([discourse](https://discourse.ladybug.tools/t/why-does-analaysis-period-have-a-1-hour-offset/35017))
and is applied **only** to the morphing window.

**Why the expanded window is built from the raw week:** the corrected week ends at hour-0 of
the *following* day (Feb-2 23:00 → Feb-3 00:00). Expanding from it still yields 216 hours,
but the period then *touches 10 calendar dates*. `RunPeriod` is **date**-based, not
hour-based, so EnergyPlus simulates 10 full days (240 hr) and the SET post-processing fails
its 216-record check. Building the expansion from the raw week keeps it aligned to day
boundaries: 9 dates, 216 hours.

Guarded by `tests/test_ladybug_revive/test_outage_period_length.py`, which asserts the
**calendar-day count** as well as the hour count — hour count alone passes in both cases.

## Chart legends vs data keys

EnergyPlus names each Zone after the Honeybee Room's `identifier` (`03_NORTH_0ac0d721`),
never its `display_name` — correct at the honeybee-energy layer, since identifiers are
unique and E+-safe while display names are neither.

`output/_shared.py` maps back to display names for **chart legends only**, via
`load_zone_labels()` / `zone_label()`, reading the HBJSON that sits beside the SQL file. It
resolves all three E+ key shapes: zone (`..._0AC0D721`), enclosure (`..._SPACE`), and
People/SET (`..._SPACE RV2024_RESILIENCE_PEOPLE`).

**`Record.Zone` is deliberately left as the raw E+ key** — it flows into the CSV/JSON
exports consumed by the Grasshopper wrapper and the web report, so it stays the stable
machine identifier. Unrecognized keys (`Environment`, Surface/Aperture names in the envelope
-details charts) fall through unchanged, which is intended: those charts identify individual
faces, and collapsing them to room names would lose information.

## Serialization

Model objects implement `to_dict()`/`from_dict()` with backward-compatible deserialization — see `CODING_STANDARDS.md`.
