# UML Class Diagram - OOP Inventory Management System

```
+------------------------------------------+
|                 Product                  |
+------------------------------------------+
| - __product_id : String                  |
| - __name : String                        |
| - __price : float                        |
| - __stock : int                          |
+------------------------------------------+
| + __init__(product_id : String,          |
|            name : String,                |
|            price : float, stock : int)   |
| + get_product_id() : String              |
| + get_name() : String                    |
| + get_price() : float                    |
| + get_stock() : int                      |
| + update_stock(quantity : int) : void    |
| + display_information() : void           |
| + __str__() : String                     |
+------------------------------------------+
                    ^
                    | 0..*
                    |
                    | 1
+------------------------------------------+
|                Inventory                 |
+------------------------------------------+
| - __products : List<Product>             |
+------------------------------------------+
| + __init__()                             |
| + add_product(product : Product) : bool  |
| + search_product(product_id : String)    |
|       : Product                          |
| + get_products() : List<Product>         |
| + display_all() : void                   |
+------------------------------------------+
```

Relationship: one Inventory holds zero or more Product objects.

## Responsibilities (Single Responsibility Principle)

| Part | File | Responsibility |
|------|------|----------------|
| Product | `product.py` | Stores product information and manages its own state (validates stock changes) |
| Inventory | `inventory.py` | Stores, adds, searches and displays products |
| Main Program | `oop_inventory_manager.py` | Displays the menu, gets user input, creates the products and inventory, calls Inventory methods |
| File Handling | `oop_inventory_manager.py` (`load_inventory`, `save_inventory`) | Loads and saves inventory data in `inventory.json` |
