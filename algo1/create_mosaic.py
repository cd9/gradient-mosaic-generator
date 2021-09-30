from glob import glob
from PIL import Image
from math import floor, sqrt
from scipy import spatial
import random
import numpy

# Grab all tiles
tile_paths = [x for x in glob("../tiles/*")]
tiles = [Image.open(x) for x in tile_paths]

# Calculate mosaic size
single_tile_width = tiles[0].size[0]
mosaic_width_in_tiles = floor(sqrt(len(tiles)))
mosaic_width_in_pixels = mosaic_width_in_tiles*single_tile_width

# Helper to make 2D grid
def get_empty_grid():
  return [[None] * mosaic_width_in_tiles
          for j in range(mosaic_width_in_tiles)]

# Create empty grid
tile_grid = get_empty_grid()

# Store average colors
average_color_list = [numpy.array(x).mean(axis=0).mean(axis=0) for x in tiles]
average_color_grid = get_empty_grid()

# Save used tiles
used_tiles = set()

# Helper to determine difference in RGB
def get_rgb_difference(k, x, y):
  if not all([z >= 0 and z < mosaic_width_in_tiles for z in [x, y]]):
    return 0
  return sum([abs(average_color_list[k][i]-average_color_grid[x][y][i]) for i in [0, 1, 2]])

# Helper to place tiles
def place_tile(tile_index, x, y):
  tile_grid[x][y] = tiles[tile_index]
  average_color_grid[x][y] = average_color_list[tile_index]
  used_tiles.add(tile_index)

# Pick a random tile for the top left corner
place_tile(random.randint(0,len(tiles)-1), 0, 0)

# Iterate from top to bottom
for i in range(mosaic_width_in_tiles):
    # Iterate from left to right
  for j in range(mosaic_width_in_tiles):
    minimum_difference = float("inf")
    tile_index = -1
    # Consider all tiles
    for k in range(len(tiles)):
      if k in used_tiles:
        continue
        # Calculate difference in left neighbor, upper neighbor and upper-left neighbor
      difference = sum(get_rgb_difference(k, *x)
                       for x in [(i-1, j), (i, j-1)])
      if difference < minimum_difference:
        minimum_difference = difference
        tile_index = k
    # Place tile
    place_tile(tile_index, i, j)

# Finally, create mosaic
mosaic = Image.new("RGB", (mosaic_width_in_pixels, mosaic_width_in_pixels))
for i in range(mosaic_width_in_tiles):
  for j in range(mosaic_width_in_tiles):
    if (tile_grid[i][j]):
      mosaic.paste(tile_grid[i][j], (i*single_tile_width, j*single_tile_width))
      mosaic.save("mosiac.png")