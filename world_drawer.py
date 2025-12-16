from PIL import Image
from config import *
from world import *

# How much vertical displacement elevation creates.
# Larger values = steeper hills / more "3D" look
HEIGHT_SCALE = 32     # how tall hills are (16–48 is a good range)
TILE_INDEX = 0       # "all sides" tile
BACKGROUND = (40, 40, 60, 255)


def normalize(heightmap):
    """
    Normalize a 2D heightmap so all values are between 0.0 and 1.0.

    This makes elevation usable for rendering (height offsets, shading, etc.)
    regardless of the original Perlin noise range.
    """
    # Find minimum and maximum height values
    min_h = min(min(row) for row in heightmap)
    max_h = max(max(row) for row in heightmap)
    # Prevent division by zero if the map is flat
    rng = max_h - min_h or 1.0

    # Scale all heights into the range [0, 1]
    return [
        [(h - min_h) / rng for h in row]
        for row in heightmap
    ]


def draw_extruded_world(world, weights, output="world_3d.png"):
    """
    Render a 2.5D (extruded) terrain map from a World object.

    world   : World instance (provides noise + terrain data)
    weights : Terrain weight configuration (WEIGHTS1 / WEIGHTS2 / WEIGHTS3)
    output  : Output PNG file name
    """

    # Convert noise values into discrete terrain types
    map_int = world.get_tiled_map(weights)
    # Normalize noise into usable elevation values (0.0 → 1.0)
    elevation = normalize(world.get_noise_map())

    tilesheet = Image.open(TILESHEET_PATH).convert("RGBA")

    # Dimensions of the world in tiles
    h = len(map_int)
    w = len(map_int[0])

    img = Image.new(
        "RGBA",
        (w * TILESIZE, h * TILESIZE - 32),
        BACKGROUND
    )

    # Build a draw list to ensure correct depth ordering.
    # Tiles that are lower on the screen or higher in elevation
    # should be drawn later (on top).
    draw_list = []
    for y in range(h):
        for x in range(w):
            draw_list.append((
                y + elevation[y][x],  # depth key
                x, y
            ))

        # Sort tiles from farthest to closest
    draw_list.sort()

    # Draw each tile in depth-correct order
    for _, x, y in draw_list:
        terrain = map_int[y][x]
        height = elevation[y][x]
        # Convert tile coordinates to pixel coordinates
        screen_x = x * TILESIZE
        # Elevation shifts tiles upward to create the "uplifted" look
        screen_y = y * TILESIZE - int(height * HEIGHT_SCALE)

        # ---------- TERRAIN WITH OVERLAYS ----------
        # Forest tiles are drawn as an overlay on top of grass
        if terrain == FOREST:
            base_x, base_y = TERRAIN_TILES[GRASS][TILE_INDEX]

            # overlay tile (forest)
            forest_x, forest_y = TERRAIN_TILES[FOREST][TILE_INDEX]

            base_tile = tilesheet.crop((
                base_x, base_y,
                base_x + TILESIZE,
                base_y + TILESIZE
            ))

            overlay_tile = tilesheet.crop((
                forest_x, forest_y,
                forest_x + TILESIZE,
                forest_y + TILESIZE
            ))
            base_tile.paste(overlay_tile, (0, 0), overlay_tile)
            img.paste(base_tile, (screen_x, screen_y), base_tile)
        # Palm trees are drawn as an overlay on top of beach tiles
        elif terrain == PALMS:
            base_x, base_y = TERRAIN_TILES[BEACH][TILE_INDEX]

            # overlay tile (palms)
            palms_x, palms_y = TERRAIN_TILES[PALMS][TILE_INDEX]

            base_tile = tilesheet.crop((
                base_x, base_y,
                base_x + TILESIZE,
                base_y + TILESIZE
            ))

            overlay_tile = tilesheet.crop((
                palms_x, palms_y,
                palms_x + TILESIZE,
                palms_y + TILESIZE
            ))
            base_tile.paste(overlay_tile, (0, 0), overlay_tile)
            img.paste(base_tile, (screen_x, screen_y), base_tile)
        # ---------- BASE TERRAIN ONLY ----------
        else:
            # Regular terrain tile (ocean, beach, grass, mountain, snow)
            tile_x, tile_y = TERRAIN_TILES[terrain][TILE_INDEX]
            tile = tilesheet.crop((
                tile_x,
                tile_y,
                tile_x + TILESIZE,
                tile_y + TILESIZE
            ))
            img.paste(tile, (screen_x, screen_y), tile)

    img.save(output)


world = World(WORLD_X, WORLD_Y, random_seed=77)

draw_extruded_world(
    world,
    WEIGHTS2,
    output="worlds2.png"
)

world = World(WORLD_X, WORLD_Y, random_seed=33)

draw_extruded_world(
    world,
    WEIGHTS1,
    output="worlds1.png"
)

world = World(WORLD_X, WORLD_Y, random_seed=111)

draw_extruded_world(
    world,
    WEIGHTS3,
    output="worlds3.png"
)
