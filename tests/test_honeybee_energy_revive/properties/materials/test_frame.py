from ph_units.unit_type import Unit
from pytest import raises

from honeybee_energy_revive.properties.materials.frame import (
    EnergyWindowFrameReviveProperties,
    EnergyWindowFrameReviveProperties_FromDictError,
)

# --  EnergyWindowFrameReviveProperties --


def test_default_EnergyWindowFrameReviveProperties():
    p = EnergyWindowFrameReviveProperties()
    assert p


def test_default_EnergyWindowFrameReviveProperties_dict_roundtrip():
    p1 = EnergyWindowFrameReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowFrameReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowFrameReviveProperties_dict_roundtrip():
    p1 = EnergyWindowFrameReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowFrameReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowFrameReviveProperties_FromDictError():
    with raises(EnergyWindowFrameReviveProperties_FromDictError):
        EnergyWindowFrameReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowFrameReviveProperties():
    p1 = EnergyWindowFrameReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2
