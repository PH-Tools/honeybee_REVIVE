"""Tests for winter SET outage slicing and certification metrics."""

from datetime import datetime, timedelta
from math import nan

import pytest

from honeybee_revive.output._shared import Record
from honeybee_revive.output.set_calculator import (
    DEGREE_HOUR_LIMIT_K_H,
    EXPECTED_RUN_HOURS,
    OUTAGE_HOURS,
    SET_THRESHOLD_C,
    SetInputError,
    evaluate_winter_set,
)

START = datetime(2021, 1, 26)


def _set_records(zone: str, values: list[float], interval_hours: int = 1) -> list[Record]:
    """Build a SET record series."""
    return [Record(START + timedelta(hours=index * interval_hours), value, zone) for index, value in enumerate(values)]


def test_evaluate_winter_set_uses_central_168_hours() -> None:
    """Cold 24-hour edge buffers do not enter certification metrics."""
    values = [0.0] * 24 + [SET_THRESHOLD_C] * OUTAGE_HOURS + [0.0] * 24
    result = evaluate_winter_set(_set_records("ZONE A", values))

    assert len(result.full_records) == EXPECTED_RUN_HOURS
    assert len(result.outage_records) == OUTAGE_HOURS
    assert len(result.deficit_records) == OUTAGE_HOURS
    assert result.outage_records[0].Date == START + timedelta(hours=24)
    assert result.outage_records[-1].Date == START + timedelta(hours=191)
    assert result.zone_metrics["ZONE A"].degree_hours_k_h == 0
    assert result.zone_metrics["ZONE A"].passes


def test_evaluate_winter_set_reports_deficits_and_degree_hours() -> None:
    """Hourly deficits sum in K-h and convert to degF-h by 1.8."""
    outage_values = [SET_THRESHOLD_C - 1.0, SET_THRESHOLD_C - 2.0] + [SET_THRESHOLD_C + 1.0] * 166
    values = [SET_THRESHOLD_C] * 24 + outage_values + [SET_THRESHOLD_C] * 24
    result = evaluate_winter_set(_set_records("ZONE A", values))

    assert [record.Value for record in result.deficit_records[:3]] == [1.0, 2.0, 0.0]
    metric = result.zone_metrics["ZONE A"]
    assert metric.degree_hours_k_h == pytest.approx(3.0)
    assert metric.degree_hours_f_h == pytest.approx(5.4)
    assert metric.passes


def test_evaluate_winter_set_applies_per_zone_limit() -> None:
    """Each zone receives its own total and verdict against 120 K-h."""
    passing = [SET_THRESHOLD_C] * EXPECTED_RUN_HOURS
    passing[24] = SET_THRESHOLD_C - DEGREE_HOUR_LIMIT_K_H
    failing = passing.copy()
    failing[24] = SET_THRESHOLD_C - DEGREE_HOUR_LIMIT_K_H - 0.01

    result = evaluate_winter_set(_set_records("PASS", passing) + _set_records("FAIL", failing))

    assert result.zone_metrics["PASS"].degree_hours_k_h == pytest.approx(120.0)
    assert result.zone_metrics["PASS"].passes
    assert result.zone_metrics["FAIL"].degree_hours_k_h == pytest.approx(120.01)
    assert not result.zone_metrics["FAIL"].passes
    assert len(result.outage_records) == OUTAGE_HOURS * 2


def test_evaluate_winter_set_exact_distributed_limit_passes() -> None:
    """Floating accumulation does not fail an exact distributed 120 K-h total."""
    hourly_deficit = DEGREE_HOUR_LIMIT_K_H / OUTAGE_HOURS
    values = [SET_THRESHOLD_C] * 24 + [SET_THRESHOLD_C - hourly_deficit] * OUTAGE_HOURS + [SET_THRESHOLD_C] * 24

    metric = evaluate_winter_set(_set_records("ZONE A", values)).zone_metrics["ZONE A"]

    assert metric.degree_hours_k_h == pytest.approx(DEGREE_HOUR_LIMIT_K_H)
    assert metric.passes


def test_evaluate_winter_set_rejects_non_finite_values() -> None:
    """NaN cannot silently become a zero deficit and certify a zone."""
    values = [SET_THRESHOLD_C] * EXPECTED_RUN_HOURS
    values[24] = nan
    with pytest.raises(SetInputError, match="finite.*ZONE A.*2021-01-27 00:00:00"):
        evaluate_winter_set(_set_records("ZONE A", values))


def test_evaluate_winter_set_rejects_non_numeric_values() -> None:
    """Non-numeric SET values produce the same actionable finite-value error."""
    values: list[float | str] = [SET_THRESHOLD_C] * EXPECTED_RUN_HOURS
    values[24] = "not-a-number"
    records = [Record(START + timedelta(hours=index), value, "ZONE A") for index, value in enumerate(values)]
    with pytest.raises(SetInputError, match="finite.*not-a-number"):
        evaluate_winter_set(records)


def test_evaluate_winter_set_rejects_empty_inputs() -> None:
    """An empty SET series cannot produce certification metrics."""
    with pytest.raises(SetInputError, match="at least one hourly record"):
        evaluate_winter_set([])


@pytest.mark.parametrize(
    ("values", "interval_hours", "message"),
    (([SET_THRESHOLD_C] * 215, 1, "216 hourly"), ([SET_THRESHOLD_C] * 216, 2, "hourly.*ZONE A")),
)
def test_evaluate_winter_set_rejects_unexpected_run_contract(
    values: list[float], interval_hours: int, message: str
) -> None:
    """Wrong row counts and intervals fail instead of slicing silently."""
    with pytest.raises(SetInputError, match=message):
        evaluate_winter_set(_set_records("ZONE A", values, interval_hours))
