from unittest.mock import Mock

import pytest

from honeybee_revive.CO2_measures import CO2ReductionMeasureCollection
from honeybee_revive.fuels import FuelCollection
from honeybee_revive.grid_region import GridRegion
from honeybee_revive.national_emissions import NationalEmissionsFactors
from honeybee_revive.properties.model import ModelReviveProperties


@pytest.fixture
def sample_model():
    mock = Mock()
    mock.display_name = "Test Model"
    return mock


@pytest.fixture
def sample_properties(sample_model) -> ModelReviveProperties:
    return ModelReviveProperties(sample_model)


def test_initialization(sample_properties, sample_model):
    assert sample_properties.host == sample_model
    assert sample_properties.id_num == 0
    assert isinstance(sample_properties.grid_region, GridRegion)
    assert isinstance(sample_properties.national_emissions_factors, NationalEmissionsFactors)
    assert sample_properties.analysis_duration == 50
    assert sample_properties.envelope_labor_cost_fraction == 0.4
    assert isinstance(sample_properties.co2_measures, CO2ReductionMeasureCollection)
    assert isinstance(sample_properties.fuels, FuelCollection)


def test_duplicate(sample_properties):
    duplicate_properties = sample_properties.duplicate()
    assert duplicate_properties.host == sample_properties.host
    assert duplicate_properties.id_num == sample_properties.id_num
    assert duplicate_properties.grid_region != sample_properties.grid_region
    assert duplicate_properties.national_emissions_factors != sample_properties.national_emissions_factors
    assert duplicate_properties.analysis_duration == sample_properties.analysis_duration
    assert duplicate_properties.envelope_labor_cost_fraction == sample_properties.envelope_labor_cost_fraction
    assert duplicate_properties.co2_measures != sample_properties.co2_measures
    assert duplicate_properties.fuels != sample_properties.fuels


def test_to_dict(sample_properties):
    properties_dict = sample_properties.to_dict()
    assert properties_dict["revive"]["type"] == "ModelRevivePropertiesAbridged"
    assert properties_dict["revive"]["id_num"] == sample_properties.id_num
    assert properties_dict["revive"]["grid_region"] == sample_properties.grid_region.to_dict()
    assert (
        properties_dict["revive"]["national_emissions_factors"]
        == sample_properties.national_emissions_factors.to_dict()
    )
    assert properties_dict["revive"]["analysis_duration"] == sample_properties.analysis_duration
    assert properties_dict["revive"]["envelope_labor_cost_fraction"] == sample_properties.envelope_labor_cost_fraction
    assert properties_dict["revive"]["co2_measures"] == sample_properties.co2_measures.to_dict()
    assert properties_dict["revive"]["fuels"] == sample_properties.fuels.to_dict()


def test_from_dict(sample_model):
    properties_dict = {
        "type": "ModelReviveProperties",
        "id_num": 1,
        "grid_region": GridRegion().to_dict(),
        "national_emissions_factors": NationalEmissionsFactors().to_dict(),
        "analysis_duration": 60,
        "envelope_labor_cost_fraction": 0.5,
        "co2_measures": CO2ReductionMeasureCollection().to_dict(),
        "fuels": FuelCollection.with_default_fuels().to_dict(),
    }
    properties = ModelReviveProperties.from_dict(properties_dict, sample_model)
    assert properties.id_num == 1
    assert properties.analysis_duration == 60
    assert properties.envelope_labor_cost_fraction == 0.5


def test_model_load_properties_from_dict(sample_properties: ModelReviveProperties):
    sample_grid_region = GridRegion()
    sample_national_emissions_factors = NationalEmissionsFactors()
    sample_measures_collection = CO2ReductionMeasureCollection()
    properties_dict = {
        "properties": {
            "revive": {
                "type": "ModelReviveProperties",
                "id_num": 1,
                "grid_region": sample_grid_region.to_dict(),
                "national_emissions_factors": sample_national_emissions_factors.to_dict(),
                "analysis_duration": 60,
                "envelope_labor_cost_fraction": 0.5,
                "co2_measures": sample_measures_collection.to_dict(),
                "fuels": FuelCollection.with_default_fuels().to_dict(),
            },
            "another_key": {},
        }
    }
    result = sample_properties.load_properties_from_dict(properties_dict)
    assert result[0].to_dict() == sample_grid_region.to_dict()
    assert result[1].to_dict() == sample_national_emissions_factors.to_dict()
    assert result[2] == 60
    assert result[3] == 0.5
    assert result[4].to_dict() == sample_measures_collection.to_dict()
