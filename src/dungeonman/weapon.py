import random
from enum import Enum

from dungeonman.item import Item


class WeaponQuality(Enum):
    RUSTY = 0.8
    COMMON = 0.95
    GOOD = 1.0
    GREAT = 1.1
    RARE = 1.4
    LEGENDARY = 1.75
    MYTHICAL = 2


class Weapon(Item):
    def __init__(
        self,
        name: str,
        level: int,
        base_attack: float,
        quality: WeaponQuality,
        durability: int,
    ):
        super().__init__(name)
        self.level = level
        self.base_attack = base_attack
        self.quality = quality
        self.durability = int(durability * quality.value)

    def __str__(self):
        q_name = self.quality.name.title()
        return f"{self.name} [{q_name}] ATK:{self.base_attack} Dur:{self.durability}"
