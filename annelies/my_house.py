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



import logging
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

# /setbuildarea ~0 -60 ~0 ~100 40 ~100


heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

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


wallThickness = 1
floorThickness = 1

sameValueGroupsPerRow = []


waterOrLavaAreas = []


# def buildRaft():
#       print('waterorLavaareas', waterOrLavaAreas)
#       plt.imshow(waterOrLavaAreas)
#       plt.show()
      
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
      #  place platform in case it is requird
      geo.placeRect(ED, Rect((left, top), (minHouseWidth + (wallThickness), minHouseDepth + (wallThickness))), smallArea['height'] - 1, Block("barrel"))
      blockHeightAtCornerTopLeft = heightsAfterMakeRoom[left - STARTX - 1][top - STARTZ - 1]
      blockHeightAtCornerBottomLeft = heightsAfterMakeRoom[left - STARTX - 1][bottom - STARTZ - 1]
      blockHeightAtCornerTopRight = heightsAfterMakeRoom[right - STARTX - 1][top - STARTZ - 1]
      blockHeightAtCornerBottomRight = heightsAfterMakeRoom[right - STARTX - 1][bottom - STARTZ - 1]


      geo.placeCuboid(ED, (left, smallArea['height'], top), (left, blockHeightAtCornerTopLeft, top), Block('barrel'))
      geo.placeCuboid(ED, (left, smallArea['height'], bottom), (left, blockHeightAtCornerBottomLeft, bottom), Block('barrel'))

      geo.placeCuboid(ED, (right, smallArea['height'], top), (right, blockHeightAtCornerTopRight, top), Block('barrel'))
      geo.placeCuboid(ED, (right, smallArea['height'], bottom), (right, blockHeightAtCornerBottomRight, bottom), Block('barrel'))

      makeHouse(smallArea['startX'] - extraWidthNeeded, smallArea['height'], smallArea['startZ'] - extraDepthNeeded, minHouseWidth, minHouseDepth, rotated=False)


def makeHouse(posX, posY, posZ, width, depth, rotated=False):
      print("Make house!")

      # search good spot that fits a house
      houseWidth = width
      roomHeight = minRoomHeight
      houseDepth = depth
      houseHeight = roomHeight * levels
      houseWallMaterial = ['pink_wool', 'magenta_terracotta'][randint(0,1)]


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
            floorType = ['smooth_quartz', 'pink_concrete'][randint(0,1)]
            geo.placeRect(ED, Rect((housePosition[0]+wallThickness,housePosition[2]+wallThickness),(houseWidth - wallThickness, houseDepth)), housePosition[1], Block(floorType))

            # place window left
            geo.placeCuboid(ED, (housePosition[0] + 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))

            # place window right
            geo.placeCuboid(ED, (housePosition[0] + houseWidth - 3, housePosition[1] + 2, housePosition[2]), (housePosition[0] + houseWidth - 3, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))

            # place big window center
            geo.placeCuboid(ED, (housePosition[0] + (houseWidth / 2) - 2, housePosition[1] + 2, housePosition[2]), (housePosition[0] + (houseWidth/2) + 2, housePosition[1] + 5, housePosition[2]), Block("glass_pane"))
            
            
      # place roof 
      geo.placeRect(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] - (wallThickness)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness + 2))), housePosition[1] + houseHeight + 1, Block("smooth_quartz"))
      geo.placeRectOutline(ED, Rect((housePosition[0] - (wallThickness),housePosition[2] - (wallThickness)),(houseWidth + (wallThickness + 2), houseDepth + (wallThickness + 2))), housePosition[1] + houseHeight, Block("smooth_quartz"))
      geo.placeRect(ED, Rect((housePosition[0] - (wallThickness) + 1,housePosition[2]),(houseWidth + (wallThickness), houseDepth + (wallThickness))), housePosition[1] + houseHeight + 2, Block("smooth_quartz_slab"))


      # make a side wall white
      level = 0
      roomDividerDepth = houseDepth
      roomDividerHeight = roomHeight - 1
      roomDividerPosY = posY + floorThickness + (level * roomHeight) - 1
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
      if(plantCornerLeft):
            for x in range(plantsAmount):
                  geo.placeCuboid(ED, (housePosition[0], housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth-balconyDepth + x), (housePosition[0], housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth-balconyDepth + x), Block(["potted_oak_sapling", "potted_pink_tulip", "potted_blue_orchid"][randint(0,2)]));
                  
      else:
            for x in range(plantsAmount):
                  geo.placeCuboid(ED, (housePosition[0] + balconyDepth - 1 - x, housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth), (housePosition[0] + balconyDepth - 1 - x, housePosition[1] + roomHeight + floorThickness, housePosition[2] + houseDepth), Block(["potted_oak_sapling", "potted_pink_tulip", "potted_blue_orchid"][randint(0,2)]));
                  


      # place stairs
      stairsWidth = roomHeight - 1
      stairsLeftToRight = True if randint(0,1) else False

      if(stairsLeftToRight):

      #  make stairs left to right
            stairsStartX = housePosition[0] + randint(wallThickness * 2, houseWidth - (stairsWidth + 1))

            for i in range(stairsWidth + 1):
                  if(i < stairsWidth):
                        geo.placeCuboid(ED, (stairsStartX + i, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + i, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "east"}) )
                        geo.placeCuboid(ED, (stairsStartX + i + 1, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + i + 1, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "west", "half": "top"}) )
            
                  if(i == stairsWidth):
                        # # place gap in ceiling
                        geo.placeCuboid(ED, (stairsStartX, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('air') )
                        geo.placeCuboid(ED, (stairsStartX + stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX + stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "east"}) )

             # room for bathroom left from the stairs
            roomOnTheLeft = stairsStartX - housePosition[0] - wallThickness
            if(roomOnTheLeft >= 6):
                  makeBathRoom(randint(housePosition[0] + wallThickness, (housePosition[0] + wallThickness) + roomOnTheLeft - 6), housePosition[1] + roomHeight, housePosition[2] + wallThickness, True)
            elif(roomOnTheLeft >= 3):
                  makeSmallBathRoom(housePosition[0] + wallThickness, housePosition[1] + roomHeight, housePosition[2] + wallThickness)
            else:
                  roomOnTheRight = (housePosition[0] + houseWidth) - (stairsStartX + stairsWidth) - wallThickness
                  if(roomOnTheRight >= 6):
                        makeBathRoom(randint((stairsStartX + stairsWidth + 2), (stairsStartX + stairsWidth + 2) + roomOnTheRight - 6), housePosition[1] + roomHeight, housePosition[2] + wallThickness, False)
                  elif(roomOnTheRight >= 3):
                        makeSmallBathRoom(randint(stairsStartX + stairsWidth + 1, stairsStartX + stairsWidth + 1 + roomOnTheRight - 3), housePosition[1] + roomHeight, housePosition[2] + wallThickness)
       
      # # if(stairsLeftToRight):
      else:
      # make stairs right to left
            stairsStartX = housePosition[0] + wallThickness + houseWidth - randint(wallThickness * 2, houseWidth - (stairsWidth + 1))

            for i in range(stairsWidth + 1):
                  if(i < stairsWidth):
                        geo.placeCuboid(ED, (stairsStartX - i, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - i, housePosition[1] + floorThickness + i, housePosition[2] + wallThickness +1), Block('purpur_stairs', {"facing": "west"}) )
                        geo.placeCuboid(ED, (stairsStartX - i - 1, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - i - 1, housePosition[1] + floorThickness + i, housePosition[2] + wallThickness +1), Block('purpur_stairs', {"facing": "east", "half": "top"}) )
            
                  if(i == stairsWidth):
                        # # place gap in ceiling
                        geo.placeCuboid(ED, (stairsStartX, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('air') )

                        geo.placeCuboid(ED, (stairsStartX - stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness), (stairsStartX - stairsWidth, housePosition[1] + floorThickness + i, housePosition[2]+wallThickness+1), Block('purpur_stairs', {"facing": "west"}) )

            # room for bathroom right from the stairs
            roomOnTheRight = (housePosition[0] + houseWidth) - stairsStartX - wallThickness
            if(roomOnTheRight >= 6):
                  makeBathRoom(randint(stairsStartX + 1, (stairsStartX + 1 + (roomOnTheRight - 6))), housePosition[1] + roomHeight, housePosition[2] + wallThickness, False)
            elif(roomOnTheRight >= 3):
                  makeSmallBathRoom(randint(stairsStartX + 1, stairsStartX + 1 + (roomOnTheRight - 3)), housePosition[1] + roomHeight, housePosition[2] + wallThickness)
            else:
                  roomOnTheLeft = (stairsStartX - stairsWidth) - housePosition[0] - wallThickness
                  if(roomOnTheLeft >= wallThickness + 6):
                        # "- 6" because the width of the big bathroom is 6, and "- 1" because you need 1 block of space between the bathroom wall and the stairs to walk.
                        makeBathRoom(randint(housePosition[0] + wallThickness, (housePosition[0] + wallThickness + roomOnTheLeft) - 6 - 1), housePosition[1] + roomHeight, housePosition[2] + wallThickness, True) 
                  elif(roomOnTheLeft >= wallThickness + 3):
                        makeSmallBathRoom(housePosition[0] + wallThickness, housePosition[1] + roomHeight, housePosition[2] + wallThickness)

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

      # place animal because Barbie likes pets
      geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2), housePosition[1] - 1, housePosition[2] + houseDepth - 2), (housePosition[0] + round(houseWidth/2), housePosition[1] - 1, housePosition[2] + houseDepth - 2), Block('minecraft:command_block', data='{Command:"/summon minecraft:panda ~ ~2 ~%s", auto:1}' %r' {MainGene:playful, Age:-6000}'))

      # place chairs
      twoChairs = randint(0,1)
      if(twoChairs == 1):      
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), (housePosition[0] + round(houseWidth/2) - 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), Block('crimson_stairs', {"facing": "west"}))
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) + 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), (housePosition[0] + round(houseWidth/2) + 2, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 1), Block('crimson_stairs', {"facing": "east"}))
      else: 
            geo.placeCuboid(ED, (housePosition[0] + round(houseWidth/2) - 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 2), (housePosition[0] + round(houseWidth/2) + 1, housePosition[1] + floorThickness, housePosition[2] + houseDepth - 2), Block('crimson_stairs', {"facing": "north"}))


      
      # make rug
      geo.placeRect(ED, Rect((housePosition[0] + houseWidth - wallThickness - 3, housePosition[2] + houseDepth - 4), (4,4)),housePosition[1] + roomHeight, Block("smooth_quartz"))

      # make bed
      bedName = ['pink_bed', 'magenta_bed'][randint(0,1)]
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
      lightsZ = housePosition[2] + houseDepth - wallThickness
      lightsY = housePosition[1] + roomHeight - floorThickness

      lanternActive = True if randint(0,1) else False
      if(cutWallOnBothSides):
            lightsEndX = lightsEndX + 1
      for x in range(0, lightsEndX - lightsStartX, 2):
            if(lanternActive):
                  geo.placeCuboid(ED, (lightsStartX + x, lightsY, lightsZ), (lightsStartX + x, lightsY, lightsZ), Block('lantern', {"hanging": True}))
            else:
                  geo.placeCuboid(ED, (lightsStartX + x, lightsY, lightsZ), (lightsStartX + x, lightsY, lightsZ), Block('beacon'))



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

def get_surface_size(a):
      return a['surfaceSize']

def get_width(a):
      return a['width']

def get_size(group):
      return len(group['coordinates'])

def has_coordinates(group):
      return len(group['coordinates']) > 0

def width_and_depth_is_bigger_than_minimum(group):
      if(group['width'] >= minHouseWidth and group['depth'] >= minHouseDepth):
            return True
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

      for ri, row in enumerate(heights):
            sameValueGroupCurrentIndex = 0

            for ci, col in enumerate(row):
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

            # Engage emergency function.
            # (To make some room for the house.)


            # Find the biggest area and fill the blocking areas with "air" blocks.
            # So cut out a part of the area. 
            # In the 'smallerAreas' list, filter out the spaces that are too close to the buildarea limit.
            smallerAreas = filter(fits_inside_buildarea, smallerAreas)
            smallerAreas = list(smallerAreas)
            
            if(len(smallerAreas) > 0):
                  makeRoom(smallerAreas[0])
            else:
                  print("There is no room at all in this build area. I will just make room for the house in the corner of the build area.")
                  if((LASTX - STARTX >= minHouseWidth) and (LASTZ - STARTZ >= minHouseDepth)): # check whether the house fits inside the build area
                        makeRoom({"height": heights[0][0], "startX": 0, "startZ": 0, "endX": minHouseWidth - 1, "endZ": minHouseDepth - 1, "width": minHouseWidth, "depth": minHouseDepth, "surfaceSize": minHouseWidth * minHouseDepth })
                  else:
                        print("It is impossible to build the house in such a small build area!")
                        print("The minHouseWidth =", minHouseWidth, "and the minHouseDepth =", minHouseDepth)
                        print("Whereas the build area is only", LASTX - STARTX, "by", LASTZ - STARTZ)


      else:
            biggestArea = bigAreas[0]

            print("BIGGEST AREA IS:", biggestArea)

            maxPossbileWidth = biggestArea['width'] if biggestArea['width'] < maxHouseWidth else maxHouseWidth
            maxPossbileDepth = biggestArea['depth'] if biggestArea['depth'] < maxHouseDepth else maxHouseDepth
            makeHouse(biggestArea['startX'], biggestArea['height'], biggestArea['startZ'], randint(minHouseWidth, maxPossbileWidth), randint(minHouseDepth, maxPossbileDepth))

            return 


    





calculateArea()
