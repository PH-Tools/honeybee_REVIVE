import pytest
from unittest.mock import Mock

from honeybee_energy_revive.properties.ruleset import (
    ScheduleRulesetReviveProperties,
    ScheduleRulesetReviveProperties_FromDictError,
)


@pytest.fixture
def mock_host():
    return Mock()


def test_initialization():
    obj = ScheduleRulesetReviveProperties()
    assert obj.host is None
    assert obj.id_num == 0


def test_initialization_with_host(mock_host):
    obj = ScheduleRulesetReviveProperties(mock_host)
    assert obj.host == mock_host
    assert obj.id_num == 0


def test_host_name(mock_host):
    obj = ScheduleRulesetReviveProperties()
    assert obj.host_name == "No Host"

    mock_host.display_name = "Mock Host"
    obj_with_host = ScheduleRulesetReviveProperties(mock_host)
    assert obj_with_host.host_name == "Mock Host"


def test_duplicate(mock_host):
    obj = ScheduleRulesetReviveProperties(mock_host)
    obj.id_num = 5
    duplicate_obj = obj.duplicate()

    assert duplicate_obj.host == mock_host
    assert duplicate_obj.id_num == 5


def test_to_dict():
    obj = ScheduleRulesetReviveProperties()
    obj.id_num = 5
    dict_repr = obj.to_dict()
    assert dict_repr == {"revive": {"type": "ScheduleRulesetReviveProperties", "id_num": 5}}

    abridged_dict_repr = obj.to_dict(abridged=True)
    assert abridged_dict_repr == {"revive": {"type": "ScheduleRulesetRevivePropertiesAbridged", "id_num": 5}}


def test_from_dict(mock_host):
    input_dict = {"type": "ScheduleRulesetReviveProperties", "id_num": 5}
    obj = ScheduleRulesetReviveProperties.from_dict(input_dict, mock_host)

    assert obj.host == mock_host
    assert obj.id_num == 5


def test_from_dict_invalid_type():
    input_dict = {"type": "InvalidType", "id_num": 5}
    with pytest.raises(ScheduleRulesetReviveProperties_FromDictError):
        ScheduleRulesetReviveProperties.from_dict(input_dict, None)


def test_str_repr(mock_host):
    mock_host.display_name = "Mock Host"
    obj = ScheduleRulesetReviveProperties(mock_host)
    assert str(obj) == "HBE-ScheduleRuleset Phius REVIVE Property: [host: Mock Host]"
    assert repr(obj) == "HBE-ScheduleRuleset Phius REVIVE Property: [host: Mock Host]"


def test_copy(mock_host):
    obj = ScheduleRulesetReviveProperties(mock_host)
    obj.id_num = 10
    copied_obj = obj.__copy__()

    assert copied_obj.host == mock_host
    assert copied_obj.id_num == 10


def test_to_dict_with_different_id():
    obj = ScheduleRulesetReviveProperties()
    obj.id_num = 15
    dict_repr = obj.to_dict()
    assert dict_repr == {"revive": {"type": "ScheduleRulesetReviveProperties", "id_num": 15}}
