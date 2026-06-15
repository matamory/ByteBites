"""
ByteBites Domain Models

Customer: Represents a verified user with identity and purchase history for accountability.
FoodItem: Represents a catalog entry with pricing, categorization, and popularity metrics for discovery.
Menu: Manages the complete collection of food items and provides category-based filtering for browsing.
Transaction: Groups selected items into a single checkout event and computes the total cost.
"""

class FoodItem:
    def __init__(self, item_id, name, price, category, popularity_rating):
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
        return (
            f"FoodItem(id={self.item_id}, name={self.name}, price={self.price:.2f}, "
            f"category={self.category}, popularity_rating={self.popularity_rating})"
        )


class Menu:
    def __init__(self, items=None):
        self.items = list(items) if items is not None else []

    def add_item(self, food_item):
        if not isinstance(food_item, FoodItem):
            raise TypeError("food_item must be a FoodItem instance")
        self.items.append(food_item)

    def get_items_by_category(self, category):
        return [item for item in self.items if item.category == category]

    def __str__(self):
        return f"Menu(items={len(self.items)})"


class Transaction:
    def __init__(self, transaction_id, items=None):
        self.transaction_id = transaction_id
        self.items = list(items) if items is not None else []
        self.total_cost = 0.0

    def add_item(self, food_item):
        if not isinstance(food_item, FoodItem):
            raise TypeError("food_item must be a FoodItem instance")
        self.items.append(food_item)

    def calculate_total(self):
        self.total_cost = sum(item.price for item in self.items)
        return self.total_cost

    def get_item_count(self):
        return len(self.items)

    def __str__(self):
        return (
            f"Transaction(id={self.transaction_id}, items={self.get_item_count()}, "
            f"total_cost={self.total_cost:.2f})"
        )


class Customer:
    def __init__(self, customer_id, name, purchase_history=None):
        self.customer_id = customer_id
        self.name = name
        self.purchase_history = list(purchase_history) if purchase_history is not None else []

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction instance")
        self.purchase_history.append(transaction)

    def get_total_spending(self):
        return sum(transaction.total_cost for transaction in self.purchase_history)

    def get_transaction_count(self):
        return len(self.purchase_history)

    def __str__(self):
        return (
            f"Customer(id={self.customer_id}, name={self.name}, "
            f"transactions={self.get_transaction_count()}, "
            f"total_spending={self.get_total_spending():.2f})"
        )