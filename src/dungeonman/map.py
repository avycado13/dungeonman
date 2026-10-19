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
    name: str
    description: str
    area: str
    exits: dict[str, "Room"] = field(default_factory=dict)
    enemies: list[Character] = field(default_factory=list)
    items: list[Item] = field(default_factory=list)
    visited: bool = False

    def connect(self, direction: str, room: "Room", two_way: bool = True):
        self.exits[direction] = room
        if two_way:
            back = OPPOSITE_DIRECTION.get(direction)
            if back:
                room.exits[back] = self

    def has_living_enemies(self) -> bool:
        return any(e.is_alive() for e in self.enemies)

    def describe(self) -> str:
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
    def __init__(self, start: Room):
        self.start = start
        self.current = start
        self.start.visited = True

    def move(self, direction: str) -> str:
        room = self.current.exits.get(direction)
        if not room:
            return "You can't go that way."
        self.current = room
        self.current.visited = True
        return self.current.describe()

    def take_item(self, index: int) -> Item | None:
        if 0 <= index < len(self.current.items):
            return self.current.items.pop(index)
        return None
