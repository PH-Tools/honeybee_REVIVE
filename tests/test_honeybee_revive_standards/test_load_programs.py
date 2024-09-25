from pathlib import Path

from honeybee_energy.programtype import ProgramType

from honeybee_revive_standards.programtypes._load_programs import load_programs_from_json_file
from honeybee_revive_standards.schedules._load_schedules import load_schedules_from_json_file


def test_load_appliance_schedules_from_standards_library():
    # -- Load all the schedules from all of the JSON files in the standards files
    schedules_dict = {}
    schedules_path = Path("honeybee_revive_standards/schedules")
    for json_file in schedules_path.glob("*.json"):
        schedules_dict.update(load_schedules_from_json_file(str(json_file)))

    programs_filepath = Path("honeybee_revive_standards/programtypes/rv2024_programs_abridged.json")

    results = load_programs_from_json_file(str(programs_filepath), _schedules_dict=schedules_dict)

    assert isinstance(results, dict)
    assert len(results) > 0
    for program_ in results.values():
        assert isinstance(program_, ProgramType)
