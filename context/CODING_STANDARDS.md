---
DATE: 2026-07-15
STATUS: CANONICAL ENGINEERING STANDARD
---

# honeybee-REVIVE — Coding Standards

## 1. The IronPython 2.7 / CPython boundary (the thing to get right)

This repo is mixed. Two zones:

- **IPy2.7-safe zone** — the model-extension code (`_extend_*`, `properties/`, model objects like `fuels.py`, `grid_region.py`, `CO2_measures.py`, and `honeybee_energy_revive/`, `ladybug_revive/`). This loads into Rhino. It must be Python-2.7 safe:
  - No f-strings/`pathlib`/modern stdlib; comment-style type hints; guard `typing` imports; keep the `# -*- Python Version: 2.7 -*-` header.
  - **No `pandas`/`numpy`.**
- **CPython-only zone** — `honeybee_revive/output/` (resilience graphs, pandas) and dev scripts (e.g. `honeybee_revive_standards/cambium_factors/_generate_json_files.py`). Modern Python is fine here.

**Hard boundary:** nothing in the CPython-only zone may be imported from a module Rhino loads (package `__init__`, `_extend`, or any model object). Keep `pandas`/`numpy` imports local to the CPython-only modules.

## 2. Backward-compatible serialization

Model objects round-trip through HBJSON. New field → default in `__init__`, written in `to_dict()`, read via `_input_dict.get("key", default)` in `from_dict()`, copied in `duplicate()`. Old HBJSON must still load.

## 3. Use the `_extend`/`properties` mechanism

Attach REVIVE data through Honeybee's `properties` extension API; the `properties/` classes own the serialization. Don't bypass it.

## 4. Formatting

- **Black** + **ruff**, line length 120.

## 5. Testing

- **pytest** — `python -m pytest`. Tests mirror the packages; keep coverage up.

## Closeout checklist

- [ ] Model-extension changes are IPy2.7-safe (no f-strings/pathlib; guarded `typing`; comment hints; 2.7 header; **no pandas/numpy**).
- [ ] Any pandas/analysis code stays in the CPython-only zone and is not imported into the Rhino load path.
- [ ] New fields follow the backward-compatible serialization pattern.
- [ ] `python -m pytest` passes.
- [ ] `docs/nav.yml` + docstrings updated for new/renamed public API.
