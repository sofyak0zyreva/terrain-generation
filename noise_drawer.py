from PIL import Image
from world import *
from config import *


def draw_noise_map(world, output="noise.png"):
    """
    Draw the raw Perlin noise as a grayscale image.
    Dark = low elevation
    Bright = high elevation
    """

    noise = world.get_noise_map()

    h = len(noise)
    w = len(noise[0])

    # Find min/max for normalization
    min_h = min(min(row) for row in noise)
    max_h = max(max(row) for row in noise)
    rng = max_h - min_h or 1.0

    img = Image.new("L", (w * TILESIZE, h * TILESIZE))
    pixels = img.load()

    for y in range(h):
        for x in range(w):
            # Normalize to 0–255
            value = int(
                255 * (noise[y][x] - min_h) / rng
            )

            # Fill an entire tile-sized block
            for ty in range(TILESIZE):
                for tx in range(TILESIZE):
                    px = x * TILESIZE + tx
                    py = y * TILESIZE + ty
                    pixels[px, py] = value

    img.save(output)


world = World(WORLD_X, WORLD_Y, random_seed=33)

draw_noise_map(world, output="noise1.png")

world = World(WORLD_X, WORLD_Y, random_seed=77)

draw_noise_map(world, output="noise2.png")

world = World(WORLD_X, WORLD_Y, random_seed=111)

draw_noise_map(world, output="noise3.png")
