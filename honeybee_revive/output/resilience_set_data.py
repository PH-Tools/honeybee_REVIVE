# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Write computed winter SET outage records from an EnergyPlus SQL file."""

import sys
from collections import namedtuple
from pathlib import Path

import pandas as pd

from honeybee_revive.output._shared import InputFileError, resolve_sql_path
from honeybee_revive.output.set_calculator import WinterSetResult, calculate_winter_set_from_sql

Filepaths = namedtuple("Filepaths", ["sql", "json"])


def resolve_paths(args: list[str]) -> Filepaths:
    """Validate CLI arguments and return the SQL and JSON paths."""
    sql_path = resolve_sql_path(args, 3)
    if not sql_path.is_file():
        raise InputFileError(sql_path)
    json_path = Path(args[2])
    json_path.parent.mkdir(parents=True, exist_ok=True)
    return Filepaths(sql_path, json_path)


def write_winter_set_json(source_file_path: Path, json_path: Path) -> WinterSetResult:
    """Write central-168 computed SET records using the existing JSON shape.

    The assigned year and UTC timestamps preserve the millisecond epoch format
    consumed by the Grasshopper IronPython wrapper.
    """
    json_path = Path(json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = json_path.with_suffix("{}.tmp".format(json_path.suffix))
    json_path.unlink(missing_ok=True)
    temporary_path.unlink(missing_ok=True)
    try:
        result = calculate_winter_set_from_sql(source_file_path, year=2016, utc=True)
        pd.DataFrame(result.outage_records).to_json(
            temporary_path,
            orient="records",
            date_format="epoch",
            date_unit="ms",
        )
        temporary_path.replace(json_path)
        return result
    finally:
        temporary_path.unlink(missing_ok=True)


if __name__ == "__main__":
    print("- " * 50)
    print(f"\t>> Using Python: {sys.version}")
    print(f"\t>> Running the script: '{__file__.split('/')[-1]}'")
    file_paths = resolve_paths(sys.argv)
    print(f"\t>> Source SQL File: '{file_paths.sql}'")
    print(f"\t>> JSON Data File: '{file_paths.json}'")
    write_winter_set_json(file_paths.sql, file_paths.json)
