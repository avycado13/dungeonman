"""Dungeon map and spatial positioning data models.

This module provides structures representing geographic layout areas within the game,
handling multidirectional node mapping, environment visibility, and item/enemy tracking.
"""

from dataclasses import dataclass, field

from dungeonman.character import Character
from dungeonman.item import Item

OPPOSITE_DIRECTION = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
    "up": "down",
    "down": "up",
}


@dataclass
class Room:
    """A distinct structural node representing an environmental coordinate space.

    Tracks absolute identity properties, directional exit mappings, present entities,
    lootable items, and user discovery visibility flags.

    Attributes:
        name (str): Unique descriptive moniker assigned to the specific chamber.
        description (str): Atmospheric flavor text displayed when entering the space.
        area (str): High-level region category classification or zone designation.
        exits (dict[str, Room]): Map associating directions to connecting instances.
        enemies (list[Character]): Collection of non-player combat agents in the chamber.
        items (list[Item]): Collection of dropped or harvestable loot items present.
        visited (bool): Identification flag marking whether a player has explored it.
    """

    name: str
    description: str
    area: str
    exits: dict[str, "Room"] = field(default_factory=dict)
    enemies: list[Character] = field(default_factory=list)
    items: list[Item] = field(default_factory=list)
    visited: bool = False

    def connect(self, direction: str, room: "Room", two_way: bool = True) -> None:
        """Establishes an adjacency link mapping out to another coordinate room.

        Args:
            direction (str): The initial heading path keyword string.
            room (Room): The targeted recipient destination node object.
            two_way (bool, optional): If set to True, registers a complementary backway
                using opposing tracking registers. Defaults to True.
        """
        self.exits[direction] = room
        if two_way:
            back = OPPOSITE_DIRECTION.get(direction)
            if back:
                room.exits[back] = self

    def has_living_enemies(self) -> bool:
        """Evaluates if any hostile agents residing in the space remain dangerous.

        Returns:
            bool: True if at least one enemy reports health above 0, otherwise False.
        """
        return any(e.is_alive() for e in self.enemies)

    def describe(self) -> str:
        """Constructs an integrated narrative breakdown detailing environmental status.

        Compiles contextual headers, room descriptions, available safe passages,
        dropped artifacts, and active adversarial identities.

        Returns:
            str: Multiline text interface printout for rendering directly to consoles.
        """
        lines = [f"== {self.area} :: {self.name} ==", self.description]
        if self.exits:
            lines.append("Exits: " + ", ".join(sorted(self.exits)))
        if self.items:
            lines.append("Items here: " + ", ".join(i.name for i in self.items))
        if self.has_living_enemies():
            names = ", ".join(e.name for e in self.enemies if e.is_alive())
            lines.append(f"Enemies here: {names}")
        return "\n".join(lines)


class GameMap:
    """Navigation system engine supervising spatial context and coordinate routing.

    Attributes:
        start (Room): The original entry terminal vector reference.
        current (Room): The current coordinate location space index tracked.
    """

    def __init__(self, start: Room):
        """Initializes a tracking grid context beginning at a designated location."""
        self.start = start
        self.current = start
        self.start.visited = True

    def move(self, direction: str) -> str:
        """Traverses the navigation pointer toward a specified directional exit path.

        Updates node visibility statuses and yields environmental feedback layout arrays.

        Args:
            direction (str): Target departure direction key vector to parse.

        Returns:
            str: Room description string if traversal succeeds, or an error response text.
        """
        room = self.current.exits.get(direction)
        if not room:
            return "You can't go that way."
        self.current = room
        self.current.visited = True
        return self.current.describe()

    def take_item(self, index: int) -> Item | None:
        """Extracts a target collection element from the floor arrays by tracking index.

        Args:
            index (int): Internal target layout offset referencing room elements array.

        Returns:
            Item, optional: The popped physical Item asset if index valid, or None.
        """
        if 0 <= index < len(self.current.items):
            return self.current.items.pop(index)
        return None
