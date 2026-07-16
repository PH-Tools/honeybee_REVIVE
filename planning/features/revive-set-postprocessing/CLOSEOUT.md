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

## Release boundary

The feature branch can be reviewed now. Merge/release remains gated on manual visual acceptance of the regenerated HTML. After merge, the repository's normal `main` workflow performs the version bump and package publication. The existing OpenStudio measure remains in place; its deletion is outside this PR and remains gated on Phius acceptance.
