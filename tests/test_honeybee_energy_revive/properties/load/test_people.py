from unittest.mock import Mock

import pytest

from honeybee_energy_revive.properties.load.people import PeopleReviveProperties, PeopleReviveProperties_FromDictError


@pytest.fixture
def mock_host():
    mock = Mock()
    mock.display_name = "Mock People Host"
    return mock


def test_people_revive_properties_initialization(mock_host):
    prop = PeopleReviveProperties(mock_host)
    assert prop.host == mock_host
    assert prop.id_num == 0


def test_people_revive_properties_host_name(mock_host):
    prop = PeopleReviveProperties(mock_host)
    assert prop.host_name == "Mock People Host"

    prop_no_host = PeopleReviveProperties()
    assert prop_no_host.host_name == "No Host"


def test_people_revive_properties_duplicate(mock_host):
    prop = PeopleReviveProperties(mock_host)
    prop.id_num = 5

    duplicated_prop = prop.duplicate(mock_host)
    assert duplicated_prop.host == mock_host
    assert duplicated_prop.id_num == 5


def test_people_revive_properties_to_dict(mock_host):
    prop = PeopleReviveProperties(mock_host)
    prop.id_num = 5

    dict_full = prop.to_dict()
    assert dict_full == {"revive": {"type": "PeopleReviveProperties", "id_num": 5}}

    dict_abridged = prop.to_dict(abridged=True)
    assert dict_abridged == {"revive": {"type": "PeopleRevivePropertiesAbridged", "id_num": 5}}


def test_people_revive_properties_from_dict(mock_host):
    input_dict = {"type": "PeopleReviveProperties", "id_num": 5}
    prop = PeopleReviveProperties.from_dict(input_dict, mock_host)
    assert prop.host == mock_host
    assert prop.id_num == 5

    input_dict_abridged = {"type": "PeopleRevivePropertiesAbridged", "id_num": 5}
    prop_abridged = PeopleReviveProperties.from_dict(input_dict_abridged, mock_host)
    assert prop_abridged.host == mock_host
    assert prop_abridged.id_num == 5


def test_people_revive_properties_from_dict_invalid_type(mock_host):
    input_dict = {"type": "InvalidType", "id_num": 5}
    with pytest.raises(PeopleReviveProperties_FromDictError):
        PeopleReviveProperties.from_dict(input_dict, mock_host)


def test_people_revive_properties_str_repr(mock_host):
    prop = PeopleReviveProperties(mock_host)
    assert str(prop) == "HBE-People Phius REVIVE Property: [host: Mock People Host]"
    assert repr(prop) == "HBE-People Phius REVIVE Property: [host: Mock People Host]"


def test_people_revive_properties_to_string(mock_host):
    prop = PeopleReviveProperties(mock_host)
    assert prop.ToString() == "HBE-People Phius REVIVE Property: [host: Mock People Host]"
