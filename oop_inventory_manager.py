import json
import math
import os

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory, LINE

INVENTORY_FILE = "inventory.json"
BANNER = "=" * 47


DEFAULT_SUPPLIER_DATA = {
    "id": "S000",
    "name": "Unassigned",
    "email": "unassigned@example.com",
}


def supplier_from_dict(data: dict, known_suppliers: dict[str, Supplier]) -> Supplier:
    supplier_id = data["id"]
    if supplier_id not in known_suppliers:
        known_suppliers[supplier_id] = Supplier(supplier_id, data["name"],
                                                data["email"])
    return known_suppliers[supplier_id]


def supplier_to_dict(supplier: Supplier) -> dict:
    return {
        "id": supplier.get_supplier_id(),
        "name": supplier.get_name(),
        "email": supplier.get_contact_email(),
    }


def product_from_dict(item: dict,
                      known_suppliers: dict[str, Supplier] | None = None) -> Product:
    if known_suppliers is None:
        known_suppliers = {}
    supplier = supplier_from_dict(item.get("supplier", DEFAULT_SUPPLIER_DATA),
                                  known_suppliers)
    product_type = item.get("type", "physical")
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], supplier,
                               item.get("weight", 0.0))
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], supplier, item["download_size"])
    raise ValueError(f"Unknown product type: {product_type}")


def product_to_dict(product: Product) -> dict:
    item = {
        "type": "digital" if isinstance(product, DigitalProduct) else "physical",
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
        "supplier": supplier_to_dict(product.get_supplier()),
    }
    if isinstance(product, DigitalProduct):
        item["download_size"] = product.get_download_size()
    else:
        item["weight"] = product.get_weight()
    return item


def load_inventory() -> Inventory:
    inventory = Inventory()

    if not os.path.exists(INVENTORY_FILE):
        print(f"{INVENTORY_FILE} not found.")
        print("Starting with an empty inventory.")
        return inventory

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Unexpected file format")
        known_suppliers: dict[str, Supplier] = {}
        for item in data:
            inventory.add_product(product_from_dict(item, known_suppliers))
    except (OSError, ValueError, KeyError, TypeError):
        print(f"{INVENTORY_FILE} found but could not be read.")
        print("Starting with an empty inventory.")
        try:
            os.replace(INVENTORY_FILE, INVENTORY_FILE + ".bak")
            print(f"The original file was kept as {INVENTORY_FILE}.bak")
        except OSError:
            pass
        return Inventory()

    print(f"{INVENTORY_FILE} found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory) -> bool:
    data = []
    for product in inventory.get_products():
        data.append(product_to_dict(product))

    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError as error:
        print(f"Error. Could not save inventory: {error}")
        return False


def get_price() -> float:
    while True:
        value = input("Price: ").strip()
        try:
            price = float(value)
            if math.isfinite(price) and price >= 0:
                return price
        except ValueError:
            pass
        print("Error. Please enter a valid price (0 or more).")


def get_stock(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            stock = int(value)
            if stock >= 0:
                return stock
        except ValueError:
            pass
        print("Error. Please enter a whole number (0 or more).")


def get_non_negative_number(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if math.isfinite(number) and number >= 0:
                return number
        except ValueError:
            pass
        print("Error. Please enter a number (0 or more).")


def get_product_type() -> str:
    while True:
        choice = input("Product Type (1. Physical, 2. Digital): ").strip()
        if choice in ("1", "2"):
            return choice
        print("Error. Please enter 1 or 2.")


def get_supplier(inventory: Inventory) -> Supplier:
    supplier_id = input("Supplier ID: ").strip().upper()
    for product in inventory.get_products():
        if product.get_supplier().get_supplier_id() == supplier_id:
            supplier = product.get_supplier()
            print(f"Using existing supplier: {supplier.get_name()}")
            return supplier

    while True:
        name = input("Supplier Name: ").strip()
        email = input("Supplier Contact Email: ").strip()
        try:
            return Supplier(supplier_id, name, email)
        except ValueError as error:
            print(f"Error. {error}")
            supplier_id = input("Supplier ID: ").strip().upper()


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("\nError. Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print("\nError. Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("\nError. Product name cannot be empty.")
        return

    product_type = get_product_type()
    price = get_price()
    stock = get_stock("Stock Quantity: ")
    supplier = get_supplier(inventory)

    if product_type == "1":
        weight = get_non_negative_number("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, supplier,
                                  weight)
    else:
        size = get_non_negative_number("Download Size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, supplier,
                                 size)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")

    product.update_stock(get_stock("New Stock Quantity: "))
    print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(product.get_fulfilment_info())
    print(LINE)


def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main() -> None:
    print(BANNER)
    print("INVENTORY MANAGEMENT SYSTEM")
    print(BANNER)
    print()

    inventory = load_inventory()
    print()
    print_menu()

    while True:
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            if save_inventory(inventory):
                print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif choice == "6":
            print("\nSaving inventory before exiting...")
            if save_inventory(inventory):
                print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
