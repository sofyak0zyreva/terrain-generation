TILESHEET_PATH = "combined.png"

WINDOW_WIDTH = 3840
WINDOW_HEIGHT = 2160
TILESIZE = 16       # tile width/height in pixels in tilesheet
WORLD_X = (WINDOW_WIDTH + TILESIZE - 1) // TILESIZE
WORLD_Y = (WINDOW_HEIGHT + TILESIZE - 1) // TILESIZE


# Terrain types
OCEAN3 = 0
OCEAN2 = 1
OCEAN1 = 2
COAST = 3
BEACH = 4
PALMS = 5
BEACH2 = 6
GRASS = 7
FOREST = 8
GRASS2 = 9
MOUNTAIN1 = 10
MOUNTAIN2 = 11
MOUNTAIN3 = 12
SNOW = 13


# List of all terrain type, ordered from lower height to higher height
ALL_TERRAIN_TYPES = [OCEAN3, OCEAN2, OCEAN1, COAST, BEACH, PALMS,
                     BEACH2, GRASS, FOREST, GRASS2, MOUNTAIN1, MOUNTAIN2, MOUNTAIN3, SNOW]


TERRAIN_TILES = [
    # Ocean depth level 3 tiles
    [
        (368, 176),  # all sides
    ],
    # Ocean depth level 2 tiles
    [
        (288, 176),  # all sides
    ],
    # Ocean depth level 1 tiles
    [
        (208, 176),  # all sides
    ],
   	# Coast level tiles
   	[
        (16, 688),  # all sides
    ],
    # Beach level tiles
    [
        (176, 16),  # all sides
    ],
   	# Palms level tiles
   	[
        (0, 496),  # all sides
    ],
   	# Beach level tiles
    [
        (176, 16),  # all sides
    ],
    # Grass level tiles
    [
        (32, 32),  # all sides
    ],
   	# Forest level tiles
	   [
        (272, 112),  # all sides
    ],
   	# Grass2 level tiles
    [
        (32, 32),  # all sides
    ],
    # Mountain1 level tiles
    [
        (320, 112),  # all sides
    ],
   	# Mountain2 level tiles
  	 [
        (80, 672),  # all sides
    ],
   	# Mountain3 level tiles
  	 [
        (96, 688),  # all sides
    ],
    # Snow level tiles
    [
        (400, 112),  # all sides
    ]
]


#OCEAN3, OCEAN2, OCEAN1, COAST, BEACH, PALMS, BEACH2, GRASS, FOREST, GRASS2, MOUNTAIN1, MOUNTAIN2, MOUNTAIN3, SNOW
WEIGHTS1 = [70, 20, 20, 12, 15, 4, 12, 20,
            35, 10, 20, 20, 10, 0]      # Islands
WEIGHTS2 = [35, 20, 20, 6, 5, 1, 10, 20, 35, 5, 30, 25, 20, 15]
WEIGHTS3 = [20, 15, 15, 5, 10, 5, 15, 45, 45, 10, 30, 25, 20, 30]     # Lakes
