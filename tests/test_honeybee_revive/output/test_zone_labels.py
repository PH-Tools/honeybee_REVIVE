# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Tests for the chart-legend zone display-name mapping in output/_shared.py.

EnergyPlus names Zones after the Honeybee Room *identifier* ("03_NORTH_0ac0d721"), which
makes for unreadable chart legends. These helpers map back to the Room's display_name for
the plotted traces only -- the underlying `Record.Zone` value stays the raw E+ key, since
it flows into the CSV/JSON exports consumed by the Grasshopper wrapper and web report.
"""

import json

import pandas as pd
import pytest

from honeybee_revive.output import _shared
from honeybee_revive.output._shared import (
    build_zone_label_map,
    create_line_plot_figure,
    find_hbjson_beside_sql,
    load_zone_labels,
    zone_label,
)


@pytest.fixture(autouse=True)
def _clear_label_cache():
    """Keep the module-level cache from leaking between tests."""
    _shared._ZONE_LABELS = {}
    yield
    _shared._ZONE_LABELS = {}


def _write_hbjson(path, rooms):
    """rooms: list of (identifier, display_name)"""
    path.write_text(
        json.dumps({"rooms": [{"identifier": i, "display_name": d} for i, d in rooms]})
    )
    return path


# -----------------------------------------------------------------------------
# -- build_zone_label_map


def test_build_map_from_hbjson(tmp_path):
    f = _write_hbjson(tmp_path / "m.hbjson", [("03_NORTH_0ac0d721", "03_NORTH")])
    assert build_zone_label_map(f) == {"03_NORTH_0AC0D721": "03_NORTH"}


def test_build_map_falls_back_to_identifier_when_no_display_name(tmp_path):
    f = tmp_path / "m.hbjson"
    f.write_text(json.dumps({"rooms": [{"identifier": "RM_1"}]}))
    assert build_zone_label_map(f) == {"RM_1": "RM_1"}


def test_build_map_disambiguates_duplicate_display_names(tmp_path):
    """Two Rooms named 'Bedroom' must not produce two identical legend entries."""
    f = _write_hbjson(
        tmp_path / "m.hbjson",
        [("BEDROOM_aaaaaaaa", "Bedroom"), ("BEDROOM_bbbbbbbb", "Bedroom")],
    )
    labels = build_zone_label_map(f)

    assert len(set(labels.values())) == 2
    assert all(v.startswith("Bedroom [") for v in labels.values())


def test_build_map_leaves_unique_names_clean(tmp_path):
    f = _write_hbjson(tmp_path / "m.hbjson", [("A_1", "Attic"), ("B_1", "Basement")])
    assert set(build_zone_label_map(f).values()) == {"Attic", "Basement"}


# -----------------------------------------------------------------------------
# -- find_hbjson_beside_sql


def test_finds_hbjson_in_the_openstudio_layout(tmp_path):
    """<openstudio>/model.hbjson  +  <openstudio>/run/eplusout.sql"""
    run = tmp_path / "openstudio" / "run"
    run.mkdir(parents=True)
    hbjson = _write_hbjson(tmp_path / "openstudio" / "model.hbjson", [("A_1", "Attic")])
    sql = run / "eplusout.sql"
    sql.touch()

    assert find_hbjson_beside_sql(sql) == hbjson


def test_returns_none_when_no_hbjson_present(tmp_path):
    sql = tmp_path / "eplusout.sql"
    sql.touch()
    assert find_hbjson_beside_sql(sql) is None


# -----------------------------------------------------------------------------
# -- zone_label


def test_label_is_passthrough_when_cache_is_empty():
    """Un-loaded cache must behave exactly as before this feature existed."""
    assert zone_label("03_NORTH_0AC0D721") == "03_NORTH_0AC0D721"


def test_label_resolves_zone_level_key(tmp_path):
    load_zone_labels(_sql_for(tmp_path))
    assert zone_label("03_NORTH_0AC0D721") == "03_NORTH"


def test_label_resolves_enclosure_level_key(tmp_path):
    """Enclosure variables append '_SPACE' to the zone name."""
    load_zone_labels(_sql_for(tmp_path))
    assert zone_label("03_NORTH_0AC0D721_SPACE") == "03_NORTH"


def test_label_resolves_people_level_key(tmp_path):
    """Thermal-comfort/SET keys are '<space-name> <people-object-name>'."""
    load_zone_labels(_sql_for(tmp_path))
    assert zone_label("03_NORTH_0AC0D721_SPACE RV2024_RESILIENCE_PEOPLE") == "03_NORTH"


def test_label_is_case_insensitive(tmp_path):
    """E+ upper-cases its keys; the HBJSON identifier is lower-case."""
    load_zone_labels(_sql_for(tmp_path))
    assert zone_label("03_north_0ac0d721") == "03_NORTH"


def test_label_leaves_environment_key_alone(tmp_path):
    load_zone_labels(_sql_for(tmp_path))
    assert zone_label("Environment") == "Environment"


def test_label_leaves_surface_names_alone(tmp_path):
    """Surface keys share a prefix with the Room but are not Zones."""
    load_zone_labels(_sql_for(tmp_path))
    assert zone_label("03_NORTH_1_4627649B") == "03_NORTH_1_4627649B"


def test_label_leaves_empty_key_alone(tmp_path):
    load_zone_labels(_sql_for(tmp_path))
    assert zone_label("") == ""


# -----------------------------------------------------------------------------
# -- load_zone_labels


def test_load_is_safe_when_no_hbjson_found(tmp_path):
    sql = tmp_path / "eplusout.sql"
    sql.touch()
    assert load_zone_labels(sql) == {}
    assert zone_label("03_NORTH_0AC0D721") == "03_NORTH_0AC0D721"


def test_load_is_safe_when_hbjson_is_unreadable(tmp_path):
    run = tmp_path / "openstudio" / "run"
    run.mkdir(parents=True)
    (tmp_path / "openstudio" / "broken.hbjson").write_text("{not valid json")
    sql = run / "eplusout.sql"
    sql.touch()

    assert load_zone_labels(sql) == {}
    assert zone_label("03_NORTH_0AC0D721") == "03_NORTH_0AC0D721"


# -----------------------------------------------------------------------------
# -- create_line_plot_figure integration


def test_plot_traces_use_display_names(tmp_path):
    load_zone_labels(_sql_for(tmp_path))
    df = pd.DataFrame(
        [
            {"Date": pd.Timestamp("2021-01-01"), "Value": 1.0, "Zone": "03_NORTH_0AC0D721"},
            {"Date": pd.Timestamp("2021-01-01"), "Value": 2.0, "Zone": "01_SOUTH_2F9F20B9"},
        ]
    )
    fig = create_line_plot_figure(df, "test")

    assert sorted(t.name for t in fig.data) == ["01_SOUTH", "03_NORTH"]


def test_plot_traces_unchanged_without_labels():
    """No map loaded -> legends keep the raw E+ keys, as before."""
    df = pd.DataFrame(
        [{"Date": pd.Timestamp("2021-01-01"), "Value": 1.0, "Zone": "03_NORTH_0AC0D721"}]
    )
    fig = create_line_plot_figure(df, "test")

    assert [t.name for t in fig.data] == ["03_NORTH_0AC0D721"]


def test_plot_does_not_mutate_the_zone_column(tmp_path):
    """The exported CSV/JSON key must stay the raw E+ identifier."""
    load_zone_labels(_sql_for(tmp_path))
    df = pd.DataFrame(
        [{"Date": pd.Timestamp("2021-01-01"), "Value": 1.0, "Zone": "03_NORTH_0AC0D721"}]
    )
    create_line_plot_figure(df, "test")

    assert df["Zone"].tolist() == ["03_NORTH_0AC0D721"]


# -----------------------------------------------------------------------------


def _sql_for(tmp_path):
    """Build the standard openstudio layout and return the SQL path."""
    run = tmp_path / "openstudio" / "run"
    run.mkdir(parents=True)
    _write_hbjson(
        tmp_path / "openstudio" / "model.hbjson",
        [("03_NORTH_0ac0d721", "03_NORTH"), ("01_SOUTH_2f9f20b9", "01_SOUTH")],
    )
    sql = run / "eplusout.sql"
    sql.touch()
    return sql
