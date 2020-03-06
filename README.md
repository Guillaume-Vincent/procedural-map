# Python Procedural Map Generator

Procedural map generator coded in python. The map consists of an image with different colored pixels, representing different terrain types, created thanks to [Python Imaging Library](https://python-pillow.org/).

# Files

The repository currently contains a single .py file that contains the entirety of the project. It may be subject to change later.

# Map specifications

## Terrain Types

The map will contain pixels of different colors that will each represent a specific terrain type. The terrain types are the following:
- Map Border (black)
- Plain (light green)
- Forest (dark green)
- Desert (yellow)
- Mountain (gray)
- River (light blue)
- Lake (dark blue)
- Road (brown)
- Town (pink)

## Terrain Rules

|Terrain Type	|Constraints|
|---------------|----------|
|Map Border		|Delimits the outer borders of the map|
|Plain			||
|Forest			||
|Desert			|Cannot be adjacent to a river or a lake|
|Mountain		||
|River			|Must only flow from a mountain to a lake|
|Lake			|Cannot be adjacent to a desert|
|Road			|Must be continuous. Must connect two towns together, or a town with a border|
|Town			|Must be adjacent to a river or a lake|
