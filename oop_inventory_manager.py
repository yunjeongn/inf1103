import json
import math
import os

from product import Product
from inventory import Inventory, LINE

INVENTORY_FILE = "inventory.json"
BANNER = "=" * 47


def load_inventory():
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
        for item in data:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)
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


def save_inventory(inventory):
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        })

    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError as error:
        print(f"Error. Could not save inventory: {error}")
        return False


def get_price():
    while True:
        value = input("Price: ").strip()
        try:
            price = float(value)
            if math.isfinite(price) and price >= 0:
                return price
        except ValueError:
            pass
        print("Error. Please enter a valid price (0 or more).")


def get_stock(prompt):
    while True:
        value = input(prompt).strip()
        try:
            stock = int(value)
            if stock >= 0:
                return stock
        except ValueError:
            pass
        print("Error. Please enter a whole number (0 or more).")


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("\nError. Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("\nError. Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("\nError. Product name cannot be empty.")
        return

    price = get_price()
    stock = get_stock("Stock Quantity: ")

    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}\n")

    product.update_stock(get_stock("New Stock Quantity: "))
    print("\nStock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(LINE)


def print_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


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
        inventory.display_all()
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
