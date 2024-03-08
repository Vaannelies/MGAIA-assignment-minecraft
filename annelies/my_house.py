#!/usr/bin/env python3


# # Saving the heights to a file
# heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
# print("heights: ", heights);
# np.savez('depth.npz', heights)

# # Loading the file
# heightsLoaded = np.load('depth.npz')['arr_0']
# print(heightsLoaded)

# # Plotting the file oyeah
# plt.imshow(heightsLoaded)
# plt.show()





# RANDOM THINGS

# random: color (purple, pink or white)
# random: at which floor does the slide start
# random: amount of floors (2 - 4)
# random: house shape (L shape or rectangle, 50% chance)
# OR: the house is always an L shape, but the shape of the L depends.



# BRICKS TO USE

# pink_glazed_terracotta
# pink_concrete_powder
# pink_concrete
# pink_wool
# brain_coral_block

# crimson_flanks
# stripped_crimson_hyphae
# amethyst_block
# purpur_block
# chorus_flower
# purple_terracotta
# magenta_terracotta
# pink_terracotta
# magenta_concrete
# bubble_coral_block

# glass
# glass_pane

# sandstone
# cut_sandstone
# smooth_sandstone
# smooth_quartz

# honeycomb_block

# stripped_warped_hyphae


# STAIRS

# purpur_stairs
# quartz_stairs
# prismarine_brick_stairs


# LIGHTS

# pearlescent_froglight
# verdant_froglight
# ochre_froglight
# lantern
# soul_lantern
# shroomlight
# end_rod
# glowstone
# redstone_lamp
# sea_lantern



# DECORATION

# pink_candle
# magenta_candle
# white_candle
# orange_candle
# yellow_candle 

# end_rod
# pink_banner
# pink_tulip
# lilac
# spore_blossom
# sea_lantern
# cake
# flower_pot
# armor_stand (+ armor erop als kleding, misschien drakenhoofdje)
# end_crystal (As items, end crystals may be placed on bedrock and obsidian, if the two blocks above the bedrock or obsidian block are air or replaceable blocks and no other entities intersect the area.)
# nether_star (in glow_item_frame)
# glow_berries (in glow_item_frame)
# totem_of_undying (in glow_item_frame)
# lingering_potion (in glow_item_frame)
# bell
# sunflower

# horn_coral_fan
# bubble_coral_fan
# brain_coral_fan
# tube_coral_fan

# small_amethyst_bud
# medium_amethyst_bud
# large_amethyst_bud
# amethyst_cluster


# FURNITURE

# scaffolding
# pink_bed
# crimson_door
# warped_door
# birch_door

# loom
# lantern
# barrel
# composter




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
import time
from random import randint

from termcolor import colored

from gdpc import Block, Editor, Rect
from gdpc import geometry as geo
from gdpc import minecraft_tools as mt
from gdpc import editor_tools as et


import numpy as np
from numpy import *
import matplotlib.pyplot as plt



# Here, we set up Python's logging system.
# GDPC sometimes logs some errors that it cannot otherwise handle.
logging.basicConfig(format=colored("%(name)s - %(levelname)s - %(message)s", color="yellow"))


# === STRUCTURE #2
# These variables are global and can be read from anywhere in the code.
# NOTE: If you want to change a global value inside one of your functions,
#       you'll have to add a line of code. For an example, search 'GLOBAL'.

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

ROADHEIGHT = 0

# === STRUCTURE #3
# Here we are defining all of our functions to keep our code organised
# They are:
# - buildPerimeter()
# - buildRoads()
# - buildCity()
# /setbuildarea ~0 0 ~0 ~64 200 ~64
# /setbuildarea 0 -60 0 100 40 100
# /setbuildarea 0 -60 0 10 -50 10
# /setbuildarea ~0 -60 ~0 ~100 40 ~100


#     In this function we're building a simple wall around the build area
#         pillar-by-pillar, which means we can adjust to the terrain height
#     """
#     # HEIGHTMAP
#     # Heightmaps are an easy way to get the uppermost block at any coordinate
#     # There are four types available in a world slice:
#     # - 'WORLD_SURFACE': The top non-air blocks
#     # - 'MOTION_BLOCKING': The top blocks with a hitbox or fluid
#     # - 'MOTION_BLOCKING_NO_LEAVES': Like MOTION_BLOCKING but ignoring leaves
#     # - 'OCEAN_FLOOR': The top solid blocks
#     heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
# print("heights: ", heights);
heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

print(heights)
# show heights in plot:
# plt.imshow(heights, interpolation="none")
# plt.colorbar()
# plt.show()


minHouseWidth = 12
minHouseDepth = 7
minRoomHeight = 7

maxHouseWidth = 25
maxHouseDepth = 10
levels = 2

# geo.placeCuboid(ED, (STARTX, STARTY+120, STARTZ), (LASTX, STARTY+120, STARTZ), Block("sandstone"));
# geo.placeCuboid(ED, (STARTX, STARTY+120, STARTZ), (STARTX, STARTY+120, LASTZ), Block("sandstone"));



wallThickness = 1
floorThickness = 1

sameValueGroupsPerRow = []

# EXPLANATION OF "sameValueGroupsPerRow"
      # [
      #     this is for the first row (x = 0)
      #     [
      #           and then y = -60 for     z = 0, z = 1, z = 2 etc.
      #           {height: -60, coordinates: [0, 1, 2, 3, 4, 5, 6, 7]},
      # 
      #           and then y = -54 for     z = 8, z = 9, z = 10 etc.
      #           {height: -54, coordinates: [8, 9, 10, 11]},
      # 
      #           etc.
      #           {height: -60, coordinates: [12, 13, 14, 15, 16, 17, 18, 20, 21, 22]},
      # 
      #           {
      #           this goes on until the coordinates reach 100, the buildarea of z.
      #           }
      #     ],
      #     this is for the second row, so x = 1
      #     [
      #           and then y = -60 for     z = 0, z = 1, z = 2 etc.
      #           {height: -60, coordinates: [0, 1, 2, 3, 4, 5, 6, 7]},
      # 
      #           and then y = -54 for     z = 8, z = 9, z = 10 etc.
      #           {height: -54, coordinates: [8, 9, 10, 11]},
      # 
      #           etc.
      #           {height: -60, coordinates: [12, 13, 14, 15, 16, 17, 18, 20, 21, 22]},
      #     ],
      #     [
      #           ... this goes on a 100 times (as big as the buildarea x is)
      #     ]
      # ]

waterOrLavaAreas = []


# def buildRaft():
#       print('waterorLavaareas', waterOrLavaAreas)
#       plt.imshow(waterOrLavaAreas)
#       plt.show()

#       for index in enumerate(heights):
#             waterOrLavaAreas.append(list(np.full(LASTZ-STARTZ,  -1)))

#       for index in enumerate(heights):
#             sameValueGroupsPerRow.append([])

#       for ri, row in enumerate(heights):
#             sameValueGroupCurrentIndex = 0

#             for ci, col in enumerate(row):
#                   if(ci > 0):
#                         # check if block it not water or lava.
#                         block = WORLDSLICE.getBlock((ri, col-1, ci))
#                         print("block", block)
#                         if(col == row[ci - 1] and block.id not in ["minecraft:water", "minecraft:lava"]):
#                               sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)
#                         else:
#                               sameValueGroupCurrentIndex += 1
#                               sameValueGroupsPerRow[ri].append({"height":col, "coordinates": []})
#                               sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['type'] =  block.id
#                               if(block.id in ["minecraft:water", "minecraft:lava"]):
#                                     waterOrLavaAreas[ri][ci-1] = col
#                               else:
#                                     sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)
#                   else:
#                         sameValueGroupsPerRow[ri].append({"height":col, "coordinates": []})
#                         sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)


#       # Filter out the groups that have no coordinates.
#       for index, row in enumerate(sameValueGroupsPerRow):
#             sameValueGroupsPerRow[index] = list(filter(has_coordinates, row))


#       for index, row in enumerate(sameValueGroupsPerRow):
#             row.sort(key=get_size, reverse = True)
#             result = map(addSize, row)
#             sameValueGroupsPerRow[index] = list(result)

#       sameValueAreasInMatrix = []
#       sameValueAreasInMatrixCurrentIndex = 0

#       for index, row in enumerate(sameValueGroupsPerRow):
#             previousRow = sameValueGroupsPerRow[index - 1]
#             previousRow.sort(key=get_size, reverse = True)

#             row.sort(key=get_size, reverse = True)
#             if(row[0]['size'] < minHouseDepth):
#                   print('return')
#                   break
#             else:
#                   if(index > 0):
#                         if(row[0]['height'] == previousRow[0]['height'] and len(intersection(sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], row[0]['coordinates'])) > 0):
#                               sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'] = intersection(sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], row[0]['coordinates'])
#                               if(index == len(sameValueGroupsPerRow) - 1):
#                                     sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex] = {"height": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['height'], "coordinates": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], "startRow": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['startRow'], "endRow": index - 1}

#                         else:
#                               sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex] = {"height": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['height'], "coordinates": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], "startRow": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['startRow'], "endRow": index - 1}
#                               sameValueAreasInMatrixCurrentIndex += 1
#                               sameValueAreasInMatrix.append({'height': row[0]['height'], 'startRow': index, 'coordinates':  row[0]['coordinates'], "endRow": 0})
#                   else:
#                         sameValueAreasInMatrix.append({'height': row[0]['height'], 'startRow': index, 'coordinates': row[0]['coordinates'], "endRow": 0})

      

      
#       # map the sameValueAreasInMatrix array
#       bigAreas = map(mapsameValueAreasInMatrix, sameValueAreasInMatrix)
#       # filter out the width smaller than minallowedwidthsize
#       bigAreas = filter(width_is_bigger_than_minimum, bigAreas)

#       bigAreas = list(bigAreas)
#       bigAreas.sort(key=get_surface_size, reverse=True)


#       print("bigAreas (", len(bigAreas), "):", bigAreas)
#       # if(len(bigAreas) == 0):

def placeRotatedHouse(smallArea):
      print("smallArea:", smallArea)
      print("minhouseDepth: ", minHouseDepth)
      print("minhouseWidth: ", minHouseWidth)
      if(smallArea['width'] >= minHouseDepth and smallArea['depth'] >= minHouseWidth ):
            print("minhouseWidth: ", minHouseWidth)
            
            makeHouse(smallArea['startX'], smallArea['height'], smallArea['startZ'], smallArea['depth'], smallArea['width'], rotated=True)
            return True
            # biggestArea['startX'], biggestArea['height'], biggestArea['startZ'], randint(minHouseWidth, maxPossbileWidth), randint(minHouseDepth, maxPossbileDepth)
      else:
            return False
      
def makeRoom(smallArea):
      print("Make some room voor the house")
      extraWidthNeeded = minHouseWidth - smallArea['width']
      extraDepthNeeded = minHouseDepth - smallArea['depth']
      

      left = STARTX + smallArea['startX'] - extraWidthNeeded
      right = STARTX + smallArea['startX'] + smallArea['width']
      top = STARTZ + smallArea['startZ'] - extraDepthNeeded
      bottom = STARTZ + smallArea['startZ'] + smallArea['depth']

      geo.placeCuboid(ED, (left, smallArea['height'], top), (right, smallArea['height'] + minRoomHeight * levels + 6, bottom), Block('air'))
      worldSliceAfterMakeRoom = ED.loadWorldSlice(BUILD_AREA.toRect(), cache=True)  # this take
      heightsAfterMakeRoom = worldSliceAfterMakeRoom.heightmaps["OCEAN_FLOOR"]
      # show heights in plot:
      # plt.imshow(heightsAfterMakeRoom, interpolation="none")
      # plt.colorbar()
      # plt.show()

      #  place platform in case it is requird
      geo.placeRect(ED, Rect((left, top), (minHouseWidth + (wallThickness), minHouseDepth + (wallThickness))), smallArea['height'] - 1, Block("barrel"))
      print("left: ", left)
      print("right: ", right)
      print("top: ", top)
      print("bottom: ", bottom)
      print("")
      print("STARTX:", STARTX)
      print("left - startx", left - STARTX)
      print("top - startz", top - STARTZ)
      # print("left - startx", left - STARTX)
      # print("top - startz", top - STARTZ)
      print("extrawidthNeeded:", smallArea)
      blockHeightAtCornerTopLeft = heightsAfterMakeRoom[left - STARTX - 1][top - STARTZ - 1]
      blockHeightAtCornerBottomLeft = heightsAfterMakeRoom[left - STARTX - 1][bottom - STARTZ - 1]
      blockHeightAtCornerTopRight = heightsAfterMakeRoom[right - STARTX - 1][top - STARTZ - 1]
      blockHeightAtCornerBottomRight = heightsAfterMakeRoom[right - STARTX - 1][bottom - STARTZ - 1]

      print("height: ", blockHeightAtCornerTopLeft)
      print("height: ", blockHeightAtCornerBottomLeft)
      print("height: ", blockHeightAtCornerTopRight)
      print("height: ", blockHeightAtCornerBottomRight)

      geo.placeCuboid(ED, (left, smallArea['height'], top), (left, blockHeightAtCornerTopLeft, top), Block('barrel'))
      geo.placeCuboid(ED, (left, smallArea['height'], bottom), (left, blockHeightAtCornerBottomLeft, bottom), Block('barrel'))

      geo.placeCuboid(ED, (right, smallArea['height'], top), (right, blockHeightAtCornerTopRight, top), Block('barrel'))
      geo.placeCuboid(ED, (right, smallArea['height'], bottom), (right, blockHeightAtCornerBottomRight, bottom), Block('barrel'))
      

      makeHouse(smallArea['startX'] - extraWidthNeeded, smallArea['height'], smallArea['startZ'] - extraDepthNeeded, minHouseWidth, minHouseDepth, rotated=False)



def makeHouse(posX, posY, posZ, width, depth, rotated=False):
      print("Make house!")

      # search good spot that fits a house
      # houseWidth = 20
      # houseHeight = 5
      # houseDepth = 7
      houseWidth = width
      roomHeight = minRoomHeight
      houseDepth = depth
      houseHeight = roomHeight * levels
      houseWallMaterial = ['pink_wool', 'magenta_terracotta'][randint(-1,1)]


      # housePosition = (STARTX, STARTY, STARTZ)
      housePosition = (STARTX + posX, posY, STARTZ+posZ)

      for level in range(1,levels + 1):

            # place house
            geo.placeCuboidHollow(ED, housePosition, (housePosition[0] + houseWidth, housePosition[1] + (roomHeight * level), housePosition[2] + houseDepth), Block(houseWallMaterial));

            # cut out wall
            if(rotated):
                  geo.placeCuboid(ED, (housePosition[0] - wallThickness, housePosition[1] + floorThickness, housePosition[2] + wallThickness), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + (roomHeight * level) - floorThickness, housePosition[2] + houseDepth - wallThickness), Block("air"));
            else:
                  geo.placeCuboid(ED, (housePosition[0] + wallThickness, housePosition[1] + floorThickness, housePosition[2] + houseDepth), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + (roomHeight * level) - floorThickness, housePosition[2] + houseDepth), Block("air"));

            # place floor
            geo.placeRect(ED, Rect((housePosition[0]+wallThickness,housePosition[2]+wallThickness),(houseWidth - wallThickness, houseDepth)), housePosition[1], Block("sandstone"))

            # place window left
            geo.placeCuboid(ED, (housePosition[0] + 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))

            # place window right
            geo.placeCuboid(ED, (housePosition[0] + houseWidth - 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + houseWidth - 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))
            print("Make house!")

            # place big window center
            geo.placeCuboid(ED, (housePosition[0] + (houseWidth / 2) - 2, housePosition[1] + 2, housePosition[2]), (housePosition[0] + (houseWidth/2) + 2, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))
            
            
      # place roof 
      geo.placeRect(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] - (wallThickness)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness + 2))), housePosition[1] + houseHeight + 1, Block("smooth_quartz"))
      geo.placeRectOutline(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] - (wallThickness)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness + 2))), housePosition[1] + houseHeight, Block("smooth_quartz"))
      geo.placeRect(ED, Rect((housePosition[0] - (wallThickness) + 1,housePosition[2]),(houseWidth + (wallThickness), houseDepth + (wallThickness))), housePosition[1] + houseHeight + 2, Block("smooth_quartz_slab"))

      # geo.placeRect(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] + (wallThickness)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness - 2))), housePosition[1] + houseHeight + 3, Block("sandstone"))
      # geo.placeRect(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] + (wallThickness + 1)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness - 4))), housePosition[1] + houseHeight + 4, Block("sandstone"))
      # geo.placeRect(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] + (wallThickness + 2)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness - 6))), housePosition[1] + houseHeight + 5, Block("sandstone"))
      # geo.placeRect(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] + (wallThickness + 3)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness - 8))), housePosition[1] + houseHeight + 6, Block("sandstone"))

      # # make room divider
      # level = 0
      # roomDividerDepth = 4
      # roomDividerHeight = roomHeight - 1
      # roomDividerPosY = posY + floorThickness + (level * roomHeight) - 1
      # # roomDividerPosZ = randint(housePosition[2], housePosition[2] + houseDepth - 4)
      # roomDividerPosZ = housePosition[2] + wallThickness
      # roomDividerPosX = housePosition[0] + 3


      # geo.placeCuboid(ED, (roomDividerPosX, roomDividerPosY, roomDividerPosZ), (roomDividerPosX, roomDividerPosY+roomDividerHeight, roomDividerPosZ+roomDividerDepth), Block('quartz_stairs', {"facing": "south", "half": "top"}) )
            


      # make a side wall white
      level = 0
      roomDividerDepth = houseDepth
      roomDividerHeight = roomHeight - 1
      roomDividerPosY = posY + floorThickness + (level * roomHeight) - 1
      # roomDividerPosZ = randint(housePosition[2], housePosition[2] + houseDepth - 4)
      roomDividerPosZ = housePosition[2] + wallThickness
      # randomly choose left or right wall
      roomDividerPosX = housePosition[0] + (randint(0,1) * houseWidth)


      geo.placeCuboid(ED, (roomDividerPosX, roomDividerPosY, roomDividerPosZ), (roomDividerPosX, roomDividerPosY+roomDividerHeight, roomDividerPosZ+roomDividerDepth - wallThickness), Block('quartz_stairs', {"facing": "south", "half": "top"}) )
            


      # place white poles first floor
      cutWallOnBothSides = randint(0,1)
      if(cutWallOnBothSides == 1):
            geo.placeCuboid(ED, (housePosition[0],  housePosition[1] + floorThickness, housePosition[2] + houseDepth - 3), (housePosition[0] + houseWidth, housePosition[1] + roomHeight - floorThickness, housePosition[2] + houseDepth), Block("air"));
      else:
            geo.placeCuboid(ED, (housePosition[0],  housePosition[1] + floorThickness, housePosition[2] + houseDepth - 3), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + roomHeight - floorThickness, housePosition[2] + houseDepth), Block("air"));

      geo.placeCuboid(ED, (housePosition[0],  housePosition[1] + floorThickness, housePosition[2] + houseDepth), (housePosition[0], housePosition[1] + roomHeight - floorThickness, housePosition[2] + houseDepth), Block("end_rod"));
      geo.placeCuboid(ED, (housePosition[0] + round(houseWidth / 4),  housePosition[1] + floorThickness, housePosition[2] + houseDepth), (housePosition[0] + round(houseWidth / 4), housePosition[1] + houseHeight - floorThickness, housePosition[2] + houseDepth), Block("end_rod"));
      geo.placeCuboid(ED, (housePosition[0] + houseWidth - round(houseWidth / 4),  housePosition[1] + floorThickness, housePosition[2] + houseDepth), (housePosition[0] + houseWidth - round(houseWidth / 4), housePosition[1] + houseHeight - floorThickness, housePosition[2] + houseDepth), Block("end_rod"));
      geo.placeCuboid(ED, (housePosition[0] + houseWidth, housePosition[1] + floorThickness, housePosition[2] + houseDepth), (housePosition[0] + houseWidth, housePosition[1] + houseHeight - floorThickness, housePosition[2] + houseDepth), Block("end_rod"));


      # make balcony

      balconyDepth = randint(3, houseDepth - 1)
      geo.placeCuboid(ED, (housePosition[0], housePosition[1] + roomHeight, housePosition[2] + houseDepth-balconyDepth), (housePosition[0], housePosition[1] + houseHeight, housePosition[2] + houseDepth), Block("air"));
      geo.placeRect(ED, Rect((housePosition[0],housePosition[2]+houseDepth-balconyDepth),(balconyDepth, balconyDepth + 1)), housePosition[1] + roomHeight, Block("pink_stained_glass"))

      # plantCornerLeft =  True if randint(0,1) else False
      plantCornerLeft =  False 
      plantsAmount = randint(1,2)
      print("plants amount: ", plantsAmount)
      if(plantCornerLeft):
            for x in range(plantsAmount):
                  print('random:', randint(0,3))
                  geo.placeCuboid(ED, (housePosition[0], housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth-balconyDepth + x), (housePosition[0], housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth-balconyDepth + x), Block(["potted_oak_sapling", "potted_pink_tulip", "potted_blue_orchid"][randint(0,2)]));
                  
      else:
            for x in range(plantsAmount):
                  print('random:', randint(0,3))
                  geo.placeCuboid(ED, (housePosition[0] + balconyDepth - 1 - x, housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth), (housePosition[0] + balconyDepth - 1 - x, housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth), Block(["potted_oak_sapling", "potted_pink_tulip", "potted_blue_orchid"][randint(0,2)]));
                  


      # place stairs
      stairsWidth = roomHeight - 1
      # houseDepth = 1
      minSpaceFromWall = 1
      stairsLeftToRight = True if randint(0,1) else False

      if(stairsLeftToRight):

      #  make stairs left to right
            stairsStartX = housePosition[0] + randint(wallThickness * 2, houseWidth - (stairsWidth + 1))

            for i in range(stairsWidth + 1):
                  print("I:", i)
                  if(i < stairsWidth):
                        geo.placeCuboid(ED, (stairsStartX + i, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + i, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "east"}) )
                        geo.placeCuboid(ED, (stairsStartX + i + 1, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + i + 1, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "west", "half": "top"}) )
            
                  if(i == stairsWidth):
                        # # place gap in ceiling
                        geo.placeCuboid(ED, (stairsStartX, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('air') )

                        geo.placeCuboid(ED, (stairsStartX + stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "east"}) )

             # room for bathroom left from the stairs
            roomOnTheLeft = stairsStartX - housePosition[0]
            if(roomOnTheLeft >= 6):
                  makeBathRoom(randint(housePosition[0], (housePosition[0] + roomOnTheLeft) - 5), housePosition[1] + roomHeight, housePosition[2] + wallThickness, True)
            elif(roomOnTheLeft >= 4):
                  makeSmallBathRoom(housePosition[0] + wallThickness, housePosition[1] + roomHeight, housePosition[2] + wallThickness)
            else:
                  roomOnTheRight = (housePosition[0] + houseWidth) - (stairsStartX + stairsWidth)
                  if(roomOnTheRight >= 6):
                        makeBathRoom(randint(stairsStartX, (stairsStartX + roomOnTheRight) - 6), housePosition[1] + roomHeight, housePosition[2] + wallThickness, False)
                  elif(roomOnTheRight >= 4):
                        makeSmallBathRoom(stairsStartX, housePosition[1] + roomHeight, housePosition[2] + wallThickness)
       
      # # if(stairsLeftToRight):
      else:
      # make stairs right to left
            stairsStartX = housePosition[0] + wallThickness + houseWidth - randint(wallThickness * 2, houseWidth - (stairsWidth + 1))

            for i in range(stairsWidth + 1):
                  print("I:", i)
                  if(i < stairsWidth):
                        geo.placeCuboid(ED, (stairsStartX - i, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - i, housePosition[1] + floorThickness + i, housePosition[2] + wallThickness +1), Block('purpur_stairs', {"facing": "west"}) )
                        geo.placeCuboid(ED, (stairsStartX - i - 1, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - i - 1, housePosition[1] + floorThickness + i, housePosition[2] + wallThickness +1), Block('purpur_stairs', {"facing": "east", "half": "top"}) )
            
                  if(i == stairsWidth):
                        # # place gap in ceiling
                        geo.placeCuboid(ED, (stairsStartX, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('air') )

                        geo.placeCuboid(ED, (stairsStartX - stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "west"}) )

            # room for bathroom right from the stairs
            roomOnTheRight = (housePosition[0] + houseWidth) - stairsStartX 
            if(roomOnTheRight >= 6):
                  makeBathRoom(randint(stairsStartX, (stairsStartX + roomOnTheRight) - 6), housePosition[1] + roomHeight, housePosition[2] + wallThickness, False)
            elif(roomOnTheRight >= 4):
                  makeSmallBathRoom(stairsStartX, housePosition[1] + roomHeight, housePosition[2] + wallThickness)
            else:
                  roomOnTheLeft = (stairsStartX - stairsWidth) - housePosition[0]
                  if(roomOnTheLeft >= wallThickness + 6 + 1):
                        makeBathRoom(randint(housePosition[0], (housePosition[0] + roomOnTheLeft) - 5), housePosition[1] + roomHeight, housePosition[2] + wallThickness, True)
                  elif(roomOnTheLeft >= wallThickness + 3 + 1):
                        makeSmallBathRoom(housePosition[0]+1, housePosition[1] + roomHeight, housePosition[2] + wallThickness)

      # make either one or 2 flower paintings on the wall
      twoFlowerPaintings = randint(0,1)
      if(twoFlowerPaintings == 1):
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 2,  housePosition[1] + roomHeight + floorThickness + 4, housePosition[2]), (housePosition[0] + round(houseWidth/2) - 2, housePosition[1] + roomHeight + floorThickness + 4, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "south"}));
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 1,  housePosition[1] + roomHeight + floorThickness + 4, housePosition[2]), (housePosition[0] + round(houseWidth/2) - 1, housePosition[1] + roomHeight + floorThickness + 4, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "west"}));
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 2,  housePosition[1] + roomHeight + floorThickness + 3, housePosition[2]), (housePosition[0] + round(houseWidth/2) - 2, housePosition[1] + roomHeight + floorThickness + 3, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "west"}));
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 1,  housePosition[1] + roomHeight + floorThickness + 3, housePosition[2]), (housePosition[0] + round(houseWidth/2) - 1, housePosition[1] + roomHeight + floorThickness + 3, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "south"}));
           
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2),  housePosition[1] + roomHeight + floorThickness + 2, housePosition[2]), (housePosition[0] + round(houseWidth/2), housePosition[1] + roomHeight + floorThickness + 2, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "south"}));
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) + 1,  housePosition[1] + roomHeight + floorThickness + 2, housePosition[2]), (housePosition[0] + round(houseWidth/2) + 1, housePosition[1] + roomHeight + floorThickness + 2, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "west"}));
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2),  housePosition[1] + roomHeight + floorThickness + 1, housePosition[2]), (housePosition[0] + round(houseWidth/2), housePosition[1] + roomHeight + floorThickness + 1, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "west"}));
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) + 1,  housePosition[1] + roomHeight + floorThickness + 1, housePosition[2]), (housePosition[0] + round(houseWidth/2) + 1, housePosition[1] + roomHeight + floorThickness + 1, housePosition[2]), Block("pink_glazed_terracotta", {"facing": "south"}));
      else:
            geo.placeCuboid(ED, (housePosition[0],  housePosition[1] + floorThickness, housePosition[2] + houseDepth - 3), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + roomHeight - floorThickness, housePosition[2] + houseDepth), Block("air"));


      # place cake table
      geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 2), (housePosition[0] + round(houseWidth/2) + 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 2), Block('crimson_trapdoor', {"facing": "north", "open": "true", "half":"bottom"}))
      geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth), (housePosition[0] + round(houseWidth/2) + 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth), Block('crimson_trapdoor', {"facing": "south", "open": "true", "half":"bottom"}))
      geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), (housePosition[0] + round(houseWidth/2) + 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), Block('quartz_slab', {"type": "top"}))
      geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2), housePosition[1] + floorThickness + 1, housePosition[2] + houseDepth - 1), (housePosition[0] + round(houseWidth/2), housePosition[1] + floorThickness + 1, housePosition[2] + houseDepth - 1), Block('pink_candle_cake', {"lit": "true"}))

      twoChairs = randint(0,1)
      if(twoChairs == 1):      
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), (housePosition[0] + round(houseWidth/2) - 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), Block('crimson_stairs', {"facing": "west"}))
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) + 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), (housePosition[0] + round(houseWidth/2) + 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), Block('crimson_stairs', {"facing": "east"}))
      else: 
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 2), (housePosition[0] + round(houseWidth/2) + 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 2), Block('crimson_stairs', {"facing": "north"}))
                  

      # place some item frames on the walls
      # (If the walls don't exist, on that spot, the frames will just disappear so that's not a suuuper big issue.)
      # geo.placeCuboid(ED, (housePosition[0], housePosition[1] + floorThickness + 1, housePosition[2]), (housePosition[0], housePosition[1] + floorThickness + 1, housePosition[2]), Block('pink_concrete', {"facing_direction": "west"}))
      # geo.placeCuboid(ED, (housePosition[0]-1, housePosition[1], housePosition[2]), (housePosition[0]-1, housePosition[1], housePosition[2]), Block('pink_concrete', {"facing_direction": 5}))



      bedName = ['pink_bed', 'magenta_bed'][randint(-1,1)]
      
      # make rug
      geo.placeRect(ED, Rect((housePosition[0] + houseWidth - wallThickness - 3, housePosition[2] + houseDepth - 4), (4,4)),housePosition[1] + roomHeight, Block("smooth_quartz"))

      # make bed
      geo.placeCuboid(ED, (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 2), (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 2), Block(bedName, {"facing": "east"}))
      geo.placeCuboid(ED, (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 3), (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 3), Block(bedName, {"facing": "east"}))
      
      # make nightstand or candles
      nightstandActive = True if randint(0,1) else False
      if(nightstandActive):
            geo.placeCuboid(ED, (housePosition[0] + houseWidth - wallThickness, housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - wallThickness), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - wallThickness), Block('enchanting_table'))
      else: 
            geo.placeCuboid(ED, (housePosition[0] + houseWidth - wallThickness, housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - wallThickness), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - wallThickness), Block('candle', {"candles": 3, "lit": True}))
      

      
      # place lights
      # where there is no balcony, place the lights
      
      lightsStartX = housePosition[0] + balconyDepth + 1
      lightsEndX = housePosition[0] + houseWidth
      print("aaaa")
      print(lightsStartX)
      print(lightsEndX)
      lightsZ = housePosition[2] + houseDepth - wallThickness
      lightsY = housePosition[1] + roomHeight - floorThickness
      print(lightsZ)
      print(lightsY)
      print(lightsEndX - lightsStartX)

      lanternActive = True if randint(0,1) else False
      if(cutWallOnBothSides):
            lightsEndX = lightsEndX + 1
      for x in range(0, lightsEndX - lightsStartX, 2):
            print(x)
            if(lanternActive):
                  geo.placeCuboid(ED, (lightsStartX + x, lightsY, lightsZ), (lightsStartX + x, lightsY, lightsZ), Block('lantern', {"hanging": True}))
            else:
                  geo.placeCuboid(ED, (lightsStartX + x, lightsY, lightsZ), (lightsStartX + x, lightsY, lightsZ), Block('beacon'))


      # make bed + nightstand 
      # geo.placeCuboid(ED, (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 2), (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 2), Block('pink_bed', {"facing": "east"}))
      # geo.placeCuboid(ED, (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 3), (housePosition[0] + houseWidth - (wallThickness * 2), housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - 3), Block('pink_bed', {"facing": "east"}))
      # geo.placeCuboid(ED, (housePosition[0] + houseWidth - wallThickness, housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - wallThickness), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + floorThickness + roomHeight, housePosition[2] + houseDepth - wallThickness), Block('enchanting_table'))
      
      # make rug
                  
      # place flowers in pots
                  
      # place amethyst blocks
                  
      # place paintings


      print("Make house!")

      return

def makeBathRoom(posX, posY, posZ, left):
      geo.placeRect(ED, Rect((posX, posZ),(6, 2)), posY, Block("diamond_block"))
      if(left):
            geo.placeCuboid(ED, (posX + 5, posY, posZ), (posX + 5, posY + 2, posZ+1), Block("diamond_block"))
            # bath tub
            geo.placeCuboid(ED, (posX, posY+1, posZ+1), (posX, posY+1, posZ+1), Block("quartz_stairs", {"facing": "south", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX + 1, posY+1, posZ+1), (posX + 1, posY+1, posZ+1), Block("quartz_stairs", {"facing": "east", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX, posY+1, posZ), (posX, posY+1, posZ), Block("quartz_stairs", {"facing": "west", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX + 1, posY+1, posZ), (posX + 1, posY+1, posZ), Block("quartz_stairs", {"facing": "east", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX, posY+1, posZ-1), (posX, posY+1, posZ-1), Block("smooth_quartz"))
            geo.placeCuboid(ED, (posX + 1, posY+1, posZ-1), (posX + 1, posY+1, posZ-1), Block("smooth_quartz"))

            # toilet
            geo.placeCuboid(ED, (posX + 3, posY+1, posZ), (posX + 3, posY+1, posZ), Block("quartz_stairs", {"facing": "north"}))
      else:
            geo.placeCuboid(ED, (posX, posY, posZ), (posX, posY + 2, posZ+1), Block("diamond_block"))

            # bath tub
            geo.placeCuboid(ED, (posX + 4, posY+1, posZ+1), (posX + 4, posY+1, posZ+1), Block("quartz_stairs", {"facing": "south", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX + 5, posY+1, posZ+1), (posX + 5, posY+1, posZ+1), Block("quartz_stairs", {"facing": "east", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX + 4, posY+1, posZ), (posX + 4, posY+1, posZ), Block("quartz_stairs", {"facing": "west", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX + 5, posY+1, posZ), (posX + 5, posY+1, posZ), Block("quartz_stairs", {"facing": "east", "waterlogged": "true"}))
            geo.placeCuboid(ED, (posX + 4, posY+1, posZ-1), (posX + 4, posY+1, posZ-1), Block("smooth_quartz"))
            geo.placeCuboid(ED, (posX + 5, posY+1, posZ-1), (posX + 5, posY+1, posZ-1), Block("smooth_quartz"))

            # toilet
            geo.placeCuboid(ED, (posX + 2, posY+1, posZ), (posX + 2, posY+1, posZ), Block("quartz_stairs", {"facing": "north"}))

def makeSmallBathRoom(posX, posY, posZ):
      geo.placeRect(ED, Rect((posX, posZ),(3, 2)), posY, Block("diamond_block"))
      geo.placeCuboid(ED, (posX, posY+1, posZ), (posX, posY+1, posZ), Block("quartz_stairs", {"facing": "north"}))

      geo.placeCuboid(ED, (posX + 1, posY+1, posZ), (posX + 1, posY+1, posZ+1), Block("birch_trapdoor", {"facing": "west", "open": "true", "half": "bottom"}))
      geo.placeCuboid(ED, (posX + 2, posY+1, posZ), (posX + 2, posY+1, posZ), Block("quartz_stairs", {"facing": "east", "waterlogged": "true"}))
      geo.placeCuboid(ED, (posX + 2, posY+1, posZ+1), (posX + 2, posY+1, posZ+1), Block("quartz_stairs", {"facing": "south", "waterlogged": "true"}))


      # if(left):

      #       geo.placeCuboid(ED, (posX, posY, posZ), (posX, posY + 2, posZ+1), Block("diamond_block"))
      #       geo.placeCuboid(ED, (posX + 5, posY, posZ), (posX + 5, posY + 2, posZ+1), Block("diamond_block"))
      # else:
      #       geo.placeCuboid(ED, (posX, posY, posZ), (posX, posY + 2, posZ+1), Block("diamond_block"))
      #       geo.placeCuboid(ED, (posX, posY, posZ), (posX, posY + 2, posZ+1), Block("diamond_block"))

      #       geo.placeCuboid(ED, (posX + 4, posY, posZ+1), (posX + 4, posY + 2, posZ+1), Block("quartz_stairs"))
      #       geo.placeCuboid(ED, (posX + 5, posY, posZ+1), (posX + 5, posY + 2, posZ+1), Block("quartz_stairs"))
      #       geo.placeCuboid(ED, (posX + 4, posY, posZ), (posX + 4, posY + 2, posZ+1), Block("quartz_stairs"))
      #       geo.placeCuboid(ED, (posX + 5, posY, posZ), (posX + 5, posY + 2, posZ+1), Block("quartz_stairs"))
      #       geo.placeCuboid(ED, (posX + 4, posY, posZ-1), (posX + 4, posY + 2, posZ-1), Block("smooth_quartz"))
      #       geo.placeCuboid(ED, (posX + 5, posY, posZ-1), (posX + 5, posY + 2, posZ-1), Block("smooth_quartz"))


def get_surface_size(a):
      return a['surfaceSize']

def get_width(a):
      return a['width']

def get_size(group):
      # print("size:", len(group['coordinates']))
      return len(group['coordinates'])

def has_coordinates(group):
      return len(group['coordinates']) > 0

def width_and_depth_is_bigger_than_minimum(group):
      print("hello", group)
      if(group['width'] >= minHouseWidth and group['depth'] >= minHouseDepth):
            print("hello", True)
            return True
      print("hello", False)
      return False
      # return (group['width'] >= minHouseWidth)

def fits_inside_buildarea(area):
      extraWidthNeeded = minHouseWidth - area['width']
      extraDepthNeeded = minHouseDepth - area['depth']
     
      return True if (area['startX'] - extraWidthNeeded >= 0) and (area['startZ'] - extraDepthNeeded >= 0) else False

def minMaxValueGroups(group):
      groupSize = len(group['coordinates'])
      startZ = group['coordinates'][0]
      endZ = group['coordinates'][groupSize-1]
      return {
            "height": group['height'],
            "startZ": startZ,
            "endZ": endZ,
            "size":  (endZ - startZ) + 1
      }

def addSize(group):
      groupSize = len(group['coordinates'])
      startZ = group['coordinates'][0]
      endZ = group['coordinates'][groupSize-1]
      return {
            "height": group['height'],
            "coordinates": group['coordinates'],
            "size":  (endZ - startZ) + 1
      }

def intersection(list_a, list_b):
      return [ e for e in list_a if e in list_b ]

def mapSameValueAreasInMatrix(g):
      startX =  g['startRow']
      endX = g['endRow']
      if(len(g['coordinates']) > 0):
            startZ = g['coordinates'][0] 
      else:
            startZ = 0
      if(len(g['coordinates']) > 0):
            endZ = g['coordinates'][len(g['coordinates']) - 1] 
      else:
            endZ = 0
      width = endX - startX + 1
      depth = endZ - startZ + 1

      if(len(g['coordinates']) == 0):
            width = 0
            depth = 0
      

      return {
            'height': g['height'],
            'startX': startX,
            'startZ': startZ,
            'endX': endX,
            'endZ': endZ,
            'width': width,
            'depth': depth,
            'surfaceSize': width * depth
      }



def calculateArea(): 
      # reset waterOrLavaAreas
      waterOrLavaAreas.clear
      for index in enumerate(heights):
            waterOrLavaAreas.append(list(np.full(LASTZ-STARTZ,  -1)))

      for index in enumerate(heights):
            sameValueGroupsPerRow.append([])
      # print("0,0:", heights[0][0])
      # print("8,8:", heights[8][8])
      # print("0,8:", heights[0][8])
      # # print("99,99:", heights[99][99])
      # print("100,100:", heights[100][100])
      # # print("100,0:", heights[100][0])
      # # print("99,0:", heights[99][0])
      # # print("-2,-2:", heights[-2][-2])
      # # print("-1,-1:", heights[-1][-1])

      # geo.placeCuboid(ED, (STARTX, STARTY, STARTZ), (LASTX, -54, STARTZ), Block('red_concrete'))

      for ri, row in enumerate(heights):
            print("ri:", ri)

            sameValueGroupCurrentIndex = 0

            for ci, col in enumerate(row):
                  print("ci:", ci)
                  if(ci > 0):
                        # check if block it not water or lava.
                        block = WORLDSLICE.getBlock((ri, col-1, ci))
                        if(col == row[ci - 1] and block.id not in ["minecraft:water", "minecraft:lava"]):
                              sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)
                        else:
                              sameValueGroupCurrentIndex += 1
                              sameValueGroupsPerRow[ri].append({"height":col, "coordinates": []})
                              if(block.id in ["minecraft:water", "minecraft:lava"]):
                                    waterOrLavaAreas[ri][ci-1] = col
                              else:
                                    sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)
                  else:
                        sameValueGroupsPerRow[ri].append({"height":col, "coordinates": []})
                        sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)
                  
                  # print('sameValueGroupsPerRow[ri]', sameValueGroupsPerRow[ri])
                  # print('')
            print("ri:", ri)
      # Filter out the groups that have no coordinates.
      for index, row in enumerate(sameValueGroupsPerRow):
            sameValueGroupsPerRow[index] = list(filter(has_coordinates, row))


      for index, row in enumerate(sameValueGroupsPerRow):
            row.sort(key=get_size, reverse = True)
            result = map(addSize, row)
            sameValueGroupsPerRow[index] = list(result)

      sameValueAreasInMatrix = []
      sameValueAreasInMatrixCurrentIndex = 0

      for index, row in enumerate(sameValueGroupsPerRow):
            previousRow = sameValueGroupsPerRow[index - 1]
            previousRow.sort(key=get_size, reverse = True)

            row.sort(key=get_size, reverse = True)
            # We only compare the first group of each row.
            # The first group is always the biggest, since we sorted it. 
            if(index > 0):
                  if(row[0]['height'] == previousRow[0]['height'] and len(intersection(sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], row[0]['coordinates'])) >= minHouseDepth):
                        sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'] = intersection(sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], row[0]['coordinates'])
                        if(index == len(sameValueGroupsPerRow) - 1): 
                              sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex] = {
                                    "height": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['height'], 
                                    "coordinates": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], 
                                    "startRow": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['startRow'], 
                                    "endRow": index - 1
                              }

                  else:
                        sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex] = {
                              "height": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['height'], 
                              "coordinates": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['coordinates'], 
                              "startRow": sameValueAreasInMatrix[sameValueAreasInMatrixCurrentIndex]['startRow'], 
                              "endRow": index - 1
                        }
                        sameValueAreasInMatrixCurrentIndex += 1
                        sameValueAreasInMatrix.append({'height': row[0]['height'], 'startRow': index, 'coordinates':  row[0]['coordinates'], "endRow": 0})
            else:
                  sameValueAreasInMatrix.append({'height': row[0]['height'], 'startRow': index, 'coordinates': row[0]['coordinates'], "endRow": 0})

            
      
      
      # map the sameValueAreasInMatrix array
      bigAreas = map(mapSameValueAreasInMatrix, sameValueAreasInMatrix)
      bigAreas = list(bigAreas)
      smallerAreas = bigAreas[:]

      # sort, so the first item is the area with the biggest width
      smallerAreas.sort(key=get_width, reverse=True)


      # filter out the width smaller than minimum allowed size
      bigAreas = filter(width_and_depth_is_bigger_than_minimum, bigAreas)
      bigAreas = list(bigAreas)

      bigAreas.sort(key=get_surface_size, reverse=True)

      if(len(bigAreas) == 0):
            print("THERE ARE NO AREAS BIG ENOUGH! :(")

            # Engage emergency functions.
            # (To make some room for the house.)

            # 1.  Try rotating the house!
            #     we use the biggest area from the array of areas that were too small for the minimum house measures
            # done = placeRotatedHouse(smallerAreas[0])
            # I deactivated placeRotatedHouse because it still has bugs which have to be fixed.
            done = False;


            # 2.  Try the same functions again, but this time don't exclude the water.
            #     If the biggest area appears to be water/lava, build a raft to place a house on..
            # buildRaft()

            # 3.  If this is not the case, and the biggest area is not just water,
            #     the area is probably a forest or an area with many mountains.
            #     In that case, find the biggest area and fill the blocking areas with "air" blocks.
            #     So cut out a part of the area. 
            if(not(done)):
                  # In the 'smallerAreas' list, filter out the spaces that are too close to the buildarea limit.
                  smallerAreas = filter(fits_inside_buildarea, smallerAreas)
                  smallerAreas = list(smallerAreas)
                  
                  if(len(smallerAreas) > 0):
                        makeRoom(smallerAreas[0])
                  else:
                        print("There is no room at all. I will just make room for the house in the corner of the build area.")
                        if((LASTX - STARTX >= minHouseWidth) and (LASTZ - STARTZ >= minHouseDepth)): # check whether the house fits inside the build area
                              makeRoom({"height": heights[0][0], "startX": 0, "startZ": 0, "endX": minHouseWidth - 1, "endZ": minHouseDepth - 1, "width": minHouseWidth, "depth": minHouseDepth, "surfaceSize": minHouseWidth * minHouseDepth })
                        else:
                              print("It is impossible to build the house in such a small build area!")

            # After these emergency functions have been successfully executed,
            # try the original function again to find a good spot for the house.

            # If that works, build the house anyway.
            # If there is somehow still no place to build the house, give up... :(

            print(bigAreas)
      else:
            biggestArea = bigAreas[0]

            print("BIGGEST AREA IS:", biggestArea)

            maxPossbileWidth = biggestArea['width'] if biggestArea['width'] < maxHouseWidth else maxHouseWidth
            maxPossbileDepth = biggestArea['depth'] if biggestArea['depth'] < maxHouseDepth else maxHouseDepth
            makeHouse(biggestArea['startX'], biggestArea['height'], biggestArea['startZ'], randint(minHouseWidth, maxPossbileWidth), randint(minHouseDepth, maxPossbileDepth))

            return 


      # plt.imshow(bigAreas)
      # plt.show()
      # for s in enumerate(sameValueAreasInMatrix):
            # print(s)

      # print(sameValueAreasInMatrix)

# if a situation occurs where there are at least 10 (minHouseWidth) samevaluegroup coordinates starting with 3 ([3, 3] [3,4] [3,5]..) and  7 rows are the same but with different first coordinate ([4,3] [4,4] [4,5] and [5,3] [5,4] [5,5] and [6,3] [6,4] [6,5] etc. then build a house there. otherwise chop trees around biggest spot.)
# for x in range(0, 10 + 1):
#     # The northern wall
#     y = heights[(x - 0, 0)]
#     geo.placeCuboid(ED, (x, y - 2, STARTZ), (x, y, STARTZ), Block("granite"))
#     geo.placeCuboid(ED, (x, y + 1, STARTZ), (x, y + 4, STARTZ), Block("granite_wall"))
#     # The southern wall
#     y = heights[(x - 0, LASTZ - STARTZ)]
#     geo.placeCuboid(ED, (x, y - 2, LASTZ), (x, y, LASTZ), Block("red_sandstone"))
#     geo.placeCuboid(ED, (x, y + 1, LASTZ), (x, y + 4, LASTZ), Block("red_sandstone_wall"))

# print("Building north-south walls...")
# for x in range(STARTX, LASTX + 1):
#     for y in range(STARTY, LASTY + 1):
#         geo.placeCuboid(ED,)

# fill the entire buildarea
# geo.placeCuboid(ED, (STARTX, STARTY, STARTZ), (LASTX, LASTY, LASTZ), Block("sandstone"));
    
# fill the entire buildarea with air
# geo.placeCuboid(ED, (STARTX, STARTY, STARTZ), (LASTX, LASTY, LASTZ), Block("air"));
    



# search good spot that fits a house

# houseWidth = 10
# houseHeight = 5
# houseDepth = 7

# wallThickness = 1
# floorThickness = 1

# housePosition = (STARTX, STARTY, STARTZ)

# # # place house
# # geo.placeCuboidHollow(ED, housePosition, (housePosition[0] + houseWidth, housePosition[1] + houseHeight, housePosition[2] + houseDepth), Block("pink_concrete"));

# # # cut out wall
# # geo.placeCuboid(ED, (housePosition[0] + wallThickness, housePosition[1] + floorThickness, housePosition[2] + houseDepth - wallThickness), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + houseHeight - floorThickness, housePosition[2] + houseDepth), Block("air"));

# # # place floor
# # geo.placeRect(ED, Rect((housePosition[0]+wallThickness,housePosition[2]+wallThickness),(houseWidth - wallThickness, houseDepth)), housePosition[1], Block("sandstone"))

# # # place window left
# # geo.placeCuboid(ED, (housePosition[0] + 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))

# # # place window right
# # geo.placeCuboid(ED, (housePosition[0] + houseWidth - 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + houseWidth - 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))

# # # place big window center
# # geo.placeCuboid(ED, (housePosition[0] + (houseWidth / 2) - 2, housePosition[1] + 2, housePosition[2]), (housePosition[0] + (houseWidth/2) + 2, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))





# fig, ax = plt.subplots()
# min_val, max_val = STARTX, STARTZ

# intersection_matrix = np.random.randint(0, 10, size=(max_val, max_val))

# ax.matshow(intersection_matrix, cmap=plt.cm.Blues)

# for i in range(15):
#       for j in range(15):
#             c = intersection_matrix[j,i]
#             ax.text(i, j, str(c), va='center', ha='center')

# plt.matshow(intersection_matrix, cmap=plt.cm.Blues)

# ax.set_xlim(min_val, max_val)
# ax.set_ylim(min_val, max_val)
# ax.set_xticks(np.arange(max_val))
# ax.set_yticks(np.arange(max_val))
# ax.grid()












calculateArea()







# for x in range(0, 30 + 1):
#     # The northern wall
#     y = heights[(x - 0, 0)]
#     print(heights[(x - 0, 0)]);
#     geo.placeCuboid(ED, (x, y - 2, STARTZ), (x, y, STARTZ), Block("granite"))
#     geo.placeCuboid(ED, (x, y + 1, STARTZ), (x, y + 4, STARTZ), Block("granite_wall"))
# #     # The southern wall
# #     y = heights[(x - 0, LASTZ - STARTZ)]
# #     geo.placeCuboid(ED, (x, y - 2, LASTZ), (x, y, LASTZ), Block("red_sandstone"))
# #     geo.placeCuboid(ED, (x, y + 1, LASTZ), (x, y + 4, LASTZ), Block("red_sandstone_wall"))

# print("Building north-south walls...")


# def buildPerimeter():
#     """Build a wall along the build area border.

#     In this function we're building a simple wall around the build area
#         pillar-by-pillar, which means we can adjust to the terrain height
#     """
#     # HEIGHTMAP
#     # Heightmaps are an easy way to get the uppermost block at any coordinate
#     # There are four types available in a world slice:
#     # - 'WORLD_SURFACE': The top non-air blocks
#     # - 'MOTION_BLOCKING': The top blocks with a hitbox or fluid
#     # - 'MOTION_BLOCKING_NO_LEAVES': Like MOTION_BLOCKING but ignoring leaves
#     # - 'OCEAN_FLOOR': The top solid blocks
#     heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

#     print("Building east-west walls...")

#     for x in range(STARTX, LASTX + 1):
#         # The northern wall
#         y = heights[(x - STARTX, 0)]
#         geo.placeCuboid(ED, (x, y - 2, STARTZ), (x, y, STARTZ), Block("granite"))
#         geo.placeCuboid(ED, (x, y + 1, STARTZ), (x, y + 4, STARTZ), Block("granite_wall"))
#         # The southern wall
#         y = heights[(x - STARTX, LASTZ - STARTZ)]
#         geo.placeCuboid(ED, (x, y - 2, LASTZ), (x, y, LASTZ), Block("red_sandstone"))
#         geo.placeCuboid(ED, (x, y + 1, LASTZ), (x, y + 4, LASTZ), Block("red_sandstone_wall"))

#     print("Building north-south walls...")

#     for z in range(STARTZ, LASTZ + 1):
#         # The western wall
#         y = heights[(0, z - STARTZ)]
#         geo.placeCuboid(ED, (STARTX, y - 2, z), (STARTX, y, z), Block("sandstone"))
#         geo.placeCuboid(ED, (STARTX, y + 1, z), (STARTX, y + 4, z), Block("sandstone_wall"))
#         # The eastern wall
#         y = heights[(LASTX - STARTX, z - STARTZ)]
#         geo.placeCuboid(ED, (LASTX, y - 2, z), (LASTX, y, z), Block("prismarine"))
#         geo.placeCuboid(ED, (LASTX, y + 1, z), (LASTX, y + 4, z), Block("prismarine_wall"))


# def buildRoads():
#     """Build a road from north to south and east to west."""
#     xaxis = STARTX + (LASTX - STARTX) // 2  # Getting start + half the length
#     zaxis = STARTZ + (LASTZ - STARTZ) // 2
#     heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

#     print("Calculating road height...")
#     # Caclulating the average height along where we want to build our road
#     y = heights[(xaxis - STARTX, zaxis - STARTZ)]
#     for x in range(STARTX, LASTX + 1):
#         newy = heights[(x - STARTX, zaxis - STARTZ)]
#         y = (y + newy) // 2
#     for z in range(STARTZ, LASTZ + 1):
#         newy = heights[(xaxis - STARTX, z - STARTZ)]
#         y = (y + newy) // 2

#     # GLOBAL
#     # By calling 'global ROADHEIGHT' we allow writing to ROADHEIGHT.
#     # If 'global' is not called, a new, local variable is created.
#     global ROADHEIGHT
#     ROADHEIGHT = y

#     print("Building east-west road...")

#     geo.placeCuboid(ED, (xaxis - 2, y, STARTZ), (xaxis - 2, y, LASTZ), Block("end_stone_bricks"))
#     geo.placeCuboid(ED, (xaxis - 1, y, STARTZ), (xaxis + 1, y, LASTZ), Block("gold_block"))
#     geo.placeCuboid(ED, (xaxis + 2, y, STARTZ), (xaxis + 2, y, LASTZ), Block("end_stone_bricks"))
#     geo.placeCuboid(ED, (xaxis - 1, y + 1, STARTZ), (xaxis + 1, y + 3, LASTZ), Block("air"))

#     print("Building north-south road...")

#     geo.placeCuboid(ED, (STARTX, y, zaxis - 2), (LASTX, y, zaxis - 2), Block("end_stone_bricks"))
#     geo.placeCuboid(ED, (STARTX, y, zaxis - 1), (LASTX, y, zaxis + 1), Block("gold_block"))
#     geo.placeCuboid(ED, (STARTX, y, zaxis + 2), (LASTX, y, zaxis + 2), Block("end_stone_bricks"))
#     geo.placeCuboid(ED, (STARTX, y + 1, zaxis - 1), (LASTX, y + 3, zaxis + 1), Block("air"))


# def buildCity():
#     xaxis = STARTX + (LASTX - STARTX) // 2  # Getting center
#     zaxis = STARTZ + (LASTZ - STARTZ) // 2
#     y = ROADHEIGHT

#     print("Building city platform...")
#     # Building a platform and clearing a dome for the city to sit in
#     geo.placeCylinder(ED, (xaxis, y,      zaxis), 39, 1, Block("end_stone_bricks"))
#     geo.placeCylinder(ED, (xaxis, y,      zaxis), 37, 1, Block("gold_block"))
#     geo.placeCylinder(ED, (xaxis, y +  1, zaxis), 37, 3, Block("air"))
#     geo.placeCylinder(ED, (xaxis, y +  4, zaxis), 35, 2, Block("air"))
#     geo.placeCylinder(ED, (xaxis, y +  6, zaxis), 33, 1, Block("air"))
#     geo.placeCylinder(ED, (xaxis, y +  7, zaxis), 32, 1, Block("air"))
#     geo.placeCylinder(ED, (xaxis, y +  8, zaxis), 27, 1, Block("air"))
#     geo.placeCylinder(ED, (xaxis, y +  9, zaxis), 21, 1, Block("air"))
#     geo.placeCylinder(ED, (xaxis, y + 10, zaxis), 13, 1, Block("air"))
#     geo.placeCylinder(ED, (xaxis, y + 11, zaxis),  3, 1, Block("air"))

#     for _ in range(50):
#         buildTower(randint(xaxis - 20, xaxis + 20),
#                    randint(zaxis - 20, zaxis + 20))

#     # Place a book on a Lectern.
#     # See the wiki for book formatting codes.
#     ED.placeBlock((xaxis, y, zaxis), Block("emerald_block"))
#     bookData = mt.bookData("This book has a page!")
#     et.placeLectern(ED, (xaxis, y + 1, zaxis), bookData=bookData)


# def buildTower(x, z):
#     radius = 3
#     diameter = 2*radius + 1
#     y = ROADHEIGHT

#     print(f"Building tower at {x}, {z}...")
#     # If the blocks to the north, south, east and west aren't all gold
#     if not (
#             ED.getBlock((x - radius, y, z)).id == "minecraft:gold_block"
#         and ED.getBlock((x + radius, y, z)).id == "minecraft:gold_block"
#         and ED.getBlock((x, y, z - radius)).id == "minecraft:gold_block"
#         and ED.getBlock((x, y, z + radius)).id == "minecraft:gold_block"
#     ):
#         return  # Return without building anything

#     # Lay the foundation
#     geo.placeCylinder(ED, (x, y, z), diameter, 1, Block("emerald_block"))

#     # Build ground floor
#     geo.placeCylinder(ED, (x, y + 1, z), diameter, 3, Block("lime_concrete"), tube=True)

#     # Extend height
#     height = randint(5, 20)
#     geo.placeCylinder(ED, (x, y + 4, z), diameter, height, Block("lime_concrete"), tube=True)
#     height += 4

#     # Build roof
#     geo.placeCylinder(ED, (x, y + height, z), diameter, 1, Block("emerald_block"))
#     geo.placeCylinder(ED, (x, y + height + 1, z), diameter-2, 2, Block("emerald_block"))
#     geo.placeCuboid(ED, (x, y + height, z), (x, y + height + 2, z), Block("lime_stained_glass"))
#     ED.placeBlock((x, y + 1, z), Block("beacon"))

#     # Trim sides and add windows and doors
#     # NOTE: When placing doors, you only need to place the bottom block.
#     geo.placeCuboid(ED, (x + radius, y + 1, z), (x + radius, y + height + 2, z), Block("air"))
#     geo.placeCuboid(ED, (x + radius - 1, y + 1, z), (x + radius - 1, y + height + 2, z), Block("lime_stained_glass"))
#     ED.placeBlock((x + radius - 1, y + 1, z), Block("warped_door", {"facing": "west"}))

#     geo.placeCuboid(ED, (x - radius, y + 1, z), (x - radius, y + height + 2, z), Block("air"))
#     geo.placeCuboid(ED, (x - radius + 1, y + 1, z), (x - radius + 1, y + height + 2, z), Block("lime_stained_glass"))
#     ED.placeBlock((x - radius + 1, y + 1, z), Block("warped_door", {"facing": "east"}))

#     geo.placeCuboid(ED, (x, y + 1, z + radius), (x, y + height + 2, z + radius), Block("air"))
#     geo.placeCuboid(ED, (x, y + 1, z + radius - 1), (x, y + height + 2, z + radius - 1), Block("lime_stained_glass"))
#     ED.placeBlock((x, y + 1, z + radius - 1), Block("warped_door", {"facing": "north"}))

#     geo.placeCuboid(ED, (x, y + 1, z - radius), (x, y + height + 2, z - radius), Block("air"))
#     geo.placeCuboid(ED, (x, y + 1, z - radius + 1), (x, y + height + 2, z - radius + 1), Block("lime_stained_glass"))
#     ED.placeBlock((x, y + 1, z - radius + 1), Block("warped_door", {"facing": "south"}))


# def main():
#     try:
#         buildPerimeter()
#         buildRoads()
#         buildCity()

#         print("Done!")

#     except KeyboardInterrupt: # useful for aborting a run-away program
#         print("Pressed Ctrl-C to kill program.")


# # === STRUCTURE #4
# # The code in here will only run if we run the file directly (not imported).
# # This prevents people from accidentally running your generator.
# # It is recommended to directly call a function here, because any variables
# # you declare outside a function will be global.
# if __name__ == '__main__':
#     main()
