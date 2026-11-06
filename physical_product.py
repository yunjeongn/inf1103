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

    def display_information(self):
        print(f"ID: {self.get_product_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Price: ${self.get_price():.2f}")
        print(f"Stock: {self.get_stock()}")
        print(f"Weight: {self.__weight:.2f} kg")
