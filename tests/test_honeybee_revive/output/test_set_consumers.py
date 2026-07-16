"""Tests for the shared computed-SET graph and JSON consumers."""

import json
import shutil
import sqlite3
from pathlib import Path

import pytest

from honeybee_revive.output.resilience_set_data import write_winter_set_json
from honeybee_revive.output.resilience_winter_graphs import Filepaths, write_SET_temp_plots

FIXTURE_PATH = Path(__file__).parents[2] / "_fixtures" / "winter_set_contract.sql"
REFERENCE_SET_VARIABLE = "Zone Thermal Comfort Pierce Model Standard Effective Temperature"
ZONE_NAME = "ROOM_1_3B02CCA3"


def _fixture_without_reference_set(tmp_path: Path) -> Path:
    """Copy the fixture and remove the measure-era Pierce SET series."""
    fixture_path = tmp_path / "winter_without_reference_set.sql"
    shutil.copyfile(FIXTURE_PATH, fixture_path)
    with sqlite3.connect(fixture_path) as connection:
        connection.execute(
            "DELETE FROM ReportData WHERE ReportDataDictionaryIndex IN "
            "(SELECT ReportDataDictionaryIndex FROM ReportDataDictionary WHERE Name=?)",
            (REFERENCE_SET_VARIABLE,),
        )
        connection.execute("DELETE FROM ReportDataDictionary WHERE Name=?", (REFERENCE_SET_VARIABLE,))
    return fixture_path


def test_write_winter_set_json_preserves_contract_and_outage_window(tmp_path: Path) -> None:
    """The export writes only 168 hours with Date/Value/Zone keys."""
    json_path = tmp_path / "computed_set.json"
    result = write_winter_set_json(FIXTURE_PATH, json_path)
    payload = json.loads(json_path.read_text())

    assert len(payload) == 168
    assert all(set(record) == {"Date", "Value", "Zone"} for record in payload)
    assert {record["Zone"] for record in payload} == {ZONE_NAME}
    assert all(isinstance(record["Date"], int) for record in payload)
    assert payload[0]["Date"] == 1453852800000
    assert payload[-1]["Date"] == 1454454000000
    assert [record["Value"] for record in payload] == pytest.approx([record.Value for record in result.outage_records])


def test_graph_and_json_share_measure_free_set_calculation(tmp_path: Path) -> None:
    """Both consumers return identical SET values without the E+ Pierce series."""
    fixture_path = _fixture_without_reference_set(tmp_path)
    json_result = write_winter_set_json(fixture_path, tmp_path / "computed_set.json")
    graph_result = write_SET_temp_plots(Filepaths(fixture_path, tmp_path))

    assert (tmp_path / "winter_SET_temperature.html").is_file()
    assert {record.Zone for record in graph_result.full_records} == {ZONE_NAME}
    assert [record.Value for record in graph_result.full_records] == pytest.approx(
        [record.Value for record in json_result.full_records]
    )


def test_write_winter_set_json_removes_stale_output_on_failure(tmp_path: Path) -> None:
    """A failed calculation cannot leave old JSON for Grasshopper to consume."""
    invalid_sql_path = tmp_path / "invalid.sql"
    invalid_sql_path.touch()
    json_path = tmp_path / "computed_set.json"
    json_path.write_text('[{"stale": true}]')

    with pytest.raises(Exception):
        write_winter_set_json(invalid_sql_path, json_path)

    assert not json_path.exists()
