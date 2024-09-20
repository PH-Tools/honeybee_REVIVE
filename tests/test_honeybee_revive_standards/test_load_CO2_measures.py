import pytest
import tempfile
import json
from pathlib import Path
from honeybee_revive_standards.CO2_measures._load_CO2_measures import load_CO2_measures_from_json_file
from honeybee_revive.CO2_measures import CO2ReductionMeasure


def test_CO2_measure_json_round_trip():
    m1 = CO2ReductionMeasure()
    j1 = json.dumps(m1.to_dict())
    m2 = CO2ReductionMeasure.from_dict(json.loads(j1))

    assert m2.to_dict() == m1.to_dict()


def test_load_CO2_measures_from_json_file_valid():
    measures_ = [
        CO2ReductionMeasure(name="Measure1", year=1),
        CO2ReductionMeasure(name="Measure2", year=22),
        CO2ReductionMeasure(name="Measure3", year=67),
    ]
    with tempfile.NamedTemporaryFile(mode="w", delete=True, suffix=".json") as temp_file:
        # -- Write out the temporary data to a JSON file --
        json.dump([e.to_dict() for e in measures_], temp_file, indent=4)

        # -- Ensure data is written to disk
        temp_file.flush()

        # -- Move the file pointer to the beginning of the JSON file
        temp_file.seek(0)

        # -- Load the data back in from the temporary JSON file
        result = load_CO2_measures_from_json_file(str(temp_file.name))

        # -- Check if the result is as expected
        assert isinstance(result, dict)
        assert "Measure1" in result
        assert "Measure2" in result
        assert "Measure3" in result
        assert isinstance(result["Measure1"], CO2ReductionMeasure)
        assert isinstance(result["Measure2"], CO2ReductionMeasure)
        assert isinstance(result["Measure3"], CO2ReductionMeasure)
        assert result["Measure1"].year == 1
        assert result["Measure2"].year == 22
        assert result["Measure3"].year == 67


def test_load_CO2_measures_from_json_file_invalid():
    with pytest.raises(ValueError):
        load_CO2_measures_from_json_file("non_existent_file.json")


def test_load_sample_file_from_standards_library():
    filepath = Path("honeybee_revive_standards/CO2_measures/phius_revive_2024_CO2_measures.json")
    results = load_CO2_measures_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for measure in results.values():
        assert isinstance(measure, CO2ReductionMeasure)
