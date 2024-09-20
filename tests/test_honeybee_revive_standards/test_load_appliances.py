import pytest
from pathlib import Path
from honeybee_revive_standards.appliances._load_appliances import (
    load_abridged_appliances_from_json_file,
)
from honeybee_energy.load.process import Process


def test_load_sample_file_from_abridged_standards_library():
    appliance_filepath = Path("honeybee_revive_standards/appliances/phius_revive_2024_appliances_abridged.json")
    schedule_filepath = Path("honeybee_revive_standards/schedules/phius_revive_2024_schedules.json")
    results = load_abridged_appliances_from_json_file(str(appliance_filepath), str(schedule_filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for measure in results.values():
        assert isinstance(measure, Process)


def test_load_abridged_raises_ValueError_with_bad_file_path():
    with pytest.raises(ValueError):
        load_abridged_appliances_from_json_file("fake_file_path.json", "fake_file_path.json")
