
# ByteBites Domain Model

## Design Overview

**Customer** — Represents a verified user with identity and purchase history for accountability.

**FoodItem** — Represents a catalog entry with pricing, categorization, and popularity metrics for discovery.

**Menu** — Manages the complete collection of food items and provides category-based filtering for browsing.

**Transaction** — Groups selected items into a single checkout event and computes the total cost.

## Key Relationships

- **Customer places Transaction** — Each customer can have multiple purchases; transactions link back to the customer.
- **Transaction contains FoodItem** — A transaction bundles the specific items selected at checkout.
- **Menu lists FoodItem** — The menu is the authoritative catalog that all transactions reference.

---

```mermaid
classDiagram
    class Customer {
        +customerId: string
        +name: string
        +purchaseHistory: Transaction[]
    }

    class FoodItem {
        +itemId: string
        +name: string
        +price: decimal
        +category: string
        +popularityRating: number
    }

    class Menu {
        +items: FoodItem[]
        +getItemsByCategory(category: string): FoodItem[]
    }

    class Transaction {
        +transactionId: string
        +items: FoodItem[]
        +totalCost: decimal
        +calculateTotal(): decimal
    }

    Customer "1" --> "0..*" Transaction : places
    Transaction "1" --> "1..*" FoodItem : contains
    Menu "1" o-- "0..*" FoodItem : lists
```
