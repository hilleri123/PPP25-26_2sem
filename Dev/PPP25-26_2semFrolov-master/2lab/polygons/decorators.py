"""
Декораторы для функций, работающих с последовательностями полигонов.

Две группы декораторов:
  Группа 1 — фильтрующие декораторы (на основе фильтров из filters.py):
    @dec_flt_convex_polygon
    @dec_flt_angle_point(point)
    @dec_flt_square(max_area)
    @dec_flt_short_side(max_length)
    @dec_flt_point_inside(point)
    @dec_flt_polygon_angles_inside(ref_poly)

  Группа 2 — трансформирующие декораторы (на основе transforms.py):
    @dec_tr_translate(dx, dy)
    @dec_tr_rotate(angle, cx, cy)
    @dec_tr_symmetry(axis, value)
    @dec_tr_homothety(k, cx, cy)

Все декораторы находят среди аргументов функции итераторы полигонов
и применяют к ним соответствующую операцию перед вызовом функции.
"""

import functools
import itertools

from polygons.filters   import (flt_convex_polygon, flt_angle_point, flt_square,
                                 flt_short_side, flt_point_inside,
                                 flt_polygon_angles_inside)
from polygons.transforms import tr_translate, tr_rotate, tr_symmetry, tr_homothety


# ─────────────────────────────────────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────────────────────────────────────

def _is_polygon_iterator(arg) -> bool:
    """
    Эвристика: аргумент считается итератором полигонов, если он является
    итерируемым (но не строкой/кортежем-точкой).
    """
    return hasattr(arg, '__iter__') and not isinstance(arg, (str, bytes))


def _apply_filter_to_args(args, predicate):
    """
    Пройти по позиционным аргументам; если аргумент — итератор,
    применить к нему filter(predicate, ...).
    Возвращает новый список аргументов.
    """
    new_args = []
    for arg in args:
        if _is_polygon_iterator(arg):
            new_args.append(filter(predicate, arg))
        else:
            new_args.append(arg)
    return new_args


def _apply_transform_to_args(args, transform_fn):
    """
    Пройти по позиционным аргументам; если аргумент — итератор,
    применить к нему map(transform_fn, ...).
    Возвращает новый список аргументов.
    """
    new_args = []
    for arg in args:
        if _is_polygon_iterator(arg):
            new_args.append(map(transform_fn, arg))
        else:
            new_args.append(arg)
    return new_args


# ─────────────────────────────────────────────────────────────────────────────
# ══ ГРУППА 1: Декораторы-фильтры ═════════════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────

def dec_flt_convex_polygon(func):
    """
    Декоратор: фильтрует итераторы полигонов в аргументах функции,
    оставляя только выпуклые полигоны.

    Использование:
        @dec_flt_convex_polygon
        def process(polygons): ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_args = _apply_filter_to_args(args, flt_convex_polygon)
        return func(*new_args, **kwargs)
    return wrapper


def dec_flt_angle_point(point, eps: float = 1e-9):
    """
    Фабрика декораторов: фильтрует итераторы полигонов в аргументах,
    оставляя только фигуры с углом в точке `point`.

    Использование:
        @dec_flt_angle_point((0, 0))
        def process(polygons): ...
    """
    predicate = flt_angle_point(point, eps)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_filter_to_args(args, predicate)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def dec_flt_square(max_area: float):
    """
    Фабрика декораторов: фильтрует итераторы полигонов в аргументах,
    оставляя только фигуры с площадью < max_area.

    Использование:
        @dec_flt_square(4.0)
        def process(polygons): ...
    """
    predicate = flt_square(max_area)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_filter_to_args(args, predicate)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def dec_flt_short_side(max_length: float):
    """
    Фабрика декораторов: фильтрует итераторы полигонов в аргументах,
    оставляя только фигуры с кратчайшей стороной < max_length.

    Использование:
        @dec_flt_short_side(1.0)
        def process(polygons): ...
    """
    predicate = flt_short_side(max_length)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_filter_to_args(args, predicate)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def dec_flt_point_inside(point):
    """
    Фабрика декораторов: фильтрует итераторы полигонов в аргументах,
    оставляя только выпуклые фигуры, содержащие точку `point`.

    Использование:
        @dec_flt_point_inside((0.5, 0.5))
        def process(polygons): ...
    """
    predicate = flt_point_inside(point)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_filter_to_args(args, predicate)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def dec_flt_polygon_angles_inside(ref_poly):
    """
    Фабрика декораторов: фильтрует итераторы полигонов в аргументах,
    оставляя только выпуклые фигуры, содержащие хотя бы один угол
    полигона ref_poly.

    Использование:
        @dec_flt_polygon_angles_inside(reference_polygon)
        def process(polygons): ...
    """
    predicate = flt_polygon_angles_inside(ref_poly)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_filter_to_args(args, predicate)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


# ─────────────────────────────────────────────────────────────────────────────
# ══ ГРУППА 2: Декораторы-трансформации ═══════════════════════════════════════
# ─────────────────────────────────────────────────────────────────────────────

def dec_tr_translate(dx: float = 0.0, dy: float = 0.0):
    """
    Фабрика декораторов: применяет tr_translate ко всем полигонам
    в итераторах среди аргументов функции.

    Использование:
        @dec_tr_translate(dx=2, dy=1)
        def process(polygons): ...
    """
    transform = functools.partial(tr_translate, dx=dx, dy=dy)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_transform_to_args(args, transform)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def dec_tr_rotate(angle: float = 0.0, cx: float = 0.0, cy: float = 0.0):
    """
    Фабрика декораторов: применяет tr_rotate ко всем полигонам
    в итераторах среди аргументов функции.

    Использование:
        @dec_tr_rotate(angle=45, cx=0, cy=0)
        def process(polygons): ...
    """
    transform = functools.partial(tr_rotate, angle=angle, cx=cx, cy=cy)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_transform_to_args(args, transform)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def dec_tr_symmetry(axis: str = 'x', value: float = 0.0):
    """
    Фабрика декораторов: применяет tr_symmetry ко всем полигонам
    в итераторах среди аргументов функции.

    Использование:
        @dec_tr_symmetry(axis='x', value=0)
        def process(polygons): ...
    """
    transform = functools.partial(tr_symmetry, axis=axis, value=value)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_transform_to_args(args, transform)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def dec_tr_homothety(k: float = 1.0, cx: float = 0.0, cy: float = 0.0):
    """
    Фабрика декораторов: применяет tr_homothety ко всем полигонам
    в итераторах среди аргументов функции.

    Использование:
        @dec_tr_homothety(k=2.0, cx=0, cy=0)
        def process(polygons): ...
    """
    transform = functools.partial(tr_homothety, k=k, cx=cx, cy=cy)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            new_args = _apply_transform_to_args(args, transform)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator
