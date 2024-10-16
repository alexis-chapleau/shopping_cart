import unittest
from shopping_cart.models.item import Item
from shopping_cart.models.shopping_cart import ShoppingCart
import json
import yaml
import csv
import io

class TestReceiptGeneration(unittest.TestCase):
    """Unit tests for receipt generation strategies."""

    def setUp(self):
        """Set up test resources."""
        self.cart = ShoppingCart()

        # Create items
        self.item1 = Item(name='Apple', price=1.00)
        self.item2 = Item(name='Banana', price=0.50)
        self.item3 = Item(name='Apple', price=1.00)

        # Add items to the cart
        self.cart.add_item(self.item1)
        self.cart.add_item(self.item2)
        self.cart.add_item(self.item3)

        # Expected total price
        self.expected_total_price = 2.50

        # Expected items list
        self.expected_items = [
            {'uid': str(self.item1.uid), 'name': 'Apple', 'unit_price': 1.00},
            {'uid': str(self.item3.uid), 'name': 'Apple', 'unit_price': 1.00},
            {'uid': str(self.item2.uid), 'name': 'Banana', 'unit_price': 0.50},
        ]

    def test_json_receipt_strategy(self):
        """Test the JSON receipt strategy."""
        receipt_content = self.cart.generate_receipt(format_type='json')

        # Parse the JSON content
        receipt = json.loads(receipt_content)

        # Verify total price
        self.assertEqual(receipt['total_price'], self.expected_total_price)

        # Verify items
        self.assertEqual(len(receipt['items']), len(self.expected_items))

        # Sort items for comparison
        receipt_items = sorted(receipt['items'], key=lambda x: x['uid'])
        expected_items = sorted(self.expected_items, key=lambda x: x['uid'])

        for expected_item, receipt_item in zip(expected_items, receipt_items):
            self.assertEqual(expected_item['uid'], receipt_item['uid'])
            self.assertEqual(expected_item['name'], receipt_item['name'])
            self.assertEqual(expected_item['unit_price'], receipt_item['unit_price'])

    def test_csv_receipt_strategy(self):
        """Test the CSV receipt strategy."""
        receipt_content = self.cart.generate_receipt(format_type='csv')

        # Read CSV content using csv.reader
        reader = csv.reader(io.StringIO(receipt_content))
        lines = list(reader)

        # Verify header
        expected_header = ['UID', 'Name', 'Unit Price']
        self.assertEqual(lines[0], expected_header)

        # Verify total price line
        total_price_line = lines[-1]
        self.assertEqual(total_price_line[0], 'Total Price')
        self.assertEqual(total_price_line[2], f"{self.expected_total_price:.2f}")

        # Verify items
        item_lines = lines[1:-1]
        self.assertEqual(len(item_lines), len(self.expected_items))

        # Parse item lines
        receipt_items = []
        for line in item_lines:
            uid, name, unit_price = line
            receipt_items.append({
                'uid': uid,
                'name': name,
                'unit_price': float(unit_price)
            })

        # Sort items for comparison
        receipt_items = sorted(receipt_items, key=lambda x: x['uid'])
        expected_items = sorted(self.expected_items, key=lambda x: x['uid'])

        for expected_item, receipt_item in zip(expected_items, receipt_items):
            self.assertEqual(expected_item['uid'], receipt_item['uid'])
            self.assertEqual(expected_item['name'], receipt_item['name'])
            self.assertEqual(expected_item['unit_price'], receipt_item['unit_price'])

    def test_text_receipt_strategy(self):
        """Test the Text receipt strategy."""
        receipt_content = self.cart.generate_receipt(format_type='text')

        # Split content into lines
        lines = receipt_content.strip().split('\n')

        # Verify receipt structure
        self.assertEqual(lines[0], "Receipt:")
        self.assertEqual(lines[1], "--------")

        # Verify items
        item_lines = lines[2:-2]  # Exclude header and total price
        expected_line_count = len(self.expected_items) * 2
        self.assertEqual(len(item_lines), expected_line_count)

        # Extract items from lines
        receipt_items = []
        for i in range(0, len(item_lines), 2):
            name_price_line = item_lines[i].strip()
            uid_line = item_lines[i + 1].strip()

            name_part, price_part = name_price_line.split('|')
            name = name_part.replace("Name: ", "").strip()
            unit_price = float(price_part.replace("Price: $", "").strip())
            uid = uid_line.replace("UID: ", "").strip()

            receipt_items.append({'uid': uid, 'name': name, 'unit_price': unit_price})

        # Sort items for comparison
        receipt_items = sorted(receipt_items, key=lambda x: x['uid'])
        expected_items = sorted(self.expected_items, key=lambda x: x['uid'])

        for expected_item, receipt_item in zip(expected_items, receipt_items):
            self.assertEqual(expected_item['uid'], receipt_item['uid'])
            self.assertEqual(expected_item['name'], receipt_item['name'])
            self.assertEqual(expected_item['unit_price'], receipt_item['unit_price'])

        # Verify total price
        self.assertEqual(lines[-2], "--------")
        self.assertEqual(lines[-1], f"Total Price: ${self.expected_total_price:.2f}")


    def test_yaml_receipt_strategy(self):
        """Test the YAML receipt strategy."""
        receipt_content = self.cart.generate_receipt(format_type='yaml')

        # Parse YAML content
        receipt = yaml.safe_load(receipt_content)

        # Verify total price
        self.assertEqual(receipt['total_price'], self.expected_total_price)

        # Verify items
        self.assertEqual(len(receipt['items']), len(self.expected_items))

        # Sort items for comparison
        receipt_items = sorted(receipt['items'], key=lambda x: x['uid'])
        expected_items = sorted(self.expected_items, key=lambda x: x['uid'])

        for expected_item, receipt_item in zip(expected_items, receipt_items):
            self.assertEqual(expected_item['uid'], receipt_item['uid'])
            self.assertEqual(expected_item['name'], receipt_item['name'])
            self.assertEqual(expected_item['unit_price'], receipt_item['unit_price'])


if __name__ == '__main__':
    unittest.main()
