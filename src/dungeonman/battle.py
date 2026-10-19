"""Headless turn-based combat mechanics."""

import random

from dungeonman.character import Character
from dungeonman.item import Potion


class BattleLog:
    def __init__(self):
        self.log: list[str] = []

    def add_log(self, message: str):
        self.log.append(message)
        if len(self.log) > 20:
            self.log.pop(0)


class Battle:
    def __init__(self, players: list[Character], enemies: list[Character]):
        self.players = players
        self.enemies = enemies
        self.log = BattleLog()
        self.finished = False
        self.started = False

    def start(self) -> None:
        """Begin a battle; callers drive each turn with player_action/enemy_phase."""
        if self.started:
            raise RuntimeError("Battle has already started")
        self.started = True
        self.log.add_log("Battle Start!")

    def player_action(
        self,
        player: Character,
        action: str,
        target: Character | None = None,
        item_index: int | None = None,
    ) -> list[str]:
        """Apply one player's attack, defend, or potion action.

        The caller is responsible for choosing actions and tracking whose turn it is.
        """
        if not self.started or self.finished or not self.any_players_alive() or not self.any_enemies_alive():
            raise RuntimeError("Battle is not active")
        if player not in self.players or not player.is_alive():
            raise ValueError("Player is not an active combatant")
        if action == "attack":
            if target is None or target not in self.enemies or not target.is_alive():
                raise ValueError("Target must be a living enemy")
            messages = player.attack(target)
        elif action == "defend":
            messages = player.defend()
        elif action == "potion":
            if item_index is None or not 0 <= item_index < len(player.inventory):
                raise ValueError("Choose a valid potion index")
            if not isinstance(player.inventory[item_index], Potion):
                raise ValueError("Chosen item is not a potion")
            message = player.use_item(item_index)
            messages = [message] if message else []
        else:
            raise ValueError(f"Unknown action: {action}")
        for message in messages:
            self.log.add_log(message)
        return messages

    def enemy_phase(self) -> list[str]:
        """Let living enemies attack random living players."""
        if not self.started or self.finished:
            raise RuntimeError("Battle is not active")
        messages = []
        for enemy in self.enemies:
            if not enemy.is_alive():
                continue
            player = self.get_random_player()
            if player:
                messages.extend(enemy.attack(player))
        for message in messages:
            self.log.add_log(message)
        return messages

    def finish_round(self) -> None:
        """Clear defending status after the enemy phase."""
        for player in self.players:
            player.defending = False

    def end_battle(self) -> list[str]:
        """Finalize rewards once a side is defeated; return result messages."""
        if not self.started or self.any_players_alive() and self.any_enemies_alive():
            raise RuntimeError("Battle is not over")
        if self.finished:
            return []
        self.finished = True
        if not self.any_players_alive():
            messages = ["You have been defeated..."]
        else:
            messages = ["Enemies defeated!"]
            xp_reward = sum(enemy.level * 30 for enemy in self.enemies)
            for player in self.players:
                if not player.is_alive():
                    continue
                messages.extend(player.add_xp(xp_reward))
                for enemy in self.enemies:
                    if enemy.equipped_weapon:
                        messages.append(player.pick_up(enemy.equipped_weapon))
                        enemy.equipped_weapon = None
        for message in messages:
            self.log.add_log(message)
        return messages

    def get_random_enemy(self) -> Character | None:
        enemies = [e for e in self.enemies if e.is_alive()]
        return random.choice(enemies) if enemies else None

    def get_random_player(self) -> Character | None:
        players = [p for p in self.players if p.is_alive()]
        return random.choice(players) if players else None

    def any_players_alive(self) -> bool:
        return any(p.is_alive() for p in self.players)

    def any_enemies_alive(self) -> bool:
        return any(e.is_alive() for e in self.enemies)
