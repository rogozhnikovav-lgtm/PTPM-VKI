import logging
import sys
import math
import os

# Настройка логирования
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/triangle_log.log", encoding="utf-8")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")


def parse_side(value: str, side_name: str) -> float:
    """
    Преобразует строку в положительное вещественное число.
    При ошибке логирует исключение и возвращает None.
    """
    try:
        num = float(value)
        if num <= 0:
            raise ValueError(f"Сторона {side_name} должна быть положительной: {num}")
        logging.debug(f"Сторона {side_name} успешно распознана: {num}")
        return num
    except ValueError as ex:
        logging.error(f"Ошибка при разборе стороны {side_name}: {value}")
        logging.exception("Трассировка стека:")
        return None

def determine_triangle_type(a: float, b: float, c: float) -> str:
    """
    Определяет вид треугольника по трём сторонам.
    Возвращает строку: 'равносторонний', 'равнобедренный', 'разносторонний', 'не треугольник'.
    """
    # Проверка неравенства треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning(f"Стороны {a}, {b}, {c} не образуют треугольник")
        return "не треугольник"

    if a == b == c:
        return "равносторонний"
    elif a == b or a == c or b == c:
        return "равнобедренный"
    else:
        return "разносторонний"

def calculate_vertices(a: float, b: float, c: float, width: int = 100, height: int = 100):
    """
    Вычисляет координаты трёх вершин треугольника для отрисовки в поле width x height.
    Возвращает список кортежей (int, int).
    При ошибочных числовых данных возвращает [(-1, -1)] * 3.
    При невалидных (нечисловых) данных возвращает [(-2, -2)] * 3.
    """
    # Если стороны не образуют треугольник — координаты сбрасываются в (-1, -1)
    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning("Невозможно вычислить координаты: стороны не образуют треугольник")
        return [(-1, -1)] * 3

    try:
        # Размещаем вершину A в начале координат (с отступом)
        margin = 10
        ax, ay = margin, height - margin
        # Вершина B на горизонтальной прямой
        bx, by = ax + a * (width - 2 * margin) / max(a, b, c), ay
        # Координаты вершины C через теорему косинусов
        # Угол при вершине A
        cos_A = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        # Ограничиваем из-за погрешностей
        cos_A = max(-1.0, min(1.0, cos_A))
        sin_A = math.sqrt(1 - cos_A ** 2)

        # Масштабируем стороны под размеры поля
        scale = (width - 2 * margin) / max(a, b, c)
        cx = ax + c * scale * cos_A
        cy = ay - c * scale * sin_A

        # Приводим к int и ограничиваем в пределах поля
        vertices = [
            (int(round(ax)), int(round(ay))),
            (int(round(bx)), int(round(by))),
            (int(round(cx)), int(round(cy)))
        ]
        # Ограничение границами поля
        vertices = [
            (max(0, min(width, x)), max(0, min(height, y)))
            for x, y in vertices
        ]
        logging.debug(f"Вычисленные координаты вершин: {vertices}")
        return vertices
    except Exception as ex:
        logging.error("Ошибка при вычислении координат вершин")
        logging.exception("Трассировка стека:")
        return [(-1, -1)] * 3

def main():
    logging.info("Начало обработки запроса")
    # Чтение трёх строк
    try:
        line1 = input("Введите длину стороны A: ")
        line2 = input("Введите длину стороны B: ")
        line3 = input("Введите длину стороны C: ")
    except Exception as ex:
        logging.error("Ошибка при чтении входных данных")
        logging.exception("Трассировка стека:")
        print("не треугольник")
        print([(-2, -2)] * 3)
        return

    logging.info(f"Параметры запроса: A='{line1}', B='{line2}', C='{line3}'")

    # Разбор сторон
    a = parse_side(line1, "A")
    b = parse_side(line2, "B")
    c = parse_side(line3, "C")

    # Если хотя бы одна сторона не распознана — нечисловые данные
    if a is None or b is None or c is None:
        logging.error("Невалидные (нечисловые) входные данные")
        print("")  # пустая строка для нечисловых данных
        print([(-2, -2)] * 3)
        return

    # Определение вида треугольника
    triangle_type = determine_triangle_type(a, b, c)

    # Вычисление координат
    vertices = calculate_vertices(a, b, c)

    # Вывод результатов
    print(triangle_type)
    print(vertices)

    # Логирование успешного запроса
    logging.info(f"Результат: тип='{triangle_type}', вершины={vertices}")
    logging.info("Запрос успешно обработан")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logging.critical("Критическая ошибка в работе программы")
        logging.exception("Трассировка стека:")
        sys.exit(1)
        #s