import pytest
from pathlib import Path
from honeybee_revive_standards.schedules._load_schedules import load_schedules_from_json_file
from honeybee_energy.schedule.ruleset import ScheduleRuleset


def test_load_appliance_schedules_from_standards_library():
    filepath = Path("honeybee_revive_standards/schedules/rv2024_appliance_schedules.json")
    results = load_schedules_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for schedule_ in results.values():
        assert isinstance(schedule_, ScheduleRuleset)


def test_load_electric_equipment_schedules_from_standards_library():
    filepath = Path("honeybee_revive_standards/schedules/rv2024_electric_equipment_schedules.json")
    results = load_schedules_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for schedule_ in results.values():
        assert isinstance(schedule_, ScheduleRuleset)


def test_load_hot_water_schedules_from_standards_library():
    filepath = Path("honeybee_revive_standards/schedules/rv2024_hot_water_schedules.json")
    results = load_schedules_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for schedule_ in results.values():
        assert isinstance(schedule_, ScheduleRuleset)


def test_load_lighting_schedules_from_standards_library():
    filepath = Path("honeybee_revive_standards/schedules/rv2024_lighting_schedules.json")
    results = load_schedules_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for schedule_ in results.values():
        assert isinstance(schedule_, ScheduleRuleset)


def test_load_occupancy_schedules_from_standards_library():
    filepath = Path("honeybee_revive_standards/schedules/rv2024_occupancy_schedules.json")
    results = load_schedules_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for schedule_ in results.values():
        assert isinstance(schedule_, ScheduleRuleset)


def test_load_setpoint_schedules_from_standards_library():
    filepath = Path("honeybee_revive_standards/schedules/rv2024_setpoint_schedules.json")
    results = load_schedules_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for schedule_ in results.values():
        assert isinstance(schedule_, ScheduleRuleset)


def test_load_raises_ValueError_with_bad_file_path():
    with pytest.raises(ValueError):
        load_schedules_from_json_file("fake_file_path.json")
