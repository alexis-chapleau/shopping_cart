import unittest
from shopping_cart.models.shopping_cart import ShoppingCart
from shopping_cart.models.item import Item
import uuid


class TestShoppingCart(unittest.TestCase):
    """Unit tests for the ShoppingCart class."""

    def setUp(self):
        """Set up test resources."""
        self.cart = ShoppingCart()
        self.item1 = Item(name='Apple', price=1.00)
        self.item2 = Item(name='Banana', price=0.50)
        self.item3 = Item(name='Apple', price=1.00)  # Another Apple
        self.item4 = Item(name='Orange', price=0.75)

    def test_add_item(self):
        """Test adding items to the cart."""
        # Add item1 to the cart
        self.cart.add_item(self.item1)
        self.assertEqual(self.cart.total_quantity, 1)
        self.assertEqual(self.cart.total_price, 1.00)
        self.assertIn('Apple', self.cart._items)
        self.assertEqual(self.cart._items['Apple']['total_quantity'], 1)

        # Add item2 to the cart
        self.cart.add_item(self.item2)
        self.assertEqual(self.cart.total_quantity, 2)
        self.assertEqual(self.cart.total_price, 1.50)
        self.assertIn('Banana', self.cart._items)
        self.assertEqual(self.cart._items['Banana']['total_quantity'], 1)

        # Add another Apple (item3)
        self.cart.add_item(self.item3)
        self.assertEqual(self.cart.total_quantity, 3)
        self.assertEqual(self.cart.total_price, 2.50)
        self.assertEqual(self.cart._items['Apple']['total_quantity'], 2)
        self.assertEqual(len(self.cart._items['Apple']['instances']), 2)

    def test_add_item_invalid(self):
        """Test adding invalid items to the cart."""
        with self.assertRaises(TypeError):
            self.cart.add_item("NotAnItemInstance")

    def test_remove_item(self):
        """Test removing specific items from the cart."""
        # Add items to the cart
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item2)
        self.cart.add_item(self.item3)

        # Remove item1
        self.cart.remove_item(self.item1)
        self.assertEqual(self.cart.total_quantity, 2)
        self.assertEqual(self.cart.total_price, 1.50)
        self.assertEqual(self.cart._items['Apple']['total_quantity'], 1)

        # Remove item2
        self.cart.remove_item(self.item2)
        self.assertEqual(self.cart.total_quantity, 1)
        self.assertEqual(self.cart.total_price, 1.00)
        self.assertNotIn('Banana', self.cart._items)

        # Remove item3
        self.cart.remove_item(self.item3)
        self.assertEqual(self.cart.total_quantity, 0)
        self.assertEqual(self.cart.total_price, 0.00)
        self.assertNotIn('Apple', self.cart._items)

    def test_remove_item_not_in_cart(self):
        """Test removing an item that's not in the cart."""
        # Attempt to remove an item not added
        with self.assertRaises(KeyError):
            self.cart.remove_item(self.item1)

        # Add item1 and remove item2 (which wasn't added)
        self.cart.add_item(self.item1)
        with self.assertRaises(KeyError):
            self.cart.remove_item(self.item2)

    def test_get_item(self):
        """Test retrieving an item from the cart."""
        self.cart.add_item(self.item1)
        item = self.cart.get_item(item_name='Apple', item_uid=str(self.item1.uid))
        self.assertEqual(item, self.item1)

        # Attempt to get an item not in the cart
        with self.assertRaises(KeyError):
            self.cart.get_item(item_name='Banana', item_uid=str(self.item2.uid))

    def test_list_items(self):
        """Test listing all items in the cart."""
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item2)
        items = self.cart.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_by_name(self):
        """Test listing items by name."""
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item3)
        apples = self.cart.list_items_by_name('Apple')
        self.assertEqual(len(apples), 2)
        self.assertIn(self.item1, apples)
        self.assertIn(self.item3, apples)

        # Attempt to list items by a name not in the cart
        with self.assertRaises(KeyError):
            self.cart.list_items_by_name('Orange')

    def test_get_total_quantity_by_name(self):
        """Test getting total quantity by item name."""
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item3)
        quantity = self.cart.get_total_quantity_by_name('Apple')
        self.assertEqual(quantity, 2)

        # Attempt to get quantity for an item not in the cart
        with self.assertRaises(KeyError):
            self.cart.get_total_quantity_by_name('Orange')

    def test_total_price_and_quantity(self):
        """Test total price and total quantity properties."""
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item2)
        self.assertEqual(self.cart.total_quantity, 2)
        self.assertEqual(self.cart.total_price, 1.50)

        # Add more items
        self.cart.add_item(self.item3)
        self.cart.add_item(self.item4)
        self.assertEqual(self.cart.total_quantity, 4)
        self.assertEqual(self.cart.total_price, 3.25)

    def test_clear_cart(self):
        """Test clearing the cart."""
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item2)
        self.cart.clear_cart()
        self.assertEqual(self.cart.total_quantity, 0)
        self.assertEqual(self.cart.total_price, 0.00)
        self.assertEqual(len(self.cart._items), 0)

    def test_generate_receipt(self):
        """Test generating receipts in various formats."""
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item2)

        formats = ['json', 'csv', 'text', 'yaml']
        for fmt in formats:
            receipt_content = self.cart.generate_receipt(format_type=fmt)
            self.assertIsInstance(receipt_content, str)
            self.assertGreater(len(receipt_content), 0)

    def test_generate_receipt_invalid_format(self):
        """Test generating receipt with an invalid format."""
        self.cart.add_item(self.item1)
        with self.assertRaises(ValueError):
            self.cart.generate_receipt(format_type='invalid_format')

    def test_get_item_invalid_uid(self):
        """Test getting an item with an invalid UID."""
        self.cart.add_item(self.item1)
        invalid_uid = str(uuid.uuid4())
        with self.assertRaises(KeyError):
            self.cart.get_item(item_name='Apple', item_uid=invalid_uid)

    def test_add_item_invalid_type(self):
        """Test adding an item of invalid type."""
        with self.assertRaises(TypeError):
            self.cart.add_item(123)  # Invalid type

    def test_remove_item_invalid_type(self):
        """Test removing an item of invalid type."""
        with self.assertRaises(TypeError):
            self.cart.remove_item(123)  # Invalid type

    def test_total_price_rounding(self):
        """Test that total price is correctly rounded."""
        item_expensive = Item(name='Laptop', price=999.9999)
        self.cart.add_item(item_expensive)
        self.assertEqual(self.cart.total_price, 1000.00)


if __name__ == '__main__':
    unittest.main()
