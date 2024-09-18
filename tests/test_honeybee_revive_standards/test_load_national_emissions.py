import json
import pytest
import tempfile
from pathlib import Path
from honeybee_revive_standards.national_emission_factors._load_national_emissions import (
    load_national_emissions_from_json_file,
)
from honeybee_revive.national_emissions import NationalEmissionsFactors


def test_load_national_emissions_from_json_file_valid():
    countryA = NationalEmissionsFactors(
        country_name="CountryA",
        us_trading_rank=0,
        GDP_million_USD=20936600.0,
        CO2_MT=4900.0,
        kg_CO2_per_USD=0.234,
    )
    countryB = NationalEmissionsFactors(
        country_name="CountryB",
        us_trading_rank=3,
        GDP_million_USD=1643407.98,
        CO2_MT=565.2,
        kg_CO2_per_USD=0.344,
    )
    countryC = NationalEmissionsFactors(
        country_name="CountryC",
        us_trading_rank=1,
        GDP_million_USD=14722730.7,
        CO2_MT=9500.0,
        kg_CO2_per_USD=0.645,
    )

    _emissions = [countryA, countryB, countryC]
    with tempfile.NamedTemporaryFile(mode="w", delete=True, suffix=".json") as temp_file:
        # -- Write out the temporary data to a JSON file --
        json.dump([e.to_dict() for e in _emissions], temp_file, indent=4)

        # -- Ensure data is written to disk
        temp_file.flush()

        # -- Move the file pointer to the beginning of the JSON file
        temp_file.seek(0)

        # -- Load the data back in from the temporary JSON file
        result = load_national_emissions_from_json_file(str(temp_file.name))

        # -- Check if the result is as expected
        assert isinstance(result, dict)
        assert "CountryA" in result
        assert "CountryB" in result
        assert isinstance(result["CountryA"], NationalEmissionsFactors)
        assert isinstance(result["CountryB"], NationalEmissionsFactors)
        assert result["CountryA"].us_trading_rank == 0
        assert result["CountryB"].us_trading_rank == 3
        assert result["CountryC"].us_trading_rank == 1


def test_load_national_emissions_from_json_file_invalid_path():
    with pytest.raises(ValueError):
        load_national_emissions_from_json_file("non_existent_file.json")


def test_sample_file_from_standards_library():
    filepath = Path("honeybee_revive_standards/national_emission_factors/national_emissions.json")
    results = load_national_emissions_from_json_file(str(filepath))

    assert isinstance(results, dict)
    assert len(results) > 0
    for country in results.values():
        assert isinstance(country, NationalEmissionsFactors)
