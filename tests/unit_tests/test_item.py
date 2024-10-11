import unittest
import uuid
from shopping_cart.models.item import Item


class TestItem(unittest.TestCase):
    def test_valid_item_creation(self):
        """Test creating a valid Item."""
        item = Item(name='Apple', price=0.99)
        self.assertEqual(item.name, 'Apple')
        self.assertEqual(item.price, 0.99)
        self.assertIsInstance(item.uid, uuid.UUID)

    def test_invalid_item_name(self):
        """Test creating an Item with invalid name."""
        with self.assertRaises(ValueError):
            Item(name='', price=0.99)
        with self.assertRaises(TypeError):
            Item(name=123, price=0.99)

    def test_invalid_item_price(self):
        """Test creating an Item with invalid price."""
        with self.assertRaises(ValueError):
            Item(name='Apple', price=-0.99)
        with self.assertRaises(TypeError):
            Item(name='Apple', price='0.99')

    def test_item_immutability(self):
        """Test that Item attributes are immutable."""
        item = Item(name='Banana', price=0.59)
        with self.assertRaises(AttributeError):
            item.name = 'Orange'
        with self.assertRaises(AttributeError):
            item.price = 0.69

    def test_item_uid_uniqueness(self):
        """Test that each Item has a unique UID."""
        item1 = Item(name='Apple', price=0.99)
        item2 = Item(name='Apple', price=0.99)
        self.assertNotEqual(item1.uid, item2.uid)

if __name__ == '__main__':
    unittest.main()
