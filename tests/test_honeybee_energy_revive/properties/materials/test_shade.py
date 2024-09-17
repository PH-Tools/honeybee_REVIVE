from ph_units.unit_type import Unit
from pytest import raises
from honeybee_energy_revive.properties.materials.shade import (
    EnergyWindowMaterialShadeReviveProperties_FromDictError,
    EnergyWindowMaterialShadeReviveProperties,
    EnergyWindowMaterialBlindReviveProperties,
)

# --  EnergyWindowMaterialShadeReviveProperties --


def test_default_EnergyWindowMaterialShadeReviveProperties():
    p = EnergyWindowMaterialShadeReviveProperties()
    assert p


def test_default_EnergyWindowMaterialShadeReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialShadeReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialShadeReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowMaterialShadeReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialShadeReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialShadeReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowMaterialShadeReviveProperties_FromDictError():
    with raises(EnergyWindowMaterialShadeReviveProperties_FromDictError):
        EnergyWindowMaterialShadeReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowMaterialShadeReviveProperties():
    p1 = EnergyWindowMaterialShadeReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2


# -- EnergyWindowMaterialBlindReviveProperties --


def test_default_EnergyWindowMaterialBlindReviveProperties():
    p = EnergyWindowMaterialBlindReviveProperties()
    assert p


def test_default_EnergyWindowMaterialBlindReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialBlindReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialBlindReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowMaterialBlindReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialBlindReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialBlindReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowMaterialBlindReviveProperties_FromDictError():
    with raises(EnergyWindowMaterialShadeReviveProperties_FromDictError):
        EnergyWindowMaterialBlindReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowMaterialBlindReviveProperties():
    p1 = EnergyWindowMaterialBlindReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2
