#!/usr/bin/env python3

from glob import glob
from PIL import Image
from math import floor, sqrt
from heapq import heappush, heappop
import random
import numpy
from copy import deepcopy
from helpers import get_delta_sum, get_empty_grid, get_rgb_delta, is_valid_coordinate

MOSAICS_TO_GENERATE = 20

# Grab all tiles
tile_paths = [x for x in glob("./tiles/*")]
tiles = [Image.open(x) for x in tile_paths]

# Calculate mosaic size
single_tile_width = tiles[0].size[0]
mosaic_width = floor(sqrt(len(tiles)))
mosaic_width_px = mosaic_width*single_tile_width

# Create grid
average_list = [numpy.array(x).mean(axis=0).mean(axis=0) for x in tiles]
tile_grid = get_empty_grid(mosaic_width)
all_coordinates = []
for i in range(mosaic_width):
	for j in range(mosaic_width):
		all_coordinates.append((i,j))
all_swaps = []
for i, c1 in enumerate(all_coordinates):
	for c2 in all_coordinates[i+1:]:
		all_swaps.append((c1,c2))

# Helper to swap two tiles and update `delta_sum` in constant time
def perform_swap(delta_sum, c1, c2):
	new_delta_sum = delta_sum
	for a, b in [(c1, c2), (c2, c1)]:
		for e in [(a[0]+1, a[1]), (a[0]-1, a[1]), (a[0], a[1]+1), (a[0], a[1]-1)]:
			if is_valid_coordinate(*e, mosaic_width) and all(sorted(e) != sorted(x) for x in [a, b]):
				# Remove the original edge deltas
				new_delta_sum -= get_rgb_delta(
						average_list[tile_grid[a[0]][a[1]]], average_list[tile_grid[e[0]][e[1]]])
				# Add the new edge deltas
				new_delta_sum += get_rgb_delta(
						average_list[tile_grid[b[0]][b[1]]], average_list[tile_grid[e[0]][e[1]]])
	temp = tile_grid[c1[0]][c1[1]]
	tile_grid[c1[0]][c1[1]] = tile_grid[c2[0]][c2[1]]
	tile_grid[c2[0]][c2[1]] = temp
	return new_delta_sum

mosaic_heap = []
for i in range(MOSAICS_TO_GENERATE):
	timeout = 0
	# Reset grid
	all_indexes = list(range(len(tiles)))
	for j in range(mosaic_width):
		for k in range(mosaic_width):
			index = random.choice(all_indexes)
			all_indexes.remove(index)
			tile_grid[j][k] = index

	# Initial delta sum
	delta_sum = get_delta_sum(0, 0, tile_grid, set(), average_list)
	swaps_to_try = deepcopy(all_swaps)
	while len(swaps_to_try) > 0:
		swap = random.choice(swaps_to_try)
		swaps_to_try.remove(swap)
		old_delta_sum = delta_sum
		delta_sum = perform_swap(delta_sum, *swap)
		if int(delta_sum) < int(old_delta_sum):
			swaps_to_try = deepcopy(all_swaps)
		else:
			delta_sum = perform_swap(delta_sum, *swap)
	# Score this mosaic
	heappush(mosaic_heap, (delta_sum, deepcopy(tile_grid)))
	print(f"Mosaic {i+1}/{MOSAICS_TO_GENERATE} complete with delta sum {delta_sum}")

# Finally, output top 10 mosaics
for k in range(10):
	delta_sum, mosaic_grid = heappop(mosaic_heap)
	print(f"Delta Sum for mosaic_{k}: {delta_sum}")
	mosaic = Image.new("RGB", (mosaic_width_px, mosaic_width_px))
	for i in range(mosaic_width):
		for j in range(mosaic_width):
			mosaic.paste(tiles[mosaic_grid[i][j]],
									 (i*single_tile_width, j*single_tile_width))
	mosaic.save(f"./output/algo2/mosaic_{k}_{int(delta_sum)}.png")
