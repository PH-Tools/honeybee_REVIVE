import pytest

from honeybee_energy.schedule.ruleset import ScheduleRuleset
from honeybee_energy.load.process import Process
from honeybee_energy_revive.properties.load.process import (
    ProcessReviveProperties,
    ProcessReviveProperties_FromDictError,
)


@pytest.fixture
def HBE_Process():
    hbe_process_object = Process(
        identifier="Mock Process Host",
        watts=0.0,
        schedule=ScheduleRuleset.from_constant_value("schedule", 1),
        fuel_type="Electricity",
    )
    return hbe_process_object


def test_initialization(HBE_Process):
    prop = ProcessReviveProperties(HBE_Process)
    assert prop.host == HBE_Process
    assert prop.id_num == 0


def test_host_name(HBE_Process):
    prop = ProcessReviveProperties(HBE_Process)
    assert prop.host_name == "Mock Process Host"

    prop_no_host = ProcessReviveProperties()
    assert prop_no_host.host_name == "No Host"


def test_duplicate(HBE_Process):
    prop = ProcessReviveProperties(HBE_Process)
    prop.id_num = 5
    new_prop = prop.duplicate()
    assert prop is not new_prop
    assert prop.to_dict() == new_prop.to_dict()
    assert new_prop.host == HBE_Process
    assert new_prop.id_num == 5


def test_to_dict(HBE_Process):
    prop = ProcessReviveProperties(HBE_Process)
    prop.id_num = 5
    d = prop.to_dict()
    assert d == {
        "revive": {
            "type": "ProcessReviveProperties",
            "id_num": 5,
            "cost": 0.0,
            "labor_fraction": 0.4,
            "lifetime_years": 25,
        }
    }

    d_abridged = prop.to_dict(abridged=True)
    assert d_abridged == {
        "revive": {
            "type": "ProcessRevivePropertiesAbridged",
            "id_num": 5,
            "cost": 0.0,
            "labor_fraction": 0.4,
            "lifetime_years": 25,
        }
    }


def test_from_dict(HBE_Process):
    input_dict = {
        "type": "ProcessReviveProperties",
        "id_num": 5,
        "cost": 100,
        "labor_fraction": 0.5,
        "lifetime_years": 20,
    }
    prop = ProcessReviveProperties.from_dict(input_dict, HBE_Process)
    assert prop.host == HBE_Process
    assert prop.id_num == 5

    input_dict_invalid = {"type": "InvalidType", "id_num": 5}
    with pytest.raises(ProcessReviveProperties_FromDictError):
        ProcessReviveProperties.from_dict(input_dict_invalid, HBE_Process)


def test_str_repr(HBE_Process):
    prop = ProcessReviveProperties(HBE_Process)
    assert str(prop) == repr(prop)
    assert str(prop) == "HBE-Process Phius REVIVE Property: [host: Mock Process Host]"

    prop_no_host = ProcessReviveProperties()
    assert str(prop_no_host) == repr(prop_no_host)
    assert str(prop_no_host) == "HBE-Process Phius REVIVE Property: [host: No Host]"


def test_ToString(HBE_Process):
    prop = ProcessReviveProperties(HBE_Process)
    assert prop.ToString() == str(prop)
