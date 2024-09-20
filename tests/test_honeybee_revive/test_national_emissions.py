import pytest
from honeybee_revive.national_emissions import NationalEmissionsFactors


def test_initialization():
    nef = NationalEmissionsFactors("USA", 1, 21000000.0, 5000.0, 0.24)
    assert nef.country_name == "USA"
    assert nef.us_trading_rank == 1
    assert nef.GDP_million_USD == 21000000.0
    assert nef.CO2_MT == 5000.0
    assert nef.kg_CO2_per_USD == 0.24


def test_to_dict():
    nef = NationalEmissionsFactors("USA", 1, 21000000.0, 5000.0, 0.24)
    nef_dict = nef.to_dict()
    assert nef_dict["country_name"] == "USA"
    assert nef_dict["us_trading_rank"] == 1
    assert nef_dict["GDP_million_USD"] == 21000000.0
    assert nef_dict["CO2_MT"] == 5000.0
    assert nef_dict["kg_CO2_per_USD"] == 0.24


def test_from_dict():
    nef_dict = {
        "type": "NationalEmissionsFactors",
        "country_name": "USA",
        "us_trading_rank": 1,
        "GDP_million_USD": 21000000.0,
        "CO2_MT": 5000.0,
        "kg_CO2_per_USD": 0.24,
    }
    nef = NationalEmissionsFactors.from_dict(nef_dict)
    assert nef.country_name == "USA"
    assert nef.us_trading_rank == 1
    assert nef.GDP_million_USD == 21000000.0
    assert nef.CO2_MT == 5000.0
    assert nef.kg_CO2_per_USD == 0.24


def test_wrong_type_raises_error_from_dict():
    nef_dict = {
        "type": "Not The Right Type",
        "country_name": "USA",
        "us_trading_rank": 1,
        "GDP_million_USD": 21000000.0,
        "CO2_MT": 5000.0,
        "kg_CO2_per_USD": 0.24,
    }
    with pytest.raises(ValueError):
        NationalEmissionsFactors.from_dict(nef_dict)


def test_duplicate():
    nef = NationalEmissionsFactors("USA", 1, 21000000.0, 5000.0, 0.24)
    nef_dup = nef.duplicate()
    assert nef_dup.country_name == "USA"
    assert nef_dup.us_trading_rank == 1
    assert nef_dup.GDP_million_USD == 21000000.0
    assert nef_dup.CO2_MT == 5000.0
    assert nef_dup.kg_CO2_per_USD == 0.24
    assert nef is not nef_dup


def test_copy():
    nef = NationalEmissionsFactors("USA", 1, 21000000.0, 5000.0, 0.24)
    nef_copy = nef.__copy__()
    assert nef_copy.country_name == "USA"
    assert nef_copy.us_trading_rank == 1
    assert nef_copy.GDP_million_USD == 21000000.0
    assert nef_copy.CO2_MT == 5000.0
    assert nef_copy.kg_CO2_per_USD == 0.24
    assert nef is not nef_copy


def test_str():
    nef = NationalEmissionsFactors("USA", 1, 21000000.0, 5000.0, 0.24)
    assert str(nef) == "NationalEmissionsFactors [USA]: 1 | 21000000.0 | 5000.0 | 0.24"


def test_repr():
    nef = NationalEmissionsFactors("USA", 1, 21000000.0, 5000.0, 0.24)
    assert repr(nef) == "NationalEmissionsFactors [USA]: 1 | 21000000.0 | 5000.0 | 0.24"


def test_ToString():
    nef = NationalEmissionsFactors("USA", 1, 21000000.0, 5000.0, 0.24)
    assert nef.ToString() == "NationalEmissionsFactors [USA]: 1 | 21000000.0 | 5000.0 | 0.24"
