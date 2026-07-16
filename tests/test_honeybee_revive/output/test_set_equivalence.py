"""EnergyPlus Pierce SET equivalence gate for post-processed SET."""

from pathlib import Path
from statistics import median

from honeybee_revive.output._shared import Record, get_time_series_data
from honeybee_revive.output.set_calculator import calculate_set, evaluate_winter_set

FIXTURE_PATH = Path(__file__).parents[2] / "_fixtures" / "winter_set_contract.sql"
ZONE_NAME = "ROOM_1_3B02CCA3"
REFERENCE_SET_VARIABLE = "Zone Thermal Comfort Pierce Model Standard Effective Temperature"


def _computed_and_reference_records() -> tuple[list[Record], list[Record]]:
    """Return computed and EnergyPlus SET Records with the same zone key."""
    computed = calculate_set(
        get_time_series_data(FIXTURE_PATH, "Zone Mean Air Temperature"),
        get_time_series_data(FIXTURE_PATH, "Zone Mean Radiant Temperature"),
        get_time_series_data(FIXTURE_PATH, "Zone Air Relative Humidity"),
    )
    reference = [
        Record(record.Date, record.Value, ZONE_NAME)
        for record in get_time_series_data(FIXTURE_PATH, REFERENCE_SET_VARIABLE)
    ]
    return computed, reference


def test_computed_set_matches_energyplus_hourly_distribution() -> None:
    """All 216 hours align and median absolute delta stays below 0.5 K."""
    computed, reference = _computed_and_reference_records()
    computed_by_key = {(record.Zone, record.Date): record.Value for record in computed}
    reference_by_key = {(record.Zone, record.Date): record.Value for record in reference}

    assert len(computed_by_key) == 216
    assert computed_by_key.keys() == reference_by_key.keys()
    absolute_deltas = [abs(computed_by_key[key] - reference_by_key[key]) for key in computed_by_key]
    assert median(absolute_deltas) <= 0.5


def test_computed_set_preserves_energyplus_compliance_verdict() -> None:
    """Central-168 verdicts match and degree-hour totals meet tolerance."""
    computed, reference = _computed_and_reference_records()
    computed_metric = evaluate_winter_set(computed).zone_metrics[ZONE_NAME]
    reference_metric = evaluate_winter_set(reference).zone_metrics[ZONE_NAME]
    tolerance_k_h = max(reference_metric.degree_hours_k_h * 0.05, 2.0)

    assert computed_metric.passes == reference_metric.passes
    assert abs(computed_metric.degree_hours_k_h - reference_metric.degree_hours_k_h) <= tolerance_k_h
