# Helper to make 2D grid
def get_empty_grid(mosaic_width):
	return [[None] * mosaic_width
			for j in range(mosaic_width)]

# Helper to check if coordinate is in grid range
def is_valid_coordinate(x, y, mosaic_width):
	return all([z >= 0 and z < mosaic_width for z in [x, y]])

# Helper to determine difference in RGB
def get_rgb_delta(color1, color2):
	return sum([abs(color1[i]-color2[i]) for i in [0, 1, 2]])

# Recursively add up the differences in between each adjacent tile
def get_delta_sum(i, j, grid, seen, average_list):
	if (i, j) in seen:
		return 0
	seen.add((i, j))
	delta_sum = 0
	if is_valid_coordinate(i+1, j, len(grid)):
		delta_sum += get_rgb_delta(average_list[grid[i][j]], average_list[grid[i+1][j]])
		delta_sum += get_delta_sum(i+1, j, grid, seen, average_list)
	if is_valid_coordinate(i, j+1, len(grid)):
		delta_sum += get_rgb_delta(average_list[grid[i][j]], average_list[grid[i][j+1]])
		delta_sum += get_delta_sum(i, j+1, grid, seen, average_list)
	return delta_sum
