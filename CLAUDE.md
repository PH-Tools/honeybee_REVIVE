# honeybee-REVIVE

A Honeybee/Ladybug-Tools extension that adds [Phius-REVIVE 2024](https://www.phius.org/phius-revive-2024) resilience and lifecycle-carbon attributes to models, and drives the ADORB carbon-cost calculation (via the `PH-ADORB` library). Published on PyPI as `honeybee-REVIVE`. Source: https://github.com/PH-Tools/honeybee_REVIVE

> Not affiliated with, reviewed, or approved by Phius.

> **Runtime nuance (important):** the model-extension code must run under **IronPython 2.7** (loaded into Rhino/Grasshopper via `honeybee_grasshopper_REVIVE`) — source files carry a `# -*- Python Version: 2.7 -*-` header. But the **`honeybee_revive/output/` reporting subpackage uses `pandas` and is CPython-only** — it must never be imported into the IPy2.7 load path. See `context/CODING_STANDARDS.md`.

## What this repo is

Five sub-packages:

| Package | Role | Runtime |
|---------|------|---------|
| `honeybee_revive` | Core REVIVE model on Honeybee objects (`_extend`, `properties`, fuels, grid_region, national_emissions, CO2_measures) | IPy2.7 — **except `output/`** (pandas, CPython-only) |
| `honeybee_energy_revive` | REVIVE attributes on Honeybee-Energy objects (constructions, HVAC) | IPy2.7 |
| `honeybee_revive_standards` | Reference JSON datasets (appliances, cambium factors, emissions, programs, schedules) | data |
| `honeybee_revive_measures` | EnergyPlus measures (`set_revive_people_eplus`) | CPython (E+ context) |
| `ladybug_revive` | Resiliency EPW + adjustment factors | IPy2.7 |

## Where things live — read before working

| Working on… | Read |
|-------------|------|
| Scope, what belongs here | `context/PRD.md` |
| Package map, `_extend`/`properties`, ADORB flow | `context/ARCHITECTURE.md` |
| IPy2.7 vs CPython split, serialization, testing | `context/CODING_STANDARDS.md` |
| Deps, packaging, CI, release | `context/TECH_STACK.md` |
| The automated API-doc generator spec | `context/AUTODOC.md` |
| Current / in-flight work | `planning/STATUS.md` |
| The public docs site (autodoc spoke — do not restructure) | `docs/.instructions.md` |

Full context index: `context/README.md`.

## Hard rules

1. **Keep the IPy2.7 / CPython boundary clean.** Model-extension code is IPy2.7-safe (no f-strings/pathlib; comment-style hints; guarded `typing`; 2.7 header). `pandas`/`numpy` may only be used in CPython-only code (`honeybee_revive/output/`, dev scripts) — never in a module reachable from a package `__init__` / `_extend` import in Rhino.
2. **Backward-compatible serialization.** New fields: default in `__init__`, written in `to_dict()`, read via `_input_dict.get("key", default)` in `from_dict()`, copied in `duplicate()`.
3. **Attach data via the `_extend`/`properties` mechanism**, not around it.
4. **Docs are an autodoc spoke.** New/renamed public API → update `docs/nav.yml` + docstrings in the `ph-docs` format (`docs/.instructions.md`). Never restructure `docs/`. (Note `nav.yml` references a planned `api/` tree — see `context/AUTODOC.md`.)
5. **Verify before closeout:** `python -m pytest`.

## Ecosystem

Model built here → ADORB cost calc via **PH-ADORB** → surfaced in Grasshopper by **honeybee_grasshopper_REVIVE**. Sibling of `honeybee_ph` (same Honeybee-extension pattern). Depends on `ph-units`.
