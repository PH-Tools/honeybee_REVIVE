import pytest
from unittest.mock import Mock
from honeybee_revive.properties.face import FaceReviveProperties


@pytest.fixture
def mock_host():
    mock = Mock()
    mock.display_name = "Test Face"
    return mock


def test_face_revive_properties_initialization(mock_host):
    properties = FaceReviveProperties(mock_host)
    assert properties.host == mock_host
    assert properties.id_num == 0


def test_face_revive_properties_host_name(mock_host):
    properties = FaceReviveProperties(mock_host)
    assert properties.host_name == "Test Face"


def test_face_revive_properties_host_name_no_host():
    properties = FaceReviveProperties(None)
    assert properties.host_name == "No Host"


def test_face_revive_properties_duplicate(mock_host):
    properties = FaceReviveProperties(mock_host)
    properties.id_num = 5
    new_properties = properties.duplicate()
    assert new_properties.host == mock_host
    assert new_properties.id_num == 5


def test_face_revive_properties_to_dict(mock_host):
    properties = FaceReviveProperties(mock_host)
    properties.id_num = 5
    expected_dict = {"revive": {"type": "FaceReviveProperties", "id_num": 5}}
    assert properties.to_dict() == expected_dict


def test_face_revive_properties_from_dict(mock_host):
    data = {"type": "FaceReviveProperties", "id_num": 5}
    properties = FaceReviveProperties.from_dict(data, mock_host)
    assert properties.host == mock_host
    assert properties.id_num == 5


def test_face_revive_properties_apply_properties_from_dict(mock_host):
    properties = FaceReviveProperties(mock_host)
    properties.apply_properties_from_dict({})
    assert properties.id_num == 0  # Since apply_properties_from_dict does nothing in this case


def test_face_revive_properties_repr(mock_host):
    properties = FaceReviveProperties(mock_host)
    assert repr(properties) == "HB-Face Phius REVIVE Property: [host: Test Face]"


def test_face_revive_properties_str(mock_host):
    properties = FaceReviveProperties(mock_host)
    assert str(properties) == "HB-Face Phius REVIVE Property: [host: Test Face]"
