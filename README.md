# Gradient Mosaic Generator

Given a set of square image tiles of the same width, the desired output is a tiled photo mosaic such that each photo appears to blend into its neighbors (i.e. a color gradient).

**Algorithm 1: Bottom-up picking of tiles with minimum difference in average RGB values**
- Calculate the average color of each tile
- Calculate the difference in average colors betweeen each tile (sum of differences between R,G, and B values)
- Pick a canvas size.
- Iterate over each (blank) tile in the canvas, first from left to right then top-down.
- Place on the blank tile the image with the minimum sum of differences in average color from it's left and above neighbors.
