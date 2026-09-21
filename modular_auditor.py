def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to stop): ")
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


total_inventory = 0
failed_entries = 0
deliveries_processed = 0
total_tax = 0.0


while True:
    result = get_valid_input()

    if result == "quit":
        break

    if result is None:
        failed_entries += 1
        continue

    total_inventory = process_delivery(total_inventory, result)
    tax = calculate_tax(result)
    total_tax += tax
    deliveries_processed += 1

    print(f"Accepted. Tax on this delivery: {tax:.2f}. "
          f"Running total: {total_inventory}")

    if total_inventory > 500:
        print(f"ALERT: Overstock! Total inventory ({total_inventory}) exceeds 500 units.")
        break

generate_report(deliveries_processed, failed_entries)