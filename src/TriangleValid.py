import math
import logging



EPS = 1e-9


class TriangleCalculator:
    def parse_side(self, value: str, side_name: str) -> float:
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

    def determine_triangle_type(self, a: float, b: float, c: float) -> str:
        """
        Определяет вид треугольника по трём сторонам.
        Возвращает строку: 'равносторонний', 'равнобедренный', 'разносторонний', 'не треугольник'.
        """
        # Проверка неравенства треугольника
        if (a + b - c <= EPS) or (a + c - b <= EPS) or (b + c - a <= EPS):
            logging.warning(f"Стороны {a}, {b}, {c} не образуют треугольник")
            return "не треугольник"

        if a == b == c:
            return "равносторонний"
        elif a == b or a == c or b == c:
            return "равнобедренный"
        else:
            return "разносторонний"

    def calculate_vertices(self, a: float, b: float, c: float, width: int = 100, height: int = 100):
        """
        Вычисляет координаты трёх вершин треугольника для отрисовки в поле width x height.
        Возвращает список кортежей (int, int).
        При ошибочных числовых данных возвращает [(-1, -1)] * 3.
        При невалидных (нечисловых) данных возвращает [(-2, -2)] * 3.
        """
        # Если стороны не образуют треугольник — координаты сбрасываются в (-1, -1)
        if (a + b - c <= EPS) or (a + c - b <= EPS) or (b + c - a <= EPS):
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


