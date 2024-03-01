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
# amethyst block
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
heights = WORLDSLICE.heightmaps["MOTION_BLOCKING"]


# show heights in plot:
# plt.imshow(heights, interpolation="none")
# plt.colorbar()
# plt.show()


minHouseWidth = 10
minHouseDepth = 7
minHouseHeight = 5

maxHouseWidth = 25
maxHouseDepth = 10

sameValueGroupsPerRow = []





def makeHouse(posX, posY, posZ, width, depth):
      print("Make house!")

      # search good spot that fits a house
      # houseWidth = 20
      # houseHeight = 5
      # houseDepth = 7
      houseWidth = width
      houseHeight = 5
      houseDepth = depth

      wallThickness = 1
      floorThickness = 1

      # housePosition = (STARTX, STARTY, STARTZ)
      housePosition = (posX, posY, posZ)

      # place house
      geo.placeCuboidHollow(ED, housePosition, (housePosition[0] + houseWidth, housePosition[1] + houseHeight, housePosition[2] + houseDepth), Block("pink_concrete"));

      # cut out wall
      geo.placeCuboid(ED, (housePosition[0] + wallThickness, housePosition[1] + floorThickness, housePosition[2] + houseDepth - wallThickness), (housePosition[0] + houseWidth - wallThickness, housePosition[1] + houseHeight - floorThickness, housePosition[2] + houseDepth), Block("air"));

      # place floor
      geo.placeRect(ED, Rect((housePosition[0]+wallThickness,housePosition[2]+wallThickness),(houseWidth - wallThickness, houseDepth)), housePosition[1], Block("sandstone"))

      # place window left
      geo.placeCuboid(ED, (housePosition[0] + 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))

      # place window right
      geo.placeCuboid(ED, (housePosition[0] + houseWidth - 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + houseWidth - 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))
      print("Make house!")

      # place big window center
      geo.placeCuboid(ED, (housePosition[0] + (houseWidth / 2) - 2, housePosition[1] + 2, housePosition[2]), (housePosition[0] + (houseWidth/2) + 2, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))

      print("Make house!")

      return


def calculateArea(): 
      for index in enumerate(heights):
            sameValueGroupsPerRow.append([])

      # print(len(sameValueGroupsPerRow))
      for ri, row in enumerate(heights):
            sameValueGroupCurrentIndex = 0
            # sameValueGroupsPerRow[ri].append({"height": 0, "coordinates":[]})


            for ci, col in enumerate(row):
                  # print([ri, ci], ": ", col)
                  if(ci > 0):
                        # print("ci: ", ci)
                              
                        # check if block it not water or lava.
                        blockName = WORLDSLICE.getBlock((ri, col-1, ci)).id
                        # print("blockname:", blockName)
                        if(col == row[ci - 1] and blockName not in ["minecraft:water", "minecraft:lava"]):
                            
                              # sameValueGroupCurrentIndex 
                              # print("previous was the same value.")
                              sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)

                        else:
                              # print('hoi', sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]["coordinates"])
                              sameValueGroupCurrentIndex += 1

                              sameValueGroupsPerRow[ri].append({"height":col, "coordinates": []})
                              sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['type'] =  WORLDSLICE.getBlock((ri, col-1, ci))
                              # print('hoi2', sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex])
                              if(blockName not in ["minecraft:water", "minecraft:lava"]):
                                    sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)
                  else:
                        # print('CI == 0')
                        sameValueGroupsPerRow[ri].append({"height":col, "coordinates": []})
                        sameValueGroupsPerRow[ri][sameValueGroupCurrentIndex]['coordinates'].append(ci)

                        

            # print("sameValueGroupsPerRow: (", ri, ")", sameValueGroupsPerRow)
      # for sameValueGroup in sameValueGroupsPerRow:
      #       print(sameValueGroup)
      # print("sameValueGroupsPerRow: ", sameValueGroupsPerRow)
      # print("sameValueGroupsPerRow of row 1", sameValueGroupsPerRow[1])


      def get_size(group):
            # print('group', group)
            return len(group['coordinates'])
      
      def has_coordinates(group):
            # print('group', group)
            return len(group['coordinates']) > 0
      
      def has_more_coordinates_than_minimum(group):
            # print('group', group)
            return group['width'] > minHouseWidth

      def minMaxValueGroups(group):
            groupSize = len(group['coordinates'])
            # startX = group['coordinates'][0][0]
            startZ = group['coordinates'][0]
            # endX = group['coordinates'][groupSize][0]
            endZ = group['coordinates'][groupSize-1]
            return {
                  "height": group['height'],
                  # "startX": group['coordinates'][0][0],
                  "startZ": startZ,
                  # "endX": group['coordinates'][groupSize-1][0],
                  "endZ": endZ,
                  "size":  (endZ - startZ) + 1
            }

      def addSize(group):
            groupSize = len(group['coordinates'])
            # startX = group['coordinates'][0][0]
            startZ = group['coordinates'][0]
            # endX = group['coordinates'][groupSize][0]
            endZ = group['coordinates'][groupSize-1]
            return {
                  "height": group['height'],
                  "coordinates": group['coordinates'],
                  "size":  (endZ - startZ) + 1
            }

      def intersection(list_a, list_b):
            return [ e for e in list_a if e in list_b ]

      # map the row groups
      # for index, row in enumerate(sameValueGroupsPerRow):
      #       row.sort(key=get_size, reverse = True)
      #       result = map(minMaxValueGroups, row)
      #       sameValueGroupsPerRow[index] = list(result)
      

      # Filter out the groups that have no coordinates.
      for index, row in enumerate(sameValueGroupsPerRow):
            sameValueGroupsPerRow[index] = list(filter(has_coordinates, row))


      for index, row in enumerate(sameValueGroupsPerRow):
            row.sort(key=get_size, reverse = True)
            result = map(addSize, row)
            sameValueGroupsPerRow[index] = list(result)
      
      # print('firstsamevaluegroup:', sameValueGroupsPerRow[0])
            # if(currentSameValueGroup)
      
      # print(len(sameValueGroupsPerRow))

      # smallestAllowedAreaSize = np.minimum(minHouseWidth, minHouseDepth)
      # smallestAllowedDepthSize = minHouseDepth

      # smallestAllowedAreaSize2 = np.maximum(minHouseWidth, minHouseDepth)
      # smallestAllowedWidthSize = minHouseWidth

      sameValueGroupsPerColumn = []
      sameValueGroupsPerColumnCurrentIndex = 0
      # counter = 0;

      # for index in range(1000):
      #       sameValueGroupsPerColumn.append({})

      for index, row in enumerate(sameValueGroupsPerRow):
            # print(row)
            previousRow = sameValueGroupsPerRow[index - 1]
            # print("currentindex:", sameValueGroupsPerColumnCurrentIndex)
            print(row[0]['size'])
            if(row[0]['size'] < minHouseDepth):
                  print('return')
                  break
            else:
                  if(index > 0):
                        # if(row[0]['height'] == sameValueGroupsPerRow[index - 1][0]['height']):
                        #       print("jahoor")
                        #       print(index, index-1)
                        if(row[0]['height'] == previousRow[0]['height'] and len(intersection(sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'], row[0]['coordinates'])) > 0):
                              # print('height', row[0]['height'])
                              # print("jahoor")

                              # print(index, index-1)
                              # isInArray = np.isin(np.array(row[0]['coordinates']), np.array(previousRow[0]['coordinates']))
                              # print("is in array: ", isInArray)

                              # print("INTERSECTION:", intersection(row[0]['coordinates'], previousRow[0]['coordinates']))
                              # print("aaaa", sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex])
                              sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'] = intersection(sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'], row[0]['coordinates'])
                              print("aaaa", sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex])
                              # if(len(intersection(sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'], row[0]['coordinates'])) > 0):
                                    
                                    # print("yes")
                                    # print("index")
                                    # print(sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'])
                                    # print("")
                                    # print(row[0]['coordinates'])
                              # sameValueGroupsPerColumn[sameValueGroupCurrentIndex].append({'height': row[0]['height']})
                              if(index == len(sameValueGroupsPerRow) - 1):
                                    # print("hoi")
                                    # print("coordinates", sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'])
                                    sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex] = {"height": sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['height'], "coordinates": sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'], "startRow": sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['startRow'], "endRow": index - 1}

                        else:
                              sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex] = {"height": sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['height'], "coordinates": sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'], "startRow": sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['startRow'], "endRow": index - 1}
                              # print("increaes current index")
                              sameValueGroupsPerColumnCurrentIndex += 1
                              sameValueGroupsPerColumn.append({'height': row[0]['height'], 'startRow': index, 'coordinates':  row[0]['coordinates'], "endRow": 0})
                              # sameValueGroupsPerColumn[sameValueGroupsPerColumnCurrentIndex]['coordinates'] = row[0]['coordinates']
                  else:
                        sameValueGroupsPerColumn.append({'height': row[0]['height'], 'startRow': index, 'coordinates': row[0]['coordinates'], "endRow": 0})
                        # sameValueGroupsPerColumnCurrentIndex += 1


      # print("samevaluegroupspercolumn", sameValueGroupsPerColumn)

      def mapSameValueGroupsPerColumn(g):
            # print("G IS: ", g)
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
            # print("AAAAAA", g['coordinates'])
            

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
      
      def get_surface_size(a):
            # print("a", a)
            return a['surfaceSize']
      
      # map the sameValueGroupsPerColumn array
      # print("SameValueGroupsPerColumn:", sameValueGroupsPerColumn)
      bigAreas = map(mapSameValueGroupsPerColumn, sameValueGroupsPerColumn)

      # filter out the width smaller than minallowedwidthsize
      bigAreas = filter(has_more_coordinates_than_minimum, bigAreas)



      bigAreas = list(bigAreas)
      bigAreas.sort(key=get_surface_size, reverse=True)

      print("bigAreas (", len(bigAreas), "):", bigAreas)
      biggestArea = bigAreas[0]

      print("BIGGEST AREA IS:", biggestArea)

      # print(WORLDSLICE.getBlock((biggestArea['startX'], biggestArea['height']-1, biggestArea['startZ'])))

      maxPossbileWidth = biggestArea['width'] if biggestArea['width'] < maxHouseWidth else maxHouseWidth
      maxPossbileDepth = biggestArea['depth'] if biggestArea['depth'] < maxHouseDepth else maxHouseDepth
      makeHouse(biggestArea['startX'], biggestArea['height'], biggestArea['startZ'], randint(minHouseWidth, maxPossbileWidth), randint(minHouseDepth, maxPossbileDepth))

      return 


      # plt.imshow(bigAreas)
      # plt.show()
      # for s in enumerate(sameValueGroupsPerColumn):
            # print(s)

      # print(sameValueGroupsPerColumn)

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
