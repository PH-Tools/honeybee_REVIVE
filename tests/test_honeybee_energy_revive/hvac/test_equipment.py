from honeybee_energy_revive.hvac.equipment import PhiusReviveHVACEquipment


def test_default_PhiusReviveHVACEquipment():
    equip_1 = PhiusReviveHVACEquipment()
    assert equip_1.identifier != None

    equip_2 = PhiusReviveHVACEquipment()
    assert equip_2.identifier != equip_1.identifier


def test_PhiusReviveHVACEquipment_dict_round_trip():
    equip_1 = PhiusReviveHVACEquipment()
    equip_1_dict = equip_1.to_dict()
    equip_2 = PhiusReviveHVACEquipment.from_dict(equip_1_dict)

    assert equip_1 is not equip_2
    assert equip_1.identifier == equip_2.identifier
    assert equip_1.display_name == equip_2.display_name
    assert equip_1_dict == equip_2.to_dict()


def test_PhiusReviveHVACEquipment_dict_abridged_round_trip():
    equip_1 = PhiusReviveHVACEquipment()
    equip_1_dict = equip_1.to_dict(abridged=True)
    equip_2 = PhiusReviveHVACEquipment.from_dict(equip_1_dict)

    assert equip_1 is not equip_2
    assert equip_1.identifier == equip_2.identifier
    assert equip_1.display_name == equip_2.display_name
    assert equip_1_dict == equip_2.to_dict(abridged=True)


def test_PhiusReviveHVACEquipment_duplicate():
    equip_1 = PhiusReviveHVACEquipment()
    equip_2 = equip_1.duplicate()

    assert equip_1 is not equip_2
    assert equip_1.identifier == equip_2.identifier
    assert equip_1.display_name == equip_2.display_name
