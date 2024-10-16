from typing import Dict, List, Optional
import logging
from shopping_cart.models.item import Item
from shopping_cart.models.receipts.receipt_strategy_factory import get_receipt_strategy

logger = logging.getLogger(__name__)


class ShoppingCart:
    """A shopping cart that manages items and supports receipt generation."""

    def __init__(self):
        """Initialize an empty shopping cart."""
        self._items: Dict[str, Dict[str, any]] = {}
        self._total_price: float = 0.0
        self._total_quantity: int = 0

    def add_item(self, item: Item) -> None:
        """Add an item to the cart.

        Args:
            item: The Item instance to add.
            quantity: The quantity of the item to add.

        Raises:
            TypeError: If the item is not an Item instance.
        """
        if not isinstance(item, Item):
            raise TypeError("Only Item instances can be added to the cart.")

        item_name = item.name

        if item_name not in self._items:
            self._items[item_name] = {
                'instances': [],
                'total_quantity': 0,
                'total_price': 0.0
            }

        item_group = self._items[item_name]
        item_group['instances'].append(item)
        item_group['total_quantity'] += 1
        item_group['total_price'] += item.price

        self._total_price += item.price
        self._total_quantity += 1

        logger.debug(f"Added '{item_name}' (UID: {item.uid}) to cart.")

    def remove_item(self, item: Item) -> None:
        """Remove a specific item instance from the cart.

        Args:
            item: The Item instance to remove.

        Raises:
            KeyError: If the item is not found in the cart.
        """
        if not isinstance(item, Item):
            raise TypeError("Only Item instances can be added to the cart.")

        item_name = item.name
        if item_name not in self._items:
            raise KeyError(f"Item '{item_name}' not in the cart.")

        item_instances = self._items[item_name].get('instances', [])
        potential_item_instance = [x for x in item_instances if x.uid == item.uid]

        if not potential_item_instance:
            raise KeyError(f"Item '{item_name}' with UID '{item.uid}' not in the cart.")

        # Remove the specific item instance
        item_instances.remove(potential_item_instance[0])

        # Update total quantity and total price for the item name
        self._items[item_name]['total_quantity'] -= 1
        self._items[item_name]['total_price'] -= item.price

        # Update the cart's total price and total quantity
        self._total_price -= item.price
        self._total_quantity -= 1

        # If there are no more instances of this item, remove the item name from the cart
        if self._items[item_name]['total_quantity'] == 0:
            del self._items[item_name]
            logger.debug(f"All instances of '{item_name}' removed from cart.")
        else:
            logger.debug(f"Removed '{item_name}' (UID: {item.uid}) from cart.")


    def _update_totals_after_removal(self, item_group: Dict[str, any], removed_item: Item) -> None:
        """Update cart totals after removing an item."""
        item_group['total_quantity'] -= 1
        item_group['total_price'] -= removed_item.price
        self._total_price -= removed_item.price
        self._total_quantity -= 1

        # Remove the item name entry if no instances remain
        if item_group['total_quantity'] == 0:
            del self._items[removed_item.name]
            logger.debug(f"All instances of '{removed_item.name}' removed from cart.")

    def clear_cart(self) -> None:
        """Remove all items from the cart."""
        self._items.clear()
        self._total_price = 0.0
        self._total_quantity = 0
        logger.debug("Cleared all items from the cart.")

    def get_item(self, item_name: str, item_uid: str) -> Optional[Item]:
        """Retrieve an item from the cart by its name and UID.

        Args:
            item_name: The name of the item to retrieve.
            item_uid: The UID of the item to retrieve.

        Returns:
            The Item instance if found; otherwise, None.

        Raises:
            KeyError: If the item is not found in the cart.
        """
        if item_name not in self._items:
            raise KeyError(f"Item '{item_name}' not found in the cart.")

        for item in self._items[item_name]['instances']:
            if str(item.uid) == item_uid:
                return item

        raise KeyError(f"Item with UID '{item_uid}' not found under name '{item_name}'.")

    def list_items(self) -> Dict[str, Dict[str, any]]:
        """List all items in the cart with their details.

        Returns:
            A dictionary mapping item names to their item groups.
        """
        return self._items.copy()

    def list_items_by_name(self, item_name: str) -> List[Item]:
        """List all item instances in the cart that have the specified name.

        Args:
            item_name: The name of the items to list.

        Returns:
            A list of Item instances.

        Raises:
            KeyError: If the item name is not found in the cart.
        """
        if item_name not in self._items:
            raise KeyError(f"Item '{item_name}' not found in the cart.")
        return self._items[item_name]['instances'].copy()

    def get_total_quantity_by_name(self, item_name: str) -> int:
        """Get the total quantity of items with the specified name.

        Args:
            item_name: The name of the items.

        Returns:
            The total quantity as an integer.

        Raises:
            KeyError: If the item name is not found in the cart.
        """
        if item_name not in self._items:
            raise KeyError(f"Item '{item_name}' not found in the cart.")
        return self._items[item_name]['total_quantity']

    @property
    def total_price(self) -> float:
        """Get the total price of all items in the cart.

        Returns:
            The total price as a float rounded to two decimals.
        """
        return round(self._total_price, 2)

    @property
    def total_quantity(self) -> int:
        """Get the total quantity of all items in the cart.

        Returns:
            The total quantity as an integer.
        """
        return self._total_quantity

    def generate_receipt(self, format_type: str = 'text', file_path: Optional[str] = None) -> str:
        """Generate a receipt using the specified format.

        Args:
            format_type: The format type ('csv', 'text', 'json', 'yaml').
            file_path: Optional file path to save the receipt.

        Returns:
            The receipt content as a string.

        Raises:
            IOError: If the file cannot be written to the specified path.
        """
        strategy = get_receipt_strategy(format_type)
        receipt_content = strategy.generate({'items': self._items, 'total_price': self.total_price}, file_path)
        logger.debug(f"Receipt generated in {format_type} format.")
        return receipt_content