from abc import ABC, abstractmethod
from typing import Dict, Optional
import uuid

class BaseReceiptStrategy(ABC):
    """Abstract base class for receipt generation strategies."""

    @abstractmethod
    def generate(self, data: Dict[str, any], file_path: Optional[str] = None) -> str:
        """Generate the receipt.

        Args:
            cart_items: A dictionary of cart items and their details.
            file_path: Optional file path to save the receipt.

        Returns:
            The receipt content as a string.

        Raises:
            IOError: If the file cannot be written to the specified path.
        """
        pass
