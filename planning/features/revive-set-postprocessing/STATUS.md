# Status — REVIVE SET post-processing

**Status:** In progress
**Current phase:** Phase 2 complete; Phase 3 next
**Branch:** `codex/revive-set-postprocessing`
**Last updated:** 2026-07-15

## Current evidence

- The SET calculation is CPython-only and belongs under `honeybee_revive/output/`.
- Track A (`People.carbon_dioxide_generation_rate`) is independent; upstream PR #1146 is open and green.
- The existing measure remains in place until computed-vs-EnergyPlus equivalence is demonstrated.
- Pre-phase baseline: `266 passed` under the existing Python 3.10 `.venv`; Phase 0 gate: `269 passed` after adding the three contract tests.
- The committed 48 KB SQLite fixture contains four hourly series, 216 records each; `PRAGMA integrity_check` returns `ok`.
- Three focused tests lock input alignment, hourly cadence, the 24 + 168 + 24 window, and the People-keyed reference SET series. Black and Ruff pass for the Phase 0 Python files.
- Phase 1 adds one typed Record/DataFrame calculation path with the normative 120 W/person, 0.16 m/s, 1.0 clo, and zero-work inputs. Eleven focused tests cover direct `pierce_set` parity, actionable alignment errors, timezone consistency, DataFrame normalization, and order-independent multi-zone joins.
- `ladybug-comfort>=0.19.0` is now a direct runtime dependency; the lock refresh also reconciles previously stale root-package metadata and runtime resolutions.
- Phase 2 exposes the full 216-hour SET series, central 168-hour outage, per-hour deficits, and per-zone K·h / °F·h totals and verdicts. Seven focused tests cover edge-buffer exclusion, exact unit math, the inclusive 120 K·h limit, finite-value validation, and incorrect count/cadence failures.

## Next step

Run the Phase 3 computed-vs-EnergyPlus equivalence gate on the committed fixture and document all 216-hour deltas plus central-168 totals/verdicts.

## Blockers

- None for Phases 0–4.
- Measure deletion remains blocked on Phius acceptance of post-processed SET.
