from dataclasses import dataclass, field
import uuid

@dataclass(frozen=True)
class Item:
    """Class representing an item/product."""
    name: str
    price: float
    uid: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("Item name nust be a string.")
        elif not self.name:
            raise ValueError("Item name must be a non-empty string.")
        if not isinstance(self.price, float):
            raise TypeError("Item price must be a float.")
        elif self.price < 0:
            raise ValueError("Price must be a non-negative float.")
