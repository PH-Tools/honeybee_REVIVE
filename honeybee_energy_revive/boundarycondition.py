"""Extra Boundary Condition objects for Energy models.

Note to developers:
    See _extend_honeybee to see where these boundary conditions are added to
    honeybee.boundarycondition module.
"""

from honeybee.boundarycondition import _BoundaryCondition


class Foundation(_BoundaryCondition):
    __slots__ = ("_boundary_condition_object",)

    def __init__(self, boundary_condition_object):
        """Initialize Surface boundary condition.

        Args:
            boundary_condition_object:
        """
        self._boundary_condition_object = boundary_condition_object

    @property
    def boundary_condition_object(self):
        """Get the identifier of the object adjacent to this one."""
        return self._boundary_condition_object

    @classmethod
    def from_dict(cls, data):
        """Initialize Foundation BoundaryCondition from a dictionary.

        Args:
            data: A dictionary representation of the boundary condition.
        """
        assert data["type"] == "Foundation", "Expected dictionary for Foundation boundary " "condition. Got {}.".format(
            data["type"]
        )
        return cls(data["boundary_condition_object"])

    def to_dict(self):
        """Get the boundary condition as a dictionary.

        Args:
            full: Set to True to get the full dictionary which includes energy
                simulation specific keys such as sun_exposure, wind_exposure and
        """
        return {"type": self.name, "boundary_condition_object": self.boundary_condition_object}

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return self.boundary_condition_object

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return "Foundation({})".format(self.boundary_condition_object)
