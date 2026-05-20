"""
Фильтры полигонов.

Все фильтры предназначены для использования через встроенную функцию filter():
    filter(flt_convex_polygon, polygons)
    filter(flt_square(max_area), polygons)

Реализованы все 6 фильтров из задания:
  1. flt_convex_polygon       — выпуклые многоугольники
  2. flt_angle_point          — фигуры с углом в заданной точке
  3. flt_square               — фигуры с площадью меньше заданной
  4. flt_short_side           — фигуры с кратчайшей стороной меньше заданного
  5. flt_point_inside         — выпуклые многоугольники, содержащие заданную точку
  6. flt_polygon_angles_inside— выпуклые многоугольники, содержащие хоть один угол
"""

import math
import functools
import itertools


# ─────────────────────────────────────────────────────────────────────────────
# Вспомогательные геометрические функции
# ─────────────────────────────────────────────────────────────────────────────

def _polygon_area(poly) -> float:
    """Площадь полигона по формуле Гаусса (shoelace formula)."""
    n = len(poly)
    return abs(functools.reduce(
        lambda acc, i: acc + poly[i][0] * poly[(i+1) % n][1]
                           - poly[(i+1) % n][0] * poly[i][1],
        range(n),
        0
    )) / 2


def _side_length(p1, p2) -> float:
    """Длина отрезка между двумя точками."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def _cross(o, a, b) -> float:
    """Векторное произведение (OA × OB)."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _is_convex(poly) -> bool:
    """
    Проверка выпуклости полигона.
    Полигон выпуклый, если все векторные произведения последовательных рёбер
    имеют одинаковый знак (или равны нулю).
    """
    n = len(poly)
    if n < 3:
        return False

    sign = None
    for i in range(n):
        cp = _cross(poly[i], poly[(i+1) % n], poly[(i+2) % n])
        if cp != 0:
            cur_sign = cp > 0
            if sign is None:
                sign = cur_sign
            elif sign != cur_sign:
                return False
    return True


def _point_in_convex_polygon(point, poly) -> bool:
    """
    Проверка нахождения точки внутри выпуклого полигона.
    Использует метод: точка внутри, если все векторные произведения
    ребро→точка имеют одинаковый знак.
    """
    n = len(poly)
    if not _is_convex(poly):
        return False

    sign = None
    px, py = point
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i+1) % n]
        cp = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
        if cp != 0:
            cur_sign = cp > 0
            if sign is None:
                sign = cur_sign
            elif sign != cur_sign:
                return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# 1. flt_convex_polygon
# ─────────────────────────────────────────────────────────────────────────────
def flt_convex_polygon(poly) -> bool:
    """
    Предикат: True, если полигон является выпуклым.
    Использование: filter(flt_convex_polygon, polygons)
    """
    return _is_convex(poly)


# ─────────────────────────────────────────────────────────────────────────────
# 2. flt_angle_point
# ─────────────────────────────────────────────────────────────────────────────
def flt_angle_point(point, eps: float = 1e-9):
    """
    Фабрика предикатов: возвращает предикат, истинный для полигонов,
    имеющих вершину (угол) в точке `point`.

    Использование: filter(flt_angle_point((0, 0)), polygons)

    Параметры
    ---------
    point : кортеж (x, y) — искомая точка
    eps   : допустимая погрешность сравнения координат
    """
    px, py = point

    def predicate(poly) -> bool:
        return any(
            abs(vx - px) < eps and abs(vy - py) < eps
            for vx, vy in poly
        )

    return predicate


# ─────────────────────────────────────────────────────────────────────────────
# 3. flt_square
# ─────────────────────────────────────────────────────────────────────────────
def flt_square(max_area: float):
    """
    Фабрика предикатов: возвращает предикат, истинный для полигонов
    с площадью строго меньше `max_area`.

    Использование: filter(flt_square(4.0), polygons)
    """
    def predicate(poly) -> bool:
        return _polygon_area(poly) < max_area

    return predicate


# ─────────────────────────────────────────────────────────────────────────────
# 4. flt_short_side
# ─────────────────────────────────────────────────────────────────────────────
def flt_short_side(max_length: float):
    """
    Фабрика предикатов: возвращает предикат, истинный для полигонов,
    кратчайшая сторона которых строго меньше `max_length`.

    Использование: filter(flt_short_side(1.5), polygons)
    """
    def predicate(poly) -> bool:
        n = len(poly)
        min_side = min(
            _side_length(poly[i], poly[(i+1) % n])
            for i in range(n)
        )
        return min_side < max_length

    return predicate


# ─────────────────────────────────────────────────────────────────────────────
# 5. flt_point_inside
# ─────────────────────────────────────────────────────────────────────────────
def flt_point_inside(point):
    """
    Фабрика предикатов: возвращает предикат, истинный для **выпуклых**
    полигонов, содержащих точку `point` внутри или на границе.

    Использование: filter(flt_point_inside((0.5, 0.5)), polygons)
    """
    def predicate(poly) -> bool:
        return _is_convex(poly) and _point_in_convex_polygon(point, poly)

    return predicate


# ─────────────────────────────────────────────────────────────────────────────
# 6. flt_polygon_angles_inside
# ─────────────────────────────────────────────────────────────────────────────
def flt_polygon_angles_inside(ref_poly):
    """
    Фабрика предикатов: возвращает предикат, истинный для **выпуклых**
    полигонов, которые содержат хотя бы одну вершину (угол)
    полигона `ref_poly`.

    Использование: filter(flt_polygon_angles_inside(triangle), polygons)

    Параметры
    ---------
    ref_poly : эталонный полигон, чьи вершины проверяются
    """
    def predicate(poly) -> bool:
        if not _is_convex(poly):
            return False
        return any(_point_in_convex_polygon(pt, poly) for pt in ref_poly)

    return predicate
