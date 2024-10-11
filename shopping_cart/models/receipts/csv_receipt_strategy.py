# csv_receipt_strategy.py

import csv
from typing import Dict, Optional
from shopping_cart.models.receipts.base_receipt_strategy import BaseReceiptStrategy
import os


class CSVReceiptStrategy(BaseReceiptStrategy):
    """Receipt generation strategy for CSV format."""

    def generate(self, data: Dict[str, any], file_path: Optional[str] = None) -> str:
        """Generate a receipt in CSV format.

        Args:
            data: A dictionary containing 'items' and 'total_price'.
            file_path: Optional file path to save the receipt.

        Returns:
            The receipt content as a CSV-formatted string.

        Raises:
            IOError: If the file cannot be written to the specified path.
        """
        output = []
        header = ['UID', 'Name', 'Unit Price']
        output.append(','.join(header))

        for item_name, item_group in data['items'].items():
            for item in item_group['instances']:
                row = [
                    str(item.uid),
                    item.name,
                    f"{item.price:.2f}"
                ]
                output.append(','.join(row))

        # Add total price
        output.append(f"Total Price,,{data['total_price']:.2f}")

        receipt_content = '\n'.join(output)

        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    file.write(receipt_content)
            except IOError as e:
                raise IOError(f"Unable to write to file: {file_path}") from e

        return receipt_content
