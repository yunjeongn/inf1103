from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        order_id = str(order_id).strip()
        if not order_id:
            raise ValueError("Order ID cannot be empty.")
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        for order_line in self.__order_lines:
            print(f"  {order_line}")
        print(f"  Total: ${self.calculate_total():.2f}")
