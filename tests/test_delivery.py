import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from Delivery import calculate_delivery_cost


class TestValidation(unittest.TestCase):
    """Проверка входных данных."""

    def test_rejects_weight_below_minimum(self):
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), (-1, "0000-00-00"))

    def test_rejects_weight_above_maximum(self):
        self.assertEqual(calculate_delivery_cost(60.0, 100, "обычный"), (-1, "0000-00-00"))

    def test_rejects_distance_below_minimum(self):
        self.assertEqual(calculate_delivery_cost(1.0, 0, "обычный"), (-1, "0000-00-00"))

    def test_rejects_distance_above_maximum(self):
        self.assertEqual(calculate_delivery_cost(1.0, 9999, "обычный"), (-1, "0000-00-00"))

    def test_rejects_unknown_package_type(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "стеклянный"), (-1, "0000-00-00"))


class TestPriceCalculation(unittest.TestCase):
    """Стоимость по бизнес-логике."""

    def test_base_price_for_small_weight(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)  # 200 + 100*5

    def test_weight_surcharge_12_percent(self):
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)  # 700 * 1.2

    def test_weight_surcharge_15_percent(self):
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)  # 700 * 1.5

    def test_fragile_package_adds_300(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)  # 700 + 300

    def test_dangerous_package_adds_1000(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)  # 700 + 1000

    def test_express_increases_price(self):
        # БИЗНЕС: экспресс дороже, а не дешевле
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(cost, 700)


class TestDeliveryDate(unittest.TestCase):
    """Дата доставки по бизнес-логике."""

    def test_short_distance_takes_one_day(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_long_distance_takes_4_days(self):
        _, date = calculate_delivery_cost(1.0, 2000, "обычный")
        self.assertEqual(date, "2026-09-07")  # 2000 // 500 = 4

    def test_express_shortens_delivery_time(self):
        _, normal = calculate_delivery_cost(1.0, 2000, "обычный")
        _, express = calculate_delivery_cost(1.0, 2000, "обычный", is_express=True)
        self.assertLess(express, normal)

    def test_express_never_takes_zero_days(self):
        # БИЗНЕС: экспресс не может приехать в день отправки
        _, date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")


if __name__ == "__main__":
    unittest.main()