from dungeonman.battle import Battle
from dungeonman.character import Character
from dungeonman.weapon import Weapon, WeaponQuality
from dungeonman.item import Potion


def main() -> None:
    hero_weapon = Weapon("Iron Sword", 1, 15, WeaponQuality.GOOD, 20)
    goblin_weapon = Weapon("Dagger", 1, 8, WeaponQuality.GREAT, 5)
    hero = Character("Hero", 100, 20, 5, weapon=hero_weapon)
    hero.pick_up(Potion("Health Potion", 30))
    hero.pick_up(Potion("Health Potion", 30))
    goblin = Character("Goblin", 60, 15, 2, weapon=goblin_weapon)

    battle = Battle(
        players=[hero],
        enemies=[goblin],
    )

    battle.start()
