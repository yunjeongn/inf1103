from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        download_size = float(download_size)
        if download_size < 0:
            raise ValueError("Download size must be 0 or more.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        print(f"ID: {self.get_product_id()}")
        print(f"Name: {self.get_name()}")
        print(f"Price: ${self.get_price():.2f}")
        print(f"Stock: {self.get_stock()}")
        print(f"Download Size: {self.__download_size:.2f} MB")
