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

## Documentation

The docs for the library are hosted on [GitHub Pages](https://avycado13.github.io/dungeonman/)

Build the API reference from the project's Google-style docstrings:

```bash
uv sync --group dev
uv run sphinx-build -b html . _build/html
```

Open `_build/html/index.html` in a browser. Alternatively, run `uv run make html`.

## Features
- Rooms that can connect to each other with corridors
- Items in Rooms
- Custom Fight system and logic
- Customizable weapons during fights
