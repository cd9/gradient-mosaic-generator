#!/usr/bin/env python3

from glob import glob
from PIL import Image
from math import floor, sqrt
from heapq import heappush, heappop
import random
import numpy
from copy import deepcopy
from helpers import get_delta_sum, get_empty_grid, get_rgb_delta, is_valid_coordinate

MOSAICS_TO_GENERATE = 111

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
all_coordinates = []
for i in range(mosaic_width):
	for j in range(mosaic_width):
		all_coordinates.append((i,j))
all_swaps = []
for i, c1 in enumerate(all_coordinates):
	for c2 in all_coordinates[i+1:]:
		all_swaps.append((c1,c2))

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

# Helper to get random coordinate
def get_random_coordinate(exclude):
	return random.sample(all_coordinates.difference(exclude), 1)[0]

# Helper to swap two tiles and update `delta_sum` in constant time
def perform_swap(delta_sum, c1, c2):
	new_delta_sum = delta_sum
	for a, b in [(c1, c2), (c2, c1)]:
		for e in [(a[0]+1, a[1]), (a[0]-1, a[1]), (a[0], a[1]+1), (a[0], a[1]-1)]:
			# Ignore adjacent edge if tiles are adjacent
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

mosaics = []
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

	# Add mosaic to list
	mosaics.append(deepcopy(tile_grid))

mosaic_heap = []
mosaics = sorted(mosaics, key=lambda m: m[0])[:MOSAICS_TO_GENERATE]
for i, mosaic in enumerate(mosaics):
	timeout = 0
	# Reset grid
	tile_grid = deepcopy(mosaic)

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
	print(f"Mosaic {i+1}/{len(mosaics)} complete with delta sum {delta_sum}")

# Finally, output top 10 mosaics
for k in range(10):
	delta_sum, mosaic_grid = heappop(mosaic_heap)
	print(f"Delta Sum for mosaic_{k}: {delta_sum}")
	mosaic = Image.new("RGB", (mosaic_width_px, mosaic_width_px))
	for i in range(mosaic_width):
		for j in range(mosaic_width):
			mosaic.paste(tiles[mosaic_grid[i][j]],
									 (i*single_tile_width, j*single_tile_width))
	mosaic.save(f"./output/algo3/mosaic_{int(delta_sum)}.png")
