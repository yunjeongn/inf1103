"""Runs the 'Predict first' checks for Lab 9 so the results can be compared."""
import os
from unittest.mock import patch

from discount_strategy import BulkDiscount, PercentageDiscount
from inventory import Inventory
from oop_inventory_manager import get_positive_float, load_products
from order import Order
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    supplier = Supplier("S1", "Acme", "sales@acme.example")

    section("2.3 Strategy on a 250 order")
    order = Order("O1", BulkDiscount(200, 20))
    order.add_order_line(PhysicalProduct("P1", "Item", 250, 1, supplier, 1), 1)
    print("BulkDiscount(200, 20):", order.calculate_total())
    order.set_discount(PercentageDiscount(10))
    print("PercentageDiscount(10):", order.calculate_total())

    section("3.2 Unknown product type")
    try:
        ProductFactory.create("service", "S1", "Install", 30, 5, supplier)
    except ValueError as error:
        print("ValueError:", error)

    section("5.1 get_positive_float with abc, -5, 12.50")
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        print("Returned:", get_positive_float("Price: "))

    section("5.2 load_products with products.csv")
    inventory = Inventory()
    load_products("products.csv", inventory, supplier)

    section("5.2 load_products with products.csv renamed")
    os.rename("products.csv", "products_renamed.csv")
    try:
        load_products("products.csv", Inventory(), supplier)
    finally:
        os.rename("products_renamed.csv", "products.csv")


if __name__ == "__main__":
    main()
