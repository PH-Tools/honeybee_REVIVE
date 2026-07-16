"""Tests for measure-free winter SET calculation."""

from datetime import datetime, timedelta, timezone

import pandas as pd
import pytest
from ladybug_comfort.pmv import pierce_set

from honeybee_revive.output._shared import Record
from honeybee_revive.output.set_calculator import (
    ACTIVITY_LEVEL_W_PER_PERSON,
    AIR_SPEED_M_S,
    CLOTHING_INSULATION_CLO,
    EXTERNAL_WORK_MET,
    SetInputError,
    calculate_set,
    calculate_winter_set,
    met_from_activity_level,
)

START = datetime(2021, 1, 27)


def _records(zone: str, values: list[float], interval_hours: int = 1) -> list[Record]:
    """Build a simple hourly record series."""
    return [Record(START + timedelta(hours=index * interval_hours), value, zone) for index, value in enumerate(values)]


def test_met_from_activity_level_uses_source_constants() -> None:
    """Activity level uses the matching E+ and ladybug-comfort constants."""
    assert met_from_activity_level(120) == pytest.approx(120 / (1.8258 * 58.2))


@pytest.mark.parametrize(
    ("air_temperature", "radiant_temperature", "relative_humidity"),
    ((20.0, 19.0, 40.0), (10.0, 8.0, 65.0), (28.0, 30.0, 55.0)),
)
def test_calculate_set_matches_pierce_set(
    air_temperature: float,
    radiant_temperature: float,
    relative_humidity: float,
) -> None:
    """Each calculated row delegates to ladybug-comfort Pierce SET."""
    result = calculate_set(
        _records("ZONE A", [air_temperature]),
        _records("ZONE A", [radiant_temperature]),
        _records("ZONE A", [relative_humidity]),
    )[0]

    expected = pierce_set(
        air_temperature,
        radiant_temperature,
        AIR_SPEED_M_S,
        relative_humidity,
        met_from_activity_level(ACTIVITY_LEVEL_W_PER_PERSON),
        CLOTHING_INSULATION_CLO,
        EXTERNAL_WORK_MET,
    )
    assert result == Record(START, expected, "ZONE A")


def test_calculate_set_rejects_duplicate_keys() -> None:
    """Duplicate zone/timestamp keys fail before SET calculation."""
    air_temperature = _records("ZONE A", [20.0, 21.0])
    with pytest.raises(SetInputError, match="duplicate.*air temperature"):
        calculate_set(
            air_temperature + [air_temperature[0]],
            _records("ZONE A", [19.0, 20.0]),
            _records("ZONE A", [40.0, 41.0]),
        )


@pytest.mark.parametrize(
    ("changed_input", "message"),
    (("missing", "missing 1.*ZONE A.*2021-01-27 01:00:00"), ("extra", "extra 1.*ZONE B.*2021-01-27 00:00:00")),
)
def test_calculate_set_rejects_mismatched_keys(changed_input: str, message: str) -> None:
    """Missing and extra input keys produce actionable errors."""
    air_temperature = _records("ZONE A", [20.0, 21.0])
    radiant_temperature = _records("ZONE A", [19.0, 20.0])
    if changed_input == "missing":
        radiant_temperature = radiant_temperature[:-1]
    else:
        radiant_temperature += _records("ZONE B", [18.0])

    with pytest.raises(SetInputError, match=message):
        calculate_set(air_temperature, radiant_temperature, _records("ZONE A", [40.0, 41.0]))


def test_calculate_set_rejects_non_hourly_records() -> None:
    """Gapped input series cannot be treated as hourly compliance data."""
    with pytest.raises(SetInputError, match="hourly.*ZONE A"):
        calculate_set(
            _records("ZONE A", [20.0, 21.0], interval_hours=2),
            _records("ZONE A", [19.0, 20.0], interval_hours=2),
            _records("ZONE A", [40.0, 41.0], interval_hours=2),
        )


def test_calculate_winter_set_validates_run_length_before_pierce(monkeypatch: pytest.MonkeyPatch) -> None:
    """An incomplete winter run fails before expensive row calculations."""
    monkeypatch.setattr(
        "honeybee_revive.output.set_calculator.pierce_set",
        lambda *_args: pytest.fail("Pierce SET should not run for an incomplete winter period."),
    )
    with pytest.raises(SetInputError, match="216 hourly records"):
        calculate_winter_set(
            _records("ZONE A", [20.0] * 215),
            _records("ZONE A", [19.0] * 215),
            _records("ZONE A", [40.0] * 215),
        )


def test_calculate_set_rejects_mixed_timezone_awareness() -> None:
    """A zone series cannot mix naive and timezone-aware timestamps."""
    air_temperature = _records("ZONE A", [20.0, 21.0])
    air_temperature[1] = Record(air_temperature[1].Date.replace(tzinfo=timezone.utc), 21.0, "ZONE A")
    with pytest.raises(SetInputError, match="timezone awareness.*ZONE A"):
        calculate_set(
            air_temperature,
            [Record(record.Date, value, "ZONE A") for record, value in zip(air_temperature, [19.0, 20.0])],
            [Record(record.Date, value, "ZONE A") for record, value in zip(air_temperature, [40.0, 41.0])],
        )


def test_calculate_set_accepts_long_form_dataframes() -> None:
    """Long-form DataFrames normalize to the same Record output contract."""
    air_temperature = _records("ZONE A", [20.0])
    radiant_temperature = _records("ZONE A", [19.0])
    relative_humidity = _records("ZONE A", [40.0])

    expected = calculate_set(air_temperature, radiant_temperature, relative_humidity)
    actual = calculate_set(
        pd.DataFrame(air_temperature),
        pd.DataFrame(radiant_temperature),
        pd.DataFrame(relative_humidity),
    )
    assert actual == expected


def test_calculate_set_rejects_incomplete_dataframe_contract() -> None:
    """Long-form DataFrames must expose all three Record columns."""
    incomplete = pd.DataFrame({"Date": [START], "Value": [20.0]})
    with pytest.raises(SetInputError, match="missing required column.*Zone"):
        calculate_set(incomplete, incomplete, incomplete)


def test_calculate_set_rejects_non_datetime_keys() -> None:
    """String timestamps cannot silently enter the hourly keyed join."""
    records = [Record("2021-01-27 00:00:00", 20.0, "ZONE A")]
    with pytest.raises(SetInputError, match="non-datetime timestamp"):
        calculate_set(records, records, records)


def test_calculate_set_rejects_empty_inputs() -> None:
    """An empty aligned input set cannot produce a compliance series."""
    with pytest.raises(SetInputError, match="at least one hourly input"):
        calculate_set([], [], [])


def test_calculate_set_keeps_zones_isolated() -> None:
    """Multi-zone records use only inputs with the same zone and timestamp."""
    air_temperature = _records("ZONE A", [20.0, 21.0]) + _records("ZONE B", [5.0, 6.0])
    radiant_temperature = list(reversed(_records("ZONE A", [19.0, 20.0]) + _records("ZONE B", [4.0, 5.0])))
    relative_humidity = list(reversed(_records("ZONE A", [40.0, 41.0]) + _records("ZONE B", [70.0, 71.0])))

    results = calculate_set(air_temperature, radiant_temperature, relative_humidity)
    result_by_key = {(record.Zone, record.Date): record.Value for record in results}
    met = met_from_activity_level(ACTIVITY_LEVEL_W_PER_PERSON)
    radiant_by_key = {(record.Zone, record.Date): record.Value for record in radiant_temperature}
    humidity_by_key = {(record.Zone, record.Date): record.Value for record in relative_humidity}
    for air_record in air_temperature:
        key = (air_record.Zone, air_record.Date)
        expected = pierce_set(
            air_record.Value,
            radiant_by_key[key],
            AIR_SPEED_M_S,
            humidity_by_key[key],
            met,
            CLOTHING_INSULATION_CLO,
            EXTERNAL_WORK_MET,
        )
        assert result_by_key[key] == expected
