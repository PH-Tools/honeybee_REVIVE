from unittest.mock import Mock

import pytest

from honeybee_energy_revive.properties.load.equipment import (
    ElectricEquipmentReviveProperties,
    ElectricEquipmentReviveProperties_FromDictError,
)


@pytest.fixture
def mock_host():
    mock = Mock()
    mock.display_name = "Mock Electric Equipment Host"
    return mock


def test_initialization(mock_host):
    prop = ElectricEquipmentReviveProperties(mock_host)
    assert prop.host == mock_host
    assert prop.id_num == 0


def test_host_name(mock_host):
    prop = ElectricEquipmentReviveProperties(mock_host)
    assert prop.host_name == "Mock Electric Equipment Host"

    prop_no_host = ElectricEquipmentReviveProperties()
    assert prop_no_host.host_name == "No Host"


def test_duplicate(mock_host):
    prop = ElectricEquipmentReviveProperties(mock_host)
    prop.id_num = 5
    new_prop = prop.duplicate()
    assert prop is not new_prop
    assert prop.to_dict() == new_prop.to_dict()
    assert new_prop.host == mock_host
    assert new_prop.id_num == 5


def test_to_dict(mock_host):
    prop = ElectricEquipmentReviveProperties(mock_host)
    prop.id_num = 5
    d = prop.to_dict()
    assert d == {"revive": {"type": "ElectricEquipmentReviveProperties", "id_num": 5}}

    d_abridged = prop.to_dict(abridged=True)
    assert d_abridged == {"revive": {"type": "ElectricEquipmentRevivePropertiesAbridged", "id_num": 5}}


def test_from_dict(mock_host):
    input_dict = {"type": "ElectricEquipmentReviveProperties", "id_num": 5}
    prop = ElectricEquipmentReviveProperties.from_dict(input_dict, mock_host)
    assert prop.host == mock_host
    assert prop.id_num == 5

    input_dict_invalid = {"type": "InvalidType", "id_num": 5}
    with pytest.raises(ElectricEquipmentReviveProperties_FromDictError):
        ElectricEquipmentReviveProperties.from_dict(input_dict_invalid, mock_host)


def test_str_repr(mock_host):
    prop = ElectricEquipmentReviveProperties(mock_host)
    assert str(prop) == repr(prop)
    assert str(prop) == "HBE-ElectricEquipment Phius REVIVE Property: [host: Mock Electric Equipment Host]"

    prop_no_host = ElectricEquipmentReviveProperties()
    assert str(prop_no_host) == repr(prop_no_host)
    assert str(prop_no_host) == "HBE-ElectricEquipment Phius REVIVE Property: [host: No Host]"


def test_ToString(mock_host):
    prop = ElectricEquipmentReviveProperties(mock_host)
    assert prop.ToString() == str(prop)
