# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Tests for reading only the final 216-hour REVIVE evaluation window from an EnergyPlus SQL.

A Kiva ground-contact run carries a conditioned lead-in before the 9-day outage window
(24 h conditioning + 168 h outage + 24 h recovery). The winter lead-in starts after the
summer outage and so crosses a year boundary.
"""

from datetime import datetime

import pandas as pd

from honeybee_revive.output._shared import EVALUATION_WINDOW_HOURS, get_time_series_data
from honeybee_revive.output.set_calculator import calculate_winter_set_from_sql
from tests.test_honeybee_revive.output._eplus_sql import write_eplus_sql

DRYBULB = "Site Outdoor Air Drybulb Temperature"
ZONES = ("ZONE_A", "ZONE_B")


def _zone_series(records, zone):
    return [r for r in records if r.Zone == zone]


def _expected_dates(first: str) -> list[pd.Timestamp]:
    return list(pd.date_range(first, periods=EVALUATION_WINDOW_HOURS, freq="h"))


def test_nine_day_run_reads_every_hour(tmp_path):
    sql = write_eplus_sql(
        tmp_path / "eplusout.sql", datetime(2025, 1, 12), datetime(2025, 1, 20), [(DRYBULB, z) for z in ZONES]
    )

    records = get_time_series_data(sql, DRYBULB)

    assert [r.Zone for r in records[:4]] == ["ZONE_A", "ZONE_B", "ZONE_A", "ZONE_B"]
    for zone in ZONES:
        zone_records = _zone_series(records, zone)
        assert [r.Date for r in zone_records] == _expected_dates("2021-01-12 00:00")
        assert [r.Value for r in zone_records] == [float(h) for h in range(EVALUATION_WINDOW_HOURS)]


def test_lead_in_run_reads_only_the_final_window(tmp_path):
    sql = write_eplus_sql(tmp_path / "eplusout.sql", datetime(2026, 2, 1), datetime(2026, 7, 27), [(DRYBULB, "ENV")])
    total_hours = (datetime(2026, 7, 28) - datetime(2026, 2, 1)).days * 24

    records = get_time_series_data(sql, DRYBULB)

    assert [r.Date for r in records] == _expected_dates("2021-07-19 00:00")
    assert records[0].Value == total_hours - EVALUATION_WINDOW_HOURS


def test_year_crossing_lead_in_reads_only_the_final_window(tmp_path):
    sql = write_eplus_sql(tmp_path / "eplusout.sql", datetime(2019, 8, 1), datetime(2020, 1, 20), [(DRYBULB, "ENV")])

    records = get_time_series_data(sql, DRYBULB)

    assert [r.Date for r in records] == _expected_dates("2021-01-12 00:00")


def test_window_crossing_new_year_stays_hourly(tmp_path):
    sql = write_eplus_sql(tmp_path / "eplusout.sql", datetime(2025, 12, 28), datetime(2026, 1, 5), [(DRYBULB, "ENV")])

    records = get_time_series_data(sql, DRYBULB)

    assert [r.Date for r in records] == _expected_dates("2021-12-28 00:00")


def test_no_window_reads_the_whole_run(tmp_path):
    sql = write_eplus_sql(tmp_path / "eplusout.sql", datetime(2019, 8, 1), datetime(2020, 1, 20), [(DRYBULB, "ENV")])

    records = get_time_series_data(sql, DRYBULB, window_hours=None)

    assert records[0].Date == pd.Timestamp("2021-08-01 00:00")
    assert records[-1].Date == pd.Timestamp("2022-01-20 23:00")


def test_winter_set_from_year_crossing_lead_in(tmp_path):
    variables = ("Zone Mean Air Temperature", "Zone Mean Radiant Temperature", "Zone Air Relative Humidity")
    sql = write_eplus_sql(
        tmp_path / "eplusout.sql",
        datetime(2019, 8, 1),
        datetime(2020, 1, 20),
        [(v, z) for v in variables for z in ZONES],
        value=lambda _: 20.0,
    )

    result = calculate_winter_set_from_sql(sql)

    assert set(result.zone_metrics) == set(ZONES)
    for zone in ZONES:
        assert len(_zone_series(result.full_records, zone)) == EVALUATION_WINDOW_HOURS
        assert _zone_series(result.outage_records, zone)[0].Date == pd.Timestamp("2021-01-13 00:00")
