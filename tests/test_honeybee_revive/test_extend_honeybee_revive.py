from honeybee.model import Model


def test_extend_honeybee_with_revive_properties(test_hb_model: Model):
    test_model = test_hb_model.duplicate()

    # -- The HB-Model
    assert hasattr(test_model.properties, "energy")
    assert hasattr(test_model.properties, "revive")

    # -- The HB-Room
    for hb_room in test_model.rooms:
        assert hasattr(hb_room.properties, "energy")
        assert hasattr(hb_room.properties, "revive")

        for face in hb_room.faces:
            assert hasattr(face.properties, "energy")
            assert hasattr(face.properties, "revive")
