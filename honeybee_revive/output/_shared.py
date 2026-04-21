# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Shared utilities for the resilience output modules."""

import os
import sqlite3
from collections import namedtuple
from pathlib import Path
from typing import Any, Iterable, cast

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


class InputFileError(Exception):
    """Raised when a specified input file path does not exist.

    Attributes:
        msg (str): Error message including the missing file path.
    """

    def __init__(self, path) -> None:
        self.msg = f"\nCannot locate the specified file:'{path}'"
        super().__init__(self.msg)


Record = namedtuple("Record", ["Date", "Value", "Zone"])


def get_time_series_data(
    source_file_path: Path, output_variable: str, year: int = 2021, utc: bool = False
) -> list[Record]:
    """Query hourly time-series data for a variable from an EnergyPlus SQL file.

    Arguments:
    ----------
        * source_file_path (Path): Path to the EnergyPlus SQL results file.
        * output_variable (str): The EnergyPlus output variable name to query.
        * year (int): The year to assign to timestamps. Default: 2021.
        * utc (bool): If True, create UTC-aware timestamps. Default: False.

    Returns:
    --------
        * list[Record]: List of (Date, Value, Zone) named tuples.
    """
    conn = sqlite3.connect(source_file_path)
    data_ = []
    try:
        c = conn.cursor()
        c.execute(
            "SELECT KeyValue, Month, Day, Hour, Value FROM 'ReportVariableWithTime' "
            "WHERE Name=? "
            "AND DayType NOT IN ('WinterDesignDay', 'SummerDesignDay') "
            "ORDER BY Month, Day, Hour",
            (output_variable,),
        )
        for row in c.fetchall():
            date = pd.to_datetime(f"{year}-{row[1]}-{row[2]} {row[3] - 1}:00:00", utc=utc)
            data_.append(Record(date, row[4], row[0]))
    except Exception as e:
        conn.close()
        raise Exception(str(e))
    finally:
        conn.close()

    return data_


def resolve_sql_path(_args: list[str], expected_arg_count: int) -> Path:
    """Validate argument count and return the SQL file path.

    Arguments:
    ----------
        * _args (list[str]): sys.args list of input arguments.
        * expected_arg_count (int): Expected number of arguments.

    Returns:
    --------
        * Path: The validated SQL file path.
    """

    assert len(_args) == expected_arg_count, "Error: Incorrect number of arguments."

    results_sql_file = Path(_args[1])
    if not results_sql_file.exists():
        raise InputFileError(results_sql_file)

    return results_sql_file


def df_in_kWh(_data: Iterable[Record]) -> pd.DataFrame:
    """Create a DataFrame from Records, converting the Value column from J to kWh.

    Arguments:
    ----------
        * _data (Iterable[Record]): Records with Value in Joules.

    Returns:
    --------
        * pd.DataFrame: DataFrame with Value column converted to kWh.
    """

    df = pd.DataFrame(_data)
    if not df.empty:
        df["Value"] = df["Value"].apply(lambda _: _ * 0.000000277778)
    return df


def df_in_m3hr(_data: list[Record]) -> pd.DataFrame:
    """Create a DataFrame from Records, converting the Value column from m3/s to m3/hr.

    Arguments:
    ----------
        * _data (list[Record]): Records with Value in m3/s.

    Returns:
    --------
        * pd.DataFrame: DataFrame with Value column converted to m3/hr.
    """

    df = pd.DataFrame(_data)
    if not df.empty:
        df["Value"] = df["Value"].apply(lambda _: _ * 3600)
    return df


def create_line_plot_figure(
    _df: pd.DataFrame,
    _title: str,
    _horizontal_lines: list[float] | None = None,
    _stack: bool = False,
) -> go.Figure:
    """Create a Plotly line plot figure from a DataFrame with Date/Value/Zone columns.

    Arguments:
    ----------
        * _df (pd.DataFrame): DataFrame with 'Date', 'Value', and 'Zone' columns.
        * _title (str): The chart title.
        * _horizontal_lines (list[float] | None): Y-values for dashed red reference lines.
        * _stack (bool): If True, stack the traces. Default: False.

    Returns:
    --------
        * go.Figure: The Plotly figure.
    """

    fig = go.Figure()
    fig.update_layout(
        title=_title,
        paper_bgcolor="rgba(0,0,0,0)",
    )

    if _df.empty:
        return fig

    for zone_name in _df["Zone"].unique():
        zone_data = _df[_df["Zone"] == zone_name]
        if _stack:
            fig.add_trace(
                go.Scatter(
                    x=zone_data["Date"],
                    y=zone_data["Value"],
                    mode="lines",
                    stackgroup="one",
                    name=zone_name,
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=zone_data["Date"],
                    y=zone_data["Value"],
                    mode="lines",
                    name=zone_name,
                )
            )

    if _horizontal_lines:
        for line in _horizontal_lines:
            fig.add_shape(
                type="line",
                x0=_df["Date"].min(),
                x1=_df["Date"].max(),
                y0=line,
                y1=line,
                line=dict(color="Red", width=2, dash="dash"),
            )

    return fig


def html_file(_filename: Path) -> Path:
    """Return the file path after removing any existing file at that location.

    Arguments:
    ----------
        * _filename (Path): The target HTML file path.

    Returns:
    --------
        * Path: The same path, ready for writing.
    """

    if os.path.exists(_filename):
        os.remove(_filename)
    return _filename


def write_figures_to_html(filepath: Path, figures: list[tuple[go.Figure, str]]) -> None:
    """Write multiple figures to a single HTML file.

    Arguments:
    ----------
        * filepath (Path): The output HTML file path.
        * figures (list[tuple[go.Figure, str]]): A list of (figure, div_id) tuples.
    """

    with open(html_file(filepath), "w") as f:
        for i, (fig, div_id) in enumerate(figures):
            include_plotlyjs: bool | str = "cdn" if i == 0 else False
            f.write(
                pio.to_html(
                    fig,
                    full_html=False,
                    include_plotlyjs=cast(Any, include_plotlyjs),
                    div_id=div_id,
                )
            )
