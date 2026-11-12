from product import Product

LINE = "-" * 47


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def get_products(self) -> list[Product]:
        return list(self.__products)

    def display_all_products(self) -> None:
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("No products in inventory.")
            print(LINE)
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
            print(LINE)
