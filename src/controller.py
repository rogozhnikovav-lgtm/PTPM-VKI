import logging
from TriangleValid import TriangleCalculator
from Database import TriangleDatabase
from user_io import UserInterface
from notifier import ExternalNotifier


class Controller:
    """Бизнес-логика сквозного сценария."""

    def __init__(self,
                 calculator: TriangleCalculator,
                 db: TriangleDatabase,
                 ui: UserInterface,
                 notifier: ExternalNotifier):
        self.calculator = calculator
        self.db = db
        self.ui = ui
        self.notifier = notifier

    def run_once(self) -> str:
        """Один проход сценария. Возвращает строку-результат."""
        logging.info("=== Начало обработки запроса ===")

        raw = self.ui.get_input()
        if raw is None:
            logging.info("Пользователь запросил выход")
            return "exit"

        line_a, line_b, line_c = raw
        logging.info(f"Вход: A='{line_a}', B='{line_b}', C='{line_c}'")

        # Разбор сторон
        a = self.calculator.parse_side(line_a, "A")
        b = self.calculator.parse_side(line_b, "B")
        c = self.calculator.parse_side(line_c, "C")

        if a is None or b is None or c is None:
            error = "невалидные входные данные"
            logging.error(error)
            self.ui.show_result("", [(-2, -2)] * 3, error)
            return f"error: {error}"

        # Проверка в БД
        record = self.db.get_record(a, b, c)
        if record:
            triangle_type, error_message = record
            logging.info(f"Результат взят из БД: {triangle_type}")
        else:
            triangle_type = self.calculator.determine_triangle_type(a, b, c)
            error_message = "" if triangle_type != "не треугольник" else "стороны не образуют треугольник"
            self.db.add_record(a, b, c, triangle_type, error_message)
            logging.info(f"Результат вычислен и сохранён в БД: {triangle_type}")

        vertices = self.calculator.calculate_vertices(a, b, c)

        # Отправка результата во внешнюю зависимость
        result_str = f"Треугольник ({a}, {b}, {c}): {triangle_type}, вершины={vertices}"
        self.notifier.send(result_str)

        # Показ пользователю
        self.ui.show_result(triangle_type, vertices, error_message)

        logging.info("=== Запрос успешно обработан ===")
        return result_str