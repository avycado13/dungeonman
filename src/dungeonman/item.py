"""Base Item and Potion definitions.

This module provides the structural base class for all collectible assets
alongside specific implementations for consumable restorative elements.
"""


class Item:
    """The foundational parent class representing a generic inventory asset.

    Attributes:
        name (str): The descriptive text identity given to the item asset.
    """

    def __init__(self, name: str):
        """Initializes a generic inventory item."""
        self.name = name


class Potion(Item):
    """A consumable restorative item that replenishes character health.

    Inherits base identity traits from the Item class and incorporates
    quantifiable healing mechanics.

    Attributes:
        name (str): Inherited text identity given to the item asset.
        heal_amount (int): The absolute capacity of health points restored upon use.
    """

    def __init__(self, name: str, heal_amount: int):
        """Initializes a consumable Potion instance with specified recovery parameters."""
        super().__init__(name)
        self.heal_amount = heal_amount

    def __str__(self) -> str:
        """Generates a text description layout summarizing the potion's potency.

        Returns:
            str: Normalized display readout highlighting name and recovery threshold.
        """
        return f"{self.name} (Heals: {self.heal_amount} HP)"
