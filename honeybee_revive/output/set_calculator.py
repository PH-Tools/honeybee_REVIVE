"""Measure-free winter Standard Effective Temperature calculation."""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Iterable

import pandas as pd
from ladybug_comfort.pmv import pierce_set

from honeybee_revive.output._shared import Record

# EnergyPlus ThermalComfort Pierce-model constants, also used by ladybug-comfort.
BODY_SURFACE_AREA_M2 = 1.8258
METABOLIC_RATE_W_M2_PER_MET = 58.2

# Phius REVIVE 2024 section 6.3.2 winter assumptions.
ACTIVITY_LEVEL_W_PER_PERSON = 120.0
AIR_SPEED_M_S = 0.16
CLOTHING_INSULATION_CLO = 1.0
EXTERNAL_WORK_MET = 0.0

RecordKey = tuple[str, datetime]
RecordInput = Iterable[Record] | pd.DataFrame


class SetInputError(ValueError):
    """Raised when winter SET input records do not align one-to-one."""


def met_from_activity_level(activity_level_w_per_person: float) -> float:
    """Convert whole-person activity in watts to metabolic rate in met.

    Arguments:
    ----------
        * activity_level_w_per_person (float): Whole-person activity level in watts.

    Returns:
    --------
        * float: Metabolic rate in met.
    """
    return activity_level_w_per_person / (BODY_SURFACE_AREA_M2 * METABOLIC_RATE_W_M2_PER_MET)


def _iter_records(records: RecordInput, label: str) -> Iterable[Record]:
    """Yield Records from a Record iterable or long-form DataFrame."""
    if isinstance(records, pd.DataFrame):
        required_columns = {"Date", "Value", "Zone"}
        missing_columns = required_columns - set(records.columns)
        if missing_columns:
            raise SetInputError(
                "SET {} DataFrame is missing required column(s): {}.".format(label, ", ".join(sorted(missing_columns)))
            )
        for date, value, zone in records.loc[:, ["Date", "Value", "Zone"]].itertuples(index=False, name=None):
            yield Record(date, value, zone)
    else:
        yield from records


def _records_by_key(records: RecordInput, label: str) -> dict[RecordKey, Record]:
    """Index records by zone and timestamp, rejecting duplicate keys."""
    records_by_key = {}
    for record in _iter_records(records, label):
        if not isinstance(record.Date, datetime):
            raise SetInputError(
                "SET {} record for zone '{}' has a non-datetime timestamp: {!r}.".format(
                    label, record.Zone, record.Date
                )
            )
        key = (record.Zone, record.Date)
        if key in records_by_key:
            raise SetInputError(
                "SET input contains duplicate {} key for zone '{}' at {}.".format(label, record.Zone, record.Date)
            )
        records_by_key[key] = record
    return records_by_key


def _validate_matching_keys(
    reference: dict[RecordKey, Record],
    candidate: dict[RecordKey, Record],
    candidate_label: str,
) -> None:
    """Require a candidate series to have exactly the reference keys."""
    missing = reference.keys() - candidate.keys()
    extra = candidate.keys() - reference.keys()
    if missing or extra:
        details = []
        if missing:
            zone, date = min(missing, key=lambda key: (str(key[0]), str(key[1])))
            details.append("missing {} key(s), for example zone '{}' at {}".format(len(missing), zone, date))
        if extra:
            zone, date = min(extra, key=lambda key: (str(key[0]), str(key[1])))
            details.append("extra {} key(s), for example zone '{}' at {}".format(len(extra), zone, date))
        raise SetInputError("SET {} keys do not match air temperature: {}.".format(candidate_label, "; ".join(details)))


def _validate_hourly(records_by_key: dict[RecordKey, Record]) -> None:
    """Require every zone series to be contiguous at one-hour intervals."""
    dates_by_zone: dict[str, list[datetime]] = defaultdict(list)
    for zone, date in records_by_key:
        dates_by_zone[zone].append(date)

    for zone, dates in dates_by_zone.items():
        awareness = {date.utcoffset() is not None for date in dates}
        if len(awareness) > 1:
            raise SetInputError("SET timestamps must use consistent timezone awareness for zone '{}'.".format(zone))
        dates.sort()
        for previous, current in zip(dates, dates[1:]):
            interval = current - previous
            if interval != timedelta(hours=1):
                raise SetInputError(
                    "SET inputs must be hourly for zone '{}'; found interval {} between {} and {}.".format(
                        zone, interval, previous, current
                    )
                )


def validate_set_inputs(
    air_temperature: RecordInput,
    mean_radiant_temperature: RecordInput,
    relative_humidity: RecordInput,
) -> tuple[dict[RecordKey, Record], dict[RecordKey, Record], dict[RecordKey, Record]]:
    """Validate and index the three hourly SET input series.

    Each input may be an iterable of Records or a long-form DataFrame with
    ``Date``, ``Value``, and ``Zone`` columns.

    Returns:
    --------
        * tuple[dict, dict, dict]: Air-temperature, mean-radiant-temperature,
          and relative-humidity Records keyed by ``(Zone, Date)``.

    Raises:
    -------
        * SetInputError: If inputs are empty, duplicated, misaligned, or not
          contiguous hourly series.
    """
    air_by_key = _records_by_key(air_temperature, "air temperature")
    radiant_by_key = _records_by_key(mean_radiant_temperature, "mean radiant temperature")
    humidity_by_key = _records_by_key(relative_humidity, "relative humidity")
    if not air_by_key:
        raise SetInputError("SET calculation requires at least one hourly input record.")

    _validate_matching_keys(air_by_key, radiant_by_key, "mean radiant temperature")
    _validate_matching_keys(air_by_key, humidity_by_key, "relative humidity")
    _validate_hourly(air_by_key)
    return air_by_key, radiant_by_key, humidity_by_key


def calculate_set(
    air_temperature: RecordInput,
    mean_radiant_temperature: RecordInput,
    relative_humidity: RecordInput,
    activity_level_w_per_person: float = ACTIVITY_LEVEL_W_PER_PERSON,
    air_speed_m_s: float = AIR_SPEED_M_S,
    clothing_insulation_clo: float = CLOTHING_INSULATION_CLO,
    external_work_met: float = EXTERNAL_WORK_MET,
) -> list[Record]:
    """Calculate winter SET records from aligned hourly zone conditions.

    Arguments:
    ----------
        * air_temperature (RecordInput): Zone air-temperature records in C.
        * mean_radiant_temperature (RecordInput): Zone MRT records in C.
        * relative_humidity (RecordInput): Zone relative-humidity records in percent.
        * activity_level_w_per_person (float): Whole-person activity in watts.
        * air_speed_m_s (float): Air speed in m/s.
        * clothing_insulation_clo (float): Clothing insulation in clo.
        * external_work_met (float): External work in met.

    Returns:
    --------
        * list[Record]: Long-form SET records in C, preserving the air-input order.

    Raises:
    -------
        * SetInputError: If the three input series do not align one-to-one at
          contiguous hourly intervals.
    """
    air_by_key, radiant_by_key, humidity_by_key = validate_set_inputs(
        air_temperature, mean_radiant_temperature, relative_humidity
    )
    metabolic_rate = met_from_activity_level(activity_level_w_per_person)

    return [
        Record(
            air_record.Date,
            pierce_set(
                air_record.Value,
                radiant_by_key[key].Value,
                air_speed_m_s,
                humidity_by_key[key].Value,
                metabolic_rate,
                clothing_insulation_clo,
                external_work_met,
            ),
            air_record.Zone,
        )
        for key, air_record in air_by_key.items()
    ]
