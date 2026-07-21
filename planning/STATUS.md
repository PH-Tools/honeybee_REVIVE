# Planning Status

Master index of tracked planning work in honeybee-REVIVE.

_Last updated: 2026-07-21_

## Active / current work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| REVIVE SET post-processing | Feature | Implemented | [`features/revive-set-postprocessing/`](features/revive-set-postprocessing/) |
| Outage RunPeriod day-alignment (9 days / 216 hrs) | Fix | **Complete** — folded into `context/ARCHITECTURE.md` | [`features/revive-set-postprocessing/CLOSEOUT.md`](features/revive-set-postprocessing/CLOSEOUT.md) → commit `f2f25cd` |
| Chart legends use HB-Room display-names | Fix | **Complete** — folded into `context/ARCHITECTURE.md` | commit `f2f25cd` |

### Notes on the two 2026-07-21 fixes

Both shipped together in `f2f25cd` and are covered in
[`context/ARCHITECTURE.md`](../context/ARCHITECTURE.md) ("The simulation period" and
"Chart legends vs data keys").

- **RunPeriod day-alignment** — `get_outage_period()` built the expanded window from the
  `+1 hoy` corrected week, which ends at hour-0 of the next day. The window stayed 216 hours
  but touched 10 calendar dates, and EnergyPlus `RunPeriod` is date-based, so runs were
  240 hours. Surfaced by the SET post-processing's 216-record check on the first real
  project model. The morphing window is unchanged, so existing morphed EPW files stay valid.
- **Display-name legends** — E+ names Zones after the HB Room `identifier`
  (`03_NORTH_0ac0d721`). Legends now resolve to `display_name` via the HBJSON beside the SQL.
  `Record.Zone` deliberately keeps the raw E+ key, since the CSV/JSON exports feed the
  Grasshopper wrapper and the web report.

Both were found while debugging a live project model (2613 Ayers), not by the test suite —
the expanded outage period had no test coverage at all. Regression tests added for both.

## Update rule

When an item reaches `Complete`, fold its outcome into the relevant `context/` doc, then move it to `archive/<slug>/` and add a row to `archive/README.md`.
