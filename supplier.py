class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        supplier_id = str(supplier_id).strip()
        name = str(name).strip()
        contact_email = str(contact_email).strip()
        if not supplier_id:
            raise ValueError("Supplier ID cannot be empty.")
        if not name:
            raise ValueError("Supplier name cannot be empty.")
        if "@" not in contact_email:
            raise ValueError("Contact email must be a valid email address.")

        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

    def __str__(self) -> str:
        return f"{self.__name} ({self.__supplier_id}) <{self.__contact_email}>"
