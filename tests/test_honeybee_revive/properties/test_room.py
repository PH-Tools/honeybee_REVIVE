import pytest
from unittest.mock import Mock
from honeybee_revive.properties.room import RoomReviveProperties


@pytest.fixture
def mock_host():
    mock = Mock()
    mock.display_name = "Test Room"
    return mock


@pytest.fixture
def room_properties(mock_host):
    return RoomReviveProperties(mock_host)


def test_room_properties_initialization(room_properties, mock_host):
    assert room_properties.host == mock_host
    assert room_properties.id_num == 0


def test_host_name(room_properties):
    assert room_properties.host_name == "Test Room"


def test_host_name_no_host():
    room_properties = RoomReviveProperties(None)
    assert room_properties.host_name == "No Host"


def test_duplicate(room_properties, mock_host):
    new_properties = room_properties.duplicate()
    assert new_properties.host == mock_host
    assert new_properties.id_num == room_properties.id_num


def test_duplicate_with_new_host(mock_host):
    room_properties = RoomReviveProperties(mock_host)
    new_properties = room_properties.duplicate(mock_host)
    assert new_properties.host == mock_host
    assert new_properties.id_num == room_properties.id_num


def test_to_dict(room_properties):
    expected_dict = {"revive": {"type": "RoomReviveProperties", "id_num": 0}}
    assert room_properties.to_dict() == expected_dict


def test_to_dict_abridged(room_properties):
    expected_dict = {"revive": {"type": "RoomRevivePropertiesAbridged"}}
    assert room_properties.to_dict(abridged=True) == expected_dict


def test_from_dict(mock_host):
    input_dict = {"type": "RoomReviveProperties", "id_num": 1}
    new_properties = RoomReviveProperties.from_dict(input_dict, mock_host)
    assert new_properties.host == mock_host
    assert new_properties.id_num == 1


def test_apply_properties_from_dict(room_properties):
    room_properties.apply_properties_from_dict({})
    assert room_properties.id_num == 0  # No change expected


def test_repr(room_properties):
    assert repr(room_properties) == "HB-Room Phius REVIVE Property: [host: Test Room]"


def test_str(room_properties):
    assert str(room_properties) == "HB-Room Phius REVIVE Property: [host: Test Room]"
