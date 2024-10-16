# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""A script to generate the Winter Resiliency Graphs.

This script is called from the command line with the following arguments:
    * [1] (str): The path to the EnergyPlus SQL file to read in.
    * [3] (str): The path to the output folder for the graphs.
"""

from collections import namedtuple
import os
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio
import shutil
import sys
import sqlite3


class InputFileError(Exception):
    def __init__(self, path) -> None:
        self.msg = f"\nCannot locate the specified file:'{path}'"
        super().__init__(self.msg)


Filepaths = namedtuple("Filepaths", ["sql", "graphs"])
Record = namedtuple("Record", ["Date", "Value", "Zone"])


def _remove_folder_and_contents(_folder: Path) -> None:
    """Remove all files in the specified folder."""
    print(f"\t>> Removing: {_folder}")
    shutil.rmtree(_folder)


def resolve_paths(_args: list[str]) -> Filepaths:
    """Sort out the file input and output paths. Make the output directory if needed.

    Arguments:
    ----------
        * _args (list[str]): sys.args list of input arguments.

    Returns:
    --------
        * Filepaths
    """

    assert len(_args) == 3, "Error: Incorrect number of arguments."

    # -----------------------------------------------------------------------------------
    # -- The EnergyPlus SQL input file.
    results_sql_file = Path(_args[1])
    if not results_sql_file.exists():
        raise InputFileError(results_sql_file)

    # -----------------------------------------------------------------------------------
    # -- Preview-Tables output folder:
    target_graphs_dir = Path(_args[2])
    if target_graphs_dir.exists():
        _remove_folder_and_contents(target_graphs_dir)

    print(f"\t>> Creating the directory: {target_graphs_dir}")
    os.mkdir(target_graphs_dir)

    return Filepaths(results_sql_file, target_graphs_dir)


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
            date = pd.to_datetime(f"2021-{row[1]}-{row[2]} {row[3]-1}:00:00")
            data_.append(Record(date, row[4], row[0]))
    except Exception as e:
        conn.close()
        raise Exception(str(e))
    finally:
        conn.close()

    return data_


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
    print(f"\t>> Target Output Folder: '{file_paths.graphs}'")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Air Dry-Bulb Temperature
    outdoor_air_drybulb = get_time_series_data(file_paths.sql, "Site Outdoor Air Drybulb Temperature")
    zone_temps = get_time_series_data(file_paths.sql, "Zone Mean Air Temperature")

    # Combine all time series data into a single DataFrame
    combined_data = outdoor_air_drybulb + zone_temps
    df = pd.DataFrame(combined_data)

    # Create the figure
    fig1 = go.Figure()
    for zone_name in df["Zone"].unique():
        zone_data = df[df["Zone"] == zone_name]
        fig1.add_trace(go.Scatter(x=zone_data["Date"], y=zone_data["Value"], mode="lines", name=zone_name))
    fig1.update_layout(title="Dry-Bulb Air Temperature.")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Air Relative Humidity
    outdoor_air_rh = get_time_series_data(file_paths.sql, "Site Outdoor Air Relative Humidity")
    zone_rh = get_time_series_data(file_paths.sql, "Zone Air Relative Humidity")

    # Combine all time series data into a single DataFrame
    combined_data = outdoor_air_rh + zone_rh
    df = pd.DataFrame(combined_data)

    # Create the figure
    fig2 = go.Figure()
    for zone_name in df["Zone"].unique():
        zone_data = df[df["Zone"] == zone_name]
        fig2.add_trace(go.Scatter(x=zone_data["Date"], y=zone_data["Value"], mode="lines", name=zone_name))
    fig2.update_layout(title="Air Relative Humidity")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # SET Comfort Temperature
    set_temps = get_time_series_data(file_paths.sql, "Zone Thermal Comfort Pierce Model Standard Effective Temperature")
    df = pd.DataFrame(set_temps)

    # Create the figure
    fig3 = go.Figure()
    for zone_name in df["Zone"].unique():
        zone_data = df[df["Zone"] == zone_name]
        fig3.add_trace(go.Scatter(x=zone_data["Date"], y=zone_data["Value"], mode="lines", name=zone_name))
    fig3.add_shape(
        type="line",
        x0=df["Date"].min(),  # Start of the line (minimum date)
        x1=df["Date"].max(),  # End of the line (maximum date)
        y0=12.222,  # Y-coordinate of the line
        y1=12.222,  # Y-coordinate of the line
        line=dict(color="Red", width=2, dash="dash"),  # Line style
    )
    fig3.update_layout(title="Zone Thermal Comfort Over Time - Plot 1")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Write all the figures to a single HTML file
    with open(file_paths.graphs / "winter_resilience.html", "w") as f:
        f.write(pio.to_html(fig1, full_html=False, include_plotlyjs="cdn"))
        f.write(pio.to_html(fig2, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(fig3, full_html=False, include_plotlyjs=False))
