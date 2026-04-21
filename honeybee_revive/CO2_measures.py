# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Model Phius REVIVE CO2-Reduction-Measure and Measure-Collection Classes."""

try:
    from typing import Iterator
except ImportError:
    pass  # Python 2.7


class CO2ReductionMeasure(object):
    """A single CO2 reduction measure for Phius REVIVE lifecycle cost analysis.

    Represents a building improvement or component with associated cost and
    embodied carbon data. Measures are classified as either PERFORMANCE
    (energy-related) or NON_PERFORMANCE (non-energy-related).

    Attributes:
        name (str): Display name of the measure.
            Default: "unnamed_CO2_measure".
        measure_type (str): Classification of the measure. Must be
            "PERFORMANCE" or "NON_PERFORMANCE". Default: "PERFORMANCE".
        year (int): The year (in the analysis timeline) when this measure
            is applied. Default: 60.
        cost (float): Total installed cost of the measure in USD.
            Default: 8500.0.
        kg_CO2 (float): Embodied carbon of the measure in kg CO2.
            Default: 0.0.
        country_name (str): Country of origin for emissions factor lookup.
            Default: "USA".
        labor_fraction (float): Fraction of cost attributable to labor
            (0.0 to 1.0). Default: 0.4.
    """

    def __init__(
        self,
        name="unnamed_CO2_measure",
        measure_type="PERFORMANCE",
        year=60,
        cost=8500.0,
        kg_CO2=0.0,
        country_name="USA",
        labor_fraction=0.4,
    ):
        self.name = name
        self._measure_type = measure_type
        self.year = year
        self.cost = cost
        self.kg_CO2 = kg_CO2
        self.country_name = country_name
        self.labor_fraction = labor_fraction

    @property
    def unique_id(self):
        # type: () -> str
        """Composite identifier derived from name, type, year, cost, and labor fraction."""
        return "{}-{}-{}-{}-{}".format(self.name, self.measure_type, self.year, int(self.cost), self.labor_fraction)

    @property
    def measure_type(self):
        # type: () -> str
        """The measure classification: 'PERFORMANCE' or 'NON_PERFORMANCE'."""
        return self._measure_type

    @measure_type.setter
    def measure_type(self, _input):
        # type: (str) -> None
        _input = str(_input).upper().strip()
        if _input not in ["PERFORMANCE", "NON_PERFORMANCE"]:
            raise ValueError("Measure type must be either 'PERFORMANCE' or 'COST'.")
        self._measure_type = _input

    def to_dict(self):
        # type: () -> dict
        d = {}
        d["type"] = "CO2ReductionMeasure"
        d["measure_type"] = self.measure_type
        d["name"] = self.name
        d["year"] = self.year
        d["cost"] = self.cost
        d["kg_CO2"] = self.kg_CO2
        d["country_name"] = self.country_name
        d["labor_fraction"] = self.labor_fraction
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict) -> CO2ReductionMeasure
        if not _dict["type"] == "CO2ReductionMeasure":
            raise ValueError("The supplied dict is not a CO2ReductionMeasure? Got: {}".format(_dict["type"]))

        measure = cls()
        measure.measure_type = _dict["measure_type"]
        measure.name = _dict["name"]
        measure.year = _dict["year"]
        measure.cost = _dict["cost"]
        measure.kg_CO2 = _dict["kg_CO2"]
        measure.country_name = _dict["country_name"]
        measure.labor_fraction = _dict["labor_fraction"]
        return measure

    def duplicate(self):
        # type: () -> CO2ReductionMeasure
        return CO2ReductionMeasure.from_dict(self.to_dict())

    def __copy__(self):
        # type: () -> CO2ReductionMeasure
        return self.duplicate()

    def __str__(self):
        # type: () -> str
        return "{}(name={})".format(self.__class__.__name__, self.name)

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return str(self)


class CO2ReductionMeasureCollection(object):
    """An ordered collection of CO2ReductionMeasure objects, keyed by unique_id.

    Supports iteration, containment testing, and len(). Measures are stored
    internally by unique_id and returned sorted by unique_id when iterated.
    """

    def __init__(self):
        self._storage = {}  # type: dict[str, CO2ReductionMeasure]

    def add_measure(self, measure):
        # type: (CO2ReductionMeasure) -> None
        """Add a CO2ReductionMeasure to the collection.

        Arguments:
        ----------
            * measure (CO2ReductionMeasure): The measure to add. Keyed by its unique_id.
        """
        self._storage[measure.unique_id] = measure

    def measures(self):
        # type: () -> list[CO2ReductionMeasure]
        """Return all measures in the collection as a list."""
        return list(self._storage.values())

    def keys(self):
        # type: () -> list[str]
        """Return all unique_id keys, sorted by unique_id."""
        return [k for k, v in sorted(self._storage.items(), key=lambda x: x[1].unique_id)]

    def values(self):
        # type: () -> list[CO2ReductionMeasure]
        """Return all measures, sorted by unique_id."""
        return list(sorted(self._storage.values(), key=lambda x: x.unique_id))

    def duplicate(self):
        # type: () -> CO2ReductionMeasureCollection
        new_collection = CO2ReductionMeasureCollection()
        for measure in self.measures():
            new_collection.add_measure(measure.duplicate())
        return new_collection

    def __copy__(self):
        # type: () -> CO2ReductionMeasureCollection
        return self.duplicate()

    def to_dict(self):
        # type: () -> dict[str, dict]
        return {k: v.to_dict() for k, v in self._storage.items()}

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict) -> CO2ReductionMeasureCollection
        collection = cls()
        for k, v in _dict.items():
            collection.add_measure(CO2ReductionMeasure.from_dict(v))
        return collection

    def __iter__(self):
        # type: () -> Iterator[CO2ReductionMeasure]
        return iter(sorted(self._storage.values(), key=lambda x: x.unique_id))

    def __contains__(self, key):
        # type: (str | CO2ReductionMeasure) -> bool
        if isinstance(key, CO2ReductionMeasure):
            return key in self._storage.values()
        return key in self._storage

    def __len__(self):
        # type: () -> int
        return len(self._storage)

    def __str__(self):
        # type: () -> str
        return "{}({}-measures)".format(self.__class__.__name__, len(self._storage))

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return str(self)
