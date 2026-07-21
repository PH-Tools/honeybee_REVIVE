"""Tests for the EnergyPlus RunPeriod length produced by get_outage_period().

Phius REVIVE models a 7-day (168 hr) outage. The simulation adds a 1-day warm-up and a
1-day cool-down, so the run must be 24 + 168 + 24 = 216 hours over exactly 9 CALENDAR DAYS.

The calendar-day count matters as much as the hour count: EnergyPlus 'RunPeriod' is
date-based, not hour-based, so a 216-hour period that happens to touch 10 dates makes E+
simulate 10 full days (240 hrs). That over-run then trips the winter-SET post-processing,
which requires exactly 216 hourly records per zone.

Regression guard for exactly that: the expanded period used to be built from the '+1 hour'
offset-corrected week, which ends at hour-0 of the following day and therefore spanned 10
dates.
"""

from pathlib import Path

from ladybug.stat import STAT

from ladybug_revive import resiliency_epw

EXPECTED_OUTAGE_HOURS = 168
EXPECTED_RUN_HOURS = 24 + EXPECTED_OUTAGE_HOURS + 24
EXPECTED_RUN_DAYS = 9

STAT_FILE = (
    Path("tests/test_ladybug_revive/_source/MN_Roch_AP") / "USA_MN_Rochester.Intl.AP.726440_TMY3.stat"
)


def _stat():
    return STAT(str(STAT_FILE.resolve()))


def _calendar_days(period):
    return len({(dt.month, dt.day) for dt in period.datetimes})


# -----------------------------------------------------------------------------
# -- The 168-hour outage window (drives the EPW morphing)


def test_winter_outage_window_is_168_hours():
    outage, _ = resiliency_epw.get_outage_period(_stat().extreme_cold_week)
    assert len(outage) == EXPECTED_OUTAGE_HOURS


def test_summer_outage_window_is_168_hours():
    outage, _ = resiliency_epw.get_outage_period(_stat().extreme_hot_week)
    assert len(outage) == EXPECTED_OUTAGE_HOURS


def test_outage_window_keeps_the_one_hour_offset_correction():
    """The morphing window is deliberately shifted +1hr off the raw STAT week."""
    raw = _stat().extreme_cold_week
    outage, _ = resiliency_epw.get_outage_period(raw)

    assert outage._st_time.int_hoy == raw._st_time.int_hoy + 1
    assert outage._end_time.int_hoy == raw._end_time.int_hoy + 1


# -----------------------------------------------------------------------------
# -- The 216-hour run period (drives the EnergyPlus RunPeriod)


def test_winter_run_period_is_216_hours():
    _, expanded = resiliency_epw.get_outage_period(_stat().extreme_cold_week)
    assert len(expanded) == EXPECTED_RUN_HOURS


def test_summer_run_period_is_216_hours():
    _, expanded = resiliency_epw.get_outage_period(_stat().extreme_hot_week)
    assert len(expanded) == EXPECTED_RUN_HOURS


def test_winter_run_period_spans_exactly_nine_calendar_days():
    """Regression: a 216-hour period touching 10 dates makes E+ run 240 hours."""
    _, expanded = resiliency_epw.get_outage_period(_stat().extreme_cold_week)
    assert _calendar_days(expanded) == EXPECTED_RUN_DAYS


def test_summer_run_period_spans_exactly_nine_calendar_days():
    _, expanded = resiliency_epw.get_outage_period(_stat().extreme_hot_week)
    assert _calendar_days(expanded) == EXPECTED_RUN_DAYS


def test_run_period_is_day_aligned():
    """Must start at hour 0 and end at hour 23, or E+ pulls in an extra date."""
    for week in (_stat().extreme_cold_week, _stat().extreme_hot_week):
        _, expanded = resiliency_epw.get_outage_period(week)
        assert expanded.st_hour == 0
        assert expanded.end_hour == 23


def test_run_period_brackets_the_raw_extreme_week_by_one_day():
    """One day of warm-up before, one day of cool-down after."""
    raw = _stat().extreme_cold_week
    _, expanded = resiliency_epw.get_outage_period(raw)

    assert expanded._st_time.int_hoy == raw._st_time.int_hoy - 24
    assert expanded._end_time.int_hoy == raw._end_time.int_hoy + 24
