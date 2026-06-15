"""
ByteBites Test Suite

Test the domain models from an external perspective:
- What does the system produce when given inputs?
- Where might it break?
"""

import pytest
from models import FoodItem, Menu, Transaction, Customer


class TestFoodItem:
    """FoodItem validation and representation tests."""

    def test_create_valid_food_item(self):
        """Verify that a valid food item stores all attributes correctly."""
        item = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        assert item.item_id == "f1"
        assert item.name == "Burger"
        assert item.price == 8.50
        assert item.category == "Entrees"
        assert item.popularity_rating == 4.8

    def test_reject_empty_name(self):
        """Verify that FoodItem rejects an empty name."""
        with pytest.raises(ValueError):
            FoodItem("f1", "", 8.50, "Entrees", 4.8)

    def test_reject_empty_category(self):
        """Verify that FoodItem rejects an empty category."""
        with pytest.raises(ValueError):
            FoodItem("f1", "Burger", 8.50, "", 4.8)

    def test_reject_negative_price(self):
        """Verify that FoodItem rejects a negative price."""
        with pytest.raises(ValueError):
            FoodItem("f1", "Burger", -5.00, "Entrees", 4.8)

    def test_zero_price_is_valid(self):
        """Verify that a price of zero is accepted (boundary: only negative prices are rejected)."""
        item = FoodItem("f1", "Free Sample", 0.0, "Promotions", 4.0)
        assert item.price == 0.0

    def test_food_item_string_representation(self):
        """Verify that FoodItem produces a readable string for debugging."""
        item = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        result = str(item)
        assert "f1" in result
        assert "Burger" in result
        assert "8.50" in result


class TestMenu:
    """Menu operations: adding items, filtering, and state management."""

    def test_create_menu_with_no_items(self):
        """Verify that a new menu starts with an empty item list."""
        menu = Menu()
        assert len(menu.items) == 0

    def test_create_menu_with_initial_items(self):
        """Verify that a menu can be initialized with a list of items."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        menu = Menu([burger, soda])
        assert len(menu.items) == 2

    def test_menu_owns_initial_items(self):
        """Verify that menu makes a defensive copy of the initial item list."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        initial_list = [burger]
        menu = Menu(initial_list)
        initial_list.clear()
        assert len(menu.items) == 1

    def test_add_item_to_menu(self):
        """Verify that items can be added to a menu after creation."""
        menu = Menu()
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        menu.add_item(burger)
        assert len(menu.items) == 1
        assert menu.items[0].name == "Burger"

    def test_reject_non_fooditem_in_menu(self):
        """Verify that menu rejects invalid item types."""
        menu = Menu()
        with pytest.raises(TypeError):
            menu.add_item("not a FoodItem")

    def test_filter_items_by_category(self):
        """Verify that filtering by category returns only items in that category."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        cake = FoodItem("f3", "Cake", 5.00, "Desserts", 4.9)
        menu = Menu([burger, soda, cake])
        
        drinks = menu.get_items_by_category("Drinks")
        assert len(drinks) == 1
        assert drinks[0].name == "Soda"

    def test_filter_returns_empty_list_when_no_match(self):
        """Verify that filtering a non-existent category returns an empty list."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        menu = Menu([burger])
        
        drinks = menu.get_items_by_category("Drinks")
        assert len(drinks) == 0

    def test_menu_string_representation(self):
        """Verify that menu produces a readable string for debugging."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        menu = Menu([burger, soda])
        result = str(menu)
        assert "items=2" in result


class TestTransaction:
    """Transaction operations: adding items, calculating totals, and state management."""

    def test_create_empty_transaction(self):
        """Verify that a new transaction starts with zero items and zero cost."""
        transaction = Transaction("t1")
        assert len(transaction.items) == 0
        assert transaction.total_cost == 0.0

    def test_transaction_initializes_total_with_items(self):
        """Verify that a transaction initialized with items calculates the total immediately."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        transaction = Transaction("t1", [burger, soda])
        assert transaction.total_cost == 10.75

    def test_add_item_to_transaction(self):
        """Verify that items can be added to a transaction after creation."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        transaction = Transaction("t1")
        transaction.add_item(burger)
        assert len(transaction.items) == 1
        assert transaction.items[0].name == "Burger"

    def test_total_cost_updates_after_adding_item(self):
        """Verify that transaction total is recalculated automatically after adding an item."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        transaction = Transaction("t1", [burger])
        assert transaction.total_cost == 8.50
        transaction.add_item(soda)
        assert transaction.total_cost == 10.75

    def test_calculate_total_returns_the_total(self):
        """Verify that calculate_total returns the computed total cost."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        transaction = Transaction("t1", [burger, soda])
        result = transaction.calculate_total()
        assert result == 10.75

    def test_order_total_is_zero_when_empty(self):
        """Verify that an empty transaction has a total cost of $0."""
        transaction = Transaction("t1")
        assert transaction.total_cost == 0.0
        assert transaction.calculate_total() == 0.0

    def test_transaction_owns_initial_items(self):
        """Verify that transaction makes a defensive copy of the initial item list."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        initial_list = [burger]
        transaction = Transaction("t1", initial_list)
        initial_list.clear()
        assert transaction.get_item_count() == 1

    def test_reject_non_fooditem_in_transaction(self):
        """Verify that transaction rejects invalid item types."""
        transaction = Transaction("t1")
        with pytest.raises(TypeError):
            transaction.add_item("not a FoodItem")

    def test_get_item_count(self):
        """Verify that get_item_count returns the correct number of items."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        transaction = Transaction("t1", [burger])
        assert transaction.get_item_count() == 1
        transaction.add_item(soda)
        assert transaction.get_item_count() == 2

    def test_transaction_string_representation(self):
        """Verify that transaction produces a readable string for debugging."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        transaction = Transaction("t1", [burger, soda])
        result = str(transaction)
        assert "t1" in result
        assert "items=2" in result
        assert "10.75" in result


class TestCustomer:
    """Customer operations: managing transactions and computing spending metrics."""

    def test_create_customer_with_no_history(self):
        """Verify that a new customer starts with no purchase history."""
        customer = Customer("c1", "Ava")
        assert len(customer.purchase_history) == 0
        assert customer.get_transaction_count() == 0

    def test_create_customer_with_initial_history(self):
        """Verify that a customer can be initialized with a list of transactions."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        transaction = Transaction("t1", [burger])
        customer = Customer("c1", "Ava", [transaction])
        assert customer.get_transaction_count() == 1

    def test_customer_owns_purchase_history(self):
        """Verify that customer makes a defensive copy of the initial history."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        transaction = Transaction("t1", [burger])
        initial_history = [transaction]
        customer = Customer("c1", "Ava", initial_history)
        initial_history.clear()
        assert customer.get_transaction_count() == 1

    def test_add_transaction_to_customer(self):
        """Verify that transactions can be added to a customer after creation."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        transaction = Transaction("t1", [burger])
        customer = Customer("c1", "Ava")
        customer.add_transaction(transaction)
        assert customer.get_transaction_count() == 1

    def test_reject_non_transaction_in_customer(self):
        """Verify that customer rejects invalid transaction types."""
        customer = Customer("c1", "Ava")
        with pytest.raises(TypeError):
            customer.add_transaction("not a Transaction")

    def test_get_transaction_count(self):
        """Verify that get_transaction_count returns the number of transactions."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        t1 = Transaction("t1", [burger])
        t2 = Transaction("t2", [burger])
        customer = Customer("c1", "Ava", [t1])
        assert customer.get_transaction_count() == 1
        customer.add_transaction(t2)
        assert customer.get_transaction_count() == 2

    def test_get_total_spending_with_single_transaction(self):
        """Verify that customer spending equals the transaction total for a single purchase."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        transaction = Transaction("t1", [burger, soda])
        customer = Customer("c1", "Ava", [transaction])
        assert customer.get_total_spending() == 10.75

    def test_get_total_spending_with_multiple_transactions(self):
        """Verify that customer spending sums across all transactions."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)
        t1 = Transaction("t1", [burger])
        t2 = Transaction("t2", [soda])
        customer = Customer("c1", "Ava", [t1, t2])
        assert customer.get_total_spending() == 10.75

    def test_customer_spending_zero_when_no_transactions(self):
        """Verify that a customer with no transactions has zero total spending."""
        customer = Customer("c1", "Ava")
        assert customer.get_total_spending() == 0.0

    def test_customer_string_representation(self):
        """Verify that customer produces a readable string for debugging."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        transaction = Transaction("t1", [burger])
        customer = Customer("c1", "Ava", [transaction])
        result = str(customer)
        assert "c1" in result
        assert "Ava" in result
        assert "transactions=1" in result
        assert "8.50" in result


class TestIntegration:
    """End-to-end scenario tests that verify the system as a whole."""

    def test_complete_order_flow(self):
        """Verify a complete workflow: menu creation, filtering, ordering, and customer verification."""
        burger = FoodItem("f1", "Spicy Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Large Soda", 2.25, "Drinks", 4.2)
        cake = FoodItem("f3", "Chocolate Cake", 5.00, "Desserts", 4.9)

        menu = Menu([burger, soda, cake])
        drinks = menu.get_items_by_category("Drinks")
        assert len(drinks) == 1

        order = Transaction("order1")
        order.add_item(burger)
        order.add_item(soda)
        assert order.get_item_count() == 2
        assert order.total_cost == 10.75

        customer = Customer("c1", "Ava")
        customer.add_transaction(order)
        assert customer.get_transaction_count() == 1
        assert customer.get_total_spending() == 10.75

    def test_multiple_customers_multiple_orders(self):
        """Verify that the system correctly tracks spending across multiple customers."""
        burger = FoodItem("f1", "Burger", 8.50, "Entrees", 4.8)
        soda = FoodItem("f2", "Soda", 2.25, "Drinks", 4.2)

        customer1 = Customer("c1", "Ava")
        order1 = Transaction("t1", [burger])
        customer1.add_transaction(order1)

        customer2 = Customer("c2", "Bob")
        order2 = Transaction("t2", [burger, soda])
        customer2.add_transaction(order2)

        assert customer1.get_total_spending() == 8.50
        assert customer2.get_total_spending() == 10.75
        assert customer1.get_transaction_count() == 1
        assert customer2.get_transaction_count() == 1
