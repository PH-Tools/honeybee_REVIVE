# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""A script to generate the Summer Resiliency Graphs.

This script is called from the command line with the following arguments:
    * [0] (str): The path to the Python script (this file).
    * [1] (str): The path to the EnergyPlus SQL file to read in.
    * [2] (str): The path to the output folder for the graphs.
"""

import os
import sys
from collections import namedtuple
from pathlib import Path

import pandas as pd

from honeybee_revive.output._shared import (
    InputFileError,
    create_line_plot_figure,
    df_in_kWh,
    get_time_series_data,
    write_figures_to_html,
)

Filepaths = namedtuple("Filepaths", ["sql", "graphs"])


def resolve_paths(_args: list[str]) -> Filepaths:
    """Sort out the file input and output paths. Make the output directory if needed.

    Arguments:
    ----------
        * _args (list[str]): sys.args list of input arguments.

    Returns:
    --------
        * Filepaths
    """

    assert len(_args) == 3, "Error: Incorrect number of arguments."

    # -----------------------------------------------------------------------------------
    # -- The EnergyPlus SQL input file.
    results_sql_file = Path(_args[1])
    if not results_sql_file.exists():
        raise InputFileError(results_sql_file)

    # -----------------------------------------------------------------------------------
    # -- Preview-Tables output folder:
    target_graphs_dir = Path(_args[2])
    if not target_graphs_dir.exists():
        print(f"\t>> Creating the directory: {target_graphs_dir}")
        os.mkdir(target_graphs_dir)

    return Filepaths(results_sql_file, target_graphs_dir)


def write_outdoor_environment_plots(file_paths: Filepaths) -> None:
    env_drybulb_C = get_time_series_data(file_paths.sql, "Site Outdoor Air Drybulb Temperature")
    env_RH = get_time_series_data(file_paths.sql, "Site Outdoor Air Relative Humidity")
    env_wind_speed_m3s = get_time_series_data(file_paths.sql, "Site Wind Speed")
    env_air_pressure_Pa = get_time_series_data(file_paths.sql, "Site Outdoor Air Barometric Pressure")

    write_figures_to_html(
        file_paths.graphs / "summer_outdoor_environment.html",
        [
            (
                create_line_plot_figure(pd.DataFrame(env_drybulb_C), "Outdoor Air Dry-Bulb Temp. [C]"),
                "env_fig1",
            ),
            (
                create_line_plot_figure(pd.DataFrame(env_RH), "Outdoor Air Relative Humidity [%]"),
                "env_fig2",
            ),
            (
                create_line_plot_figure(pd.DataFrame(env_wind_speed_m3s), "Outdoor Wind Speed [m/s]"),
                "env_fig3",
            ),
            (
                create_line_plot_figure(pd.DataFrame(env_air_pressure_Pa), "Outdoor Air Pressure [Pa]"),
                "env_fig4",
            ),
        ],
    )


def write_heat_index_plots(file_paths: Filepaths) -> None:
    heat_index = get_time_series_data(file_paths.sql, "Zone Heat Index")
    drybulb_C = get_time_series_data(file_paths.sql, "Zone Mean Air Temperature")
    zone_RH = get_time_series_data(file_paths.sql, "Zone Air Relative Humidity")
    env_drybulb_C = get_time_series_data(file_paths.sql, "Site Outdoor Air Drybulb Temperature")
    env_RH = get_time_series_data(file_paths.sql, "Site Outdoor Air Relative Humidity")

    hi_df = pd.DataFrame(heat_index)
    hi_fig1 = create_line_plot_figure(hi_df, "Zone Heat Index [C]", [26.7, 32.2, 39.4, 51.7])
    hi_fig1.add_annotation(
        x=hi_df["Date"].min(),
        y=26.7 + 2,
        showarrow=False,
        text="Caution",
        xanchor="left",
    )
    hi_fig1.add_annotation(
        x=hi_df["Date"].min(),
        y=32.2 + 2,
        showarrow=False,
        text="Warning",
        xanchor="left",
    )
    hi_fig1.add_annotation(
        x=hi_df["Date"].min(),
        y=39.4 + 2,
        showarrow=False,
        text="Danger",
        xanchor="left",
    )
    hi_fig1.add_annotation(
        x=hi_df["Date"].min(),
        y=51.7 + 2,
        showarrow=False,
        text="Extreme Danger",
        xanchor="left",
    )

    hi_fig2 = create_line_plot_figure(pd.DataFrame(drybulb_C + env_drybulb_C), "Zone Dry-Bulb Air Temp. [C]")
    hi_fig3 = create_line_plot_figure(pd.DataFrame(zone_RH + env_RH), "Zone Air Relative Humidity [%]")

    write_figures_to_html(
        file_paths.graphs / "summer_heat_index.html",
        [
            (hi_fig1, "hi_fig1"),
            (hi_fig2, "hi_fig2"),
            (hi_fig3, "hi_fig3"),
        ],
    )


def write_ventilation_plots(file_paths: Filepaths) -> None:
    vent_infiltration_ach = get_time_series_data(file_paths.sql, "Zone Infiltration Standard Density Air Change Rate")
    vent_zone_ach = get_time_series_data(file_paths.sql, "Zone Ventilation Standard Density Air Change Rate")
    vent_mech_ach = get_time_series_data(file_paths.sql, "Zone Mechanical Ventilation Air Changes per Hour")

    write_figures_to_html(
        file_paths.graphs / "summer_ventilation.html",
        [
            (
                create_line_plot_figure(pd.DataFrame(vent_infiltration_ach), "Zone Infiltration [ACH]"),
                "vent_fig1",
            ),
            (
                create_line_plot_figure(pd.DataFrame(vent_zone_ach), "Zone Ventilation [ACH]"),
                "vent_fig2",
            ),
            (
                create_line_plot_figure(pd.DataFrame(vent_mech_ach), "Zone Mechanical Ventilation [ACH]"),
                "vent_fig3",
            ),
        ],
    )


def write_energy_flow_plots(file_paths: Filepaths) -> None:
    total_J_people = get_time_series_data(file_paths.sql, "Zone People Total Heating Energy")
    total_J_lights = get_time_series_data(file_paths.sql, "Zone Lights Total Heating Energy")
    total_J_elec_equip = get_time_series_data(file_paths.sql, "Zone Electric Equipment Total Heating Energy")
    total_J_solar_direct_gain = get_time_series_data(
        file_paths.sql,
        "Enclosure Exterior Windows Total Transmitted Beam Solar Radiation Energy",
    )
    total_J_solar_diffuse_gain = get_time_series_data(
        file_paths.sql,
        "Enclosure Exterior Windows Total Transmitted Diffuse Solar Radiation Energy",
    )
    total_J_win_gain = get_time_series_data(file_paths.sql, "Zone Windows Total Heat Gain Energy")
    total_J_win_loss = get_time_series_data(file_paths.sql, "Zone Windows Total Heat Loss Energy")
    total_J_infiltration_gain = get_time_series_data(file_paths.sql, "Zone Infiltration Total Heat Gain Energy")
    total_J_infiltration_loss = get_time_series_data(file_paths.sql, "Zone Infiltration Total Heat Loss Energy")
    total_J_vent_gain = get_time_series_data(file_paths.sql, "Zone Ventilation Total Heat Loss Energy")
    total_J_vent_loss = get_time_series_data(file_paths.sql, "Zone Ventilation Total Heat Gain Energy")

    energy_fig1 = create_line_plot_figure(df_in_kWh(total_J_people), "Total People Energy [kWh]")
    energy_fig2 = create_line_plot_figure(df_in_kWh(total_J_lights), "Total Lighting Energy [kWh]")
    energy_fig3 = create_line_plot_figure(df_in_kWh(total_J_elec_equip), "Total Elec. Equipment Energy [kWh]")

    win_gain_df = df_in_kWh(total_J_win_gain)
    win_loss_df = df_in_kWh(total_J_win_loss)
    win_gain_df["Value"] = win_gain_df["Value"] - win_loss_df["Value"]
    energy_fig4 = create_line_plot_figure(win_gain_df, "Total Window Heat Gain [kWh]")

    solar_beam_df = df_in_kWh(total_J_solar_direct_gain)
    solar_diffuse_df = df_in_kWh(total_J_solar_diffuse_gain)
    solar_beam_df["Value"] = solar_beam_df["Value"] + solar_diffuse_df["Value"]
    energy_fig5 = create_line_plot_figure(solar_beam_df, "Total (Beam + Diffuse) Window Solar Heat Gain [kWh]")

    infiltration_gain_df = df_in_kWh(total_J_infiltration_gain)
    infiltration_loss_df = df_in_kWh(total_J_infiltration_loss)
    infiltration_gain_df["Value"] = infiltration_gain_df["Value"] - infiltration_loss_df["Value"]
    energy_fig6 = create_line_plot_figure(infiltration_gain_df, "Total Infiltration Heat Gain [kWh]")

    vent_gain_df = df_in_kWh(total_J_vent_gain)
    vent_loss_df = df_in_kWh(total_J_vent_loss)
    if not vent_gain_df.empty and not vent_loss_df.empty:
        vent_gain_df["Value"] = vent_gain_df["Value"] - vent_loss_df["Value"]
    energy_fig7 = create_line_plot_figure(vent_gain_df, "Total Ventilation Heat Gain [kWh]")

    write_figures_to_html(
        file_paths.graphs / "summer_energy_flow.html",
        [
            (energy_fig1, "energy_fig1"),
            (energy_fig2, "energy_fig2"),
            (energy_fig3, "energy_fig3"),
            (energy_fig4, "energy_fig4"),
            (energy_fig5, "energy_fig5"),
            (energy_fig6, "energy_fig6"),
            (energy_fig7, "energy_fig7"),
        ],
    )


if __name__ == "__main__":
    # ------------------------------------------------------------------------------------------------------------------
    print("- " * 50)
    print(f"\t>> Using Python: {sys.version}")
    print(f"\t>> Running the script: '{__file__.split('/')[-1]}'")
    print("\t>> With the arguments:")
    print("\n".join([f"\t\t{i} | {a}" for i, a in enumerate(sys.argv)]))
    print("\t>> Resolving file paths...")
    file_paths = resolve_paths(sys.argv)
    print(f"\t>> Source SQL File: '{file_paths.sql}'")
    print(f"\t>> Target Output Folder: '{file_paths.graphs}'")

    # ------------------------------------------------------------------------------------------------------------------
    # -- Generate the Summer Resiliency Graphs
    write_outdoor_environment_plots(file_paths)
    write_heat_index_plots(file_paths)
    write_ventilation_plots(file_paths)
    write_energy_flow_plots(file_paths)
