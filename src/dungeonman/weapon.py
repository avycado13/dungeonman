"""Weapon and Weapon Quality data models.

This module provides structures representing weapons inside the game engine,
including handling their static stats, durability scale values, and item classifications.
"""

import random
from enum import Enum

from dungeonman.item import Item


class WeaponQuality(Enum):
    """Enumeration representing weapon quality multipliers.

    The value bound to each quality key acts as a scalar applied directly
    to baseline parameters (e.g., base attack thresholds and durability levels).
    """

    RUSTY = 0.8
    COMMON = 0.95
    GOOD = 1.0
    GREAT = 1.1
    RARE = 1.4
    LEGENDARY = 1.75
    MYTHICAL = 2


class Weapon(Item):
    """Data model representing a Weapon asset available for deployment in combat.

    Inherits base properties from the standard Item module and tracks
    structural levels, quality classifications, and operational condition states.

    Attributes:
        name (str): Inherited text identity given to the item asset.
        level (int): Minimum required tier rank or drop scaling factor.
        base_attack (float): Raw attack power factor provided by the asset frame.
        quality (WeaponQuality): The enum quality tier defining total modifier scaling.
        durability (int): Functional life value calculated from quality coefficients.
    """

    def __init__(
        self,
        name: str,
        level: int,
        base_attack: float,
        quality: WeaponQuality,
        durability: int,
    ):
        """Initializes a Weapon asset instance and scales starting durability values."""
        super().__init__(name)
        self.level = level
        self.base_attack = base_attack
        self.quality = quality
        self.durability = int(durability * quality.value)

    def __str__(self) -> str:
        """Generates a text description layout summarizing core weapon statistics.

        Returns:
            str: Normalized display readout highlighting name, quality, and stats.
        """
        q_name = self.quality.name.title()
        return f"{self.name} [{q_name}] ATK:{self.base_attack} Dur:{self.durability}"
