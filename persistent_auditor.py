ORDERS_FILE = "orders.txt"        
INVENTORY_FILE = "inventory.txt"  

def load_inventory():

    orders = []
    total = 0
    history = []
    inventory_found = False

    try:
        with open(ORDERS_FILE, "r") as file:
            for line in file:
                parts = [p.strip() for p in line.strip().split(",")]
                if len(parts) == 3 and parts[0].isdigit() and parts[2].isdigit():
                    orders.append((int(parts[0]), parts[1], int(parts[2])))
    except FileNotFoundError:
        pass

    try:
        with open(INVENTORY_FILE, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        total = int(lines[0])
        history = [int(line) for line in lines[1:]]
        inventory_found = True
    except (FileNotFoundError, IndexError, ValueError):
        pass

    if not inventory_found:
        history = [quantity for _, _, quantity in orders]
        total = sum(history)

    return orders, total, history


def display_orders(orders):
    print("Current Orders:\n")
    for order_id, product, quantity in orders:
        print(f"{order_id}, {product}, {quantity}")


def get_valid_input():
    user_input = input("Enter Quantity: ")
    if user_input.lower() == "quit":
        return "quit"
    if user_input.isdigit():
        return int(user_input)
    print("Error. Please try again.")
    return None


def calculate_tax(amount, rate=0.10):
    return amount * rate


def process_delivery(current_total, new_value):
    return current_total + new_value


def generate_report(total_units, failed_attempts):
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


orders, total_inventory, transaction_history = load_inventory()
failed_entries = 0
deliveries_processed = 0
total_tax = 0.0

display_orders(orders)
print()

while True:
    product = input("Enter Product Name (or 'quit' to stop): ").strip()
    if product.lower() == "quit":
        break
    if not product:
        print("Error. Please try again.")
        failed_entries += 1
        continue

    result = get_valid_input()

    if result == "quit":
        break

    if result is None:
        failed_entries += 1
        continue

    total_inventory = process_delivery(total_inventory, result)
    transaction_history.append(result)
    total_tax += calculate_tax(result)
    deliveries_processed += 1

    order_id = orders[-1][0] + 1 if orders else 1001
    orders.append((order_id, product, result))

    print("\nNew Order Added:")
    print(f"{order_id},{product},{result}\n")

    if total_inventory > 500:
        print(f"ALERT: Overstock! Total inventory ({total_inventory}) exceeds 500 units.")
        break

print(f"Total: {total_inventory}")
print(f"Transaction History: {transaction_history}\n")
generate_report(deliveries_processed, failed_entries)