import pytest
from unittest.mock import Mock

from honeybee_energy_revive.properties.construction.window import (
    WindowConstructionReviveProperties,
    WindowConstructionReviveProperties_FromDictError,
)


@pytest.fixture
def mock_host():
    return Mock(display_name="Test Window")


def test_window_construction_revive_properties_init(mock_host):
    props = WindowConstructionReviveProperties(mock_host)
    assert props.host == mock_host
    assert props.id_num == 0


def test_window_construction_revive_properties_host_name(mock_host):
    props = WindowConstructionReviveProperties(mock_host)
    assert props.host_name == "Test Window"

    props_no_host = WindowConstructionReviveProperties()
    assert props_no_host.host_name == "No Host"


def test_window_construction_revive_properties_duplicate(mock_host):
    props = WindowConstructionReviveProperties(mock_host)
    props.id_num = 123

    new_host = Mock(display_name="New Test Window")
    duplicated_props = props.duplicate(new_host)
    assert duplicated_props.host == new_host
    assert duplicated_props.id_num == 123


def test_window_construction_revive_properties_to_dict(mock_host):
    props = WindowConstructionReviveProperties(mock_host)
    props.id_num = 123

    expected_dict = {"revive": {"type": "WindowConstructionReviveProperties", "id_num": 123}}
    assert props.to_dict() == expected_dict

    expected_abridged_dict = {"revive": {"type": "WindowConstructionRevivePropertiesAbridged", "id_num": 123}}
    assert props.to_dict(abridged=True) == expected_abridged_dict


def test_window_construction_revive_properties_from_dict(mock_host):
    input_dict = {"type": "WindowConstructionReviveProperties", "id_num": 123}
    props = WindowConstructionReviveProperties.from_dict(input_dict, mock_host)
    assert props.host == mock_host
    assert props.id_num == 123

    input_dict_invalid = {"type": "InvalidType", "id_num": 123}
    with pytest.raises(WindowConstructionReviveProperties_FromDictError):
        WindowConstructionReviveProperties.from_dict(input_dict_invalid, mock_host)


def test_window_construction_revive_properties_str_repr(mock_host):
    props = WindowConstructionReviveProperties(mock_host)
    expected_str = "HBE-WindowConstruction Phius REVIVE Property: [host: Test Window]"
    assert str(props) == expected_str
    assert repr(props) == expected_str


def test_window_construction_revive_properties_to_string(mock_host):
    props = WindowConstructionReviveProperties(mock_host)
    expected_str = "HBE-WindowConstruction Phius REVIVE Property: [host: Test Window]"
    assert props.ToString() == expected_str
