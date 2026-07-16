# Plan — REVIVE SET post-processing

## Phase 0 — Baseline and data contract

- Run `python -m pytest` in the existing `.venv` and record the result.
- Document the current graph and Grasshopper JSON consumers.
- Inspect a real winter SQL file and commit a repository-owned fixture or deterministic trimmed fixture.
- Test hourly reporting, identical `(zone, timestamp)` keys for air temperature / MRT / RH, 216 hours per zone, and a central 168-hour compliance window with 24-hour edge buffers.

## Phase 1 — Pure SET calculation

- Add aligned-input validation and `ladybug_comfort.pmv.pierce_set` calculation under `honeybee_revive/output/`.
- Test normative inputs, alignment failures, and multi-zone isolation.

## Phase 2 — Outage metrics

- Expose full SET records, central-168 records, hourly deficits, per-zone K·h / °F·h totals, and verdicts against 120 K·h.
- Preserve the current 36 °F output semantics pending clarification.

## Phase 3 — EnergyPlus equivalence gate

- Compare all 216 common hours and document median / 95th / maximum absolute SET delta.
- Compare central-168 degree-hour totals and per-zone verdicts.

## Phase 4 — Shared graph and JSON path

- Add the computed-SET JSON entry point and update winter graphs to use the same calculator.
- Declare `ladybug-comfort` directly and remove the measure-era zone rename from the computed path.

## Phase 5 — Closeout

- Run the 100% coverage gate and visually compare a regenerated winter report.
- Release the core package without deleting the existing measure.
