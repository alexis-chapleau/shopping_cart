from typing import Dict
from .base_receipt_strategy import BaseReceiptStrategy
from shopping_cart.models.receipts.csv_receipt_strategy import CSVReceiptStrategy
from shopping_cart.models.receipts.text_receipt_strategy import TextReceiptStrategy
from shopping_cart.models.receipts.json_receipt_strategy import JSONReceiptStrategy
from shopping_cart.models.receipts.yaml_receipt_strategy import YAMLReceiptStrategy

def get_receipt_strategy(format_type: str) -> BaseReceiptStrategy:
    """Factory function to get the appropriate receipt strategy.

    Args:
        format_type: The desired format ('csv', 'text', 'json', 'yaml').

    Returns:
        An instance of a ReceiptStrategy.

    Raises:
        ValueError: If the format_type is not supported.
    """
    strategies: Dict[str, BaseReceiptStrategy] = {
        'csv': CSVReceiptStrategy,
        'text': TextReceiptStrategy,
        'json': JSONReceiptStrategy,
        'yaml': YAMLReceiptStrategy
    }
    strategy = strategies.get(format_type.lower())
    if strategy is None:
        raise ValueError(f"Unsupported format '{format_type}'. Supported formats are: {list(strategies.keys())}")
    return strategy()
