import pytest
from honeybee_revive.properties.shade import ShadeReviveProperties


class MockShade:
    def __init__(self, display_name):
        self.display_name = display_name
        self.properties = self


@pytest.fixture
def mock_shade():
    return MockShade("Mock Shade")


@pytest.fixture
def shade_properties(mock_shade):
    return ShadeReviveProperties(mock_shade)


def test_shade_properties_initialization(shade_properties, mock_shade):
    assert shade_properties.host == mock_shade
    assert shade_properties.id_num == 0


def test_shade_properties_host_name(shade_properties, mock_shade):
    assert shade_properties.host_name == "Mock Shade"
    shade_properties._host = None
    assert shade_properties.host_name == "No Host"


def test_shade_properties_duplicate(shade_properties, mock_shade):
    new_mock_shade = MockShade("New Mock Shade")
    duplicate_properties = shade_properties.duplicate(new_mock_shade)
    assert duplicate_properties.host == new_mock_shade
    assert duplicate_properties.id_num == shade_properties.id_num


def test_shade_properties_to_dict(shade_properties):
    properties_dict = shade_properties.to_dict()
    assert properties_dict["revive"]["type"] == "ShadeReviveProperties"
    assert properties_dict["revive"]["id_num"] == shade_properties.id_num


def test_shade_properties_from_dict(mock_shade):
    data = {"type": "ShadeReviveProperties", "id_num": 1}
    new_properties = ShadeReviveProperties.from_dict(data, mock_shade)
    assert new_properties.host == mock_shade
    assert new_properties.id_num == 1


def test_shade_properties_repr(shade_properties):
    assert repr(shade_properties) == "HB-Shade Phius REVIVE Properties: [host: Mock Shade]"


def test_shade_properties_str(shade_properties):
    assert str(shade_properties) == "HB-Shade Phius REVIVE Properties: [host: Mock Shade]"
