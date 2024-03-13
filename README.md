# Minecraft Barbie House Generator - GDPC Framework

## Assignment: Procedural Content Generation
* Generate a house on the minecraft map in a build area of 100x100.
* It should only be generated in realistic places. (Not on the water/lava, not in the air, not on top of a tree).
* You may not alter the area heavily (remove all blocks to make the house fit).
* The house should have a clear theme.
* The house should look a bit different every time.
* Clone the GDPC GitHub repository and use that framework to generate blocks in Minecraft.


## Result
I have used the GDPC framework to generate Barbie houses.

Things that are variable:
* Width of the house
* Depth of the house
* Direction of the stairs (left/right)
* X-position of the stairs
* Which side of the stairs the bathroom is on
* Size of the bathroom + small or big bath tub (Figure 10)
* Color of the building
* Color of the floor
* Color of the bed
* Nightstand or candles next to the bed
* Position of the chairs near the dining table
* Pink flower ”paintings” on the wall or not
* Size of the pink glass balcony
* Position of the flowers on the balcony + amount + type of flower
* Type of lanterns hanging from the ceiling
* Which side the white wall is on (left/right)
* Whether the living room wall is cut only on the left side, or both sides

![image_2024-03-07_09-55-46](https://github.com/Vaannelies/MGAIA-assignment-minecraft/assets/43701941/4304ff1e-6bc2-42cb-9843-49e8a46eadd6)
![image_2024-03-08_16-55-44](https://github.com/Vaannelies/MGAIA-assignment-minecraft/assets/43701941/33a41ba1-d446-4994-b714-49a3b702c36a)
![image_2024-03-09_22-07-24](https://github.com/Vaannelies/MGAIA-assignment-minecraft/assets/43701941/ccf2e340-ecf2-4487-82be-72299e63e97c)











# GDPC 6.0 (Transformative Update)

GDPC (Generative Design Python Client) is a Python framework for use in conjunction with the [GDMC-HTTP](https://github.com/Niels-NTG/gdmc_http_interface) mod for Minecraft Java edition.
It is designed for the [Generative Design in Minecraft Competition (GDMC)](https://gendesignmc.engineering.nyu.edu).

You need to be playing in a Minecraft world with the mod installed to use the framework.

The latest version of GDPC is compatible with GDMC-HTTP versions **>=1.0.0, <2.0.0**.


## Quick example

```python
from gdpc import Editor, Block, geometry

editor = Editor(buffering=True)

# Get a block
block = editor.getBlock((0,48,0))

# Place a block
editor.placeBlock((0,80,0), Block("stone"))

# Build a cube
geometry.placeCuboid(editor, (0,80,2), (2,82,4), Block("oak_planks"))
```

## What's the difference between GDMC, GDMC-HTTP and GDPC?

These abbreviations are all very similar, but stand for different things.

GDMC is short for the [Generative Design in Minecraft Competition](https://gendesignmc.engineering.nyu.edu), a yearly competition for generative AI systems in Minecraft.
The challenge is to write an algorithm that creates a settlement while adapting to the pre-existing terrain. The competition also has a [Discord server](https://discord.gg/YwpPCRQWND).

[GDMC-HTTP](https://github.com/Niels-NTG/gdmc_http_interface) is a Minecraft Forge mod that provides a HTTP interface to edit the world.
It allows you to modify the world live, while you're playing in it. This makes it possible to iterate quickly on generator algorithms.
The mod is an official submission method for the competition.

GDPC (notice the "P") is a Python framework for interacting with the GDMC-HTTP interface.
It provides many high-level tools that make working with the interface much simpler.


## Installation

GDPC is available on PyPI. To install the latest stable release, type one of the following commands:
- On Linux/MacOS: `python3 -m pip install gdpc`
- On Windows: `py -m pip install gdpc`

For the latest sexy-but-might-break-something prerelease, type the following instead:
- On Linux/MacOS: `python3 -m pip install --pre gdpc`
- On Windows: `py -m pip install --pre gdpc`

To update your package, type the following:
- On Linux/MacOS: `python3 -m pip install --upgrade gdpc`
- On Windows: `py -m pip install --upgrade gdpc`

If you would like to install the latest (pre)release version directly from GitHub, replace `gdpc` with\
`git+https://github.com/avdstaaij/gdpc`\
If instead you want to install the latest cutting-edge development version, replace `gdpc` with\
`git+https://github.com/avdstaaij/gdpc@dev`

For more information on installing from GitHub (such as getting old versions) see the [pip documentation](https://pip.pypa.io/en/stable/topics/vcs-support/).

If you are having trouble with dependencies, download `requirements.txt` and try running `python3 -m pip install -r requirements.txt` (or `py -m pip pip install -r requirements.txt` if you are using Windows). You **should not** use `requirements-dev.txt`!


## Tutorials and examples

There are various [**tutorial scripts**](examples/tutorials) that will help to get you started.

Some practical examples are also available, though they're slightly older and may not reflect the latest features:
- [**`visualize_map.py`**](examples/visualize_map.py): Displays a map of the Minecraft world using OpenCV.
- [**`emerald_city.py`**](examples/emerald_city.py): Demonstrates basic GDPC functionality by building a simple model of the Emerald City.


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information about how to contribute.
