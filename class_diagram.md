# UML Class Diagram - OOP Inventory Management System

```
                       +------------------------------------------+
                       |        <<abstract>> Product              |
                       +------------------------------------------+
                       | - __product_id : String                  |
                       | - __name : String                        |
                       | - __price : float                        |
                       | - __stock : int                          |
                       +------------------------------------------+
                       | + __init__(product_id, name, price,      |
                       |            stock)                        |
                       | + get_product_id() : String              |
                       | + get_name() : String                    |
                       | + get_price() : float                    |
                       | + get_stock() : int                      |
                       | + update_stock(quantity : int) : void    |
                       | + display_information() : void           |
                       | + __str__() : String                     |
                       | + {abstract} get_fulfilment_info()       |
                       |       : String                           |
                       +------------------------------------------+
                          ^                    ^               ^
                          |                    |               | 0..*
        +-----------------+                    |               |
        |                                      |               | 1
+-------------------------------+  +----------------------+  +--------------------------+
|        PhysicalProduct        |  |    DigitalProduct    |  |        Inventory         |
+-------------------------------+  +----------------------+  +--------------------------+
| - __weight : float            |  | - __download_size    |  | - __products :           |
|                               |  |       : float        |  |       List<Product>      |
+-------------------------------+  +----------------------+  +--------------------------+
| + get_weight() : float        |  | + get_download_size()|  | + add_product(product)   |
| + calculate_shipping_cost()   |  |       : float        |  |       : bool             |
|       : float                 |  | + get_fulfilment_info|  | + search_product(id)     |
| + get_fulfilment_info()       |  |       () : String    |  |       : Product          |
|       : String                |  | + display_information|  | + get_products()         |
| + display_information() : void|  |       () : void      |  |       : List<Product>    |
+-------------------------------+  +----------------------+  | + display_all() : void   |
        :                                                    +--------------------------+
        :
        V   (dashed line, hollow triangle: realisation)
+------------------------------------------+
|     <<interface>> CanBeShipped (ABC)     |
+------------------------------------------+
| + {abstract} calculate_shipping_cost()   |
|       : float                            |
+------------------------------------------+
```

Notation:

- Solid line with hollow triangle (`^`): inheritance. `PhysicalProduct` and `DigitalProduct` extend `Product`.
- Dashed line with hollow triangle (`:` / `V`): interface realisation. `PhysicalProduct` realises `CanBeShipped`. `DigitalProduct` does not.
- `Product` is `<<abstract>>` and `get_fulfilment_info()` is an abstract method, so `Product` cannot be instantiated directly.
- `CanBeShipped` is an interface-style abstract base class (single class inheritance plus one interface).

Relationship: one Inventory holds zero or more Product objects (physical or digital).

## Responsibilities (Single Responsibility Principle)

| Part | File | Responsibility |
|------|------|----------------|
| Product | `product.py` | Abstract base: stores common product information and manages its own state (validates stock changes) |
| PhysicalProduct | `physical_product.py` | Adds weight and shipping cost calculation |
| DigitalProduct | `digital_product.py` | Adds download size |
| CanBeShipped | `can_be_shipped.py` | Interface-style contract for shippable objects |
| Inventory | `inventory.py` | Stores, adds, searches and displays products |
| Main Program | `oop_inventory_manager.py` | Displays the menu, gets user input, creates the products and inventory, calls Inventory methods |
| File Handling | `oop_inventory_manager.py` (`load_inventory`, `save_inventory`) | Loads and saves inventory data in `inventory.json`, using a `type` identifier (`physical` / `digital`) to rebuild the right subclass |
