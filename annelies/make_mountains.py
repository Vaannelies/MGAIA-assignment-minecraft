#!/usr/bin/env python3


"""
NOTE: This file is an old example script. Although it is no longer
      comprehensive, and it does not use the most modern features or best
      practices of GDPC, it still contains a good amount of information while
      performing a practical task.

      New users are advised to look at the scripts in tutorials/ first, and
      then come back here for a slightly outdated, but practical application.

---

Generate an emerald city.

This file contains a collection of functions designed
to introduce new coders to the GDMC HTTP client in Python.

The source code of this module contains examples for:
- How to structure a file neatly (search 'STRUCTURE')
- Requesting the build area (search 'BUILDAREA')
- Introduction to world slices (search 'WORLDSLICE')
- Introduction to basic heightmaps (search 'HEIGHTMAP')
- Introduction to basic geometric shapes (search 'geo')

NOTE: We recommend creating your own files instead of modifying or adding code
      to these pre-existing files.

NOTE: If part of the program is running to fast for you to understand, insert
      >>> from time import sleep
      and
      >>> sleep(0.1)
      at the appropriate locations for a delay of 1/10 of a second
      Alternatively, inserting
      >>> input("Waiting for user to press [Enter]")
      will pause the program at that point.

NOTE: This file will only be updated in the case of breaking changes
      and will not showcase new features!

NOTE: Should you have any questions regarding this software, feel free to visit
      the #ℹ-framework-support channel on the GDMC Discord Server
      (Invite link: https://discord.gg/ueaxuXj)

This file is not meant to be imported.
"""


# === STRUCTURE #1
# These are the modules (libraries) we will use in this code
# We are giving these modules shorter, but distinct, names for convenience

import logging
from random import randint

from termcolor import colored

from gdpc import Block, Editor, Rect
from gdpc import geometry as geo
from gdpc import minecraft_tools as mt
from gdpc import editor_tools as et


import numpy as np
import matplotlib.pyplot as plt



# Here, we set up Python's logging system.
# GDPC sometimes logs some errors that it cannot otherwise handle.
logging.basicConfig(format=colored("%(name)s - %(levelname)s - %(message)s", color="yellow"))

# Here we construct an Editor object
ED = Editor(buffering=True)

# Here we read start and end coordinates of our build area
BUILD_AREA = ED.getBuildArea()  # BUILDAREA
STARTX, STARTY, STARTZ = BUILD_AREA.begin
LASTX, LASTY, LASTZ = BUILD_AREA.last

# WORLDSLICE
# Using the start and end coordinates we are generating a world slice
# It contains all manner of information, including heightmaps and biomes
# For further information on what information it contains, see
# https://minecraft.fandom.com/wiki/Chunk_format
#
# IMPORTANT: Keep in mind that a wold slice is a 'snapshot' of the world,
# and any changes you make later on will not be reflected in the world slice
WORLDSLICE = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this takes a while


# /setbuildarea ~0 0 ~0 ~64 200 ~64
# /setbuildarea 0 -60 0 100 40 100
# /setbuildarea 0 -60 0 10 -50 10


# print("heights: ", heights);
heights = WORLDSLICE.heightmaps["MOTION_BLOCKING"]




for i in range(10):
      geo.placeEllipsoid(ED, (randint(STARTX,LASTX), STARTY, randint(STARTZ,LASTZ)), (randint(10,30), randint(10,30), randint(10,30)), Block("dirt"), hollow = True)
    


