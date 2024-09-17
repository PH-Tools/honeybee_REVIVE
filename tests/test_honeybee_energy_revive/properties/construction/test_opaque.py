from honeybee_energy_revive.properties.construction.opaque import (
    OpaqueConstructionReviveProperties,
    OpaqueConstructionReviveProperties_FromDictError,
)


def test_OpaqueConstructionReviveProperties():
    p = OpaqueConstructionReviveProperties()
    assert p


def test_default_OpaqueConstructionReviveProperties_dict_round_trip():
    p1 = OpaqueConstructionReviveProperties()
    d = p1.to_dict()
    p2 = OpaqueConstructionReviveProperties.from_dict(_input_dict=d["revive"], _host=None)
    assert d == p2.to_dict()
