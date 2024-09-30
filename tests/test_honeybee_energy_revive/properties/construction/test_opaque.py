import pytest
from ph_units.unit_type import Unit
from pytest import approx

from honeybee_energy.construction.opaque import OpaqueConstruction
from honeybee_energy.material.opaque import EnergyMaterial, EnergyMaterialNoMass, EnergyMaterialVegetation

from honeybee_energy_revive.properties.construction.opaque import (
    OpaqueConstructionReviveProperties,
    OpaqueConstructionReviveProperties_FromDictError,
)
from honeybee_energy_revive.properties.materials.opaque import (
    EnergyMaterialNoMassReviveProperties,
    EnergyMaterialReviveProperties,
    EnergyMaterialVegetationReviveProperties,
)


@pytest.fixture
def hbe_opaque_construction():
    hb_e_mat_1 = EnergyMaterial("mat_1", 0.1, 1.0, 99, 999)
    rv_prop_1: EnergyMaterialReviveProperties = getattr(hb_e_mat_1.properties, "revive")
    rv_prop_1.kg_CO2_per_m2 = Unit(10.0, "KG/M2")
    rv_prop_1.cost_per_m2 = Unit(10.0, "COST/M2")

    hb_e_mat_2 = EnergyMaterial("mat_2", 0.2, 2.0, 99, 999)
    rv_prop_2: EnergyMaterialReviveProperties = getattr(hb_e_mat_2.properties, "revive")
    rv_prop_2.kg_CO2_per_m2 = Unit(20.0, "KG/M2")
    rv_prop_2.cost_per_m2 = Unit(10.0, "COST/M2")

    materials = [
        hb_e_mat_1,
        hb_e_mat_2,
    ]
    return OpaqueConstruction("Mock Construction", materials)


def test_host(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.host == hbe_opaque_construction


def test_host_name(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.host_name == "Mock Construction"

    prop_no_host = OpaqueConstructionReviveProperties()
    assert prop_no_host.host_name == "No Host"


def test_kg_CO2_per_m2(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.kg_CO2_per_m2.value == 30.0
    assert prop.kg_CO2_per_m2.unit == "KG/M2"

    prop_no_host = OpaqueConstructionReviveProperties()
    assert prop_no_host.kg_CO2_per_m2.value == 0.0
    assert prop_no_host.kg_CO2_per_m2.unit == "KG/M2"


def test_cost_per_m2(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.cost_per_m2.value == 20.0
    assert prop.cost_per_m2.unit == "COST/M2"

    prop_no_host = OpaqueConstructionReviveProperties()
    assert prop_no_host.cost_per_m2.value == 0.0
    assert prop_no_host.cost_per_m2.unit == "COST/M2"


def test_duplicate(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    duplicate_prop = prop.duplicate()
    assert duplicate_prop.host == hbe_opaque_construction
    assert duplicate_prop.id_num == prop.id_num


def test_to_dict(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    prop_dict = prop.to_dict()
    assert prop_dict["revive"]["type"] == "OpaqueConstructionReviveProperties"
    assert prop_dict["revive"]["id_num"] == prop.id_num

    prop_dict_abridged = prop.to_dict(abridged=True)
    assert prop_dict_abridged["revive"]["type"] == "OpaqueConstructionRevivePropertiesAbridged"


def test_from_dict(hbe_opaque_construction):
    input_dict = {"type": "OpaqueConstructionReviveProperties", "id_num": 1}
    prop = OpaqueConstructionReviveProperties.from_dict(input_dict, hbe_opaque_construction)
    assert prop.host == hbe_opaque_construction
    assert prop.id_num == 1

    with pytest.raises(OpaqueConstructionReviveProperties_FromDictError):
        OpaqueConstructionReviveProperties.from_dict({"type": "InvalidType"}, hbe_opaque_construction)


def test_str_repr(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert str(prop) == repr(prop)
    assert str(prop) == "HBE-OpaqueConstruction Phius REVIVE Property: [host: Mock Construction]"


def test_to_string(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.ToString() == str(prop)


def test_total_thickness_no_host(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(None)

    assert prop.total_thickness_m == 0.0


def test_total_thickness(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.total_thickness_m.value == approx(0.30)


def test_construction_labor_fraction(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.labor_fraction == 0.4


def test_construction_lifetime_years(hbe_opaque_construction):
    prop = OpaqueConstructionReviveProperties(hbe_opaque_construction)
    assert prop.lifetime_years == 25
