# Gradient Mosaic Generator

Given a set of square image tiles of the same width, the desired output is a tiled photo mosaic such that each photo appears to blend into its neighbors (i.e. a color gradient).

### Algorithm 1: Bottom-up picking of tiles with minimum difference in average RGB values

- Calculate the average color of each tile
- For each possible tile to place at (0,0)
  - Iterate over each (blank) tile in the canvas by diagonals starting from top-right to bottom-left
  - Place on the blank tile the image with the minimum sum of differences in average color from it's left, upper, and upper-left neighbors
	- Rank the mosaic based on the sum of average color RGB differences between adjacent tiles
- Output the 5 top ranking mosaics

#### Sample Algorithm 1 results:
<p float="left">
<img src="./algo1/mosaic_3.png" width=400/>
<img src="./algo1/mosaic_5.png" width=400/>
<img src="./algo1/mosaic_0.png" width=400/>
<img src="./algo1/mosaic_1.png" width=400/>
</p>
