# Winter SET data contract

## Measure-era two-consumer pipeline

Before this implementation, the workflow had two independent consumers of the same EnergyPlus Pierce SET variable:

1. `honeybee_revive/output/resilience_winter_graphs.py::write_SET_temp_plots()` reads `Zone Thermal Comfort Pierce Model Standard Effective Temperature`, rewrites the People-keyed result name with `rename_set_temps()`, and plots it in the winter HTML report.
2. `honeybee_REVIVE_grasshopper/.../generate_winter_output.py::GHCompo_ResiliencyWinterOutput.run()` separately invokes `resilience_hourly_data.py` for that same variable, reads the resulting `Date` / `Value` / `Zone` JSON, and builds the two existing IronPython Grasshopper degree-hour DataTrees.

The core package now exposes one CPython loader/calculator pipeline through `read_winter_set_inputs_from_sql()` and `calculate_winter_set()`, with `calculate_winter_set_from_sql()` as the direct composition. The winter graph reuses the loaded inputs and plots the full 216-hour result; `resilience_set_data.py` writes the central 168-hour result with the existing JSON shape. The Grasshopper wrapper remains a JSON consumer and will switch to this entry point after the core release; it does not import pandas or `ladybug-comfort` into Rhino.

## Repository-owned SQL fixture

`tests/_fixtures/winter_set_contract.sql` is a trimmed copy of the four relevant hourly series from:

`honeybee_REVIVE_grasshopper/sample_models/resilience/winter/unnamed/openstudio/run/eplusout.sql`

Regenerate it from a local checkout with:

```console
.venv/bin/python tests/_fixtures/generate_winter_set_fixture.py \
  /path/to/honeybee_REVIVE_grasshopper/sample_models/resilience/winter/unnamed/openstudio/run/eplusout.sql \
  tests/_fixtures/winter_set_contract.sql
```

Tests use only the committed fixture; they never reach into the sibling Grasshopper repository.

Fixture SHA-256: `79b22f559d680fe33cb2de546f354a19c171d6921a97fc91e027040fd576421b`.

## Locked real-model facts

- Input variables: Zone Mean Air Temperature, Zone Mean Radiant Temperature, and Zone Air Relative Humidity.
- Every input is reported `Hourly` for the same zone and the same 216 `(zone, timestamp)` keys.
- The nine-day run spans 2021-01-26 00:00 through 2021-02-03 23:00 in the reporting helper's assigned year.
- The compliance slice is `records[24:-24]`: 168 hours from 2021-01-27 00:00 through 2021-02-02 23:00.
- The reference EnergyPlus Pierce SET series also has 216 hourly values. Its key is People-based (`<zone>_SPACE <people-object>`) rather than zone-based.
  - The former graph-only `rename_set_temps()` workaround has been **removed**. People-based keys are now resolved by the general legend mapper, `output/_shared.zone_label()`, which handles all three E+ key shapes (zone, `_SPACE` enclosure, and People). See `context/ARCHITECTURE.md` → "Chart legends vs data keys".
- The nine-day / 216-hour run is **not** automatic — it depends on `ladybug_revive.resiliency_epw.get_outage_period()` returning a day-aligned expanded period. See the note in `CLOSEOUT.md`.
