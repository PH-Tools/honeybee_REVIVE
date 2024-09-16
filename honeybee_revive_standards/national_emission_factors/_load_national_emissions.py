# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility function to load NationalEmissionsFactor data from a JSON file."""

import json
import os

try:
    from honeybee_revive.national_emissions import NationalEmissionsFactors
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_revive:\n\t{}".format(e))


def load_national_emissions_from_json_file(_filepath):
    # type: (str) -> dict[str, NationalEmissionsFactors]
    """Load a NationalEmissionsFactors object from a JSON file."""
    if not os.path.isfile(_filepath):
        raise ValueError("File does not exist: {}".format(_filepath))

    with open(_filepath, "r") as json_file:
        all_emissions = (NationalEmissionsFactors(**item) for item in json.load(json_file))
        return {_.country_name: _ for _ in all_emissions}
