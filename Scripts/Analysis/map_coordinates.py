from __future__ import annotations

from typing import Tuple, List

import numpy as np
import pandas as pd

####
# Contains function for the mapping of ingame coordinates to radar coordinates. Standard radar size is 2048 x 2048.
# Coordinate transformations and radars were used from https://github.com/boltgolt/boltobserv
####

def map_de_ancient(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 2590) / 2.13
    y = abs(2048 - ((y + 2520) / 2.13))
    return x, y, z

def map_de_nuke(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 3290) / 3.49
    y = abs(2048 - ((y + 5990) / 3.49))
    shift = (z <= -482)
    y -= shift * 1109
    return x, y, z

def map_de_dust2(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 2480) / 2.2
    y = abs(2048 - ((y + 1265) / 2.2))
    return x, y, z

def map_de_inferno(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 2090) / 2.455
    y = abs(2048 - ((y + 1150) / 2.455))
    return x, y, z

def map_de_mirage(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 3240) / 2.51
    y = abs(2048 - ((y + 3410) / 2.51))
    return x, y, z

def map_de_overpass(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 4830) / 2.59
    y = abs(2048 - ((y + 3540) / 2.59))
    return x, y, z

def map_de_train(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 2510) / 2.37
    y = abs(2048 - ((y + 2440) / 2.37))
    return x, y, z

def map_de_vertigo(
        x: int | pd.Series | np.array,
        y: int | pd.Series | np.array,
        z: int | pd.Series | np.array
) -> Tuple[int | pd.Series, int | pd.Series, int | pd.Series]:
    """
        Map game coordinates to radar coordinates
    """
    x = (x + 3900) / 2.48
    y = abs(2048 - ((y + 3800) / 2.48))
    shift = z <= 11600
    y -= shift * 1175
    x -= shift * 8
    return x, y, z

def map_coordinates_to_grid(coordinates: pd.DataFrame, map_name: str = "", n: int = 2048) -> np.array:
    """
    Map the coordinate values to n x n grid.
    :param coordinates: Coordinate values
    :param n: Side length of grid
    :return: Grid with mapped coordinates
    """
    if map_name != "":
        mapping_function = mapping_functions[map_name]
        coordinates['x'], coordinates['y'], coordinates['z'] = mapping_function(coordinates['x'], coordinates['y'], coordinates['z'])

    grid = np.zeros((n, n))
    x = (coordinates['x']).astype(int).tolist()
    y = (coordinates['y']).astype(int).tolist()
    for x_i, y_i in zip(x, y):
        grid[y_i, x_i] += 1
    return grid

def map_players_to_grid(coordinates: pd.DataFrame, map_name: str = "", n: int = 2048, return_coords=False) -> np.array:
    """
    Map the coordinate values to n x n grid.
    :param map_name: Map name. If not empty, the coordinates will be mapped to radar coordinates of the specified map
    :param coordinates: Coordinate values
    :param n: Side length of grid
    :return: Grid with mapped coordinates
    """
    grid = np.zeros((n, n))

    if map_name != "":
        mapping_function = mapping_functions[map_name]
        coordinates['playerx'], coordinates['playery'], coordinates['playerz'] = mapping_function(coordinates['playerx'], coordinates['playery'], coordinates['playerz'])

    x = (coordinates['playerx']).astype(int).tolist()
    y = (coordinates['playery']).astype(int).tolist()
    for x_i, y_i, side in zip(x, y, coordinates['side']):
        if side == 'CT':
            grid[y_i, x_i] -= 1
        else:
            grid[y_i, x_i] += 1
    if return_coords:
        return grid, x, y
    return grid

mapping_functions = {
    "de_nuke": map_de_nuke,
    "de_dust2": map_de_dust2,
    "de_inferno": map_de_inferno,
    "de_mirage": map_de_mirage,
    "de_overpass": map_de_overpass,
    "de_train": map_de_train,
    "de_vertigo": map_de_vertigo,
    "de_ancient": map_de_ancient
}