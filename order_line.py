from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def __str__(self) -> str:
        return (f"{self.__product.get_name()} x {self.__quantity} "
                f"@ ${self.__product.get_price():.2f} = "
                f"${self.calculate_subtotal():.2f}")
