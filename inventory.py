from product import Product

LINE = "-" * 47


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_products(self):
        return list(self.__products)

    def display_all(self):
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            print(product)
        print(LINE)
