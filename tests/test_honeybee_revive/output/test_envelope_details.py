# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Tests for the winter envelope-details charts on ground-contact and Kiva floors.

EnergyPlus does not report 'Surface Average Face Conduction Heat Transfer Energy' or
'Surface Heat Storage Energy' for surfaces with a Kiva 'Foundation' boundary condition
(ExtBoundCond -6); it does report 'Surface Inside Face Conduction Heat Transfer Energy'.
"""

import sqlite3
from contextlib import closing
from datetime import datetime

import pytest

from honeybee_revive.output import resilience_winter_graphs
from honeybee_revive.output.resilience_winter_graphs import Filepaths, write_envelope_details_plots
from tests.test_honeybee_revive.output._eplus_sql import write_eplus_sql

AVG_FACE = "Surface Average Face Conduction Heat Transfer Energy"
INSIDE_FACE = "Surface Inside Face Conduction Heat Transfer Energy"
STORAGE = "Surface Heat Storage Energy"

# -- (SurfaceName, ClassName, ExtBoundCond)
SURFACES = (
    ("WALL_OUTDOORS", "Wall", 0),
    ("FLOOR_GROUND", "Floor", -1),
    ("FLOOR_KIVA", "Floor", -6),
    ("WALL_INTERZONE", "Wall", 5),
)
# -- (Variable, SurfaceName): Kiva reports inside-face only, as EnergyPlus does.
SERIES = (
    (AVG_FACE, "WALL_OUTDOORS"),
    (AVG_FACE, "FLOOR_GROUND"),
    (AVG_FACE, "WALL_INTERZONE"),
    (STORAGE, "WALL_OUTDOORS"),
    (STORAGE, "FLOOR_GROUND"),
    (INSIDE_FACE, "WALL_OUTDOORS"),
    (INSIDE_FACE, "FLOOR_GROUND"),
    (INSIDE_FACE, "FLOOR_KIVA"),
)


@pytest.fixture
def envelope_sql(tmp_path):
    """A minimal SQL with the tables the envelope-details plots read. 1 kWh per hour for one day."""
    sql_path = write_eplus_sql(
        tmp_path / "eplusout.sql", datetime(2025, 1, 1), datetime(2025, 1, 1), SERIES, value=lambda _: 3600000.0
    )
    with closing(sqlite3.connect(sql_path)) as conn:
        conn.execute(
            "CREATE TABLE Surfaces (SurfaceIndex INTEGER, SurfaceName TEXT, ClassName TEXT, Area REAL, "
            "GrossArea REAL, Tilt REAL, ZoneIndex INTEGER, ExtBoundCond INTEGER, ConstructionIndex INTEGER)"
        )
        conn.execute("CREATE TABLE Constructions (ConstructionIndex INTEGER, Name TEXT, UValue REAL)")
        conn.executemany(
            "INSERT INTO Surfaces VALUES (?, ?, ?, 10.0, 10.0, 90.0, 1, ?, 1)",
            [(i, name, class_name, bc) for i, (name, class_name, bc) in enumerate(SURFACES, start=1)],
        )
        conn.execute("INSERT INTO Constructions VALUES (1, 'CONSTRUCTION', 0.2)")
        conn.commit()
    return sql_path


@pytest.fixture
def figures(envelope_sql, tmp_path, monkeypatch):
    """Capture the envelope-details figures by div_id instead of writing the HTML."""
    captured = {}

    def _capture(_filepath, _figures):
        captured.update({div_id: fig for fig, div_id in _figures})

    monkeypatch.setattr(resilience_winter_graphs, "write_figures_to_html", _capture)
    write_envelope_details_plots(Filepaths(envelope_sql, tmp_path))
    return captured


def _trace_values(fig) -> dict[str, list[float]]:
    return {trace.name: list(trace.y) for trace in fig.data}


def test_conduction_chart_includes_kiva_floor_from_inside_face(figures):
    """A Kiva floor has no average-face output, so its inside-face conduction is charted, labeled."""
    traces = _trace_values(figures["envelope_fig1"])

    assert traces["FLOOR_KIVA (inside face)"] == pytest.approx([1.0] * 24, abs=1e-5)
    assert "FLOOR_KIVA" not in traces


def test_conduction_chart_includes_ground_floor_and_excludes_interzone(figures):
    """Every surface facing the outdoors or the ground is charted; interzone surfaces are not."""
    traces = _trace_values(figures["envelope_fig1"])

    assert set(traces) == {"WALL_OUTDOORS", "FLOOR_GROUND", "FLOOR_KIVA (inside face)"}


def test_storage_chart_states_kiva_floors_are_omitted(figures):
    """EnergyPlus reports no heat storage for Kiva floors, and the chart title says so."""
    fig = figures["envelope_fig5"]

    assert set(_trace_values(fig)) == {"WALL_OUTDOORS", "FLOOR_GROUND"}
    assert "Kiva" in fig.layout.title.text
