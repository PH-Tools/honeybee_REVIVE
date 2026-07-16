"""Tests locking the real winter SQL input and outage-window contract."""

import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from honeybee_revive.output._shared import Record, get_time_series_data

FIXTURE_PATH = Path(__file__).parents[2] / "_fixtures" / "winter_set_contract.sql"
INPUT_VARIABLES = (
    "Zone Mean Air Temperature",
    "Zone Mean Radiant Temperature",
    "Zone Air Relative Humidity",
)
REFERENCE_SET_VARIABLE = "Zone Thermal Comfort Pierce Model Standard Effective Temperature"
ZONE_NAME = "ROOM_1_3B02CCA3"


def _records_by_zone(variable_name: str) -> dict[str, list[Record]]:
    """Return fixture records grouped by zone."""
    records: dict[str, list[Record]] = defaultdict(list)
    for record in get_time_series_data(FIXTURE_PATH, variable_name):
        records[record.Zone].append(record)
    return records


def test_winter_set_inputs_share_hourly_keys() -> None:
    """The three SET inputs align one-to-one by zone and hourly timestamp."""
    key_sets = []
    for variable_name in INPUT_VARIABLES:
        records_by_zone = _records_by_zone(variable_name)
        assert set(records_by_zone) == {ZONE_NAME}
        zone_records = records_by_zone[ZONE_NAME]
        assert len(zone_records) == 216
        assert all(
            current.Date - previous.Date == timedelta(hours=1)
            for previous, current in zip(zone_records, zone_records[1:])
        )
        key_sets.append({(record.Zone, record.Date) for record in zone_records})

    assert key_sets[0] == key_sets[1] == key_sets[2]

    with sqlite3.connect(FIXTURE_PATH) as connection:
        reporting_frequencies = connection.execute(
            "SELECT DISTINCT Name, ReportingFrequency " "FROM ReportVariableWithTime WHERE Name IN (?, ?, ?)",
            INPUT_VARIABLES,
        ).fetchall()
    assert set(reporting_frequencies) == {(name, "Hourly") for name in INPUT_VARIABLES}


def test_winter_set_compliance_window_excludes_edge_buffers() -> None:
    """The nine-day run contains a central seven-day compliance window."""
    zone_records = _records_by_zone(INPUT_VARIABLES[0])[ZONE_NAME]
    compliance_records = zone_records[24:-24]

    assert len(zone_records) == 216
    assert len(compliance_records) == 168
    assert zone_records[0].Date == datetime(2021, 1, 26, 0)
    assert compliance_records[0].Date == datetime(2021, 1, 27, 0)
    assert compliance_records[-1].Date == datetime(2021, 2, 2, 23)
    assert zone_records[-1].Date == datetime(2021, 2, 3, 23)


def test_winter_set_reference_series_is_hourly_and_people_keyed() -> None:
    """The reference E+ Pierce SET series retains its measure-era People key."""
    records_by_zone = _records_by_zone(REFERENCE_SET_VARIABLE)
    assert set(records_by_zone) == {"ROOM_1_3B02CCA3_SPACE RV2024_RESILIENCE_PEOPLE"}
    reference_records = next(iter(records_by_zone.values()))
    input_records = _records_by_zone(INPUT_VARIABLES[0])[ZONE_NAME]
    assert len(reference_records) == 216
    assert [record.Date for record in reference_records] == [record.Date for record in input_records]

    with sqlite3.connect(FIXTURE_PATH) as connection:
        reporting_frequency = connection.execute(
            "SELECT DISTINCT ReportingFrequency FROM ReportVariableWithTime WHERE Name=?",
            (REFERENCE_SET_VARIABLE,),
        ).fetchone()[0]
    assert reporting_frequency == "Hourly"
