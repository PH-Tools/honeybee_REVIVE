from ph_units.unit_type import Unit
from pytest import raises

from honeybee_energy_revive.properties.materials.opaque import (
    EnergyMaterialNoMassReviveProperties,
    EnergyMaterialReviveProperties,
    EnergyMaterialReviveProperties_FromDictError,
    EnergyMaterialVegetationReviveProperties,
)

# -- EnergyMaterialReviveProperties --


def test_default_EnergyMaterialReviveProperties():
    p = EnergyMaterialReviveProperties()
    assert p


def test_default_EnergyMaterialReviveProperties_dict_roundtrip():
    p1 = EnergyMaterialReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyMaterialReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyMaterialReviveProperties_dict_roundtrip():
    p1 = EnergyMaterialReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyMaterialReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyMaterialReviveProperties_FromDictError():
    with raises(EnergyMaterialReviveProperties_FromDictError):
        EnergyMaterialReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyMaterialReviveProperties():
    p1 = EnergyMaterialReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2


# --- EnergyMaterialNoMassReviveProperties ---


def test_default_EnergyMaterialNoMassReviveProperties():
    p = EnergyMaterialNoMassReviveProperties()
    assert p


def test_default_EnergyMaterialNoMassReviveProperties_dict_roundtrip():
    p1 = EnergyMaterialNoMassReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyMaterialNoMassReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyMaterialNoMassReviveProperties_dict_roundtrip():
    p1 = EnergyMaterialNoMassReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyMaterialNoMassReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyMaterialNoMassReviveProperties_FromDictError():
    with raises(EnergyMaterialReviveProperties_FromDictError):
        EnergyMaterialNoMassReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyMaterialNoMassReviveProperties():
    p1 = EnergyMaterialNoMassReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2


# --- EnergyMaterialVegetationReviveProperties ---


def test_default_EnergyMaterialVegetationReviveProperties():
    p = EnergyMaterialVegetationReviveProperties()
    assert p


def test_default_EnergyMaterialVegetationReviveProperties_dict_roundtrip():
    p1 = EnergyMaterialVegetationReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyMaterialVegetationReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyMaterialVegetationReviveProperties_dict_roundtrip():
    p1 = EnergyMaterialVegetationReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyMaterialVegetationReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyMaterialVegetationReviveProperties_FromDictError():
    with raises(EnergyMaterialReviveProperties_FromDictError):
        EnergyMaterialVegetationReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyMaterialVegetationReviveProperties():
    p1 = EnergyMaterialVegetationReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2
