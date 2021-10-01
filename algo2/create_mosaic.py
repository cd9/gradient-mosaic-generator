from glob import glob
from PIL import Image
from math import floor, sqrt
from scipy import spatial
from heapq import heappush, heappop
import random
import numpy
from copy import deepcopy

TIMEOUT = 50000
MOSAICS_TO_GENERATE = 50

# Grab all tiles
tile_paths = [x for x in glob("../tiles/*")]
tiles = [Image.open(x) for x in tile_paths]

# Calculate mosaic size
single_tile_width = tiles[0].size[0]
mosaic_width = floor(sqrt(len(tiles)))
mosaic_width_px = mosaic_width*single_tile_width

# Helper to make 2D grid
def get_empty_grid():
	return [[None] * mosaic_width
					for j in range(mosaic_width)]

# Create grid
average_list = [numpy.array(x).mean(axis=0).mean(axis=0) for x in tiles]
tile_grid = get_empty_grid()
all_coordinates = set()
for i in range(mosaic_width):
	for j in range(mosaic_width):
		all_coordinates.add((i,j))

# Helper to check if coordinate is in grid range
def is_valid_coordinate(x, y):
	return all([z >= 0 and z < mosaic_width for z in [x, y]])

# Helper to determine difference in RGB
def get_rgb_delta(color1, color2):
	return sum([abs(color1[i]-color2[i]) for i in [0, 1, 2]])

# Recursively add up the differences in between each adjacent tile
def get_delta_sum(i, j, grid, seen):
	if (i, j) in seen:
		return 0
	seen.add((i, j))
	delta_sum = 0
	if is_valid_coordinate(i+1, j):
		delta_sum += get_rgb_delta(average_list[grid[i][j]], average_list[grid[i+1]
																																			[j]]) + get_delta_sum(i+1, j, grid, seen)
	if is_valid_coordinate(i, j+1):
		delta_sum += get_rgb_delta(average_list[grid[i][j]], average_list[grid[i]
																																			[j+1]]) + get_delta_sum(i, j+1, grid, seen)
	return delta_sum

def get_neighbor_coordinates(x, y):
	neighbors = [(x+1,y),(x,y+1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1),(x-1,y),(x,y-1)]
	return [n for n in neighbors if is_valid_coordinate(*n)]

def get_random_coordinate(exclude):
	return random.sample(all_coordinates.difference(exclude), 1)[0]

def perform_swap(delta_sum, c1, c2):
	new_delta_sum = delta_sum
	for a, b in [(c1, c2), (c2, c1)]:
		for e in [(a[0]+1, a[1]), (a[0]-1, a[1]), (a[0], a[1]+1), (a[0], a[1]-1)]:
			# Ignore adjacent edge if tiles are adjacent
			if is_valid_coordinate(*e) and all(sorted(e) != sorted(x) for x in [a, b]):
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
	delta_sum = get_delta_sum(0, 0, tile_grid, set())
	while True:
		x = get_random_coordinate(set())
		y = get_random_coordinate(set(x))
		swap = (x,y)
		old_delta_sum = delta_sum
		delta_sum = perform_swap(delta_sum, *swap)
		if int(delta_sum) < int(old_delta_sum):
			timeout = 0
		else:
			delta_sum = perform_swap(delta_sum, *swap)
			timeout += 1
			if timeout >= TIMEOUT:
				break
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
	mosaic.save(f"mosaic_{k}_{int(delta_sum)}.png")
