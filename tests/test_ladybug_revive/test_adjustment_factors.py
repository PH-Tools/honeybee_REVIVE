from pathlib import Path
import pandas as pd

from ladybug.epw import EPW
from ladybug.stat import STAT

from ladybug_revive import resiliency_epw


def test_period_morphing_factors_from_winter_csv():
    with open(
        Path("tests/test_ladybug_revive/_source/MN_Roch_AP/USA_MN_Roch_Intl_AP_726440_period_data_winter.csv")
    ) as f:
        data = pd.read_csv(f)

    # --------------------------------------------------------------------------------------------------------------
    # -- Calculate the Phius-REVIVE Weather-Morphing Factors
    dry_bulb_factor, dew_point_factor = resiliency_epw.calculate_winter_morphing_factors(
        -32.6,
        data["Dry Bulb Temperature {C}"],
        -32.6,
        data["Dew Point Temperature {C}"],
    )

    assert dry_bulb_factor == 12.208218363106132
    assert dew_point_factor == 38.41817806003023


def test_period_morphing_factors_from_summer_csv_Jun29():
    with open(
        Path("tests/test_ladybug_revive/_source/MN_Roch_AP/USA_MN_Roch_Intl_AP_726440_period_summer_Jun29.csv")
    ) as f:
        data = pd.read_csv(f)

    # --------------------------------------------------------------------------------------------------------------
    # -- Calculate the Phius-REVIVE Weather-Morphing Factors
    dry_bulb_factor, dew_point_factor = resiliency_epw.calculate_summer_morphing_factors(
        36.8,
        data["Dry Bulb Temperature {C}"],
        26.7,
        data["Dew Point Temperature {C}"],
    )

    assert dry_bulb_factor == 7.414380217261422
    assert dew_point_factor == 4.339485741255028


def test_period_morphing_factors_from_summer_csv_Jul29():
    with open(
        Path("tests/test_ladybug_revive/_source/MN_Roch_AP/USA_MN_Roch_Intl_AP_726440_period_summer_Jul29.csv")
    ) as f:
        data = pd.read_csv(f)

    # --------------------------------------------------------------------------------------------------------------
    # -- Calculate the Phius-REVIVE Weather-Morphing Factors
    dry_bulb_factor, dew_point_factor = resiliency_epw.calculate_summer_morphing_factors(
        36.8,
        data["Dry Bulb Temperature {C}"],
        26.7,
        data["Dew Point Temperature {C}"],
    )

    assert dry_bulb_factor == 7.914965551813527
    assert dew_point_factor == 3.7937954982283815


def test_winter_morphing_factors_Rochester_Minnesota_AP():
    folder = Path("tests/test_ladybug_revive/_source/MN_Roch_AP")
    lb_epw = EPW(str((folder / "USA_MN_Rochester.Intl.AP.726440_TMY3.epw").resolve()))
    lb_stat = STAT(str((folder / "USA_MN_Rochester.Intl.AP.726440_TMY3.stat").resolve()))
    outage_period, _ = resiliency_epw.get_outage_period(lb_stat.extreme_cold_week)

    assert outage_period._st_time.int_hoy == 625  # (January 27th, 01:00)
    assert outage_period._end_time.int_hoy == 792  # (Feb 3rd, 00:00)
    assert len(outage_period) == 168

    # --------------------------------------------------------------------------------------------------------------
    # -- Get the raw EPW data
    full_hourly_dry_bulb_deg_C = lb_epw.dry_bulb_temperature
    full_hourly_dew_point_deg_C = lb_epw.dew_point_temperature

    # --------------------------------------------------------------------------------------------------------------
    # -- Slice out the Winter period hourly data from the EPW
    hourly_dry_bulb_deg_C = resiliency_epw.apply_analysis_period_to_data(full_hourly_dry_bulb_deg_C, outage_period)
    hourly_dew_point_deg_C = resiliency_epw.apply_analysis_period_to_data(full_hourly_dew_point_deg_C, outage_period)

    assert len(hourly_dew_point_deg_C) == 168
    assert len(hourly_dew_point_deg_C) == 168

    # --------------------------------------------------------------------------------------------------------------
    # -- Calculate the Phius-REVIVE Weather-Morphing Factors
    dry_bulb_factor, dew_point_factor = resiliency_epw.calculate_winter_morphing_factors(
        -32.6,
        hourly_dry_bulb_deg_C,
        -32.6,
        hourly_dew_point_deg_C,
    )

    assert dry_bulb_factor == 12.208218363106132
    assert dew_point_factor == 38.41817806003023


def test_summer_morphing_factors_Rochester_Minnesota_AP():
    folder = Path("tests/test_ladybug_revive/_source/MN_Roch_AP")
    lb_epw = EPW(str((folder / "USA_MN_Rochester.Intl.AP.726440_TMY3.epw").resolve()))
    lb_stat = STAT(str((folder / "USA_MN_Rochester.Intl.AP.726440_TMY3.stat").resolve()))

    outage_period, _ = resiliency_epw.get_outage_period(lb_stat.extreme_hot_week)

    assert outage_period._st_time.int_hoy == 4297  # (June 29th, 01:00)
    assert outage_period._end_time.int_hoy == 4464  # (July 6th, 00:00)
    assert len(outage_period) == 168

    # --------------------------------------------------------------------------------------------------------------
    # -- Slice out the Summer period hourly data from the EPW
    hourly_dry_bulb_deg_C = resiliency_epw.apply_analysis_period_to_data(lb_epw.dry_bulb_temperature, outage_period)
    hourly_dew_point_deg_C = resiliency_epw.apply_analysis_period_to_data(lb_epw.dew_point_temperature, outage_period)

    # --------------------------------------------------------------------------------------------------------------
    # -- Calculate the Phius-REVIVE Weather-Morphing Factors
    dry_bulb_factor, dew_point_factor = resiliency_epw.calculate_summer_morphing_factors(
        36.8,
        hourly_dry_bulb_deg_C,
        26.7,
        hourly_dew_point_deg_C,
    )

    assert dry_bulb_factor == 7.414380217261422
    assert dew_point_factor == 4.339485741255028
