# Функциональный API для работы с полигонами

## Описание проекта

Python-приложение, реализующее функциональный API для генерации, трансформации,
фильтрации и визуализации плоских полигонов.

**Принципы функционального программирования:**
- Функции высшего порядка (`map`, `filter`, `functools.reduce`)
- Модули `itertools` и `functools`
- Бесконечные итераторы-генераторы
- Декораторы
- Неизменяемые данные (полигоны — кортежи кортежей)

---

## Структура проекта

```
project/
├── main.py                  ← Точка входа, все демонстрации
├── requirements.txt         ← Зависимости
├── README.md
└── polygons/
    ├── __init__.py
    ├── generators.py        ← gen_rectangle, gen_triangle, gen_hexagon
    ├── transforms.py        ← tr_translate, tr_rotate, tr_symmetry, tr_homothety
    ├── filters.py           ← 6 функций фильтрации
    ├── aggregators.py       ← 5 агрегирующих функций (через reduce)
    ├── decorators.py        ← Декораторы обеих групп
    ├── utils.py             ← zip_polygons, count_2D, zip_tuple
    └── visualize.py         ← Функция визуализации
```

---

## Инструкция по запуску

### 1. Требования к системе
- Python **3.8** или новее
- pip (менеджер пакетов Python)

### 2. Установка зависимостей

Откройте терминал в папке проекта и выполните:

```bash
pip install -r requirements.txt
```

Или установите вручную:

```bash
pip install matplotlib numpy
```

### 3. Запуск приложения

```bash
python main.py
```

### 4. Что произойдёт при запуске

Приложение последовательно выполнит **8 демонстраций**, для каждой
откроется интерактивное окно matplotlib с графиком.
**Закройте окно**, чтобы перейти к следующей демонстрации.

| Демонстрация | Содержание |
|---|---|
| 01 | Генераторы: 7 прямоугольников, 7 треугольников, 7 шестиугольников |
| 02 | Все 4 трансформации на примере одного полигона |
| 03 | 4 сценария: ленты, пересечения, симметрия, гомотетия |
| 04 | Все 3 сценария применения фильтров |
| 05 | Все декораторы обеих групп |
| 06 | Все 5 агрегирующих функций через functools.reduce |
| 07 | zip_polygons, count_2D, zip_tuple |

Все графики также сохраняются в папке **`output/`**.

### 5. Запуск в виртуальном окружении (рекомендуется)

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux / macOS)
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск
python main.py
```

### 6. Возможные проблемы

| Проблема | Решение |
|---|---|
| `ModuleNotFoundError: No module named 'matplotlib'` | Выполните `pip install matplotlib` |
| Окно не открывается (headless-сервер) | Установите `pip install matplotlib` и используйте бэкенд `Agg`: `MPLBACKEND=Agg python main.py` |
| `python` не найден | Попробуйте `python3 main.py` |

---

## Выполненные задания

### Базовые (обязательные) — 15 баллов

| Компонент | Реализация |
|---|---|
| Визуализация | `polygons/visualize.py` — функция `visualize()` |
| Генераторы | `gen_rectangle`, `gen_triangle`, `gen_hexagon` |
| Трансформации | `tr_translate`, `tr_rotate`, `tr_symmetry`, `tr_homothety` |
| Визуализация сценариев | 4 сценария в `demo_transform_scenarios()` |
| Фильтры (≥2) | Все 6 фильтров |
| Применение фильтров (≥1) | Все 3 сценария |
| Декораторы (≥1 группа) | Обе группы (фильтры + трансформации) |
| Агрегаторы | Все 5 через `functools.reduce` |
| Утилиты | `zip_polygons`, `count_2D`, `zip_tuple` |

### Дополнительные — 7 баллов

| № | Задание | Баллы |
|---|---|---|
| 1 | Все 6 фильтров | 2 |
| 2 | Все 3 сценария фильтрации | 1 |
| 3 | Все декораторы обеих групп | 1 |
| 5 | Все 5 агрегирующих функций | 2 |
| 6 | `zip_polygons`, `count_2D`, `zip_tuple` | 1 |
| | **ИТОГО** | **7** |

**Суммарно: 15 + 7 = 22 балла**

---

## Примеры использования API

```python
import itertools, functools
from polygons.generators  import gen_rectangle, gen_triangle, gen_hexagon
from polygons.transforms  import tr_translate, tr_rotate, tr_symmetry, tr_homothety
from polygons.filters     import flt_convex_polygon, flt_square, flt_short_side
from polygons.aggregators import agr_area, agr_perimeter
from polygons.utils       import zip_polygons
from polygons.visualize   import visualize

# Генерация 10 прямоугольников
rects = list(itertools.islice(gen_rectangle(w=1, h=0.5, gap=0.2), 10))

# Трансформации через map
rotated   = list(map(lambda p: tr_rotate(p, angle=30), rects))
scaled    = list(map(lambda p: tr_homothety(p, k=1.5, cx=0, cy=0), rects))

# Фильтрация
convex    = list(filter(flt_convex_polygon, rotated))
small     = list(filter(flt_square(2.0), rects))

# Агрегация через reduce
total_area = functools.reduce(agr_area, rects)
total_peri = functools.reduce(agr_perimeter, rects)
print(f"Суммарная площадь: {total_area:.2f}")
print(f"Суммарный периметр: {total_peri:.2f}")

# Склейка последовательностей
merged = list(zip_polygons(iter(rects[:5]), iter(rotated[:5])))

# Визуализация
visualize(iter(rects))
```
