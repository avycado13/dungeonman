# DungeonMan
Mechanics for basic text based RPG games.

I mainly built this for making the mechanics of the game and not the game so the gameplay might not be exceptional.

## Usage
Run the example game with [UV](https://github.com/astral-sh/uv):
```bash
uvx dungeonman
```
or use the fight systems in your own game
```python
   from dungeonman.map import Room, GameMap
   from dungeonman.character import Character
 ```

## Features
- Rooms that can connect to each other with corridors
- Items in Rooms
- Custom Fight system and logic
- Customizable weapons during fights
