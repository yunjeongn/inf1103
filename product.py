import math
from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        product_id = str(product_id).strip()
        name = str(name).strip()
        if not product_id:
            raise ValueError("Product ID cannot be empty.")
        if not name:
            raise ValueError("Product name cannot be empty.")
        price = float(price)
        if not math.isfinite(price) or price < 0:
            raise ValueError("Price must be 0 or more.")

        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock: int = 0
        self.__supplier: Supplier = supplier
        self.update_stock(stock)

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print(f"Supplier: {self.__supplier.get_name()}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def __str__(self):
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")
