---
DATE: 2026-07-15
STATUS: CANONICAL ENGINEERING STANDARD
---

# honeybee-REVIVE — Coding Standards

## 1. The IronPython 2.7 / CPython boundary (the thing to get right)

The generic dual-runtime rules (banned syntax and modules, comment-style type
hints, guarded `typing` imports, defensive third-party imports, and the lint
settings they imply) live in the **ironpython-27-compatibility** skill. Apply it
before editing anything on the Rhino load path. Only this repo's specifics are
recorded below.

This repo is mixed, and the boundary is the thing to get right.

- **IPy2.7 zone** (loads into Rhino): the model-extension code (`_extend_*`,
  `properties/`, model objects like `fuels.py`, `grid_region.py`,
  `CO2_measures.py`) plus `honeybee_energy_revive/` and `ladybug_revive/`.
  Keep the `# -*- Python Version: 2.7 -*-` header here.
- **CPython-only zone:** `honeybee_revive/output/` (resilience graphs, pandas)
  and dev scripts such as
  `honeybee_revive_standards/cambium_factors/_generate_json_files.py`.

**Hard boundary:** nothing in the CPython-only zone may be imported from a
module Rhino loads (package `__init__`, `_extend`, or any model object). Keep
`pandas`/`numpy` imports local to the CPython-only modules.

## 2. Backward-compatible serialization

The HBJSON round-trip contract (four steps for a new field, when `.get()` is
required, mutable constructor ownership, `duplicate()` recursion) and the
`_extend`/`properties` attachment mechanism live in the
**hbjson-serialization-contract** skill. Apply it before adding or changing any
field on a model class.

REVIVE model objects round-trip through HBJSON. These objects sit in the IPy2.7 zone, so the
**ironpython-27-compatibility** skill governs their serialization methods too.

## 3. Use the `_extend`/`properties` mechanism


REVIVE data attaches through Honeybee's `properties` extension API; the
`properties/` classes own the serialization.

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
