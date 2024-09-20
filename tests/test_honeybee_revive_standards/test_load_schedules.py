import pytest
from pathlib import Path
from honeybee_revive_standards.schedules._load_schedules import load_schedules_from_json_file
from honeybee_energy.schedule.ruleset import ScheduleRuleset


def test_load_sample_file_from_standards_library():
    filepath = Path("honeybee_revive_standards/schedules/phius_revive_2024_schedules.json")
    results = load_schedules_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for measure in results.values():
        assert isinstance(measure, ScheduleRuleset)


def test_load_raises_ValueError_with_bad_file_path():
    with pytest.raises(ValueError):
        load_schedules_from_json_file("fake_file_path.json")
