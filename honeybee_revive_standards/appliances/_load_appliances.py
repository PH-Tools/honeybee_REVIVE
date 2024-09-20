# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility function to load Appliance (HB-E Process) Objects from a JSON file."""

import json
import os

try:
    from honeybee_energy.load.process import Process
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy:\n\t{}".format(e))

try:
    from honeybee_revive_standards.schedules._load_schedules import load_schedules_from_json_file
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_revive_standards:\n\t{}".format(e))


def is_abridged_process(_json_object):
    # type: (dict) -> bool
    """Check if a JSON object is a valid 'ProcessAbridged' dict."""
    if "type" not in _json_object:
        return False
    if not _json_object["type"] == "ProcessAbridged":
        return False
    return True


def load_abridged_appliances_from_json_file(_appliance_filepath, _scheduled_filepath):
    # type: (str, str) -> dict[str, Process]
    """Load a HBE-Process object from a JSON file."""
    schedule_dict = load_schedules_from_json_file(_scheduled_filepath)

    if not os.path.exists(_appliance_filepath):
        raise ValueError("File not found: {}".format(_appliance_filepath))

    with open(_appliance_filepath, "r") as json_file:
        all_measures = (
            Process.from_dict_abridged(d, schedule_dict) for d in json.load(json_file) if is_abridged_process(d)
        )
        return {_.display_name: _ for _ in all_measures}
