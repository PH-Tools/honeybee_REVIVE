from ph_units.unit_type import Unit
from pytest import raises
from honeybee_energy_revive.properties.materials.gas import (
    EnergyWindowMaterialGasReviveProperties_FromDictError,
    EnergyWindowMaterialGasReviveProperties,
    EnergyWindowMaterialGasMixtureReviveProperties,
    EnergyWindowMaterialGasCustomReviveProperties,
)

# --  EnergyWindowMaterialGasReviveProperties --


def test_default_EnergyWindowMaterialGasReviveProperties():
    p = EnergyWindowMaterialGasReviveProperties()
    assert p


def test_default_EnergyWindowMaterialGasReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGasReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGasReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowMaterialGasReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGasReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGasReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowMaterialGasReviveProperties_FromDictError():
    with raises(EnergyWindowMaterialGasReviveProperties_FromDictError):
        EnergyWindowMaterialGasReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowMaterialGasReviveProperties():
    p1 = EnergyWindowMaterialGasReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2


# -- EnergyWindowMaterialGasMixtureReviveProperties --


def test_default_EnergyWindowMaterialGasMixtureReviveProperties():
    p = EnergyWindowMaterialGasMixtureReviveProperties()
    assert p


def test_default_EnergyWindowMaterialGasMixtureReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGasMixtureReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGasMixtureReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowMaterialGasMixtureReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGasMixtureReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGasMixtureReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowMaterialGasMixtureReviveProperties_FromDictError():
    with raises(EnergyWindowMaterialGasReviveProperties_FromDictError):
        EnergyWindowMaterialGasMixtureReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowMaterialGasMixtureReviveProperties():
    p1 = EnergyWindowMaterialGasMixtureReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2


# -- EnergyWindowMaterialGasCustomReviveProperties --


def test_default_EnergyWindowMaterialGasCustomReviveProperties():
    p = EnergyWindowMaterialGasCustomReviveProperties()
    assert p


def test_default_EnergyWindowMaterialGasCustomReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGasCustomReviveProperties()
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGasCustomReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_customized_EnergyWindowMaterialGasCustomReviveProperties_dict_roundtrip():
    p1 = EnergyWindowMaterialGasCustomReviveProperties()
    p1.kg_CO2_per_m2 = Unit(24, "KG/M2")
    p1.cost_per_m2 = Unit(24, "COST/M2")
    p1.labor_fraction = 0.6
    p1.lifetime_years = 34
    d1 = p1.to_dict()
    p2 = EnergyWindowMaterialGasCustomReviveProperties.from_dict(d1["revive"], _host=None)
    assert d1 == p2.to_dict()


def test_bad_dict_raises_EnergyWindowMaterialGasCustomReviveProperties_FromDictError():
    with raises(EnergyWindowMaterialGasReviveProperties_FromDictError):
        EnergyWindowMaterialGasCustomReviveProperties.from_dict({"type": "wrong_type"}, _host=None)


def test_duplicate_EnergyWindowMaterialGasCustomReviveProperties():
    p1 = EnergyWindowMaterialGasCustomReviveProperties()
    p2 = p1.duplicate()
    assert p1.to_dict() == p2.to_dict()
    assert p1 is not p2
