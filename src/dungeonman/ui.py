import os
from dungeonman.character import Character

WIDTH = 28


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def bar(current, maximum, length=10):
    if maximum == 0:
        return "░" * length
    filled = int((current / maximum) * length)
    return "█" * filled + "░" * (length - filled)


def show_character(character: Character):
    inner = WIDTH - 4
    print("╔" + "═" * (WIDTH - 2) + "╗")
    print(f"║ {character.name:<{inner}} ║")
    print(f"║ Lv {character.level:<{inner - 3}} ║")
    hp_bar = bar(character.hp, character.max_hp)
    hp_text = f"{int(character.hp)}/{int(character.max_hp)}"
    print(f"║ HP {hp_bar} {hp_text:<{inner - 14}} ║")
    xp_bar = bar(character.xp, character.xp_to_next)
    xp_text = f"{int(character.xp)}/{int(character.xp_to_next)}"
    print(f"║ XP {xp_bar} {xp_text:<{inner - 14}} ║")
    print("╚" + "═" * (WIDTH - 2) + "╝")


def render(players, enemies, log):
    clear_screen()
    for p in players:
        show_character(p)
    print()
    for e in enemies:
        show_character(e)
    print()
    print("─" * WIDTH)
    for msg in log[-8:]:
        print(msg)
    print("─" * WIDTH)


def menu(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        choice = input("> ").strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(options):
                return num
        print("Invalid choice. Try again.")
