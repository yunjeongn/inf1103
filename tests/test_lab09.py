import inspect
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import order as order_module
from digital_product import DigitalProduct
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from inventory import Inventory
from oop_inventory_manager import get_positive_float, load_products
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S1", "Acme", "sales@acme.example")


def make_order(price: float = 250, discount=None) -> Order:
    order = Order("O1", discount)
    order.add_order_line(PhysicalProduct("P1", "Item", price, 1,
                                         make_supplier(), 1), 1)
    return order


class DiscountTests(unittest.TestCase):
    def test_default_is_no_discount(self):
        self.assertEqual(make_order().calculate_total(), 250)

    def test_strategies_inherit_discount_strategy(self):
        for cls in (NoDiscount, PercentageDiscount, BulkDiscount,
                    StudentDiscount):
            self.assertTrue(issubclass(cls, DiscountStrategy))

    def test_base_class_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_percentage(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_at_and_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)
        self.assertEqual(BulkDiscount(200, 20).apply(199), 199)

    def test_order_uses_strategy(self):
        order = make_order(250, BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_set_discount_changes_existing_order(self):
        order = make_order(250, BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_strategy_needs_no_change_to_order(self):
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        self.assertEqual(make_order(250, HalfPrice()).calculate_total(), 125)
        self.assertAlmostEqual(
            make_order(100, StudentDiscount()).calculate_total(), 95)

    def test_order_has_no_discount_if_elif_logic(self):
        source = inspect.getsource(order_module.Order).lower()
        for word in ("percentage", "bulk", "student", "elif", "discount_type"):
            self.assertNotIn(word, source)

    def test_invalid_strategy_values_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(101)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 5)

    def test_one_strategy_shared_by_two_orders(self):
        shared = PercentageDiscount(10)
        a, b = make_order(100, shared), make_order(200, shared)
        self.assertAlmostEqual(a.calculate_total(), 90)
        self.assertAlmostEqual(b.calculate_total(), 180)


class FactoryTests(unittest.TestCase):
    def test_creates_each_type_as_product(self):
        s = make_supplier()
        physical = ProductFactory.create("physical", "P1", "Lamp", 25, 10, s, 2)
        digital = ProductFactory.create("digital", "D1", "App", 50, 5, s, 100)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(physical.get_weight(), 2)

    def test_unknown_type_raises_clear_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "Install", 30, 5,
                                  make_supplier())
        self.assertEqual(str(ctx.exception), "Unknown product type: service")


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.supplier = make_supplier()

    def test_price_must_be_positive(self):
        for price in (0, -1):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P1", "x", price, 1,
                                      self.supplier)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "x", 5, -1, self.supplier)
        product = ProductFactory.create("digital", "D1", "x", 5, 0,
                                        self.supplier)
        with self.assertRaises(ValueError):
            product.update_stock(-3)

    def test_order_quantity_must_be_positive(self):
        product = ProductFactory.create("physical", "P1", "x", 5, 1,
                                        self.supplier)
        for quantity in (0, -2):
            with self.assertRaises(ValueError) as ctx:
                OrderLine(product, quantity)
            self.assertEqual(str(ctx.exception),
                             "Quantity must be greater than zero.")


class InputTests(unittest.TestCase):
    def run_input(self, entries):
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=entries), \
                redirect_stdout(buffer):
            value = get_positive_float("Price: ")
        return value, buffer.getvalue()

    def test_asks_again_until_valid(self):
        value, output = self.run_input(["abc", "-5", "12.50"])
        self.assertEqual(value, 12.5)
        self.assertEqual(output.splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_nan_and_inf_rejected(self):
        value, _ = self.run_input(["0", "nan", "inf", "3"])
        self.assertEqual(value, 3)


class LoadProductsTests(unittest.TestCase):
    CSV = ("product_type,product_id,name,price,stock_quantity\n"
           "physical,P001,Desk Lamp,25.00,10\n"
           "digital,D001,Photo Editor,49.90,100\n"
           "service,S001,Installation,30.00,5\n"
           "physical,P002,Office Chair,abc,3\n"
           "physical,P003,Monitor Stand,39.50,7\n")

    def load(self, path):
        inventory = Inventory()
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            load_products(path, inventory, make_supplier())
        return inventory, buffer.getvalue().splitlines()

    def test_bad_rows_skipped_and_valid_rows_loaded(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as file:
                file.write(self.CSV)
            inventory, lines = self.load(path)
        ids = [p.get_product_id() for p in inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertEqual(len(lines), 4)
        self.assertIn("Row 4 skipped: Unknown product type: service", lines[0])
        self.assertIn("Row 5 skipped", lines[1])
        self.assertEqual(lines[2:],
                         ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_handled(self):
        inventory, lines = self.load("no_such_products.csv")
        self.assertEqual(inventory.get_products(), [])
        self.assertEqual(lines, ["Products file not found: no_such_products.csv",
                                 "Load attempt finished."])


if __name__ == "__main__":
    unittest.main()
