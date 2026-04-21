# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions for calculating the Phius2024 REVIVE weather adjustment factors.

See: https://vimeo.com/phius/review/998041212/3323b22b3e for background
"""

import math

try:
    from itertools import izip as zip  # Using Python2.x # type: ignore
except ImportError:
    pass  # Using Python 3.x

try:
    from typing import Callable
except ImportError:
    pass  # IronPython 2.7


def calculate_adjustment_factor(_target_return, _original_week, _extreme_func, _relaxation_factor=0.1, _tolerance=0.01):
    # type: (float, list[float], Callable, float, float) -> tuple[int, float]
    """Calculate the delta value for drybulb and dewpoint temps to apply to the original EPW values.

    Iteratively solves for the temperature offset (delta) that, when applied as a
    sinusoidal morph to the original week, produces the target return-period extreme.

    Adapted from https://github.com/Phius-ResearchComittee/REVIVE/blob/main/REVIVE2024/weatherMorph.py

    See also Section 6.1.2.1 'Resilience Extreme Week Morphing Algorithm'
    Phius Revive 2024 Retrofit Standard for Buildings v24.1.1.

    Arguments:
    ----------
        * _target_return (float): n-year return extreme value of dry-bulb or dewpoint (deg C).
        * _original_week (list[float]): Original hourly temps from the outage week.
        * _extreme_func (Callable): Function to apply to morphed week: max() for
            summer, min() for winter.
        * _relaxation_factor (float): Iteration relaxation factor. Default: 0.1.
        * _tolerance (float): Convergence tolerance in degrees. Default: 0.01.

    Returns:
    --------
        * tuple[int, float]: Iteration count and the delta value to apply.
    """
    phase_adjustment = [math.sin(math.pi * hr / len(_original_week)) for hr in range(len(_original_week))]

    # -- Starting conditions
    delta = _target_return - (sum(_original_week) / len(_original_week))
    morphed_week = [temp + delta * adj for temp, adj in zip(_original_week, phase_adjustment)]
    extreme_value = _extreme_func(morphed_week)

    # -- Iteration to determine adjustment factor
    iteration_count = 0
    while abs(_target_return - extreme_value) >= _tolerance:
        if iteration_count >= 100:
            print("Max iterations reached!")
            break
        iteration_count += 1
        delta += _relaxation_factor * (_target_return - extreme_value)
        morphed_week = [temp + delta * adj for temp, adj in zip(_original_week, phase_adjustment)]
        extreme_value = _extreme_func(morphed_week)

    return iteration_count, delta


def calculate_period_morphing_factors(
    _extreme_dry_bulb_C, _hourly_dry_bulb_deg_C, _extreme_dew_point_C, _hourly_dew_point_deg_C, func
):
    # type: (float, list[float], float, list[float], Callable) -> tuple[float, float]
    """Calculate the Phius2024 REVIVE weather-morphing factors for a specific period.

    Computes both the dry-bulb and dew-point adjustment deltas for the given
    extreme week using the specified extreme function (min for winter, max for summer).

    Arguments:
    ----------
        * _extreme_dry_bulb_C (float): Target return-period dry-bulb temperature (deg C).
        * _hourly_dry_bulb_deg_C (list[float]): Original hourly dry-bulb temps from outage week.
        * _extreme_dew_point_C (float): Target return-period dew-point temperature (deg C).
        * _hourly_dew_point_deg_C (list[float]): Original hourly dew-point temps from outage week.
        * func (Callable): Extreme function: min for winter, max for summer.

    Returns:
    --------
        * tuple[float, float]: The (dry-bulb delta, dew-point delta) morphing factors.
    """
    print("Using the function: {}".format(func.__name__))

    iters, period_dry_bulb_factor = calculate_adjustment_factor(_extreme_dry_bulb_C, _hourly_dry_bulb_deg_C, func)
    print("Dry-Bulb Factor: {:,.3f} (took {} iterations)".format(period_dry_bulb_factor, iters))

    iters, period_dew_point_factor = calculate_adjustment_factor(_extreme_dew_point_C, _hourly_dew_point_deg_C, func)
    print("Dew-Point Factor: {:,.3f} (took {} iterations)".format(period_dew_point_factor, iters))

    return period_dry_bulb_factor, period_dew_point_factor


def calculate_winter_morphing_factors(
    _extreme_dry_bulb_C,
    _hourly_dry_bulb_deg_C,
    _extreme_dew_point_C,
    _hourly_dew_point_deg_C,
):
    # type: (float, list[float], float, list[float]) -> tuple[float, float]
    """Calculate the Phius2024 REVIVE weather-morphing factors for the winter period.

    Uses 10-year return values and min() as the extreme function.

    Arguments:
    ----------
        * _extreme_dry_bulb_C (float): 10-year return dry-bulb temperature (deg C).
        * _hourly_dry_bulb_deg_C (list[float]): Original hourly dry-bulb temps from cold week.
        * _extreme_dew_point_C (float): 10-year return dew-point temperature (deg C).
        * _hourly_dew_point_deg_C (list[float]): Original hourly dew-point temps from cold week.

    Returns:
    --------
        * tuple[float, float]: The (dry-bulb delta, dew-point delta) morphing factors.
    """
    return calculate_period_morphing_factors(
        _extreme_dry_bulb_C, _hourly_dry_bulb_deg_C, _extreme_dew_point_C, _hourly_dew_point_deg_C, min
    )


def calculate_summer_morphing_factors(
    _extreme_dry_bulb_C,
    _hourly_dry_bulb_deg_C,
    _extreme_dew_point_C,
    _hourly_dew_point_deg_C,
):
    # type: (float, list[float], float, list[float]) -> tuple[float, float]
    """Calculate the Phius2024 REVIVE weather-morphing factors for the summer period.

    Uses 20-year return values and max() as the extreme function.

    Arguments:
    ----------
        * _extreme_dry_bulb_C (float): 20-year return dry-bulb temperature (deg C).
        * _hourly_dry_bulb_deg_C (list[float]): Original hourly dry-bulb temps from hot week.
        * _extreme_dew_point_C (float): 20-year return dew-point temperature (deg C).
        * _hourly_dew_point_deg_C (list[float]): Original hourly dew-point temps from hot week.

    Returns:
    --------
        * tuple[float, float]: The (dry-bulb delta, dew-point delta) morphing factors.
    """
    return calculate_period_morphing_factors(
        _extreme_dry_bulb_C, _hourly_dry_bulb_deg_C, _extreme_dew_point_C, _hourly_dew_point_deg_C, max
    )
