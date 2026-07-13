from dungeonman.ui import render, menu
from dungeonman.character import Character
from dungeonman.weapon import Weapon
from dungeonman.item import Potion


class BattleLog:
    def __init__(self):
        self.log: list[str] = []

    def add_log(self, message):
        self.log.append(message)
        if len(self.log) > 20:
            self.log.pop(0)


class Battle:
    def __init__(
        self,
        players: list[Character],
        enemies: list[Character],
    ):
        self.players = players
        self.enemies = enemies
        self.log = BattleLog()
        self.finished = False

    def start(self):
        self.log.add_log("Battle Start!")
        while self.any_players_alive() and self.any_enemies_alive():
            self.player_phase()
            self.enemy_phase()
            for p in self.players:
                p.defending = False
        self.end_battle()

    def player_phase(self):
        for player in self.players:
            if not player.is_alive():
                continue
            enemy = self.get_random_enemy()
            if not enemy:
                break
            while True:
                render(self.players, self.enemies, self.log.log)
                print(f"\n{player.name}'s turn:")
                has_potions = any(isinstance(i, Potion) for i in player.inventory)
                options = ["Attack", "Defend"]
                if has_potions:
                    options.append("Use Potion")
                options.append("Inventory")
                choice = menu(options)
                if choice == 1:
                    msgs = player.attack(enemy)
                    for m in msgs:
                        self.log.add_log(m)
                    break
                elif choice == 2:
                    msgs = player.defend()
                    for m in msgs:
                        self.log.add_log(m)
                    break
                elif has_potions and choice == 3:
                    for i, item in enumerate(player.inventory):
                        if isinstance(item, Potion):
                            msg = player.use_item(i)
                            if msg:
                                self.log.add_log(msg)
                            break
                else:
                    self.inventory_menu(player)

    def enemy_phase(self):
        for enemy in self.enemies:
            if not enemy.is_alive():
                continue
            player = self.get_random_player()
            if player:
                msgs = enemy.attack(player)
                for m in msgs:
                    self.log.add_log(m)

    def inventory_menu(self, player):
        while True:
            render(self.players, self.enemies, self.log.log)
            print(f"\n=== {player.name}'s Inventory ===")
            if player.equipped_weapon:
                print(f"  Equipped: {player.equipped_weapon}")
            else:
                print("  Equipped: (none)")
            print()
            if not player.inventory:
                print("  (empty)")
            else:
                for i, item in enumerate(player.inventory):
                    item_type = ""
                    if isinstance(item, Weapon):
                        item_type = "WPN"
                    elif isinstance(item, Potion):
                        item_type = "POT"
                    prefix = f"[{item_type}]" if item_type else ""
                    print(f"  {i + 1}. {prefix} {item}")
            print()
            print("  [item#] Equip/Use  [u] Unequip  [b] Back")
            cmd = input("> ").strip().lower()
            if cmd == "b":
                break
            elif cmd == "u":
                if player.equipped_weapon:
                    msg = player.unequip()
                    if msg:
                        self.log.add_log(msg)
            elif cmd.isdigit():
                idx = int(cmd) - 1
                if 0 <= idx < len(player.inventory):
                    item = player.inventory[idx]
                    if isinstance(item, Weapon):
                        msg = player.equip(idx)
                    elif isinstance(item, Potion):
                        msg = player.use_item(idx)
                    else:
                        msg = "Can't use that."
                    if msg:
                        self.log.add_log(msg)

    def end_battle(self):
        if self.any_players_alive():
            self.log.add_log("Enemies defeated!")
            xp_reward = sum(enemy.level * 30 for enemy in self.enemies)
            for player in self.players:
                msgs = player.add_xp(xp_reward)
                for m in msgs:
                    self.log.add_log(m)
                for enemy in self.enemies:
                    if enemy.equipped_weapon:
                        msg = player.pick_up(enemy.equipped_weapon)
                        self.log.add_log(msg)
                        enemy.equipped_weapon = None
            render(self.players, self.enemies, self.log.log)
            for player in self.players:
                print(f"\n{player.name} wins!")
                print(f"Lv {player.level} ({player.xp}/{player.xp_to_next} XP)")
                if player.inventory:
                    names = [item.name for item in player.inventory]
                    print(f"Inventory: {', '.join(names)}")
            input("\nPress Enter to exit...")
        else:
            render(self.players, self.enemies, self.log.log)
            print("\nYou have been defeated...")
            input("\nPress Enter to exit...")

    def get_random_enemy(self):
        import random
        enemies = [e for e in self.enemies if e.is_alive()]
        return random.choice(enemies) if enemies else None

    def get_random_player(self):
        import random
        players = [p for p in self.players if p.is_alive()]
        return random.choice(players) if players else None

    def any_players_alive(self):
        return any(p.is_alive() for p in self.players)

    def any_enemies_alive(self):
        return any(e.is_alive() for e in self.enemies)
