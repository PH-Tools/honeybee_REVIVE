import pytest
from ph_units.unit_type import Unit

from honeybee_energy_revive.properties.construction.opaque import (
    OpaqueConstructionReviveProperties,
    OpaqueConstructionReviveProperties_FromDictError,
)


class MockMaterial:
    def __init__(self, kg_CO2_per_m2, cost_per_m2):
        self.properties = MockProperties(kg_CO2_per_m2, cost_per_m2)


class MockProperties:
    def __init__(self, kg_CO2_per_m2, cost_per_m2):
        self.revive = MockRevive(kg_CO2_per_m2, cost_per_m2)


class MockRevive:
    def __init__(self, kg_CO2_per_m2, cost_per_m2):
        self.kg_CO2_per_m2 = Unit(kg_CO2_per_m2, "KG/M2")
        self.cost_per_m2 = Unit(cost_per_m2, "COST/M2")


class MockOpaqueConstruction:
    def __init__(self, materials, display_name="Mock Construction"):
        self.materials = materials
        self.display_name = display_name


@pytest.fixture
def mock_construction():
    materials = [
        MockMaterial(10.0, 5.0),
        MockMaterial(20.0, 15.0),
    ]
    return MockOpaqueConstruction(materials)


def test_host(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    assert prop.host == mock_construction


def test_host_name(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    assert prop.host_name == "Mock Construction"

    prop_no_host = OpaqueConstructionReviveProperties()
    assert prop_no_host.host_name == "No Host"


def test_kg_CO2_per_m2(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    assert prop.kg_CO2_per_m2.value == 30.0
    assert prop.kg_CO2_per_m2.unit == "KG/M2"

    prop_no_host = OpaqueConstructionReviveProperties()
    assert prop_no_host.kg_CO2_per_m2.value == 0.0
    assert prop_no_host.kg_CO2_per_m2.unit == "KG/M2"


def test_cost_per_m2(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    assert prop.cost_per_m2.value == 20.0
    assert prop.cost_per_m2.unit == "COST/M2"

    prop_no_host = OpaqueConstructionReviveProperties()
    assert prop_no_host.cost_per_m2.value == 0.0
    assert prop_no_host.cost_per_m2.unit == "COST/M2"


def test_duplicate(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    duplicate_prop = prop.duplicate()
    assert duplicate_prop.host == mock_construction
    assert duplicate_prop.id_num == prop.id_num


def test_to_dict(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    prop_dict = prop.to_dict()
    assert prop_dict["revive"]["type"] == "OpaqueConstructionReviveProperties"
    assert prop_dict["revive"]["id_num"] == prop.id_num

    prop_dict_abridged = prop.to_dict(abridged=True)
    assert prop_dict_abridged["revive"]["type"] == "OpaqueConstructionRevivePropertiesAbridged"


def test_from_dict(mock_construction):
    input_dict = {"type": "OpaqueConstructionReviveProperties", "id_num": 1}
    prop = OpaqueConstructionReviveProperties.from_dict(input_dict, mock_construction)
    assert prop.host == mock_construction
    assert prop.id_num == 1

    with pytest.raises(OpaqueConstructionReviveProperties_FromDictError):
        OpaqueConstructionReviveProperties.from_dict({"type": "InvalidType"}, mock_construction)


def test_str_repr(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    assert str(prop) == repr(prop)
    assert str(prop) == "HBE-OpaqueConstruction Phius REVIVE Property: [host: Mock Construction]"


def test_to_string(mock_construction):
    prop = OpaqueConstructionReviveProperties(mock_construction)
    assert prop.ToString() == str(prop)
