from product import Product


class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight must be 0 or more.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def get_fulfilment_info(self):
        return "Requires physical shipping to the customer."

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")
