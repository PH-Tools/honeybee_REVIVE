# Computed vs EnergyPlus Pierce SET comparison

## Fixture and method

- Fixture: `tests/_fixtures/winter_set_contract.sql` (`79b22f559d680fe33cb2de546f354a19c171d6921a97fc91e027040fd576421b`)
- Zone: `ROOM_1_3B02CCA3`
- Hours compared: all 216 common hourly timestamps
- Certification window: central 168 hours (`records[24:-24]`)
- Computed inputs: hourly zone air temperature, mean radiant temperature, and relative humidity
- Fixed assumptions: 1.0 clo, 120 W/person, 0.16 m/s, zero external work, `met = 120 / (1.8258 * 58.2)`

The EnergyPlus reference is the measure-era `Zone Thermal Comfort Pierce Model Standard Effective Temperature` series. Its People-object key is mapped to the actual zone only for this validation comparison. The production computed path uses actual zone keys directly.

## Hourly delta results

`Delta SET = computed - EnergyPlus reference`.

| Statistic | Absolute delta |
|---|---:|
| Median | 0.082138 K |
| 95th percentile | 0.121371 K |
| Maximum | 0.134251 K |

Worst five timestamps:

| Timestamp | Computed (C) | E+ reference (C) | Delta (K) |
|---|---:|---:|---:|
| 2021-01-29 02:00 | 10.052175 | 10.186426 | -0.134251 |
| 2021-01-29 03:00 | 9.597354 | 9.731061 | -0.133708 |
| 2021-01-29 01:00 | 10.590087 | 10.723212 | -0.133125 |
| 2021-01-29 04:00 | 9.149876 | 9.281145 | -0.131269 |
| 2021-01-29 00:00 | 10.843729 | 10.974960 | -0.131231 |

The small systematic difference is consistent with the known aggregation boundary: EnergyPlus calculates SET at the zone timestep and reports an hourly average, while post-processing applies Pierce SET to hourly-average air temperature, MRT, and RH.

## Central-168 compliance results

| Series | Degree-hours (K-h) | Degree-hours (degF-h) | 120 K-h verdict |
|---|---:|---:|---|
| Computed | 971.710697 | 1749.079255 | Fail |
| E+ reference | 957.789744 | 1724.021539 | Fail |
| Difference | 13.920953 (1.453%) | 25.057716 | Identical |

Acceptance checks:

- Identical per-zone verdict: pass.
- Median absolute hourly delta at most 0.5 K: pass (`0.082138 K`).
- Degree-hour difference within 5% or 2 K-h, whichever is larger: pass (`1.453%`).

No physical constants were tuned against the fixture.
