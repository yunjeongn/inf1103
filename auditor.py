total_inventory = 0
failed_entries = 0

while True:
        user_input = input("Enter stock quantity (or 'quit' to stop): ")

        if user_input.lower() == "quit":
            break

        if user_input.isdigit():
            quantity = int(user_input)
        else:
            print(f"Error. Please try again.")
            failed_entries += 1
            continue

        total_inventory += quantity
        print(f"Accepted. Running total: {total_inventory}")

        if total_inventory > 500:
            print(f"ALERT: Overstock! Total inventory ({total_inventory}) exceeds 500 units.")
            break

print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")