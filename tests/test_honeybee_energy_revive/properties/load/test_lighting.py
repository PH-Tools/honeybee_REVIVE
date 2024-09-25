from unittest.mock import Mock

import pytest

from honeybee_energy_revive.properties.load.lighting import (
    LightingReviveProperties,
    LightingReviveProperties_FromDictError,
)


@pytest.fixture
def mock_host():
    mock = Mock()
    mock.display_name = "Mock Lighting Host"
    return mock


def test_lighting_revive_properties_initialization(mock_host):
    lighting_props = LightingReviveProperties(mock_host)
    assert lighting_props.host == mock_host
    assert lighting_props.id_num == 0


def test_lighting_revive_properties_host_name(mock_host):
    lighting_props = LightingReviveProperties(mock_host)
    assert lighting_props.host_name == mock_host.display_name

    lighting_props_no_host = LightingReviveProperties()
    assert lighting_props_no_host.host_name == "No Host"


def test_lighting_revive_properties_duplicate(mock_host):
    lighting_props = LightingReviveProperties(mock_host)
    lighting_props.id_num = 5

    duplicated_props = lighting_props.duplicate(mock_host)
    assert duplicated_props.host == mock_host
    assert duplicated_props.id_num == 5

    duplicated_props_with_new_host = lighting_props.duplicate(mock_host)
    assert duplicated_props_with_new_host.host == mock_host
    assert duplicated_props_with_new_host.id_num == 5


def test_lighting_revive_properties_to_dict(mock_host):
    lighting_props = LightingReviveProperties(mock_host)
    lighting_props.id_num = 5

    expected_dict = {
        "revive": {
            "type": "LightingReviveProperties",
            "id_num": 5,
            "cost": 0.0,
            "labor_fraction": 0.4,
            "lifetime_years": 25,
        }
    }
    assert lighting_props.to_dict() == expected_dict

    expected_abridged_dict = {
        "revive": {
            "type": "LightingRevivePropertiesAbridged",
            "id_num": 5,
            "cost": 0.0,
            "labor_fraction": 0.4,
            "lifetime_years": 25,
        }
    }
    assert lighting_props.to_dict(abridged=True) == expected_abridged_dict


def test_lighting_revive_properties_from_dict(mock_host):
    input_dict = {
        "type": "LightingReviveProperties",
        "id_num": 5,
        "cost": 0.0,
        "labor_fraction": 0.4,
        "lifetime_years": 25,
    }

    lighting_props = LightingReviveProperties.from_dict(input_dict, mock_host)
    assert lighting_props.host == mock_host
    assert lighting_props.id_num == 5

    with pytest.raises(LightingReviveProperties_FromDictError):
        invalid_input_dict = {"type": "InvalidType", "id_num": 5}
        LightingReviveProperties.from_dict(invalid_input_dict, mock_host)


def test_lighting_revive_properties_str_repr(mock_host):
    lighting_props = LightingReviveProperties(mock_host)
    expected_str = "HBE-Lighting Phius REVIVE Property: [host: Mock Lighting Host]"
    assert str(lighting_props) == expected_str
    assert repr(lighting_props) == expected_str
