"""
Агрегирующие функции для применения через functools.reduce().

Все функции принимают два полигона (или накопленное значение и полигон)
и возвращают «результат» (полигон, число, точку).

Пример использования:
    functools.reduce(agr_perimeter, polygons)
    functools.reduce(agr_origin_nearest, polygons)

Реализованы все 5 агрегаторов:
  1. agr_origin_nearest — вершина, ближайшая к началу координат
  2. agr_max_side       — длина наибольшей стороны среди всех полигонов
  3. agr_min_area       — наименьшая площадь среди всех полигонов
  4. agr_perimeter      — суммарный периметр
  5. agr_area           — суммарная площадь
"""

import math
import functools


# ─────────────────────────────────────────────────────────────────────────────
# Вспомогательные функции
# ─────────────────────────────────────────────────────────────────────────────

def polygon_area(poly) -> float:
    """Площадь полигона (формула Гаусса / shoelace formula)."""
    n = len(poly)
    return abs(functools.reduce(
        lambda acc, i: acc + poly[i][0] * poly[(i+1) % n][1]
                           - poly[(i+1) % n][0] * poly[i][1],
        range(n),
        0
    )) / 2


def polygon_perimeter(poly) -> float:
    """Периметр полигона."""
    n = len(poly)
    return functools.reduce(
        lambda acc, i: acc + math.hypot(
            poly[(i+1) % n][0] - poly[i][0],
            poly[(i+1) % n][1] - poly[i][1]
        ),
        range(n),
        0.0
    )


def _max_side(poly) -> float:
    """Длина наибольшей стороны полигона."""
    n = len(poly)
    return max(
        math.hypot(poly[(i+1) % n][0] - poly[i][0],
                   poly[(i+1) % n][1] - poly[i][1])
        for i in range(n)
    )


def _nearest_vertex_to_origin(poly):
    """Вершина полигона, ближайшая к началу координат (0, 0)."""
    return min(poly, key=lambda pt: math.hypot(pt[0], pt[1]))


# ─────────────────────────────────────────────────────────────────────────────
# 1. agr_origin_nearest
# ─────────────────────────────────────────────────────────────────────────────
def agr_origin_nearest(acc, poly):
    """
    reduce-функция: возвращает вершину (из всех полигонов),
    ближайшую к началу координат.

    acc : предыдущий результат — кортеж-точка (x, y) или полигон
          (на первом шаге reduce передаёт первый полигон как acc).
    poly: текущий полигон.

    Первый вызов: acc = полигон, poly = второй полигон.
    """
    # Если acc — полигон (кортеж кортежей), найти его ближайшую вершину
    if isinstance(acc[0], tuple):
        best_acc = _nearest_vertex_to_origin(acc)
    else:
        # acc уже является точкой
        best_acc = acc

    best_poly = _nearest_vertex_to_origin(poly)

    dist_acc  = math.hypot(best_acc[0],  best_acc[1])
    dist_poly = math.hypot(best_poly[0], best_poly[1])

    return best_acc if dist_acc <= dist_poly else best_poly


# ─────────────────────────────────────────────────────────────────────────────
# 2. agr_max_side
# ─────────────────────────────────────────────────────────────────────────────
def agr_max_side(acc, poly):
    """
    reduce-функция: накапливает максимальную длину стороны среди всех полигонов.

    acc : предыдущее значение — полигон (1-й вызов) или float.
    poly: текущий полигон.
    """
    if isinstance(acc, tuple):
        prev_max = _max_side(acc)
    else:
        prev_max = acc

    return max(prev_max, _max_side(poly))


# ─────────────────────────────────────────────────────────────────────────────
# 3. agr_min_area
# ─────────────────────────────────────────────────────────────────────────────
def agr_min_area(acc, poly):
    """
    reduce-функция: накапливает минимальную площадь среди всех полигонов.

    acc : предыдущее значение — полигон (1-й вызов) или float.
    poly: текущий полигон.
    """
    if isinstance(acc, tuple):
        prev_min = polygon_area(acc)
    else:
        prev_min = acc

    return min(prev_min, polygon_area(poly))


# ─────────────────────────────────────────────────────────────────────────────
# 4. agr_perimeter
# ─────────────────────────────────────────────────────────────────────────────
def agr_perimeter(acc, poly):
    """
    reduce-функция: накапливает суммарный периметр всех полигонов.

    acc : предыдущее значение — полигон (1-й вызов) или float.
    poly: текущий полигон.
    """
    if isinstance(acc, tuple):
        prev = polygon_perimeter(acc)
    else:
        prev = acc

    return prev + polygon_perimeter(poly)


# ─────────────────────────────────────────────────────────────────────────────
# 5. agr_area
# ─────────────────────────────────────────────────────────────────────────────
def agr_area(acc, poly):
    """
    reduce-функция: накапливает суммарную площадь всех полигонов.

    acc : предыдущее значение — полигон (1-й вызов) или float.
    poly: текущий полигон.
    """
    if isinstance(acc, tuple):
        prev = polygon_area(acc)
    else:
        prev = acc

    return prev + polygon_area(poly)
