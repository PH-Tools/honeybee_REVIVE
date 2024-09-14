# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-Energy-REVIVE properties for Honeybee-Energy ShadeConstruction Objects"""

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False
    pass  # Python 2.7

try:
    if TYPE_CHECKING:
        from honeybee_energy.construction.shade import ShadeConstruction
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy:\n\t{}".format(e))


class ShadeConstructionReviveProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(ShadeConstructionReviveProperties_FromDictError, self).__init__(self.msg)


class ShadeConstructionReviveProperties(object):
    """Honeybee-REVIVE Properties for storing REVIVE data."""

    def __init__(self, _host):
        # type: (ShadeConstruction | None) -> None
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        # type: () -> ShadeConstruction | None
        return self._host

    @property
    def host_name(self):
        # type: () -> str
        return self.host.display_name if self.host else "No Host"

    def duplicate(self, new_host=None):
        # type: (ShadeConstruction | None) -> ShadeConstructionReviveProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (ShadeConstruction | None) -> ShadeConstructionReviveProperties
        host = new_host or self.host
        new_obj = self.__class__(host)
        new_obj.id_num = self.id_num
        return new_obj

    def to_dict(self, abridged=False):
        # type: (bool) -> dict
        d = {}
        if abridged:
            d["type"] = "ShadeConstructionRevivePropertiesAbridged"
        else:
            d["type"] = "ShadeConstructionReviveProperties"
        return {"revive": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (dict, ShadeConstruction | None) -> ShadeConstructionReviveProperties
        valid_types = (
            "ShadeConstructionReviveProperties",
            "ShadeConstructionRevivePropertiesAbridged",
        )
        if _input_dict["type"] not in valid_types:
            raise ShadeConstructionReviveProperties_FromDictError(valid_types, _input_dict["type"])
        new_obj = cls(host)
        new_obj.id_num = _input_dict["id_num"]
        return new_obj

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "HBE-ShadeConstruction Phius REVIVE Property: [host: {}]".format(self.host_name)

    def ToString(self):
        return str(self)
