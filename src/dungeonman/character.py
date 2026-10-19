"""Character and Inventory
This Module has the Character class which defines the stats of the character for battles and manages the character's inventory.

Exported Classes:
    Character: class for Characters in Game
"""

from typing import Self
import random

from dungeonman.item import Item
from dungeonman.weapon import Weapon


class Character:
    """Stores Character Information and manages inventory and weapons of character"""

    def __init__(
        self,
        name: str,
        hp: float,
        attack_power: float,
        defense: float,
        weapon: Weapon | None = None,
    ):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.equipped_weapon = weapon
        self.inventory: list[Item] = []
        self.level = 1
        self.xp = 0
        self.xp_to_next = 50
        self.defending = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        if self.defending:
            damage = int(damage * 0.5)
            self.defending = False
        self.hp = max(0, self.hp - damage)

    def attack(self, target: Self):
        base = (
            self.equipped_weapon.base_attack * self.equipped_weapon.quality.value
            if self.equipped_weapon
            else self.attack_power
        )
        damage = base * random.uniform(0.8, 1.2)
        damage -= target.defense
        damage = max(1, round(damage))
        crit = random.random() < 0.10
        if crit:
            damage *= 2

        messages = []
        if crit:
            messages.append("Critical hit!")

        if self.equipped_weapon:
            self.equipped_weapon.durability -= 1
            if self.equipped_weapon.durability <= 0:
                messages.append(f"{self.name}'s {self.equipped_weapon.name} breaks!")
                self.equipped_weapon = None

        target.take_damage(damage)
        messages.append(f"{self.name} attacks {target.name} for {damage} damage!")
        return messages

    def defend(self):
        self.defending = True
        return [f"{self.name} braces for impact!"]

    def add_xp(self, amount: int):
        self.xp += amount
        messages = [f"{self.name} gains {amount} XP!"]
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            messages.append(self.level_up())
        return messages

    def level_up(self):
        self.level += 1
        self.xp_to_next = self.level * 50
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack_power += 2
        self.defense += 1
        return (
            f"{self.name} reaches level {self.level}! "
            f"HP:{self.max_hp} ATK:{self.attack_power} DEF:{self.defense}"
        )

    def pick_up(self, item: Item):
        self.inventory.append(item)
        return f"{self.name} picks up {item.name}!"

    def equip(self, index: int):
        item = self.inventory[index]
        if isinstance(item, Weapon):
            old = self.equipped_weapon
            self.equipped_weapon = item
            self.inventory.pop(index)
            if old:
                self.inventory.append(old)
            return f"{self.name} equips {item.name}!"
        return "Can't equip that!"

    def unequip(self):
        if self.equipped_weapon:
            self.inventory.append(self.equipped_weapon)
            name = self.equipped_weapon.name
            self.equipped_weapon = None
            return f"{self.name} unequips {name}!"
        return None

    def use_item(self, index: int):
        from dungeonman.item import Potion

        item = self.inventory[index]
        if isinstance(item, Potion):
            heal = min(item.heal_amount, self.max_hp - self.hp)
            self.hp += heal
            self.inventory.pop(index)
            return f"{self.name} uses {item.name}, healing for {heal} HP!"
        return None
