from perlin_noise import PerlinNoise
from config import *


class World():
    """
    World is responsible for generating a 2D heightmap using Perlin noise
    and converting that heightmap into terrain types (ocean, grass, mountain, etc.)
    """

    def __init__(self, size_x, size_y, random_seed):
        """
        Create a new world.

        size_x, size_y : number of tiles horizontally and vertically
        random_seed    : ensures reproducible worlds
        """

        # Generate a 2D noise map (this represents elevation)
        self.generate_noisemap(size_x, size_y, random_seed)

        # Flatten the 2D noise map into a 1D list so we can find
        # the absolute minimum and maximum elevation values.
        # These are used later to normalize heights.
        flat_list = [item for sublist in self.noise_map for item in sublist]
        self.min_value = min(flat_list)
        self.max_value = max(flat_list)

    def generate_noisemap(self, size_x, size_y, random_seed):
        """
        Generate a 2D Perlin noise heightmap.

        Each value in noise_map represents terrain elevation at that point.
        Higher values = higher terrain.
        """

        self.noise_map = []

        # Create multiple Perlin noise generators at different scales.
        # Lower octaves = large smooth features (continents)
        # Higher octaves = small sharp details (hills, bumps)
        noise1 = PerlinNoise(octaves=3, seed=random_seed)
        noise2 = PerlinNoise(octaves=6, seed=random_seed)
        noise3 = PerlinNoise(octaves=12, seed=random_seed)
        noise4 = PerlinNoise(octaves=24, seed=random_seed)

        # Number of points sampled in x and y direction.
        # +1 ensures edges line up cleanly.
        xpix, ypix = size_x + 1, size_y + 1
        # Loop over every position in the world grid
        for j in range(ypix):
            row = []
            for i in range(xpix):
                # Sample noise at normalized coordinates (0.0 → 1.0)
                # This makes noise independent of map size.
                nx = i / xpix
                ny = j / ypix
                # Combine multiple noise layers
                # Each higher octave contributes less to the final height.
                noise_val = noise1([nx, ny])
                noise_val += 0.5 * noise2([nx, ny])
                noise_val += 0.25 * noise3([nx, ny])
                noise_val += 0.125 * noise4([nx, ny])
                row.append(noise_val)
            self.noise_map.append(row)

    def get_noise_map(self):
        """
        Return the raw heightmap.
        Used for elevation-based rendering and 3D effects.
        """

        return self.noise_map

    def get_tiled_map(self, weights):
        """
        Convert the heightmap into discrete terrain types.

        weights : list defining how much vertical space each terrain occupies
                  (e.g., more ocean vs more mountains)
        """

        # Sum of all weights
        total_weights = sum(weights)

        # Total elevation range of the world
        total_range = self.max_value - self.min_value

        # This list will store the maximum height allowed for each terrain type.
        # Anything below that height belongs to that terrain.
        max_terrain_heights = []
        # Start from the lowest possible height
        previous_height = self.min_value
        # Build height thresholds for each terrain type
        for terrain_type in ALL_TERRAIN_TYPES:
            percentage_of_total_height = weights[terrain_type] / total_weights
            # How many units of elevation terrain occupies
            occupied_units = total_range * percentage_of_total_height
            # Where this terrain ends
            height = occupied_units + previous_height
            max_terrain_heights.append(height)
            previous_height = height
        # Force snow to always occupy the highest elevations
        max_terrain_heights[SNOW] = self.max_value

        map_int = []

        # Convert each elevation value into a terrain type
        for row in self.noise_map:
            map_row = []
            for value in row:
                # Find the first terrain whose max height
                # is greater than the elevation value
                for terrain_type in ALL_TERRAIN_TYPES:
                    if value <= max_terrain_heights[terrain_type]:
                        map_row.append(terrain_type)
                        break

            map_int.append(map_row)

            # map_int is a 2D grid of terrain IDs
        return map_int
