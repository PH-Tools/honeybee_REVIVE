"""Build the trimmed winter SET SQLite fixture from an EnergyPlus result file."""

import argparse
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Sequence

VARIABLE_NAMES = (
    "Zone Mean Air Temperature",
    "Zone Mean Radiant Temperature",
    "Zone Air Relative Humidity",
    "Zone Thermal Comfort Pierce Model Standard Effective Temperature",
)
TABLE_NAMES = ("Time", "ReportDataDictionary", "ReportData", "ReportExtendedData")


def _insert_rows(
    connection: sqlite3.Connection,
    table_name: str,
    rows: Sequence[tuple],
) -> None:
    """Insert rows into a table using its existing column order."""
    if not rows:
        return
    placeholders = ", ".join("?" for _ in rows[0])
    connection.executemany(
        "INSERT INTO {} VALUES ({})".format(table_name, placeholders),
        rows,
    )


def _variable_placeholders() -> str:
    """Return SQLite placeholders for the selected output variables."""
    return ", ".join("?" for _ in VARIABLE_NAMES)


def _populate_fixture(source: sqlite3.Connection, target: sqlite3.Connection) -> None:
    """Copy the selected schemas and time series into a fixture database."""
    for table_name in TABLE_NAMES:
        schema = source.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        ).fetchone()[0]
        target.execute(schema)

    variable_filter = _variable_placeholders()
    dictionary_rows = source.execute(
        "SELECT * FROM ReportDataDictionary WHERE Name IN ({}) "
        "AND ReportingFrequency = 'Hourly' "
        "ORDER BY ReportDataDictionaryIndex".format(variable_filter),
        VARIABLE_NAMES,
    ).fetchall()
    time_rows = source.execute(
        "SELECT DISTINCT t.* FROM Time AS t "
        "INNER JOIN ReportData AS rd ON rd.TimeIndex = t.TimeIndex "
        "INNER JOIN ReportDataDictionary AS rdd "
        "ON rd.ReportDataDictionaryIndex = rdd.ReportDataDictionaryIndex "
        "WHERE rdd.Name IN ({}) "
        "AND rdd.ReportingFrequency = 'Hourly' "
        "AND t.DayType NOT IN ('WinterDesignDay', 'SummerDesignDay') "
        "ORDER BY t.TimeIndex".format(variable_filter),
        VARIABLE_NAMES,
    ).fetchall()
    report_rows = source.execute(
        "SELECT rd.* FROM ReportData AS rd "
        "INNER JOIN Time AS t ON rd.TimeIndex = t.TimeIndex "
        "INNER JOIN ReportDataDictionary AS rdd "
        "ON rd.ReportDataDictionaryIndex = rdd.ReportDataDictionaryIndex "
        "WHERE rdd.Name IN ({}) "
        "AND rdd.ReportingFrequency = 'Hourly' "
        "AND t.DayType NOT IN ('WinterDesignDay', 'SummerDesignDay') "
        "ORDER BY rd.ReportDataIndex".format(variable_filter),
        VARIABLE_NAMES,
    ).fetchall()

    for table_name, rows in (
        ("Time", time_rows),
        ("ReportDataDictionary", dictionary_rows),
        ("ReportData", report_rows),
    ):
        _insert_rows(target, table_name, rows)

    view_schema = source.execute(
        "SELECT sql FROM sqlite_master " "WHERE type='view' AND name='ReportVariableWithTime'"
    ).fetchone()[0]
    target.execute(view_schema)
    target.commit()
    target.execute("VACUUM")
    integrity = target.execute("PRAGMA integrity_check").fetchone()[0]
    if integrity != "ok":
        raise RuntimeError("Generated SQLite fixture failed integrity check: {}".format(integrity))


def build_fixture(source_path: Path, target_path: Path) -> None:
    """Atomically write a trimmed SQLite winter SET fixture."""
    source_path = source_path.resolve()
    target_path = target_path.resolve()
    if source_path == target_path:
        raise ValueError("Source and target SQLite paths must be different.")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = target_path.with_suffix("{}.tmp".format(target_path.suffix))
    temporary_path.unlink(missing_ok=True)

    try:
        source_uri = "file:{}?mode=ro".format(source_path)
        with closing(sqlite3.connect(source_uri, uri=True)) as source:
            with closing(sqlite3.connect(temporary_path)) as target:
                _populate_fixture(source, target)
        temporary_path.replace(target_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def main(args: Sequence[str] | None = None) -> None:
    """Build a fixture from command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source EnergyPlus eplusout.sql")
    parser.add_argument("target", type=Path, help="Target trimmed SQLite fixture")
    parsed = parser.parse_args(args)
    build_fixture(parsed.source, parsed.target)


if __name__ == "__main__":
    main()
