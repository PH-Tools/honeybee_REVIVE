from honeybee.model import Model

from honeybee_energy.hvac.doas.vrf import VRFwithDOAS
from honeybee_energy.hvac.allair.furnace import ForcedAirFurnace
from honeybee_energy.hvac.heatcool.vrf import VRF
from honeybee_energy.hvac.idealair import IdealAirSystem

from honeybee_energy_revive.hvac.equipment import PhiusReviveHVACEquipment
from honeybee_energy_revive.properties.hvac.heatcool import HeatCoolSystemReviveProperties
from honeybee_energy_revive.properties.hvac.idealair import IdealAirSystemReviveProperties
from honeybee_energy_revive.properties.hvac.allair import AllAirSystemReviveProperties
from honeybee_energy_revive.properties.hvac.doas import DOASSystemReviveProperties


def test_doas_hvac_with_no_equipment_dict_roundtrip(test_hb_model: Model):
    test_model = test_hb_model.duplicate()

    # -- The HB-Room
    hb_room = test_model.rooms[0]
    assert hasattr(hb_room.properties.energy, "hvac")

    # -- Add a DOAS System to the Room
    new_system = VRFwithDOAS(identifier="test_vrf_system")
    assert hasattr(new_system.properties, "revive")
    hb_room.properties.energy.hvac = new_system

    # -- Dict Round-trip
    d1 = test_model.to_dict()
    m2 = Model.from_dict(d1)
    assert m2.to_dict() == d1


def test_doas_hvac_with_equipment_dict_roundtrip(test_hb_model: Model):
    test_model = test_hb_model.duplicate()

    # -- The HB-Room
    hb_room = test_model.rooms[0]
    assert hasattr(hb_room.properties.energy, "hvac")

    # -- Add a DOAS System to the Room
    new_system = VRFwithDOAS(identifier="test_vrf_system")
    sys_revive_props: DOASSystemReviveProperties = getattr(new_system.properties, "revive")
    sys_revive_props.add_equipment(PhiusReviveHVACEquipment())

    assert hasattr(new_system.properties, "revive")
    hb_room.properties.energy.hvac = new_system

    # -- Dict Round-trip
    d1 = test_model.to_dict()
    m2 = Model.from_dict(d1)
    assert m2.to_dict() == d1


def test_ideal_air_with_equipment_dict_roundtrip(test_hb_model: Model):
    test_model = test_hb_model.duplicate()

    # -- The HB-Room
    hb_room = test_model.rooms[0]
    assert hasattr(hb_room.properties.energy, "hvac")

    # -- Add an Ideal Air System to the Room
    new_system = IdealAirSystem(identifier="test_ideal_air_system")
    sys_revive_props: IdealAirSystemReviveProperties = getattr(new_system.properties, "revive")
    sys_revive_props.add_equipment(PhiusReviveHVACEquipment())

    assert hasattr(new_system.properties, "revive")
    hb_room.properties.energy.hvac = new_system

    # -- Dict Round-trip
    d1 = test_model.to_dict()
    m2 = Model.from_dict(d1)
    assert m2.to_dict() == d1


def test_heatcool_with_equipment_dict_roundtrip(test_hb_model: Model):
    test_model = test_hb_model.duplicate()

    # -- The HB-Room
    hb_room = test_model.rooms[0]
    assert hasattr(hb_room.properties.energy, "hvac")

    # -- Add a HeatCool System to the Room
    new_system = VRF(identifier="test_vrf_system")
    sys_revive_props: HeatCoolSystemReviveProperties = getattr(new_system.properties, "revive")
    sys_revive_props.add_equipment(PhiusReviveHVACEquipment())

    assert hasattr(new_system.properties, "revive")
    hb_room.properties.energy.hvac = new_system

    # -- Dict Round-trip
    d1 = test_model.to_dict()
    m2 = Model.from_dict(d1)
    assert m2.to_dict() == d1


def test_allair_with_equipment_dict_roundtrip(test_hb_model: Model):
    test_model = test_hb_model.duplicate()

    # -- The HB-Room
    hb_room = test_model.rooms[0]
    assert hasattr(hb_room.properties.energy, "hvac")

    # -- Add an AllAir System to the Room
    new_system = ForcedAirFurnace(identifier="test_forced_air_furnace")
    sys_revive_props: AllAirSystemReviveProperties = getattr(new_system.properties, "revive")
    sys_revive_props.add_equipment(PhiusReviveHVACEquipment())

    assert hasattr(new_system.properties, "revive")
    hb_room.properties.energy.hvac = new_system

    # -- Dict Round-trip
    d1 = test_model.to_dict()
    m2 = Model.from_dict(d1)
    assert m2.to_dict() == d1
