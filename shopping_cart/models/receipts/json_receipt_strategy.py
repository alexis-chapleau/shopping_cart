# json_receipt_strategy.py

import json
from typing import Dict, Optional
from shopping_cart.models.receipts.base_receipt_strategy import BaseReceiptStrategy


class JSONReceiptStrategy(BaseReceiptStrategy):
    """Receipt generation strategy for JSON format."""

    def generate(self, data: Dict[str, any], file_path: Optional[str] = None) -> str:
        """Generate a receipt in JSON format.

        Args:
            data: A dictionary containing 'items' and 'total_price'.
            file_path: Optional file path to save the receipt.

        Returns:
            The receipt content as a JSON-formatted string.

        Raises:
            IOError: If the file cannot be written to the specified path.
        """
        receipt = {
            'items': [],
            'total_price': data['total_price']
        }
        for item_name, item_group in data['items'].items():
            for item in item_group['instances']:
                receipt['items'].append({
                    'uid': str(item.uid),
                    'name': item.name,
                    'unit_price': item.price
                })
        receipt_content = json.dumps(receipt, indent=4)

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(receipt_content)
            except IOError as e:
                raise IOError(f"Unable to write to file: {file_path}") from e

        return receipt_content
