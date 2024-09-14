# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBPH-Space Phius REVIVE Properties."""

try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False
    pass  # Python 2.7

try:
    if TYPE_CHECKING:
        from honeybee_ph.space import Space
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))


class SpaceReviveProperties(object):
    def __init__(self, _host):
        # type: (Space | None) -> None
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        # type: () -> Space | None
        return self._host

    @property
    def host_name(self):
        # type: () -> str
        return self.host.display_name if self.host else "No Host"

    def duplicate(self, new_host=None):
        # type: (Space | None) -> SpaceReviveProperties
        """Create a duplicate of the SpaceReviveProperties object.

        Arguments:
        ----------
            * new_host (Space | None): The new host for the properties.

        Returns:
        ----------
            * SpaceReviveProperties: The duplicated SpaceReviveProperties object.
        """
        _host = new_host or self._host
        new_properties_obj = SpaceReviveProperties(_host)
        return new_properties_obj

    def __copy__(self):
        # type: () -> SpaceReviveProperties
        return self.duplicate()

    def __repr__(self):
        return "HBPH-Space Phius REVIVE Properties: [host: {}]".format(self.host_name)

    def __str__(self):
        return self.__repr__()

    def ToString(self):
        return str(self)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        """Return the properties as a dictionary.

        Arguments:
        ----------
            * abridged (bool): Set to True to return an abridged version of the dictionary.

        Returns:
        ----------
            * dict: The properties as a dictionary.
        """

        d = {}

        if abridged:
            d["type"] = "SpaceRevivePropertiesAbridged"
        else:
            d["type"] = "SpaceReviveProperties"

        return {"revive": d}

    @classmethod
    def from_dict(cls, data, host):
        # type: (dict, Space | None) -> SpaceReviveProperties
        """Create a SpaceReviveProperties object from a dictionary.

        Arguments:
        ----------
            * data (dict): A dictionary with the SpaceReviveProperties properties.
            * host (Space | None): The host object for the properties.

        Returns:
        ----------
            * SpaceReviveProperties: The SpaceReviveProperties object.
        """

        assert "SpaceReviveProperties" in data["type"], "Expected SpaceReviveProperties. Got {}.".format(data["type"])
        new_prop = cls(host)

        return new_prop


def get_revive_prop_from_space(_space):
    # type: (Space) -> SpaceReviveProperties
    """Get the HBPH-Space's Phius REVIVE-Properties."""
    return getattr(_space.properties, "revive")
