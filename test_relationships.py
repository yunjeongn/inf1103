import io
import unittest
from contextlib import redirect_stdout

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def capture(function, *args) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        function(*args)
    return buffer.getvalue()


class RelationshipTestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Acme", "sales@acme.example")
        self.guitar = PhysicalProduct("G1", "Guitar", 500, 3, self.supplier, 3.5)
        self.windows = DigitalProduct("OS1", "Windows", 99.99, 10, self.supplier, 4000)


class AssociationTests(RelationshipTestBase):
    def test_product_stores_supplier_reference(self):
        self.assertIs(self.guitar.get_supplier(), self.supplier)
        self.assertIs(self.windows.get_supplier(), self.supplier)

    def test_products_display_supplier_information(self):
        self.assertIn("Acme", capture(self.guitar.get_supplier().display_information))

    def test_product_survives_deleting_supplier_variable(self):
        del self.supplier
        self.assertEqual(self.windows.get_supplier().get_name(), "Acme")

    def test_supplier_exists_without_products(self):
        lonely = Supplier("S2", "Lonely", "a@b.example")
        self.assertEqual(lonely.get_supplier_id(), "S2")


class AggregationTests(RelationshipTestBase):
    def test_product_exists_before_inventory(self):
        self.assertEqual(self.guitar.get_name(), "Guitar")

    def test_remove_keeps_product_usable_and_transferable(self):
        inventory_a, inventory_b = Inventory(), Inventory()
        inventory_a.add_product(self.guitar)
        removed = inventory_a.remove_product("G1")
        self.assertIs(removed, self.guitar)
        self.assertIsNone(inventory_a.find_product("G1"))
        self.guitar.update_stock(9)
        self.assertEqual(self.guitar.get_stock(), 9)
        self.assertTrue(inventory_b.add_product(self.guitar))
        self.assertIs(inventory_b.find_product("G1"), self.guitar)

    def test_emptying_inventory_does_not_destroy_products(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.remove_product("G1")
        self.assertEqual(inventory.get_products(), [])
        self.assertEqual(self.guitar.get_price(), 500)

    def test_remove_missing_product_returns_none(self):
        self.assertIsNone(Inventory().remove_product("NOPE"))


class CompositionTests(RelationshipTestBase):
    def test_order_creates_its_own_lines(self):
        order = Order("O1")
        order.add_order_line(self.guitar, 2)
        order.add_order_line(self.windows, 1)
        lines = order.get_order_lines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(isinstance(line, OrderLine) for line in lines))

    def test_total_uses_order_lines(self):
        order = Order("O1")
        order.add_order_line(self.guitar, 2)
        order.add_order_line(self.windows, 1)
        self.assertAlmostEqual(order.calculate_total(), 1099.99)

    def test_same_product_in_two_orders_gives_separate_lines(self):
        order_1, order_2 = Order("O1"), Order("O2")
        order_1.add_order_line(self.guitar, 1)
        order_2.add_order_line(self.guitar, 1)
        line_1 = order_1.get_order_lines()[0]
        line_2 = order_2.get_order_lines()[0]
        self.assertIsNot(line_1, line_2)
        self.assertIs(line_1.get_product(), line_2.get_product())

    def test_removing_line_does_not_destroy_product(self):
        order = Order("O1")
        order.add_order_line(self.guitar, 1)
        self.assertTrue(order.remove_order_line("G1"))
        self.assertEqual(order.calculate_total(), 0)
        self.assertEqual(self.guitar.get_name(), "Guitar")

    def test_invalid_quantity_rejected(self):
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(self.guitar, 0)


class SubstitutabilityTests(RelationshipTestBase):
    def test_show_product_details_works_for_every_product(self):
        for product in (self.guitar, self.windows):
            output = capture(show_product_details, product)
            self.assertIn(product.get_name(), output)
            self.assertIn(product.get_fulfilment_info(), output)

    def test_update_stock_means_the_same_for_every_subclass(self):
        for product in (self.guitar, self.windows):
            product.update_stock(4)
            self.assertEqual(product.get_stock(), 4)
            with self.assertRaises(ValueError):
                product.update_stock(-1)


class PolymorphismTests(RelationshipTestBase):
    def test_one_collection_dispatches_to_each_subclass(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.windows)
        infos = [p.get_fulfilment_info() for p in inventory.get_products()]
        self.assertEqual(infos, [
            "Requires physical shipping to the customer.",
            "Delivered digitally via a download link.",
        ])

    def test_display_all_products_uses_each_products_own_display(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.windows)
        output = capture(inventory.display_all_products)
        self.assertIn("Weight: 3.50 kg", output)
        self.assertIn("Download Size: 4000.00 MB", output)


if __name__ == "__main__":
    unittest.main()
