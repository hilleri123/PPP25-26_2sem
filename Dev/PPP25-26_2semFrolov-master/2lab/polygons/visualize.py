"""
Визуализация последовательностей полигонов.

Основная функция: visualize(iterator, ax=None, title='', ...)
Использует matplotlib.patches.Polygon для отрисовки фигур.
"""

import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
import matplotlib.colors as mc
import numpy as np


# Палитра по умолчанию (циклически повторяется)
_DEFAULT_COLORS = [
    '#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
    '#59a14f', '#edc948', '#b07aa1', '#ff9da7',
    '#9c755f', '#bab0ac'
]


def visualize(iterator,
              ax=None,
              title: str = '',
              color: str = None,
              colors: list = None,
              alpha: float = 0.55,
              edge_color: str = 'black',
              edge_width: float = 1.2,
              show_axes: bool = True,
              equal_aspect: bool = True) -> plt.Axes:
    """
    Визуализация последовательности полигонов из итератора.

    Параметры
    ---------
    iterator     : итератор полигонов (кортежи кортежей координат)
    ax           : объект matplotlib Axes; если None — создаётся новый
    title        : заголовок графика
    color        : единый цвет для всех фигур (переопределяет colors)
    colors       : список цветов для каждой фигуры (циклически)
    alpha        : прозрачность заливки
    edge_color   : цвет контура
    edge_width   : ширина контура
    show_axes    : показывать ли оси
    equal_aspect : равный масштаб осей

    Возвращает
    ----------
    Объект matplotlib Axes с отрисованными полигонами.
    """
    standalone = ax is None
    if standalone:
        fig, ax = plt.subplots(figsize=(7, 6))

    # Материализуем итератор (потребляется один раз)
    polys = list(iterator)

    if not polys:
        ax.set_title(title + " (пусто)")
        return ax

    # Определяем цвета
    if color is not None:
        color_cycle = itertools.cycle([color])
    elif colors is not None:
        color_cycle = itertools.cycle(colors)
    else:
        color_cycle = itertools.cycle(_DEFAULT_COLORS)

    for poly in polys:
        c = next(color_cycle)
        patch = MplPolygon(
            poly,
            closed=True,
            facecolor=c,
            edgecolor=edge_color,
            linewidth=edge_width,
            alpha=alpha,
        )
        ax.add_patch(patch)

    # Настройка осей
    ax.autoscale_view()
    if equal_aspect:
        ax.set_aspect('equal', adjustable='datalim')
    ax.grid(True, linestyle='--', alpha=0.35)

    if title:
        ax.set_title(title, fontsize=10, fontweight='bold')

    if standalone:
        plt.tight_layout()
        plt.show()

    return ax
