# UML Class Diagram - OOP Inventory Management System

This diagram covers the product hierarchy with `CanBeShipped`, plus `Supplier`, `Inventory`, `Order` and `OrderLine`, with types, multiplicities and the relationship kinds made explicit. Types are language-independent (`String`, `Integer`, `Real`, `Boolean`, `Product [0..*]`, `Product [0..1]`).

```
+-------------------------------+                             +--------------------------------------------+
| Supplier                      |                             | <<abstract>>                               |
+-------------------------------+                             | Product                                    |
| - supplier_id: String         | 1                      0..* +--------------------------------------------+                  +------------------------------+
| - name: String                +-----------------------------+ - product_id: String                       |                  | OrderLine                    |
| - contact_email: String       |  (association)              | - name: String                             | 1           0..* +------------------------------+
+-------------------------------+                             | - price: Real                              +------------------+ - product: Product           |
| + display_information(): void |                             | - stock: Integer                           |  (association)   | - quantity: Integer          |
+-------------------------------+                             | - supplier: Supplier                       |                  +------------------------------+
                                                              +--------------------------------------------+                  | + calculate_subtotal(): Real |
                                                              | + get_product_id(): String                 |                  +------------------------------+
+------------------------------------------+                  | + get_name(): String                       |                              |  0..*
| Inventory                                |                  | + get_price(): Real                        |                              |
+------------------------------------------+ 0..1        0..* | + get_stock(): Integer                     |                              |       (composition)
| - products: Product [0..*]               +<>----------------+ + get_supplier(): Supplier                 |                              |
+------------------------------------------+  (aggregation)   | + update_stock(quantity: Integer): void    |                              |
| + add_product(product: Product): Boolean |                  | + display_information(): void              |                             <#> 1
| + remove_product(product_id: String):    |                  | + {abstract} get_fulfilment_info(): String |                              |
|       Product [0..1]                     |                  +--------------------------------------------+                  +-------------------------------------------------------------+
| + find_product(product_id: String):      |                                         ^                                        | Order                                                       |
|       Product [0..1]                     |                                         | (inheritance)                          +-------------------------------------------------------------+
| + get_products(): Product [0..*]         |                                         |                                        | - order_id: String                                          |
| + display_all_products(): void           |                                         |                                        | - order_lines: OrderLine [0..*]                             |
+------------------------------------------+                                         |                                        +-------------------------------------------------------------+
                                                                                     |                                        | + add_order_line(product: Product, quantity: Integer): void |
                                                                                     |                                        | + remove_order_line(product_id: String): Boolean            |
                                                                                     |                                        | + calculate_total(): Real                                   |
                                                                      ---------------+--------------------------              +-------------------------------------------------------------+
                                                                      |                                        |
                                                    +-----------------------------------+     +---------------------------------+
                                                    | PhysicalProduct                   |     | DigitalProduct                  |
                                                    +-----------------------------------+     +---------------------------------+
                                                    | - weight: Real                    |     | - download_size: Real           |
                                                    +-----------------------------------+     +---------------------------------+
                                                    | + get_weight(): Real              |     | + get_download_size(): Real     |
                                                    | + calculate_shipping_cost(): Real |     | + get_fulfilment_info(): String |
                                                    | + get_fulfilment_info(): String   |     | + display_information(): void   |
                                                    | + display_information(): void     |     +---------------------------------+
                                                    +-----------------------------------+
                                                                      :
                                                                      : (realisation)
                                                                      :
                                                                      v
                                                    +----------------------------------------------+
                                                    | <<interface>>                                |
                                                    | CanBeShipped                                 |
                                                    +----------------------------------------------+
                                                    | + {abstract} calculate_shipping_cost(): Real |
                                                    +----------------------------------------------+
```

Notation:

- Solid line with `^` (hollow triangle): inheritance. `PhysicalProduct` and `DigitalProduct` extend `Product`, which is `<<abstract>>` with the abstract method `get_fulfilment_info()`.
- Dashed line with `v` (hollow triangle): interface realisation. `PhysicalProduct` realises `CanBeShipped`. `DigitalProduct` does not.
- Plain solid line: association. `<>` (hollow diamond) sits at the whole end of an aggregation. `<#>` (filled diamond) sits at the whole end of a composition.
- Types written as `Product [0..*]` correspond to Python's `list[Product]`, and `Product [0..1]` to `Product | None`. Every type shown matches the hints in the Python source.

Relationships (each checked against Section 1 of the lab):

| Relationship | Kind | Multiplicity | Why |
|---|---|---|---|
| `PhysicalProduct`, `DigitalProduct` to `Product` | Inheritance | n/a | is-a; `Product` is abstract |
| `PhysicalProduct` to `CanBeShipped` | Realisation | n/a | Only physical products can be shipped |
| `Supplier` to `Product` | Association | `Supplier 1` to `Product 0..*` | A supplier is not part of a product or vice versa. It is created independently and passed to the product. A stored reference alone does not make it aggregation |
| `Inventory` to `Product` | Aggregation (diamond at `Inventory`) | `Inventory 0..1` to `Product 0..*` | Whole-part, but a product exists before, outside and after an inventory and can be transferred |
| `Order` to `OrderLine` | Composition (diamond at `Order`) | `Order 1` to `OrderLine 0..*` | `Order` creates its lines. A line belongs to exactly one order and is never transferred |
| `OrderLine` to `Product` | Association | `OrderLine 0..*` to `Product 1` | A line refers to a product but does not own it. The product also lives in inventories |

## Responsibilities (Single Responsibility Principle)

| Part | File | Responsibility |
|------|------|----------------|
| Product | `product.py` | Abstract base: stores common product information and manages its own state (validates stock changes) |
| PhysicalProduct | `physical_product.py` | Adds weight and shipping cost calculation |
| DigitalProduct | `digital_product.py` | Adds download size |
| CanBeShipped | `can_be_shipped.py` | Interface-style contract for shippable objects |
| Inventory | `inventory.py` | Stores, adds, removes, finds and displays products (aggregation) |
| Supplier | `supplier.py` | Holds supplier details (association with Product) |
| Order | `order.py` | Creates and manages its own order lines and calculates the total (composition) |
| OrderLine | `order_line.py` | One product and quantity within an order, calculates its subtotal |
| Main Program | `oop_inventory_manager.py` | Displays the menu, gets user input, creates the products and inventory, calls Inventory methods |
| File Handling | `oop_inventory_manager.py` (`load_inventory`, `save_inventory`) | Loads and saves inventory data in `inventory.json`, using a `type` identifier (`physical` / `digital`) to rebuild the right subclass |
