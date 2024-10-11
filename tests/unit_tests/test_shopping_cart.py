import unittest
from unittest.mock import MagicMock
from shopping_cart.models.item import Item
from shopping_cart.models.shopping_cart import ShoppingCart


class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart()
        self.item1 = Item(name="Apple", price=1.0, uid="123")
        self.item2 = Item(name="Banana", price=0.5, uid="456")

    def test_add_item(self):
        self.cart.add_item(self.item1, quantity=3)
        self.assertEqual(self.cart.total_quantity, 3)
        self.assertEqual(self.cart.total_price, 3.0)
        self.assertIn("Apple", self.cart.list_items())

    def test_add_item_invalid(self):
        with self.assertRaises(TypeError):
            self.cart.add_item("NotAnItem")

        with self.assertRaises(ValueError):
            self.cart.add_item(self.item1, quantity=0)

    def test_remove_item_by_quantity(self):
        self.cart.add_item(self.item1, quantity=5)
        self.cart.remove_item("Apple", quantity=3)
        self.assertEqual(self.cart.get_total_quantity_by_name("Apple"), 2)
        self.assertEqual(self.cart.total_quantity, 2)
        self.assertEqual(self.cart.total_price, 2.0)

    def test_remove_item_by_uid(self):
        self.cart.add_item(self.item1, quantity=2)
        self.cart.remove_item("Apple", quantity=1, item_uid="123")
        self.assertEqual(self.cart.get_total_quantity_by_name("Apple"), 1)
        self.assertEqual(self.cart.total_quantity, 1)
        self.assertEqual(self.cart.total_price, 1.0)

    def test_remove_item_not_found(self):
        with self.assertRaises(KeyError):
            self.cart.remove_item("Orange")

    def test_remove_item_uid_not_found(self):
        self.cart.add_item(self.item1)
        with self.assertRaises(ValueError):
            self.cart.remove_item("Apple", quantity=1, item_uid="999")

    def test_clear_cart(self):
        self.cart.add_item(self.item1, quantity=4)
        self.cart.add_item(self.item2, quantity=3)
        self.cart.clear_cart()
        self.assertEqual(self.cart.total_quantity, 0)
        self.assertEqual(self.cart.total_price, 0.0)
        self.assertEqual(len(self.cart.list_items()), 0)

    def test_get_item(self):
        self.cart.add_item(self.item1)
        item = self.cart.get_item("Apple", "123")
        self.assertEqual(item, self.item1)

    def test_get_item_not_found(self):
        with self.assertRaises(KeyError):
            self.cart.get_item("Apple", "999")

    def test_list_items(self):
        self.cart.add_item(self.item1, quantity=2)
        self.cart.add_item(self.item2, quantity=1)
        items = self.cart.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Apple", items)
        self.assertIn("Banana", items)

    def test_generate_receipt(self):
        self.cart.add_item(self.item1, quantity=2)
        self.cart.add_item(self.item2)
        mock_strategy = MagicMock()
        mock_strategy.generate.return_value = "Receipt Content"
        get_receipt_strategy = MagicMock(return_value=mock_strategy)

        receipt = self.cart.generate_receipt(format_type='text')
        self.assertEqual(receipt, "Receipt Content")


if __name__ == '__main__':
    unittest.main()