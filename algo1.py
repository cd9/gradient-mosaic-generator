from glob import glob
from PIL import Image
from math import floor, sqrt
from heapq import heappush, heappop
import numpy
from copy import deepcopy
from helpers import get_delta_sum, get_empty_grid, get_rgb_delta, is_valid_coordinate

# Grab all tiles
tile_paths = [x for x in glob("./tiles/*")]
tiles = [Image.open(x) for x in tile_paths]

# Calculate mosaic size
single_tile_width = tiles[0].size[0]
mosaic_width = floor(sqrt(len(tiles)))
mosaic_width_px = mosaic_width*single_tile_width

# Create grid
average_list = [numpy.array(x).mean(axis=0).mean(axis=0) for x in tiles]
tile_grid = None
used_tiles = None

# Helper to determine difference in RGB, without knowing index of first tile
def get_rgb_delta_weighted(k, x1, y1, x2, y2):
  if not is_valid_coordinate(x2, y2, mosaic_width):
    return 0
  weight = 1/sqrt((x2-x1)**2+(y2-y1)**2)
  return get_rgb_delta(average_list[k], average_list[tile_grid[x2][y2]])*weight

# Helper to place tiles
def place_tile(tile_index, x, y):
  tile_grid[x][y] = tile_index
  used_tiles.add(tile_index)

mosaic_heap = []
for t in range(len(tiles)):
  # Pick the starting tile (the seed)
  tile_grid = get_empty_grid(mosaic_width)
  used_tiles = set()
  place_tile(t, 0, 0)
  seen_coords = set()
  queue = [(1, 0), (0, 1)]

  # Populate the mosaic using a greedy approach, breadth-first
  while queue:
    i, j = queue.pop(0)
    minimum_difference = float("inf")
    tile_index = -1

    # Try to place every tile that hasn't been placed
    for k in [x for x in range(len(tiles)) if not x in used_tiles]:
      # Sum RGB component difference with nearest neighbors
      difference = sum(get_rgb_delta_weighted(k, i, j, *x)
                       for x in [(i-1, j), (i, j-1), (i-1, j-1), (i-2, j), (i, j-2)])
      if difference < minimum_difference:
        minimum_difference = difference
        tile_index = k
    # Place the best tile
    place_tile(tile_index, i, j)

    # Queue neighbors
    for x, y in [(i+1, j), (i, j+1)]:
      if is_valid_coordinate(x, y, mosaic_width) and not (x, y) in seen_coords:
        queue.append((x, y))
        seen_coords.add((x, y))

  # Score this mosaic
  heappush(mosaic_heap, (get_delta_sum(
      0, 0, tile_grid, set(), average_list), deepcopy(tile_grid)))

# Finally, output top 10 mosaics
for k in range(10):
  delta_sum, grid = heappop(mosaic_heap)
  print(f"Delta Sum for mosaic_{k}: {delta_sum}")
  mosaic = Image.new("RGB", (mosaic_width_px, mosaic_width_px))
  for i in range(mosaic_width):
    for j in range(mosaic_width):
      mosaic.paste(tiles[grid[i][j]],
                   (i*single_tile_width, j*single_tile_width))
  mosaic.save(f"./output/algo1/mosaic_{k}_{int(delta_sum)}.png")
