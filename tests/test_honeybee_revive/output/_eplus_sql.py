# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Build small synthetic EnergyPlus SQL files with the real Time/ReportData/view schema.

Each simulated hour writes the same Time rows EnergyPlus does for a 10-minute timestep run:
five sub-hourly rows (Hour = start hour, Minute 10..50), one sub-hourly row at the top of the
next hour, then the hourly row (IntervalType 1). Data is written for the hourly rows only.
"""

import sqlite3
from contextlib import closing
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Iterable

SCHEMA = (
    "CREATE TABLE Time (TimeIndex INTEGER PRIMARY KEY, Year INTEGER, Month INTEGER, Day INTEGER, "
    "Hour INTEGER, Minute INTEGER, Dst INTEGER, Interval INTEGER, IntervalType INTEGER, "
    "SimulationDays INTEGER, DayType TEXT, EnvironmentPeriodIndex INTEGER, WarmupFlag INTEGER)",
    "CREATE TABLE ReportDataDictionary(ReportDataDictionaryIndex INTEGER PRIMARY KEY, IsMeter INTEGER, "
    "Type TEXT, IndexGroup TEXT, TimestepType TEXT, KeyValue TEXT, Name TEXT, ReportingFrequency TEXT, "
    "ScheduleName TEXT, Units TEXT)",
    "CREATE TABLE ReportData (ReportDataIndex INTEGER PRIMARY KEY, TimeIndex INTEGER, "
    "ReportDataDictionaryIndex INTEGER, Value REAL)",
    "CREATE TABLE ReportExtendedData (ReportExtendedDataIndex INTEGER PRIMARY KEY, ReportDataIndex INTEGER, "
    "MaxValue REAL, MaxMonth INTEGER, MaxDay INTEGER, MaxHour INTEGER, MaxStartMinute INTEGER, "
    "MaxMinute INTEGER, MinValue REAL, MinMonth INTEGER, MinDay INTEGER, MinHour INTEGER, "
    "MinStartMinute INTEGER, MinMinute INTEGER)",
    "CREATE VIEW ReportVariableWithTime AS SELECT rd.ReportDataIndex, rd.TimeIndex, "
    "rd.ReportDataDictionaryIndex, red.ReportExtendedDataIndex, rd.Value, t.Month, t.Day, t.Hour, "
    "t.Minute, t.Dst, t.Interval, t.IntervalType, t.SimulationDays, t.DayType, t.EnvironmentPeriodIndex, "
    "t.WarmupFlag, rdd.IsMeter, rdd.Type, rdd.IndexGroup, rdd.TimestepType, rdd.KeyValue, rdd.Name, "
    "rdd.ReportingFrequency, rdd.ScheduleName, rdd.Units, red.MaxValue, red.MaxMonth, red.MaxDay, "
    "red.MaxStartMinute, red.MaxMinute, red.MinValue, red.MinMonth, red.MinDay, red.MinStartMinute, "
    "red.MinMinute FROM ReportData As rd INNER JOIN ReportDataDictionary As rdd "
    "ON rd.ReportDataDictionaryIndex = rdd.ReportDataDictionaryIndex LEFT OUTER JOIN ReportExtendedData "
    "As red ON rd.ReportDataIndex = red.ReportDataIndex INNER JOIN Time As t ON rd.TimeIndex = t.TimeIndex",
)


def write_eplus_sql(
    sql_path: Path,
    run_start: datetime,
    run_end: datetime,
    series: Iterable[tuple[str, str]],
    value: Callable[[int], float] = float,
) -> Path:
    """Write an hourly run period from run_start (00:00) through the end of run_end's day.

    Arguments:
    ----------
        * sql_path (Path): The SQL file to create.
        * run_start (datetime): First day of the RunPeriod.
        * run_end (datetime): Last day of the RunPeriod (simulated through hour 24).
        * series (Iterable[tuple[str, str]]): (Variable Name, KeyValue) pairs to report hourly.
        * value (Callable[[int], float]): Hour index from the run start -> reported value.

    Returns:
    --------
        * Path: The written SQL file.
    """
    series = list(series)
    hours = int((run_end + timedelta(days=1) - run_start).total_seconds() // 3600)
    with closing(sqlite3.connect(sql_path)) as conn:
        for statement in SCHEMA:
            conn.execute(statement)
        conn.executemany(
            "INSERT INTO ReportDataDictionary VALUES (?, 0, 'Avg', 'Zone', 'Zone', ?, ?, 'Hourly', '', '')",
            [(i, key, name) for i, (name, key) in enumerate(series, start=1)],
        )

        time_rows = []
        data_rows = []
        for h in range(hours):
            begin = run_start + timedelta(hours=h)
            day_type = begin.strftime("%A")
            sim_day = h // 24 + 1
            for minute in (10, 20, 30, 40, 50):
                time_rows.append((begin.year, begin.month, begin.day, begin.hour, minute, 10, -1, sim_day, day_type))
            for interval, interval_type in ((10, -1), (60, 1)):
                time_rows.append(
                    (begin.year, begin.month, begin.day, begin.hour + 1, 0, interval, interval_type, sim_day, day_type)
                )
            hourly_time_index = len(time_rows)
            data_rows.extend((hourly_time_index, i, value(h)) for i in range(1, len(series) + 1))

        conn.executemany(
            "INSERT INTO Time (Year, Month, Day, Hour, Minute, Dst, Interval, IntervalType, SimulationDays, "
            "DayType, EnvironmentPeriodIndex, WarmupFlag) VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?, ?, 1, 0)",
            time_rows,
        )
        conn.executemany(
            "INSERT INTO ReportData (TimeIndex, ReportDataDictionaryIndex, Value) VALUES (?, ?, ?)",
            data_rows,
        )
        conn.commit()
    return sql_path
