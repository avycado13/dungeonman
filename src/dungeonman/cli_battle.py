"""Terminal interface for a headless Battle."""

from dungeonman.battle import Battle
from dungeonman.character import Character
from dungeonman.item import Potion
from dungeonman.ui import menu, render
from dungeonman.weapon import Weapon


def play_battle(battle: Battle) -> None:
    battle.start()
    while battle.any_players_alive() and battle.any_enemies_alive():
        for player in battle.players:
            if not player.is_alive() or not battle.any_enemies_alive():
                continue
            player_turn(battle, player)
        if battle.any_enemies_alive():
            battle.enemy_phase()
        battle.finish_round()

    battle.end_battle()
    render(battle.players, battle.enemies, battle.log.log)
    if battle.any_players_alive():
        for player in battle.players:
            if player.is_alive():
                print(f"\n{player.name} wins!")
                print(f"Lv {player.level} ({player.xp}/{player.xp_to_next} XP)")
                if player.inventory:
                    print(f"Inventory: {', '.join(item.name for item in player.inventory)}")
    else:
        print("\nYou have been defeated...")
    input("\nPress Enter to exit...")


def player_turn(battle: Battle, player: Character) -> None:
    while True:
        render(battle.players, battle.enemies, battle.log.log)
        print(f"\n{player.name}'s turn:")
        potions = [i for i, item in enumerate(player.inventory) if isinstance(item, Potion)]
        options = ["Attack", "Defend"]
        if potions:
            options.append("Use Potion")
        options.append("Inventory")
        choice = options[menu(options) - 1]
        if choice == "Attack":
            target = battle.get_random_enemy()
            if target:
                battle.player_action(player, "attack", target=target)
            return
        if choice == "Defend":
            battle.player_action(player, "defend")
            return
        if choice == "Use Potion":
            battle.player_action(player, "potion", item_index=potions[0])
            return
        if inventory_menu(battle, player):
            return


def inventory_menu(battle: Battle, player: Character) -> bool:
    while True:
        render(battle.players, battle.enemies, battle.log.log)
        print(f"\n=== {player.name}'s Inventory ===")
        print(f"  Equipped: {player.equipped_weapon or '(none)'}\n")
        if not player.inventory:
            print("  (empty)")
        else:
            for i, item in enumerate(player.inventory):
                kind = "WPN" if isinstance(item, Weapon) else "POT" if isinstance(item, Potion) else ""
                print(f"  {i + 1}. [{kind}] {item}")
        print("\n  [item#] Equip/Use  [u] Unequip  [b] Back")
        cmd = input("> ").strip().lower()
        if cmd == "b":
            return False
        if cmd == "u":
            message = player.unequip()
        elif cmd.isdigit() and 0 <= int(cmd) - 1 < len(player.inventory):
            index = int(cmd) - 1
            item = player.inventory[index]
            if isinstance(item, Weapon):
                message = player.equip(index)
            elif isinstance(item, Potion):
                # Inventory use is a combat action, just like the potion shortcut.
                battle.player_action(player, "potion", item_index=index)
                return True
            else:
                message = "Can't use that."
        else:
            continue
        if message:
            battle.log.add_log(message)
