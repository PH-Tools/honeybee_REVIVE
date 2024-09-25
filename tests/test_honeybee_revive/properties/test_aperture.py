from unittest.mock import Mock

import pytest

from honeybee_revive.properties.aperture import ApertureReviveProperties


@pytest.fixture
def mock_host():
    mock = Mock()
    mock.display_name = "Test Aperture"
    return mock


def test_aperture_revive_properties_initialization(mock_host):
    properties = ApertureReviveProperties(mock_host)
    assert properties.host == mock_host
    assert properties.id_num == 0


def test_aperture_revive_properties_host_name(mock_host):
    properties = ApertureReviveProperties(mock_host)
    assert properties.host_name == "Test Aperture"

    properties_no_host = ApertureReviveProperties(None)
    assert properties_no_host.host_name == "No Host"


def test_aperture_revive_properties_duplicate(mock_host):
    properties = ApertureReviveProperties(mock_host)
    properties.id_num = 5

    duplicated_properties = properties.duplicate(mock_host)
    assert duplicated_properties.host == mock_host
    assert duplicated_properties.id_num == 5

    duplicated_properties_same_host = properties.duplicate()
    assert duplicated_properties_same_host.host == mock_host
    assert duplicated_properties_same_host.id_num == 5


def test_aperture_revive_properties_to_string(mock_host):
    properties = ApertureReviveProperties(mock_host)
    assert properties.ToString() == "HB-Aperture Phius REVIVE Property: [host: Test Aperture]"


def test_aperture_revive_properties_to_dict(mock_host):
    properties = ApertureReviveProperties(mock_host)
    properties.id_num = 10
    expected_dict = {"revive": {"type": "ApertureReviveProperties", "id_num": 10}}
    assert properties.to_dict() == expected_dict


def test_aperture_revive_properties_from_dict(mock_host):
    input_dict = {"type": "ApertureReviveProperties", "id_num": 15}
    properties = ApertureReviveProperties.from_dict(input_dict, mock_host)
    assert properties.host == mock_host
    assert properties.id_num == 15


def test_aperture_revive_properties_apply_properties_from_dict(mock_host):
    properties = ApertureReviveProperties(mock_host)
    properties.id_num = 20

    input_dict = {"type": "ApertureReviveProperties", "id_num": 25}
    properties.apply_properties_from_dict(input_dict)
    assert properties.id_num == 20  # apply_properties_from_dict does nothing in current implementation
