import tempfile
import json
from pathlib import Path
from honeybee_revive.grid_region import GridRegion
from honeybee_revive_standards.cambium_factors._load_grid_region import load_grid_region_from_json_file


def test_GridRegion_json_round_trip():
    m1 = GridRegion()
    j1 = json.dumps(m1.to_dict())
    m2 = GridRegion.from_dict(json.loads(j1))

    assert m2.to_dict() == m1.to_dict()


def test_load_grid_region():
    with tempfile.NamedTemporaryFile(mode="w", delete=True, suffix=".json") as temp_file:
        # -- Write out the temporary data to a JSON file --
        region_01 = GridRegion(_filepath=temp_file.name)
        json.dump(region_01.to_dict(), temp_file, indent=4)

        # -- Ensure data is written to disk
        temp_file.flush()

        # -- Move the file pointer to the beginning of the JSON file
        temp_file.seek(0)

        # -- Load the data back in from the temporary JSON file
        region_02 = load_grid_region_from_json_file(str(temp_file.name))

        # -- Check if the result is as expected
        assert isinstance(region_02, GridRegion)
        assert region_02.to_dict() == region_01.to_dict()


def test_example_grid_region_from_standards_library():
    filepath = Path("honeybee_revive_standards/cambium_factors/MROEc.json")
    region = load_grid_region_from_json_file(str(filepath))
    assert region.region_name == "MRO East"
    assert region.region_code == "MROEc"
    assert region.description == "Eastern Wisconsin"
