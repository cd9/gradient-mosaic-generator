# Gradient Mosaic Generator

Given a set of square image tiles of the same width, the desired output is a tiled photo mosaic such that each photo appears to blend into its neighbors (i.e. a color gradient).

### Algorithm 1: Bottom-up picking of tiles with minimum difference in average RGB values
- Calculate the average color of each tile
- Pick a random tile to place at (0,0)
- Iterate over each (blank) tile in the canvas by diagonals starting from top-left to bottom-right
- Place on the blank tile the image with the minimum sum of differences in average color from it's left, upper, and upper-left neighbors
