import unittest

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from oop_inventory_manager import product_from_dict, product_to_dict


class ProductTests(unittest.TestCase):
    def setUp(self):
        self.physical = PhysicalProduct("G1", "Guitar", 500, 3, 3.5)
        self.digital = DigitalProduct("OS1", "Windows", 99.99, 10, 4000)

    def test_weight_and_download_size(self):
        self.assertEqual(self.physical.get_weight(), 3.5)
        self.assertEqual(self.digital.get_download_size(), 4000)

    def test_fulfilment_info(self):
        self.assertIn("shipping", self.physical.get_fulfilment_info())
        self.assertIn("digitally", self.digital.get_fulfilment_info())

    def test_product_is_abstract(self):
        with self.assertRaises(TypeError):
            Product("X", "x", 1, 1)

    def test_shipping_cost(self):
        self.assertEqual(self.physical.calculate_shipping_cost(), 12.0)
        heavy = PhysicalProduct("H1", "Piano", 3000, 1, 100)
        self.assertEqual(heavy.calculate_shipping_cost(), 205.0)

    def test_digital_not_shippable(self):
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertNotIsInstance(self.digital, CanBeShipped)

    def test_inventory_operations(self):
        inventory = Inventory()
        self.assertTrue(inventory.add_product(self.physical))
        self.assertTrue(inventory.add_product(self.digital))
        self.assertFalse(inventory.add_product(self.physical))
        inventory.search_product("G1").update_stock(7)
        self.assertEqual(inventory.search_product("G1").get_stock(), 7)
        self.assertIsNone(inventory.search_product("NOPE"))

    def test_json_round_trip_keeps_types(self):
        for original in (self.physical, self.digital):
            restored = product_from_dict(product_to_dict(original))
            self.assertIs(type(restored), type(original))
            self.assertEqual(product_to_dict(restored), product_to_dict(original))


if __name__ == "__main__":
    unittest.main()
