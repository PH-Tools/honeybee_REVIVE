from unittest.mock import Mock

import pytest

from honeybee_energy_revive.properties.generator.pv import (
    PVPropertiesReviveProperties,
    PVPropertiesReviveProperties_FromDictError,
)


@pytest.fixture
def mock_host():
    return Mock(display_name="Test PvProperties")


def test_pv_revive_properties_init(mock_host):
    props = PVPropertiesReviveProperties(mock_host)
    assert props.host == mock_host
    assert props.id_num == 0


def test_pv_revive_properties_host_name(mock_host):
    props = PVPropertiesReviveProperties(mock_host)
    assert props.host_name == "Test PvProperties"

    props_no_host = PVPropertiesReviveProperties()
    assert props_no_host.host_name == "No Host"


def test_pv_revive_properties_duplicate(mock_host):
    props = PVPropertiesReviveProperties(mock_host)
    props.id_num = 5

    new_host = Mock(display_name="Test PvProperties")
    new_props = props.duplicate(new_host)
    assert new_props.host == new_host
    assert new_props.id_num == 5


def test_pv_revive_properties_to_dict(mock_host):
    props = PVPropertiesReviveProperties(mock_host)
    props.id_num = 5

    expected_dict = {
        "revive": {
            "type": "PVPropertiesReviveProperties",
            "id_num": 5,
            "cost": 0.0,
            "labor_fraction": 0.0,
            "lifetime_years": 0,
        }
    }
    assert props.to_dict() == expected_dict

    expected_abridged_dict = {
        "revive": {
            "type": "PVPropertiesRevivePropertiesAbridged",
            "id_num": 5,
            "cost": 0.0,
            "labor_fraction": 0.0,
            "lifetime_years": 0,
        }
    }
    assert props.to_dict(abridged=True) == expected_abridged_dict


def test_pv_revive_properties_from_dict(mock_host):
    input_dict = {
        "type": "PVPropertiesReviveProperties",
        "id_num": 5,
        "cost": 0.0,
        "labor_fraction": 0.0,
        "lifetime_years": 0,
    }
    props = PVPropertiesReviveProperties.from_dict(input_dict, mock_host)
    assert props.host == mock_host
    assert props.id_num == 5

    with pytest.raises(PVPropertiesReviveProperties_FromDictError):
        invalid_dict = {"type": "InvalidType", "id_num": 5}
        PVPropertiesReviveProperties.from_dict(invalid_dict, mock_host)


def test_pv_revive_properties_str_repr(mock_host):
    props = PVPropertiesReviveProperties(mock_host)
    expected_str = "HBE-PVPropertiesRevive Phius REVIVE Property: [host: Test PvProperties]"
    assert str(props) == expected_str
    assert repr(props) == expected_str
