"""DungeonMan game mechanics and terminal game."""

from dungeonman.battle import Battle, BattleLog
from dungeonman.character import Character
from dungeonman.item import Item, Potion
from dungeonman.map import GameMap, Room
from dungeonman.weapon import Weapon, WeaponQuality


def main() -> None:
    """Run the terminal game (also available as the dungeonman command)."""
    from dungeonman.main import main as run

    run()


__all__ = [
    "Battle",
    "BattleLog",
    "Character",
    "GameMap",
    "Item",
    "Potion",
    "Room",
    "Weapon",
    "WeaponQuality",
    "main",
]
