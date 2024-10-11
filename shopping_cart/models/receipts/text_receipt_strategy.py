# text_receipt_strategy.py

from typing import Dict, Optional
from shopping_cart.models.receipts.base_receipt_strategy import BaseReceiptStrategy


class TextReceiptStrategy(BaseReceiptStrategy):
    """Receipt generation strategy for plain text format."""

    def generate(self, data: Dict[str, any], file_path: Optional[str] = None) -> str:
        """Generate a receipt in plain text format.

        Args:
            data: A dictionary containing 'items' and 'total_price'.
            file_path: Optional file path to save the receipt.

        Returns:
            The receipt content as a plain text string.

        Raises:
            IOError: If the file cannot be written to the specified path.
        """
        lines = []
        lines.append("Receipt:")
        lines.append("--------")

        for item_name, item_group in data['items'].items():
            for item in item_group['instances']:
                line = f"UID: {item.uid} | Name: {item.name} | Unit Price: ${item.price:.2f}"
                lines.append(line)

        lines.append("--------")
        lines.append(f"Total Price: ${data['total_price']:.2f}")

        receipt_content = '\n'.join(lines)

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(receipt_content)
            except IOError as e:
                raise IOError(f"Unable to write to file: {file_path}") from e

        return receipt_content
