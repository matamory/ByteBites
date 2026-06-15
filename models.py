"""
ByteBites Domain Models

Customer: Represents a verified user with identity and purchase history for accountability.
FoodItem: Represents a catalog entry with pricing, categorization, and popularity metrics for discovery.
Menu: Manages the complete collection of food items and provides category-based filtering for browsing.
Transaction: Groups selected items into a single checkout event and computes the total cost.
"""

class FoodItem:
    def __init__(self, item_id, name, price, category, popularity_rating):
        """Create a validated catalog item."""
        if not name:
            raise ValueError("name cannot be empty")
        if not category:
            raise ValueError("category cannot be empty")
        if price < 0:
            raise ValueError("price cannot be negative")
        self.item_id = item_id
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating

    def __str__(self):
        """Return a readable summary for debugging and logging."""
        return (
            f"FoodItem(id={self.item_id}, name={self.name}, price={self.price:.2f}, "
            f"category={self.category}, popularity_rating={self.popularity_rating})"
        )


class Menu:
    def __init__(self, items=None):
        """Create a menu that owns its item collection."""
        self.items = list(items) if items is not None else []

    def add_item(self, food_item):
        """Add a FoodItem to the menu."""
        if not isinstance(food_item, FoodItem):
            raise TypeError("food_item must be a FoodItem instance")
        self.items.append(food_item)

    def get_items_by_category(self, category):
        """Return only menu items that match the requested category."""
        return [item for item in self.items if item.category == category]

    def __str__(self):
        """Return a readable summary for debugging and logging."""
        return f"Menu(items={len(self.items)})"


class Transaction:
    def __init__(self, transaction_id, items=None):
        """Create a transaction with an owned list of items."""
        self.transaction_id = transaction_id
        self.items = list(items) if items is not None else []
        self.total_cost = 0.0
        self.calculate_total()

    def add_item(self, food_item):
        """Add a FoodItem to the transaction."""
        if not isinstance(food_item, FoodItem):
            raise TypeError("food_item must be a FoodItem instance")
        self.items.append(food_item)
        self.calculate_total()

    def calculate_total(self):
        """Compute and store the transaction total cost."""
        self.total_cost = sum(item.price for item in self.items)
        return self.total_cost

    def get_item_count(self):
        """Return the number of items in the transaction."""
        return len(self.items)

    def __str__(self):
        """Return a readable summary for debugging and logging."""
        return (
            f"Transaction(id={self.transaction_id}, items={self.get_item_count()}, "
            f"total_cost={self.total_cost:.2f})"
        )


class Customer:
    def __init__(self, customer_id, name, purchase_history=None):
        """Create a customer with owned purchase history."""
        self.customer_id = customer_id
        self.name = name
        self.purchase_history = list(purchase_history) if purchase_history is not None else []

    def add_transaction(self, transaction):
        """Append a Transaction to the customer's history."""
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction instance")
        self.purchase_history.append(transaction)

    def get_total_spending(self):
        """Return the sum of all transaction totals in purchase history."""
        return sum(transaction.total_cost for transaction in self.purchase_history)

    def get_transaction_count(self):
        """Return the number of transactions in purchase history."""
        return len(self.purchase_history)

    def __str__(self):
        """Return a readable summary for debugging and logging."""
        return (
            f"Customer(id={self.customer_id}, name={self.name}, "
            f"transactions={self.get_transaction_count()}, "
            f"total_spending={self.get_total_spending():.2f})"
        )


if __name__ == "__main__":
    burger = FoodItem("f1", "Spicy Burger", 8.50, "Entrees", 4.8)
    soda = FoodItem("f2", "Large Soda", 2.25, "Drinks", 4.2)
    dessert = FoodItem("f3", "Chocolate Cake", 5.00, "Desserts", 4.9)

    menu = Menu([burger])
    menu.add_item(soda)
    menu.add_item(dessert)

    sorted_by_price = sorted(menu.items, key=lambda item: item.price)
    drinks = menu.get_items_by_category("Drinks")

    order = Transaction("t1")
    order.add_item(burger)
    order.add_item(soda)
    order_total = order.calculate_total()

    customer = Customer("c1", "Ava", [order])

    print("Sorted menu by price:", [item.name for item in sorted_by_price])
    print("Drinks:", [item.name for item in drinks])
    print("Order total:", order_total)
    print("Customer spending:", customer.get_total_spending())
    print("Customer transactions:", customer.get_transaction_count())