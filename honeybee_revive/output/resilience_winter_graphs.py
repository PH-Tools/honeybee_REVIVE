# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""A script to generate the Winter Resiliency Graphs.

This script is called from the command line with the following arguments:
    * [0] (str): The path to the Python script (this file).
    * [1] (str): The path to the EnergyPlus SQL file to read in.
    * [2] (str): The path to the output folder for the graphs.
"""

import os
import sqlite3
import sys
from collections import namedtuple
from pathlib import Path

import pandas as pd

from honeybee_revive.output._shared import (
    InputFileError,
    Record,
    create_line_plot_figure,
    df_in_kWh,
    get_time_series_data,
    write_figures_to_html,
)

Filepaths = namedtuple("Filepaths", ["sql", "graphs"])
Surface = namedtuple(
    "Surface",
    [
        "Name",
        "Class",
        "Area",
        "GrossArea",
        "Tilt",
        "ZoneIndex",
        "SurfaceIndex",
        "ExtBoundCond",
        "ConstructionIndex",
    ],
)
Construction = namedtuple("Construction", ["ConstructionIndex", "Name", "UValue"])


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
    os.makedirs(target_graphs_dir, exist_ok=True)

    return Filepaths(results_sql_file, target_graphs_dir)


def get_constructions(source_file_path: Path) -> dict[int, Construction]:
    conn = sqlite3.connect(source_file_path)
    data_ = {}
    try:
        c = conn.cursor()
        c.execute("SELECT ConstructionIndex, Name, UValue FROM 'Constructions'")
        for row in c.fetchall():
            c = Construction(*row)
            data_[c.ConstructionIndex] = c
    except Exception as e:
        conn.close()
        raise Exception(str(e))
    finally:
        conn.close()

    return data_


def get_surface_data(source_file_path: Path) -> list[Surface]:
    conn = sqlite3.connect(source_file_path)
    data_ = []
    try:
        c = conn.cursor()
        c.execute(
            "SELECT SurfaceName, ClassName, Area, GrossArea, Tilt, ZoneIndex, SurfaceIndex, ExtBoundCond, ConstructionIndex FROM 'Surfaces' "
        )
        for row in c.fetchall():
            data_.append(Surface(*row))
    except Exception as e:
        conn.close()
        raise Exception(str(e))
    finally:
        conn.close()

    return data_


def surface_df_by_construction(
    _records: list[Record],
    _constructions: dict[int, Construction],
    _surfaces_df: pd.DataFrame,
    _exterior_surface_names: set[str],
) -> pd.DataFrame:
    """Get the surface data as a DataFrame, merged by the construction type."""

    ext_surfaces = (r for r in _records if r.Zone in _exterior_surface_names)
    surface_conductance_df = df_in_kWh(ext_surfaces)
    return surface_conductance_df


def rename_set_temps(_data: list[Record]) -> list[Record]:
    """Rename the SET temperature Zones.

    For some reason, when pulling SET temps from the SQL file, the Zone names come in as the
    identifier of the Honeybee-Room's Honeybee-Energy-People object. ie: 'FLOOR-0_SPACE RV2024_RESILIENCE_PEOPLE'
    Shrug. So try and break off the first part of the string and use that as the Zone Name for plotting.
    """
    for i, r in enumerate(_data):
        name_parts = str(r.Zone).split("_SPACE RV2024_")
        _data[i] = Record(r.Date, r.Value, name_parts[0])
    return _data


def write_outdoor_environment_plots(_file_paths: Filepaths) -> None:
    env_drybulb_C = get_time_series_data(_file_paths.sql, "Site Outdoor Air Drybulb Temperature")
    env_RH = get_time_series_data(_file_paths.sql, "Site Outdoor Air Relative Humidity")
    env_wind_speed_m3s = get_time_series_data(_file_paths.sql, "Site Wind Speed")
    env_air_pressure_Pa = get_time_series_data(_file_paths.sql, "Site Outdoor Air Barometric Pressure")

    write_figures_to_html(
        _file_paths.graphs / "winter_outdoor_environment.html",
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


def write_ventilation_plots(_file_paths: Filepaths) -> None:
    vent_infiltration_ach = get_time_series_data(_file_paths.sql, "Zone Infiltration Standard Density Air Change Rate")
    vent_mech_ach = get_time_series_data(_file_paths.sql, "Zone Mechanical Ventilation Air Changes per Hour")
    vent_zone_ach = get_time_series_data(_file_paths.sql, "Zone Ventilation Standard Density Air Change Rate")
    # vent_infiltration_m3s = get_time_series_data(
    #     _file_paths.sql, "Zone Infiltration Standard Density Volume Flow Rate"
    # )
    # vent_mech_m3s = get_time_series_data(
    #     _file_paths.sql, "Zone Mechanical Ventilation Standard Density Volume Flow Rate"
    # )
    # vent_zone_m3s = get_time_series_data(
    #     _file_paths.sql, "Zone Ventilation Standard Density Volume Flow Rate"
    # )

    write_figures_to_html(
        _file_paths.graphs / "winter_ventilation.html",
        [
            (
                create_line_plot_figure(
                    pd.DataFrame(vent_infiltration_ach),
                    "Zone Envelope Infiltration [ACH]",
                ),
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


def write_SET_temp_plots(_file_paths: Filepaths) -> None:
    drybulb_C = get_time_series_data(_file_paths.sql, "Zone Mean Air Temperature")
    zone_RH = get_time_series_data(_file_paths.sql, "Zone Air Relative Humidity")
    set_temps = rename_set_temps(
        get_time_series_data(
            _file_paths.sql,
            "Zone Thermal Comfort Pierce Model Standard Effective Temperature",
        )
    )
    env_drybulb_C = get_time_series_data(_file_paths.sql, "Site Outdoor Air Drybulb Temperature")
    env_RH = get_time_series_data(_file_paths.sql, "Site Outdoor Air Relative Humidity")

    set_fig1 = create_line_plot_figure(pd.DataFrame(set_temps), "Zone SET Temperature [C]", [12.22])
    set_fig2 = create_line_plot_figure(pd.DataFrame(drybulb_C + env_drybulb_C), "Dry-Bulb Air Temperature [C]")
    set_fig3 = create_line_plot_figure(pd.DataFrame(zone_RH + env_RH), "Air Relative Humidity [%]")

    write_figures_to_html(
        _file_paths.graphs / "winter_SET_temperature.html",
        [
            (set_fig1, "set_fig1"),
            (set_fig2, "set_fig2"),
            (set_fig3, "set_fig3"),
        ],
    )


def write_energy_flow_plots(_file_paths: Filepaths) -> None:
    total_J_people = get_time_series_data(_file_paths.sql, "Zone People Total Heating Energy")
    total_J_lights = get_time_series_data(_file_paths.sql, "Zone Lights Total Heating Energy")
    total_J_elec_equip = get_time_series_data(_file_paths.sql, "Zone Electric Equipment Total Heating Energy")
    total_J_solar_direct_gain = get_time_series_data(
        _file_paths.sql,
        "Enclosure Exterior Windows Total Transmitted Beam Solar Radiation Energy",
    )
    total_J_solar_diffuse_gain = get_time_series_data(
        _file_paths.sql,
        "Enclosure Exterior Windows Total Transmitted Diffuse Solar Radiation Energy",
    )
    total_J_win_gain = get_time_series_data(_file_paths.sql, "Zone Windows Total Heat Gain Energy")
    total_J_win_loss = get_time_series_data(_file_paths.sql, "Zone Windows Total Heat Loss Energy")
    total_J_infiltration_gain = get_time_series_data(_file_paths.sql, "Zone Infiltration Total Heat Gain Energy")
    total_J_infiltration_loss = get_time_series_data(_file_paths.sql, "Zone Infiltration Total Heat Loss Energy")
    total_J_vent_gain = get_time_series_data(_file_paths.sql, "Zone Ventilation Total Heat Gain Energy")
    total_J_vent_loss = get_time_series_data(_file_paths.sql, "Zone Ventilation Total Heat Loss Energy")

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
        _file_paths.graphs / "winter_energy_flow.html",
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


def write_envelope_details_plots(_file_paths: Filepaths):
    srfc_avg_face_conductance = get_time_series_data(
        _file_paths.sql, "Surface Average Face Conduction Heat Transfer Energy"
    )
    srfc_win_heat_transfer = get_time_series_data(_file_paths.sql, "Surface Window Net Heat Transfer Energy")
    srfc_win_heat_gain = get_time_series_data(_file_paths.sql, "Surface Window Heat Gain Energy")
    srfc_win_heat_loss = get_time_series_data(_file_paths.sql, "Surface Window Heat Loss Energy")
    srfc_heat_storage = get_time_series_data(_file_paths.sql, "Surface Heat Storage Energy")
    srfc_shading_device_on = get_time_series_data(_file_paths.sql, "Surface Shading Device Is On Time Fraction")
    srfc_inside_face_temp = get_time_series_data(_file_paths.sql, "Surface Inside Face Temperature")

    constructions = get_constructions(_file_paths.sql)
    surfaces = get_surface_data(_file_paths.sql)
    surfaces_df = pd.DataFrame(surfaces)
    exterior_surface_names = {s.Name for s in surfaces if s.ExtBoundCond == 0}

    write_figures_to_html(
        _file_paths.graphs / "winter_envelope_details.html",
        [
            (
                create_line_plot_figure(
                    surface_df_by_construction(
                        srfc_avg_face_conductance,
                        constructions,
                        surfaces_df,
                        exterior_surface_names,
                    ),
                    "Surface Average Face Conduction Heat Transfer Energy [kWh]",
                    _stack=True,
                ),
                "envelope_fig1",
            ),
            (
                create_line_plot_figure(
                    surface_df_by_construction(
                        srfc_win_heat_transfer,
                        constructions,
                        surfaces_df,
                        exterior_surface_names,
                    ),
                    "Window Net Heat Transfer Energy [kWh]",
                    _stack=True,
                ),
                "envelope_fig2",
            ),
            (
                create_line_plot_figure(
                    surface_df_by_construction(
                        srfc_win_heat_gain,
                        constructions,
                        surfaces_df,
                        exterior_surface_names,
                    ),
                    "Window Heat Gain Energy [kWh]",
                    _stack=True,
                ),
                "envelope_fig3",
            ),
            (
                create_line_plot_figure(
                    surface_df_by_construction(
                        srfc_win_heat_loss,
                        constructions,
                        surfaces_df,
                        exterior_surface_names,
                    ),
                    "Window Heat Loss Energy [kWh]",
                    _stack=True,
                ),
                "envelope_fig4",
            ),
            (
                create_line_plot_figure(
                    surface_df_by_construction(
                        srfc_heat_storage,
                        constructions,
                        surfaces_df,
                        exterior_surface_names,
                    ),
                    "Heat Storage Energy [kWh]",
                    _stack=True,
                ),
                "envelope_fig5",
            ),
            (
                create_line_plot_figure(pd.DataFrame(srfc_shading_device_on), "Surface Shading Device On"),
                "envelope_fig6",
            ),
            (
                create_line_plot_figure(pd.DataFrame(srfc_inside_face_temp), "Surface Inside Face Temp. [C]"),
                "envelope_fig7",
            ),
        ],
    )


if __name__ == "__main__":
    # ------------------------------------------------------------------------------------------------------------------
    print("- " * 50)
    print(f"\t>> Using Python: {sys.version}")
    print(f"\t>> Running the script: '{__file__.split('/')[-1]}'")
    print("\t>> With the arguments:")
    print("\n".join([f"\t\t{i} | {a}" for i, a in enumerate(sys.argv)]))

    # ------------------------------------------------------------------------------------------------------------------
    # --- Input / Output file Path
    print("\t>> Resolving file paths...")
    file_paths = resolve_paths(sys.argv)
    print(f"\t>> Source SQL File: '{file_paths.sql}'")
    print(f"\t>> Target Output Folder: '{file_paths.graphs}'")

    # ------------------------------------------------------------------------------------------------------------------
    # -- Generate the Winter Resiliency Graphs
    write_outdoor_environment_plots(file_paths)
    write_SET_temp_plots(file_paths)
    write_ventilation_plots(file_paths)
    write_energy_flow_plots(file_paths)
    write_envelope_details_plots(file_paths)
