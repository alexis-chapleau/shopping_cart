import unittest
from shopping_cart.models.item import Item
from shopping_cart.models.shopping_cart import ShoppingCart
import json
import yaml
import csv
import io

class TestShoppingCartIntegration(unittest.TestCase):
    """Integration tests for the ShoppingCart class and receipt generation."""

    def test_shopping_cart_integration(self):
        """Test the full functionality of the ShoppingCart."""

        # Instantiate the shopping cart
        cart = ShoppingCart()

        # Create items
        item1 = Item(name='Apple', price=1.00)
        item2 = Item(name='Banana', price=0.50)
        item3 = Item(name='Apple', price=1.00)
        item4 = Item(name='Orange', price=0.75)

        # Add items to the cart
        cart.add_item(item1)
        cart.add_item(item2)
        cart.add_item(item3)
        cart.add_item(item4)

        # Verify total quantity and price
        self.assertEqual(cart.total_quantity, 4)
        self.assertEqual(cart.total_price, 3.25)

        # Get total quantity by name
        total_apples = cart.get_total_quantity_by_name('Apple')
        self.assertEqual(total_apples, 2)

        # List items by name
        apples = cart.list_items_by_name('Apple')
        self.assertEqual(len(apples), 2)

        # Remove an Apple
        cart.remove_item(item1)

        # Verify total quantity and price after removal
        self.assertEqual(cart.total_quantity, 3)
        self.assertEqual(cart.total_price, 2.25)

        # Verify total quantity of Apples after removal
        total_apples = cart.get_total_quantity_by_name('Apple')
        self.assertEqual(total_apples, 1)

        # Attempt to remove a non-existent item (should raise KeyError)
        with self.assertRaises(KeyError):
            cart.remove_item(item1)

        # Clear the cart
        cart.clear_cart()

        # Verify the cart is empty
        self.assertEqual(cart.total_quantity, 0)
        self.assertEqual(cart.total_price, 0.0)
        self.assertEqual(len(cart.list_items()), 0)

        # Add items again
        cart.add_item(item1)
        cart.add_item(item2)
        cart.add_item(item3)
        cart.add_item(item4)

        # Generate receipts in all formats and verify contents
        formats = ['json', 'csv', 'text', 'yaml']
        for fmt in formats:
            receipt_content = cart.generate_receipt(format_type=fmt)
            self.assertIsNotNone(receipt_content)
            self.assertTrue(len(receipt_content) > 0)
            # Additional format-specific checks
            if fmt == 'json':
                receipt = json.loads(receipt_content)
                self.assertEqual(receipt['total_price'], 3.25)
                self.assertEqual(len(receipt['items']), 4)
            elif fmt == 'yaml':
                receipt = yaml.safe_load(receipt_content)
                self.assertEqual(receipt['total_price'], 3.25)
                self.assertEqual(len(receipt['items']), 4)
            elif fmt == 'csv':
                reader = csv.reader(io.StringIO(receipt_content))
                lines = list(reader)
                self.assertEqual(len(lines), 6)  # Header + 4 items + total price
                self.assertEqual(lines[0], ['UID', 'Name', 'Unit Price'])
            elif fmt == 'text':
                lines = receipt_content.strip().split('\n')
                self.assertTrue("Receipt:" in lines[0])
                self.assertTrue(f"Total Price: ${cart.total_price:.2f}" in lines[-1])

        # Update the cart: Remove all Bananas
        cart.remove_item(item2)

        # Verify total quantity and price after removing Bananas
        self.assertEqual(cart.total_quantity, 3)
        self.assertEqual(cart.total_price, 2.75)

        # Generate a receipt and check that Bananas are not included
        receipt_content = cart.generate_receipt(format_type='json')
        receipt = json.loads(receipt_content)
        item_names = [item['name'] for item in receipt['items']]
        self.assertNotIn('Banana', item_names)
        self.assertEqual(receipt['total_price'], 2.75)

        # Bonus Implementation: Test edge cases
        # Try removing an item by UID that has already been removed
        with self.assertRaises(KeyError):
            cart.remove_item(item2)

        # Try adding an item with invalid type
        with self.assertRaises(TypeError):
            cart.add_item("NotAnItemInstance")

        # Try adding an item with invalid price
        with self.assertRaises(ValueError):
            invalid_item = Item(name='Invalid', price=-10.00)
            cart.add_item(invalid_item)

        # Verify the cart's integrity after exceptions
        self.assertEqual(cart.total_quantity, 3)
        self.assertEqual(cart.total_price, 2.75)

        # Final cleanup: Clear the cart
        cart.clear_cart()
        self.assertEqual(cart.total_quantity, 0)
        self.assertEqual(cart.total_price, 0.0)

if __name__ == '__main__':
    unittest.main()
