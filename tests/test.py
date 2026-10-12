import unittest
from unittest.mock import patch
import io
import sys
import math

# Импортируем тестируемые функции из вашего модуля.

from src.lab1 import (
    parse_side,
    determine_triangle_type,
    calculate_vertices,
    main,
)


class TestParseSide(unittest.TestCase):
    """Тесты для функции parse_side."""

    def test_parse_side_valid(self):
        """Корректное положительное число распознаётся."""
        self.assertAlmostEqual(parse_side("3.5", "A"), 3.5)

    def test_parse_side_negative(self):
        """Отрицательное число возвращает None."""
        self.assertIsNone(parse_side("-1", "A"))

    def test_parse_side_zero(self):
        """Ноль возвращает None."""
        self.assertIsNone(parse_side("0", "A"))

    def test_parse_side_non_numeric(self):
        """Нечисловая строка возвращает None."""
        self.assertIsNone(parse_side("abc", "A"))


class TestDetermineTriangleType(unittest.TestCase):
    """Тесты для функции determine_triangle_type."""

    def test_equilateral(self):
        """Равносторонний треугольник."""
        self.assertEqual(determine_triangle_type(3, 3, 3), "равносторонний")

    def test_isosceles(self):
        """Равнобедренный треугольник."""
        self.assertEqual(determine_triangle_type(3, 3, 4), "равнобедренный")

    def test_scalene(self):
        """Разносторонний треугольник."""
        self.assertEqual(determine_triangle_type(3, 4, 5), "разносторонний")

    def test_not_triangle(self):
        """Стороны не образуют треугольник."""
        self.assertEqual(determine_triangle_type(1, 2, 10), "не треугольник")

    def test_degenerate_triangle(self):
        """Вырожденный треугольник (a + b == c) — не треугольник."""
        self.assertEqual(determine_triangle_type(2, 3, 5), "не треугольник")


class TestCalculateVertices(unittest.TestCase):
    """Тесты для функции calculate_vertices."""

    def test_vertices_not_triangle(self):
        """Для не-треугольника возвращаются (-1, -1) трижды."""
        result = calculate_vertices(1, 2, 10)
        self.assertEqual(result, [(-1, -1)] * 3)

    def test_vertices_valid_triangle(self):
        """Для корректного треугольника возвращаются три точки в границах поля."""
        result = calculate_vertices(3, 4, 5, width=100, height=100)
        self.assertEqual(len(result), 3)
        for x, y in result:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_vertices_equilateral(self):
        """Равносторонний треугольник — координаты не совпадают."""
        result = calculate_vertices(5, 5, 5)
        self.assertEqual(len(result), 3)
        # Все три вершины должны быть различны
        self.assertEqual(len(set(result)), 3)


class TestMainFunction(unittest.TestCase):
    """Тесты для функции main через подмену input и перехват stdout."""

    def _run_main_with_inputs(self, inputs):
        """
        Вспомогательный метод: запускает main() с заданным списком
        входных строк, перехватывает stdout и возвращает его.
        """
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                try:
                    main()
                except StopIteration:
                    pass  # input закончился — выходим
                return fake_out.getvalue()

    def test_main_exit(self):
        """Команда exit завершает программу."""
        output = self._run_main_with_inputs(["exit"])
        self.assertIn("Программа завершена.", output)

    def test_main_scalene_triangle(self):
        """Разносторонний треугольник: вывод содержит тип и координаты."""
        output = self._run_main_with_inputs(["3", "4", "5", "exit"])
        self.assertIn("разносторонний", output)
        self.assertIn("[(", output)  # координаты — список кортежей

    def test_main_invalid_data(self):
        """Нечисловые данные: пустая строка и (-2, -2)."""
        output = self._run_main_with_inputs(["abc", "4", "5", "exit"])
        self.assertIn("(-2, -2)", output)

    def test_main_not_triangle(self):
        """Стороны не образуют треугольник: вывод 'не треугольник' и (-1, -1)."""
        output = self._run_main_with_inputs(["1", "2", "10", "exit"])
        self.assertIn("не треугольник", output)
        self.assertIn("(-1, -1)", output)


if __name__ == "__main__":
    unittest.main()
