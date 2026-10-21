# Closeout evidence — REVIVE SET post-processing

## Automated gates

- Full pytest suite: `298 passed`.
- Focused SET suite: `32 passed`.
- `set_calculator.py`: 146/146 statements and 46/46 branches covered (100%).
- Repository-wide configured coverage gate: 75%, failing the existing `fail_under = 100` threshold with 760 uncovered statements in legacy modules. This feature does not broaden coverage exclusions or add unrelated tests to mask that baseline.

## Regenerated report

Source SQL:

`honeybee_REVIVE_grasshopper/sample_models/resilience/winter/unnamed/openstudio/run/eplusout.sql`

Generated artifact:

`/tmp/revive-set-report/winter_SET_temperature.html`

Regeneration command (from the repository root):

```sh
rm -rf /tmp/revive-set-report && mkdir -p /tmp/revive-set-report
.venv/bin/python -c 'from pathlib import Path; from honeybee_revive.output.resilience_winter_graphs import Filepaths, write_SET_temp_plots; write_SET_temp_plots(Filepaths(Path("../honeybee_REVIVE_grasshopper/sample_models/resilience/winter/unnamed/openstudio/run/eplusout.sql"), Path("/tmp/revive-set-report")))'
```

Checks:

- 216 full hourly records and 168 central-outage records.
- Zone: `ROOM_1_3B02CCA3`.
- Computed result: 971.710697125807 K·h / 1749.079254826453 °F·h; verdict fails.
- HTML contains `set_fig1`, `set_fig2`, and `set_fig3` with the SET, dry-bulb, and RH chart titles.
- Controlled-browser visual inspection could not open the local `file://` artifact. Manual visual acceptance remains required; no alternate browser bypass was used.

## Follow-up: the 216-hour contract required a run-period fix (2026-07-21)

`EXPECTED_RUN_HOURS = 24 + 168 + 24` was correct, but **no real project run satisfied it**.
The first live model it met (2613 Ayers) raised:

```
SetInputError: Winter SET calculation requires 216 hourly records
               for zone '00_CRAWLSPACE_BB9B1CF6'; received 240.
```

Root cause was upstream in `ladybug_revive.resiliency_epw.get_outage_period()`, not in this
feature. That function applies a `+1 hoy` correction to the STAT extreme week (reversing
Ladybug's 0-23 vs EPW 1-24 offset), and the expanded RunPeriod window was being built from
the *corrected* week. The corrected week ends at hour-0 of the following day, so the
expansion stayed 216 hours long but **touched 10 calendar dates**. `RunPeriod` is
date-based, so EnergyPlus simulated 10 full days = 240 hours.

Fixed in `f2f25cd` by building the expansion from the raw week instead, keeping it aligned
to day boundaries (9 dates / 216 hours). The `+1` correction is retained on the morphing
window, so morphed EPW hours are unchanged — the EPW golden-value tests pass untouched, and
existing morphed weather files remain valid.

Verified end-to-end on 2613 Ayers after re-running both seasons:

| | before | after |
|---|---|---|
| RunPeriod (winter) | `01/26 → 02/04`, 10 days | `01/26 → 02/03`, **9 days** |
| RunPeriod (summer) | 10 days | **9 days** |
| SET records per zone | 240 | **216** |
| `write_SET_temp_plots` | raised `SetInputError` | passes |

Guarded by `tests/test_ladybug_revive/test_outage_period_length.py` (9 tests). The expanded
period previously had **zero** coverage — every existing test discarded it
(`outage_period, _ = get_outage_period(...)`), which is why this survived. The new tests
assert the **calendar-day count** as well as the hour count; hour count alone passes in both
the broken and fixed cases.

Note for future readers: this feature's `PRD.md` already specified "The full nine-day run
provides 216 hourly values per zone". The contract was documented correctly all along — the
run-period implementation simply never matched it, and nothing checked.

## Release boundary

The feature branch can be reviewed now. Merge/release remains gated on manual visual acceptance of the regenerated HTML. After merge, the repository's normal `main` workflow performs the version bump and package publication. The existing OpenStudio measure remains in place; its deletion is outside this PR and remains gated on Phius acceptance.
