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
    def __init__(self, path) -> None:
        self.msg = f"\nCannot locate the specified file:'{path}'"
        super().__init__(self.msg)


Record = namedtuple("Record", ["Date", "Value", "Zone"])


def get_time_series_data(
    source_file_path: Path, output_variable: str, year: int = 2021, utc: bool = False
) -> list[Record]:
    """Get Time-Series data from the SQL File."""
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
    """Convert the data from J to kWh."""

    df = pd.DataFrame(_data)
    if not df.empty:
        df["Value"] = df["Value"].apply(lambda _: _ * 0.000000277778)
    return df


def df_in_m3hr(_data: list[Record]) -> pd.DataFrame:
    """Convert the data from m3/s to m3/hr."""

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
    """Create a line plot figure from the DataFrame."""

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
    """Create an HTML file, but remove it if it already exists."""

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
