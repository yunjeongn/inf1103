from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight must be 0 or more.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def calculate_shipping_cost(self):
        return 5.0 + 2.0 * self.__weight

    def get_fulfilment_info(self):
        return "Requires physical shipping to the customer."

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")
