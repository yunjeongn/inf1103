from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        weight = float(weight)
        if weight < 0:
            raise ValueError("Weight must be 0 or more.")
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def calculate_shipping_cost(self) -> float:
        return 5.0 + 2.0 * self.__weight

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping to the customer."

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")
