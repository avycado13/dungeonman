from dungeonman.battle import Battle
from dungeonman.character import Character
from dungeonman.cli_battle import play_battle
from dungeonman.item import Potion
from dungeonman.map import GameMap, Room
from dungeonman.ui import prompt_command, show_room
from dungeonman.weapon import Weapon, WeaponQuality

DIRECTION_ALIASES = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west",
    "u": "up",
    "d": "down",
}


def build_world() -> GameMap:
    entrance = Room(
        name="Entrance Hall",
        description="A crumbling hall lit by torchlight. A cold draft blows from the north.",
        area="Old Crypt",
    )

    corridor = Room(
        name="Corridor",
        description="A narrow stone corridor slick with moss.",
        area="Old Crypt",
        items=[Potion("Health Potion", 30)],
    )

    armory = Room(
        name="Abandoned Armory",
        description="Rusted weapons hang from the walls. Most are useless.",
        area="Old Crypt",
        items=[
            Weapon("Iron Sword", 4, 10, WeaponQuality.GOOD, 15),
        ],
    )

    shrine = Room(
        name="Forgotten Shrine",
        description="Ancient statues surround a glowing altar.",
        area="Old Crypt",
        items=[
            Potion("Greater Health Potion", 60),
        ],
    )

    goblin_den = Room(
        name="Goblin Den",
        description="Bones litter the floor. Something is growling nearby.",
        area="Old Crypt",
        enemies=[
            Character(
                "Goblin",
                60,
                15,
                2,
                weapon=Weapon("Dagger", 1, 8, WeaponQuality.GREAT, 5),
            )
        ],
    )

    prison = Room(
        name="Forgotten Prison",
        description="Broken cells line the walls. Chains rattle in the darkness.",
        area="Old Crypt",
        enemies=[
            Character(
                "Skeleton",
                80,
                18,
                4,
                weapon=Weapon("Rusty Sword", 3, 10, WeaponQuality.COMMON, 10),
            )
        ],
    )

    treasury = Room(
        name="Hidden Treasury",
        description="Dust-covered chests lie forgotten for centuries.",
        area="Old Crypt",
        items=[
            Potion("Health Potion", 30),
            Weapon("Steel Axe", 6, 14, WeaponQuality.GREAT, 30),
        ],
    )

    crypt = Room(
        name="Ancient Crypt",
        description="An enormous stone sarcophagus dominates the chamber.",
        area="Old Crypt",
        enemies=[
            Character(
                "Crypt Guardian",
                180,
                30,
                8,
                weapon=Weapon(
                    "Ancient Greatsword", 10, 18, WeaponQuality.LEGENDARY, 100
                ),
            )
        ],
    )

    # Connections
    entrance.connect("north", corridor)

    corridor.connect("west", armory)
    corridor.connect("east", goblin_den)
    corridor.connect("north", shrine)

    goblin_den.connect("north", prison)
    prison.connect("east", treasury)

    shrine.connect("north", crypt)

    return GameMap(entrance)


def explore(game_map: GameMap, hero: Character):
    show_room(game_map.current.describe())
    while True:
        room = game_map.current

        if room.has_living_enemies():
            battle = Battle(players=[hero], enemies=room.enemies)
            play_battle(battle)
            if not hero.is_alive():
                return
            continue

        command = prompt_command()
        parts = command.split()
        if not parts:
            continue
        verb, *rest = parts

        direction = DIRECTION_ALIASES.get(verb, verb)
        if direction in {
            "north",
            "south",
            "east",
            "west",
            "up",
            "down",
        }:
            show_room(game_map.move(direction))
        elif verb in ("look", "l"):
            show_room(room.describe())
        elif verb == "take" and rest:
            item_name = " ".join(rest)
            for i, item in enumerate(room.items):
                if item.name.lower() == item_name:
                    taken = game_map.take_item(i)
                    if taken:
                        print(hero.pick_up(taken))
                    break
            else:
                print("There's nothing like that here.")
        elif verb in ("inventory", "i"):
            if hero.inventory:
                for item in hero.inventory:
                    print(f"  {item}")
            else:
                print("Your inventory is empty.")
        elif verb in ("quit", "exit"):
            return
        else:
            print(
                "Unknown command. Try: north/south/east/west, look, take <item>, inventory"
            )


def main() -> None:
    hero_weapon = Weapon("Iron Sword", 1, 15, WeaponQuality.GOOD, 20)
    hero = Character("Hero", 100, 20, 5, weapon=hero_weapon)
    hero.pick_up(Potion("Health Potion", 30))
    hero.pick_up(Potion("Health Potion", 30))

    game_map = build_world()
    explore(game_map, hero)
