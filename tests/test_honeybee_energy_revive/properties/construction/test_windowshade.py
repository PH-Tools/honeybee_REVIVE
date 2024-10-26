from unittest.mock import Mock

import pytest

from honeybee_energy_revive.properties.construction.windowshade import (
    WindowConstructionShadeReviveProperties,
    WindowConstructionShadeReviveProperties_FromDictError,
)


@pytest.fixture
def mock_host():
    return Mock(display_name="Test Shade")


def test_shade_construction_revive_properties_init(mock_host):
    props = WindowConstructionShadeReviveProperties(mock_host)
    assert props.host == mock_host
    assert props.id_num == 0


def test_shade_construction_revive_properties_host_name(mock_host):
    props = WindowConstructionShadeReviveProperties(mock_host)
    assert props.host_name == "Test Shade"

    props_no_host = WindowConstructionShadeReviveProperties()
    assert props_no_host.host_name == "No Host"


def test_shade_construction_revive_properties_duplicate(mock_host):
    props = WindowConstructionShadeReviveProperties(mock_host)
    props.id_num = 5

    new_host = Mock(display_name="New Test Shade")
    new_props = props.duplicate(new_host)
    assert new_props.host == new_host
    assert new_props.id_num == 5


def test_shade_construction_revive_properties_to_dict(mock_host):
    props = WindowConstructionShadeReviveProperties(mock_host)
    props.id_num = 5

    expected_dict = {"revive": {"type": "WindowConstructionShadeReviveProperties", "id_num": 5}}
    assert props.to_dict() == expected_dict

    expected_abridged_dict = {"revive": {"type": "WindowConstructionShadeRevivePropertiesAbridged", "id_num": 5}}
    assert props.to_dict(abridged=True) == expected_abridged_dict


def test_shade_construction_revive_properties_from_dict(mock_host):
    input_dict = {"type": "WindowConstructionShadeReviveProperties", "id_num": 5}
    props = WindowConstructionShadeReviveProperties.from_dict(input_dict, mock_host)
    assert props.host == mock_host
    assert props.id_num == 5

    with pytest.raises(WindowConstructionShadeReviveProperties_FromDictError):
        invalid_dict = {"type": "InvalidType", "id_num": 5}
        WindowConstructionShadeReviveProperties.from_dict(invalid_dict, mock_host)


def test_shade_construction_revive_dict_round_trip(mock_host):
    props = WindowConstructionShadeReviveProperties(mock_host)
    props.id_num = 5

    props_dict = props.to_dict()
    new_props = WindowConstructionShadeReviveProperties.from_dict(props_dict["revive"], mock_host)
    assert new_props.host == mock_host
    assert new_props.id_num == 5


def test_shade_construction_revive_properties_str_repr(mock_host):
    props = WindowConstructionShadeReviveProperties(mock_host)
    expected_str = "HBE-WindowConstructionShade Phius REVIVE Property: [host: Test Shade]"
    assert str(props) == expected_str
    assert repr(props) == expected_str
