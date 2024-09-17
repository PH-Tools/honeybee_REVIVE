from ph_units.unit_type import Unit
from pytest import raises
from honeybee_energy_revive.properties.materials.glazing import (
    EnergyWindowMaterialGlazingReviveProperties,
    EnergyWindowMaterialSimpleGlazSysReviveProperties,
    EnergyWindowMaterialGlazingReviveProperties_FromDictError,
)

# -- EnergyWindowMaterialGlazingReviveProperties --


def test_default_EnergyWindowMaterialGlazingReviveProperties():
    p = EnergyWindowMaterialGlazingReviveProperties()
    assert p


def test_default_EnergyWindowMaterialGlazingReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGlazingReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGlazingReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowMaterialGlazingReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGlazingReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGlazingReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowMaterialGlazingReviveProperties_FromDictError():
    with raises(EnergyWindowMaterialGlazingReviveProperties_FromDictError):
        EnergyWindowMaterialGlazingReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowMaterialGlazingReviveProperties():
    p1 = EnergyWindowMaterialGlazingReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2


# --- EnergyWindowMaterialSimpleGlazSysReviveProperties ---


def test_default_EnergyWindowMaterialSimpleGlazSysReviveProperties():
    p = EnergyWindowMaterialSimpleGlazSysReviveProperties()
    assert p


def test_default_EnergyWindowMaterialSimpleGlazSysReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialSimpleGlazSysReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialSimpleGlazSysReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowMaterialSimpleGlazSysReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialSimpleGlazSysReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialSimpleGlazSysReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowMaterialSimpleGlazSysReviveProperties_FromDictError():
    with raises(EnergyWindowMaterialGlazingReviveProperties_FromDictError):
        EnergyWindowMaterialSimpleGlazSysReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowMaterialSimpleGlazSysReviveProperties():
    p1 = EnergyWindowMaterialSimpleGlazSysReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2
