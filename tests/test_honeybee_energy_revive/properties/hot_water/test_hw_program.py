import pytest
from unittest.mock import Mock

from honeybee_energy_revive.properties.hot_water.hw_program import (
    ServiceHotWaterReviveProperties,
    ServiceHotWaterReviveProperties_FromDictError,
)


@pytest.fixture
def mock_host():
    mock = Mock()
    mock.display_name = "Mock SHW Host"
    return mock


def test_service_hot_water_revive_properties_init(mock_host):
    props = ServiceHotWaterReviveProperties(mock_host)
    assert props.host == mock_host
    assert props.id_num == 0


def test_service_hot_water_revive_properties_host_name(mock_host):
    props = ServiceHotWaterReviveProperties(mock_host)
    assert props.host_name == "Mock"

    props_no_host = ServiceHotWaterReviveProperties(None)
    assert props_no_host.host_name == "No Host"


def test_service_hot_water_revive_properties_duplicate(mock_host):
    props = ServiceHotWaterReviveProperties(mock_host)
    props.id_num = 42

    duplicated_props = props.duplicate(mock_host)
    assert duplicated_props.host == mock_host
    assert duplicated_props.id_num == 42


def test_service_hot_water_revive_properties_to_dict(mock_host):
    props = ServiceHotWaterReviveProperties(mock_host)
    props.id_num = 42

    expected_dict = {"revive": {"type": "ServiceHotWaterReviveProperties", "id_num": 42}}
    assert props.to_dict() == expected_dict

    expected_abridged_dict = {"revive": {"type": "ServiceHotWaterRevivePropertiesAbridged", "id_num": 42}}
    assert props.to_dict(abridged=True) == expected_abridged_dict


def test_service_hot_water_revive_properties_from_dict(mock_host):
    input_dict = {"type": "ServiceHotWaterReviveProperties", "id_num": 42}

    props = ServiceHotWaterReviveProperties.from_dict(input_dict, mock_host)
    assert props.host == mock_host
    assert props.id_num == 42

    with pytest.raises(ServiceHotWaterReviveProperties_FromDictError):
        invalid_dict = {"type": "InvalidType", "id_num": 42}
        ServiceHotWaterReviveProperties.from_dict(invalid_dict, mock_host)


def test_service_hot_water_revive_properties_str_repr(mock_host):
    props = ServiceHotWaterReviveProperties(mock_host)
    expected_str = "HBE-ServiceHotWaterProperties Phius REVIVE Property: [host: Mock]"
    assert str(props) == expected_str
    assert repr(props) == expected_str
    assert props.ToString() == expected_str


def test_service_hot_water_revive_properties_copy(mock_host):
    props = ServiceHotWaterReviveProperties(mock_host)
    props.id_num = 42

    copied_props = props.__copy__()
    assert copied_props.host == mock_host
    assert copied_props.id_num == 42


def test_service_hot_water_revive_properties_to_dict_empty(mock_host):
    props = ServiceHotWaterReviveProperties(mock_host)
    expected_dict = {"revive": {"type": "ServiceHotWaterReviveProperties", "id_num": 0}}
    assert props.to_dict() == expected_dict


def test_service_hot_water_revive_properties_from_dict_abridged(mock_host):
    input_dict = {"type": "ServiceHotWaterRevivePropertiesAbridged", "id_num": 42}

    props = ServiceHotWaterReviveProperties.from_dict(input_dict, mock_host)
    assert props.host == mock_host
    assert props.id_num == 42
