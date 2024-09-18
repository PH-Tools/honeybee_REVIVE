import pytest
from honeybee_revive.properties.space import SpaceReviveProperties


class MockSpace:
    def __init__(self, display_name):
        self.display_name = display_name
        self.properties = self


@pytest.fixture
def mock_space():
    return MockSpace("Mock Space")


@pytest.fixture
def space_revive_properties(mock_space):
    return SpaceReviveProperties(mock_space)


def test_host(space_revive_properties, mock_space):
    assert space_revive_properties.host == mock_space


def test_host_name(space_revive_properties):
    assert space_revive_properties.host_name == "Mock Space"


def test_host_name_no_host():
    prop = SpaceReviveProperties(None)
    assert prop.host_name == "No Host"


def test_duplicate(space_revive_properties, mock_space):
    new_host = MockSpace("New Mock Space")
    duplicate_prop = space_revive_properties.duplicate(new_host)
    assert duplicate_prop.host == new_host
    assert duplicate_prop.host_name == "New Mock Space"


def test_copy(space_revive_properties):
    copied_prop = space_revive_properties.__copy__()
    assert copied_prop.host == space_revive_properties.host


def test_repr(space_revive_properties):
    assert repr(space_revive_properties) == "HBPH-Space Phius REVIVE Properties: [host: Mock Space]"


def test_to_string(space_revive_properties):
    assert space_revive_properties.ToString() == "HBPH-Space Phius REVIVE Properties: [host: Mock Space]"


def test_to_dict(space_revive_properties):
    expected_dict = {"revive": {"type": "SpaceReviveProperties"}}
    assert space_revive_properties.to_dict() == expected_dict


def test_to_dict_abridged(space_revive_properties):
    expected_dict = {"revive": {"type": "SpaceRevivePropertiesAbridged"}}
    assert space_revive_properties.to_dict(abridged=True) == expected_dict


def test_from_dict(mock_space):
    data = {"type": "SpaceReviveProperties"}
    prop = SpaceReviveProperties.from_dict(data, mock_space)
    assert prop.host == mock_space
