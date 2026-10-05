import math

BANNER = "=" * 47
LINE = "-" * 47


def create_inventory():
    return [
        {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.5, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.0, "stock": 25},
    ]


def find_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


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
    if find_product(inventory, product_id):
        print("\nError. Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("\nError. Product name cannot be empty.")
        return

    price = get_price()
    stock = get_stock("Stock Quantity: ")

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = find_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}\n")

    product["stock"] = get_stock("New Stock Quantity: ")
    print("\nStock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = find_product(inventory, product_id)

    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)


def display_all(inventory):
    print("\nCurrent Inventory")
    print(LINE)
    if not inventory:
        print("No products in inventory.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print(LINE)


def print_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Exit")
    print("----------------------------")

print(BANNER)
print("INVENTORY MANAGEMENT SYSTEM")
print(BANNER)
print()

inventory = create_inventory()
print_menu()

while True:
    choice = input("\nEnter option: ").strip()

    if choice == "1":
        display_all(inventory)
    elif choice == "2":
        add_product(inventory)
    elif choice == "3":
        update_stock(inventory)
    elif choice == "4":
        search_product(inventory)
    elif choice == "5":
        print("\nThank you for using Inventory Management System.")
        print("Program terminated.")
        break
    else:
        print("\nInvalid option. Please choose 1-5.")