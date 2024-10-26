# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""A script to generate the Summer Resiliency Graphs.

This script is called from the command line with the following arguments:
    * [0] (str): The path to the Python script (this file).
    * [1] (str): The path to the EnergyPlus SQL file to read in.
    * [2] (str): The path to the output folder for the graphs.
"""

from collections import namedtuple
import os
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import plotly.io as pio
import sys
import sqlite3


class InputFileError(Exception):
    def __init__(self, path) -> None:
        self.msg = f"\nCannot locate the specified file:'{path}'"
        super().__init__(self.msg)


Filepaths = namedtuple("Filepaths", ["sql", "graphs"])
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

    assert len(_args) == 3, "Error: Incorrect number of arguments."

    # -----------------------------------------------------------------------------------
    # -- The EnergyPlus SQL input file.
    results_sql_file = Path(_args[1])
    if not results_sql_file.exists():
        raise InputFileError(results_sql_file)

    # -----------------------------------------------------------------------------------
    # -- Preview-Tables output folder:
    target_graphs_dir = Path(_args[2])
    if not target_graphs_dir.exists():
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
    df1 = pd.DataFrame(combined_data)

    # Create the figure
    fig1 = go.Figure()
    for zone_name in df1["Zone"].unique():
        zone_data = df1[df1["Zone"] == zone_name]
        fig1.add_trace(go.Scatter(x=zone_data["Date"], y=zone_data["Value"], mode="lines", name=zone_name))
    fig1.update_layout(title="Dry-Bulb Air Temperature.")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Air Relative Humidity
    outdoor_air_rh = get_time_series_data(file_paths.sql, "Site Outdoor Air Relative Humidity")
    zone_rh = get_time_series_data(file_paths.sql, "Zone Air Relative Humidity")

    # Combine all time series data into a single DataFrame
    combined_data = outdoor_air_rh + zone_rh
    df2 = pd.DataFrame(combined_data)

    # Create the figure
    fig2 = go.Figure()
    for zone_name in df2["Zone"].unique():
        zone_data = df2[df2["Zone"] == zone_name]
        fig2.add_trace(go.Scatter(x=zone_data["Date"], y=zone_data["Value"], mode="lines", name=zone_name))
    fig2.update_layout(title="Air Relative Humidity")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # SET Comfort Temperature
    set_temps = get_time_series_data(file_paths.sql, "Zone Thermal Comfort Pierce Model Standard Effective Temperature")
    df3 = pd.DataFrame(set_temps)

    # Create the figure
    fig3 = go.Figure()
    for zone_name in df3["Zone"].unique():
        zone_data = df3[df3["Zone"] == zone_name]
        fig3.add_trace(go.Scatter(x=zone_data["Date"], y=zone_data["Value"], mode="lines", name=zone_name))
    fig3.add_shape(
        type="line",
        x0=df3["Date"].min(),  # Start of the line (minimum date)
        x1=df3["Date"].max(),  # End of the line (maximum date)
        y0=12.222,  # Y-coordinate of the line
        y1=12.222,  # Y-coordinate of the line
        line=dict(color="Red", width=2, dash="dash"),  # Line style
    )
    fig3.update_layout(title="Zone Thermal Comfort Over Time")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Zone Heat Index
    heat_index = get_time_series_data(file_paths.sql, "Zone Heat Index")
    df4 = pd.DataFrame(heat_index)

    # Create the figure
    fig4 = go.Figure()
    for zone_name in df4["Zone"].unique():
        zone_data = df4[df4["Zone"] == zone_name]
        fig4.add_trace(go.Scatter(x=zone_data["Date"], y=zone_data["Value"], mode="lines", name=zone_name))
    # -- Caution Zone (> 26.7 deg C [80 deg F])
    fig4.add_shape(
        type="line",
        x0=df4["Date"].min(),  # Start of the line (minimum date)
        x1=df4["Date"].max(),  # End of the line (maximum date)
        y0=26.7,  # Y-coordinate of the line
        y1=26.7,  # Y-coordinate of the line
        line=dict(color="Green", width=2, dash="dash"),  # Line style
    )
    # -- Warning Zone (> 32.2 deg C [90 deg F])
    fig4.add_shape(
        type="line",
        x0=df4["Date"].min(),  # Start of the line (minimum date)
        x1=df4["Date"].max(),  # End of the line (maximum date)
        y0=32.2,  # Y-coordinate of the line
        y1=32.2,  # Y-coordinate of the line
        line=dict(color="Orange", width=2, dash="dash"),  # Line style
    )
    # -- Danger Zone (>39.4 deg-C [103 deg-F])
    fig4.add_shape(
        type="line",
        x0=df4["Date"].min(),  # Start of the line (minimum date)
        x1=df4["Date"].max(),  # End of the line (maximum date)
        y0=39.4,  # Y-coordinate of the line
        y1=39.4,  # Y-coordinate of the line
        line=dict(color="Red", width=2, dash="dash"),  # Line style
    )
    # -- Extreme Danger Zone (>51.7 deg-C [125 deg-F])
    fig4.add_shape(
        type="line",
        x0=df4["Date"].min(),  # Start of the line (minimum date)
        x1=df4["Date"].max(),  # End of the line (maximum date)
        y0=51.7,  # Y-coordinate of the line
        y1=51.7,  # Y-coordinate of the line
        line=dict(color="Black", width=2, dash="dash"),  # Line style
    )
    fig4.update_layout(title="Zone Heat Index")

    # -------------------------------------------------------------------------
    # -------------------------------------------------------------------------
    # Write all the figures to a single HTML file
    with open(file_paths.graphs / "summer_resilience.html", "w") as f:
        f.write(pio.to_html(fig1, full_html=False, include_plotlyjs="cdn"))
        f.write(pio.to_html(fig2, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(fig3, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(fig4, full_html=False, include_plotlyjs=False))
