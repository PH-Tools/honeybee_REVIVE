# Status — REVIVE SET post-processing

**Status:** In progress
**Current phase:** Phase 0 complete; Phase 1 next
**Branch:** `codex/revive-set-postprocessing`
**Last updated:** 2026-07-15

## Current evidence

- The SET calculation is CPython-only and belongs under `honeybee_revive/output/`.
- Track A (`People.carbon_dioxide_generation_rate`) is independent; upstream PR #1146 is open and green.
- The existing measure remains in place until computed-vs-EnergyPlus equivalence is demonstrated.
- Pre-phase baseline: `266 passed` under the existing Python 3.10 `.venv`; Phase 0 gate: `269 passed` after adding the three contract tests.
- The committed 48 KB SQLite fixture contains four hourly series, 216 records each; `PRAGMA integrity_check` returns `ok`.
- Three focused tests lock input alignment, hourly cadence, the 24 + 168 + 24 window, and the People-keyed reference SET series. Black and Ruff pass for the Phase 0 Python files.

## Next step

Begin Phase 1 with red tests for normative metabolic-rate conversion, direct `pierce_set` parity, alignment failures, and multi-zone isolation.

## Blockers

- None for Phases 0–4.
- Measure deletion remains blocked on Phius acceptance of post-processed SET.
