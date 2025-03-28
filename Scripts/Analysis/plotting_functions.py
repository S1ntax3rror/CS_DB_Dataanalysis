from __future__ import annotations

from typing import Callable, List

import numpy as np
import pandas as pd
import seaborn as sns
import scipy
from matplotlib import pyplot as plt, image as mpimg, patches
from matplotlib.animation import FuncAnimation, PillowWriter

from Scripts.Analysis.map_coordinates import map_players_to_grid

sns.set()

def scatter_plot(
        ax,
        map: str,
        grid: pd.DataFrame | np.array,
        size: int,
        cmap: str = "bwr",
        modified: bool = False
):
    """
    Plot grid coordinates on map
    :param ax: Matplotlib subplot axis
    :param map: Map name
    :param grid: Coordinate grid data
    :param size: Scatter point size multiplier
    :param cmap: Color map
    """
    i, j = np.where(grid != 0)
    values = grid[i, j]

    sorted_indices = np.argsort(np.abs(values))
    i = i[sorted_indices]
    j = j[sorted_indices]
    values = values[sorted_indices]

    ax.imshow(plt.imread(f'../../Resources/maps/{map}.png'))

    if not modified:
        scatter = plt.scatter(
            x=j,
            y=i,
            s=np.abs(values) * size,
            alpha=0.25,
            c=values,
            cmap=cmap
        )
    else:
        scatter = plt.scatter(
            x=j,
            y=i,
            s=size,
            alpha=1,
            c=values,
            cmap=cmap
        )

def smooth_scale(data, map_name, mask_value: int = None):
    """
    Smooths counting data. Returns a positive count grid
    :param data:
    :param map_name:
    :param mask_value:
    :return:
    """
    grid = map_players_to_grid(data, map_name)
    if np.any(grid < 0):
        grid *= -1

    data = scipy.ndimage.gaussian_filter(grid, sigma=2)

    data = np.log(data + 1)

    return data

def heatmap_plot(
        ax,
        map: str,
        data: pd.DataFrame,
        cmap: str,
        mask_value: float = 0,
        alpha: float = 0.75
):
    data = np.ma.masked_where(abs(data) < mask_value, data)

    ax.imshow(plt.imread(f'../../Resources/maps/{map}.png'))
    ax.contourf(data, alpha=alpha, cmap=cmap)

def animate(imageName: str, mappingFunction: Callable[[float, float], List[float]], title: str, frames: List[dict]):
    """
    Animates object moving on a map
    :param imageName: Name of Map image
    :param mappingFunction: lambda function used for the mapping of coordinates onto plot f:(x, y) -> (x', y')
    :param title: Title of plot
    :param frames: Frames to be animated
    """
    """def init():
        animationPlot.set_data([], [])
        return animationPlot,"""
    def update(frame):
        view.set_center([frames[frame]['x'], frames[frame]['y']])
        player.set_data([frames[frame]['x'], frames[frame]['y']])
        return view, player

    n = 2048

    image = mpimg.imread(f'maps/{imageName}.png')

    fig, ax = plt.subplots()
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)

    view = ax.add_patch(patches.Wedge(frames[0]['x'], frames[0]['y'], 100, 60, 120, color="g", alpha=0.2))
    player = ax.plot(frames[0]['x'], frames[0]['y'])[0]

    ax.imshow(image, aspect='auto')

    animationPlot, = ax.plot([], [], 'go', ms=5)

    animation = FuncAnimation(fig, update, frames=len(frames))
    animation.save(f'{imageName}_{title}.gif', writer=PillowWriter(fps=30))


def price_plot(
        plot_ax,
        data,
        x,
        y,
        Wins: List = None,
        Loses: List = None
):
    ymin = data[y].min()
    ymax = data[y].max()

    if Wins:
        plot_ax.vlines(x=Wins, color='green', alpha=1, label='Win', ymin=ymin - 10, ymax=ymax + 10)
    if Loses:
        plot_ax.vlines(x=Loses, color='red', alpha=1, label='Lose', ymin=ymin - 10, ymax=ymax + 10)

    sns.lineplot(data, x=x, y=y, ax=plot_ax)

    min_x = min(data[x])
    max_x = max(max(Wins), max(Loses))
    min_game = min(min(Wins), min(Loses))
    if min_game > min_x:
        min_x = min_game

    plot_ax.set_xlim([min_x, max_x])

    if Wins or Loses:
        plot_ax.legend()