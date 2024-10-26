# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""A script to generate the Winter Resiliency Graphs.

This script is called from the command line with the following arguments:
    * [0] (str): The path to the Python script (this file).
    * [1] (str): The path to the EnergyPlus SQL file to read in.
    * [2] (str): The path to the output folder for the graphs.
"""

from collections import namedtuple
import os
import pandas as pd
from pathlib import Path
import sys
import sqlite3


class InputFileError(Exception):
    def __init__(self, path) -> None:
        self.msg = f"\nCannot locate the specified file:'{path}'"
        super().__init__(self.msg)


Filepaths = namedtuple("Filepaths", ["sql", "SET_json_data_path", "heat_index_json_data_path"])
Record = namedtuple("Record", ["Date", "Value", "Zone"])


def resolve_paths(_args: list[str]) -> Filepaths:
    """Sort out the file input and output paths. Make the output directory if needed.

    Arguments:
    ----------
        * _args (list[str]): sys.args list of input arguments.

    Returns:
    --------
        * Filepaths
    """

    assert len(_args) == 4, "Error: Incorrect number of arguments."

    # -----------------------------------------------------------------------------------
    # -- The EnergyPlus SQL input file.
    results_sql_file = Path(_args[1])
    if not results_sql_file.exists():
        raise InputFileError(results_sql_file)

    # -----------------------------------------------------------------------------------
    # -- JSON File paths:
    SET_target_json_filepath = Path(_args[2])
    if SET_target_json_filepath.exists():
        print(f"\t>> Removing the file: {SET_target_json_filepath}")
        os.remove(SET_target_json_filepath)

    heat_index_target_json_filepath = Path(_args[3])
    if heat_index_target_json_filepath.exists():
        print(f"\t>> Removing the file: {heat_index_target_json_filepath}")
        os.remove(heat_index_target_json_filepath)

    return Filepaths(results_sql_file, SET_target_json_filepath, heat_index_target_json_filepath)


def get_time_series_data(source_file_path: Path, output_variable: str) -> list[Record]:
    """Get Time-Series data from the SQL File."""
    conn = sqlite3.connect(source_file_path)
    data_ = []  # defaultdict(list)
    try:
        c = conn.cursor()
        c.execute(
            "SELECT KeyValue, Month, Day, Hour, Value FROM 'ReportVariableWithTime' "
            "WHERE Name=? "
            "ORDER BY Month, Day, Hour",
            (output_variable,),
        )
        for row in c.fetchall():
            date = pd.to_datetime(f"2016-{row[1]}-{row[2]} {row[3]-1}:00:00", utc=True)
            data_.append(Record(date, row[4], row[0]))
    except Exception as e:
        conn.close()
        raise Exception(str(e))
    finally:
        conn.close()

    return data_


def pivot_df_by_zone_name(_df: pd.DataFrame) -> pd.DataFrame:
    """Pivot the DataFrame so the columns are the Zone names."""
    pivot_df = _df.pivot(index="Date", columns="Zone", values="Value")
    pivot_df.reset_index(inplace=True)
    return pivot_df


if __name__ == "__main__":
    print("- " * 50)
    print(f"\t>> Using Python: {sys.version}")
    print(f"\t>> Running the script: '{__file__.split('/')[-1]}'")
    print(f"\t>> With the arguments:")
    print("\n".join([f"\t\t{i} | {a}" for i, a in enumerate(sys.argv)]))

    # -------------------------------------------------------------------------
    # --- Input / Output file Path
    print("\t>> Resolving file paths...")
    file_paths = resolve_paths(sys.argv)
    print(f"\t>> Source SQL File: '{file_paths.sql}'")
    print(f"\t>> SET JSON Data File: '{file_paths.SET_json_data_path}'")
    print(f"\t>> Heat-Index JSON Data File: '{file_paths.heat_index_json_data_path}'")

    # -------------------------------------------------------------------------
    # -- Get the Hourly Data from the SQL File, output it to a JSON file.
    set_temps = get_time_series_data(file_paths.sql, "Zone Thermal Comfort Pierce Model Standard Effective Temperature")
    set_df = pd.DataFrame(set_temps)
    set_df.to_json(file_paths.SET_json_data_path, orient="records")
    set_df = pivot_df_by_zone_name(set_df)
    set_df.to_csv(file_paths.SET_json_data_path.with_suffix(".csv"), index=False)

    heat_index = get_time_series_data(file_paths.sql, "Zone Heat Index")
    heat_index_df = pd.DataFrame(heat_index)
    heat_index_df.to_json(file_paths.heat_index_json_data_path, orient="records")
    heat_index_df = pivot_df_by_zone_name(heat_index_df)
    heat_index_df.to_csv(file_paths.heat_index_json_data_path.with_suffix(".csv"), index=False)
