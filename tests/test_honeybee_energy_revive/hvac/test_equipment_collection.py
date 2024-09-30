from honeybee_energy_revive.hvac.equipment import PhiusReviveHVACEquipment, PhiusReviveHVACEquipmentCollection


def test_default_PhiusReviveHVACEquipmentCollection():
    equip_col = PhiusReviveHVACEquipmentCollection()
    assert len(equip_col) == 0


def test_add_one_Equipment_to_PhiusReviveHVACEquipmentCollection():
    equip_col = PhiusReviveHVACEquipmentCollection()
    equip = PhiusReviveHVACEquipment()
    equip_col.add_equipment(equip)
    assert len(equip_col) == 1
    assert equip_col.get_equipment_by_identifier(equip.identifier) == equip
    assert equip in equip_col


def test_add_two_Equipment_to_PhiusReviveHVACEquipmentCollection():
    equip_col = PhiusReviveHVACEquipmentCollection()
    equip_1 = PhiusReviveHVACEquipment()
    equip_2 = PhiusReviveHVACEquipment()
    equip_col.add_equipment(equip_1)
    equip_col.add_equipment(equip_2)
    assert len(equip_col) == 2
    assert equip_col.get_equipment_by_identifier(equip_1.identifier) == equip_1
    assert equip_col.get_equipment_by_identifier(equip_2.identifier) == equip_2
    assert equip_1 in equip_col
    assert equip_2 in equip_col


def test_Collection_with_multiple_equipment_dict_round_trip():
    equip_col = PhiusReviveHVACEquipmentCollection()
    equip_1 = PhiusReviveHVACEquipment()
    equip_2 = PhiusReviveHVACEquipment()
    equip_col.add_equipment(equip_1)
    equip_col.add_equipment(equip_2)

    equip_col_dict = equip_col.to_dict()
    equip_col_2 = PhiusReviveHVACEquipmentCollection.from_dict(equip_col_dict)

    assert len(equip_col) == len(equip_col_2)


def test_Collection_with_multiple_equipment_dict_abridged_round_trip():
    equip_col = PhiusReviveHVACEquipmentCollection()
    equip_1 = PhiusReviveHVACEquipment()
    equip_2 = PhiusReviveHVACEquipment()
    equip_col.add_equipment(equip_1)
    equip_col.add_equipment(equip_2)

    equip_col_dict = equip_col.to_dict(abridged=True)
    equip_col_2 = PhiusReviveHVACEquipmentCollection.from_dict(equip_col_dict)

    assert len(equip_col) == len(equip_col_2)


def test_Collection_with_multiple_equipment_duplicate():
    equip_col = PhiusReviveHVACEquipmentCollection()
    equip_1 = PhiusReviveHVACEquipment()
    equip_2 = PhiusReviveHVACEquipment()
    equip_col.add_equipment(equip_1)
    equip_col.add_equipment(equip_2)

    equip_col_2 = equip_col.duplicate()

    assert len(equip_col) == len(equip_col_2)
    assert all(equip in equip_col_2 for equip in equip_col)
    assert all(equip in equip_col for equip in equip_col_2)


def test_Collection_str():
    equip_col = PhiusReviveHVACEquipmentCollection()

    assert str(equip_col) == "PhiusReviveHVACEquipmentCollection(0 items)"
    assert repr(equip_col) == "PhiusReviveHVACEquipmentCollection(0 items)"
    assert equip_col.ToString() == "PhiusReviveHVACEquipmentCollection(0 items)"

    # -- Add some equipment
    equip_1 = PhiusReviveHVACEquipment()
    equip_col.add_equipment(equip_1)
    assert str(equip_col) == "PhiusReviveHVACEquipmentCollection(1 items)"
    assert repr(equip_col) == "PhiusReviveHVACEquipmentCollection(1 items)"
    assert equip_col.ToString() == "PhiusReviveHVACEquipmentCollection(1 items)"

    # -- Adding the same equipment twice should ignore it
    equip_col.add_equipment(equip_1)
    assert str(equip_col) == "PhiusReviveHVACEquipmentCollection(1 items)"
    assert repr(equip_col) == "PhiusReviveHVACEquipmentCollection(1 items)"
    assert equip_col.ToString() == "PhiusReviveHVACEquipmentCollection(1 items)"

    # -- Add new equipment
    equip_2 = PhiusReviveHVACEquipment()
    equip_col.add_equipment(equip_2)
    assert str(equip_col) == "PhiusReviveHVACEquipmentCollection(2 items)"
    assert repr(equip_col) == "PhiusReviveHVACEquipmentCollection(2 items)"
    assert equip_col.ToString() == "PhiusReviveHVACEquipmentCollection(2 items)"
