# Status — REVIVE SET post-processing

**Status:** Implemented
**Current phase:** Phase 5 implementation checks complete; review/release pending
**Branch:** `codex/revive-set-postprocessing`
**Pull request:** [PH-Tools/honeybee_REVIVE #5](https://github.com/PH-Tools/honeybee_REVIVE/pull/5)
**Last updated:** 2026-07-16

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
- Phase 3 equivalence gate passed on all 216 hours: median / 95th / maximum absolute ΔSET = 0.082138 / 0.121371 / 0.134251 K. Central-168 totals are 971.710697 K·h computed vs 957.789744 K·h EnergyPlus (1.453% difference); both verdicts fail. See `SET_COMPARISON.md`.
- Phase 4 adds `resilience_set_data.py` for the existing `Date` / `Value` / `Zone` JSON shape (central 168 only) and switches the winter SET graph to the same SQL-to-calculator function. Consumer tests pass after deleting the EnergyPlus Pierce output from the fixture; computed records use the actual zone key, writes are atomic, and the rename hack is gone. The full Phase 4 suite is `293 passed`.
- Phase 5 automated checks finish at `298 passed` and exercise every statement and branch in `set_calculator.py`: `146` statements and `46` branches at 100%. The repository-wide configured gate still reports the pre-existing package baseline at 75% (`760` uncovered statements across legacy modules), so it cannot truthfully pass from this feature alone. Visual acceptance and release remain pending.
- A fresh report generated from `honeybee_REVIVE_grasshopper/sample_models/resilience/winter/unnamed/openstudio/run/eplusout.sql` contains 216 full / 168 outage records, the three expected Plotly figures, and the same 971.710697 K·h failed verdict. Browser visual inspection remains manual because the controlled browser rejects local `file://` documents; no alternate browser bypass was used.
- PR #5 CI passes its Python 3.10 `Tests` job; the publish job correctly skips on the feature branch.

## Next step

Review PR #5. Before merge, manually open the regenerated winter HTML. Merge then triggers the normal release workflow; record the released version afterward. Do not delete the existing measure.

## Blockers

- Repository-wide 100% coverage is a pre-existing project baseline issue, not a SET regression; the new SET calculator itself is at 100% statement/branch coverage.
- Final visual acceptance requires a person to open the regenerated local HTML.
- Package release is gated on PR review/merge to `main`.
- Measure deletion remains blocked on Phius acceptance of post-processed SET.
