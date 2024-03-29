# Gradient Mosaic Generator

### Motivation

Once upon a time, ~40 square, ceramic album art coasters were created as part of a weekend arts-and-crafts project. After all the coasters had been properly assembled, glued, and dried, they were laid out on a coffee table in a contemporary living room both for the aesthetics of the moment and for an obligatory *à la mode* photoshoot. It was soon realized that tiling the coasters randomly on the coffee table resulted in suboptimal aesthetics. *Was there a better way to lay the coasters out on the table?* 

Having endured frightening amounts of exposure to leetcode problems, my brain reactively, and against my free will, context-switched into a state of problem-solving automation. It was agreed upon that **the optimal tile layout would be one such that each tile appears to blend into the next.**

Generally, an ideal layout would most closely approximate a gradient. But the formal requirement can have several different interpretations, each with their own specification of what entails an *optimal* mosaic. 

Since encountering this larger-than-life problem, I haven't been able to kick the urge to try and code up some of the proposed solutions. This repository contains a few different algorithms and approaches on how to generate an optimal "gradient mosaic".

### The Problem

Given a set of square image tiles of the same width, the desired output is a tiled photo mosaic such that each photo appears to blend into its neighbors (i.e. a color gradient).

### Algorithm 1: Breadth-First Greedy
- Calculate the average color of each tile
- Place a seed tile at (0,0)
- For each blank tile in a breadth-first order, starting at (0,0):
	- Place the candidate tile with the minimum sum of RGB differences between it's nearest neighbors
- Rank the mosaic based on the sum of RGB differences between all pairs of adjacent tiles (sum weights in the graph)

#### Sample Algorithm 1 results
<p float="left">
<img src="./output/algo1/mosaic_3_8131.png" width=400/>
<img src="./output/algo1/mosaic_0_7898.png" width=400/>
</p>

#### Algorithm 1 Observations
- The greedy approach of picking the closest-matching tile has a two-fold effect:
  - Locally, it naturally makes the current tile blend into its neighbors.
  - Globally, tiles are gradually filtered out of the selection pool as they are chosen, eventually sorting them into color groups.

### Algorithm 2: Random Swaps
- Start with a random configuration of tiles on a canvas
- Calculate the sum of RGB differences between all pairs of adjacent tiles (sum weights in the graph)
  - Call this sum the `delta_sum`
- For every possible swap, chosen in random order, and without replacement:
	- Swap two tiles and update the `delta_sum` (done in constant time)
	- If the new `delta_sum` is lower than the old `delta_sum`, reset the list of all possible swaps
	- Else, reverse the changes by swapping again
	- Exit when all possible swaps have been attempted

#### Sample Algorithm 2 results
<p float="left">
<img src="./output/algo2/mosaic_3622.png" width=400/>
<img src="./output/algo2/mosaic_3650.png" width=400/>
</p>

#### Algorithm 2 Visualization
<img src="./output/algo2/animation.gif" width=400/>

#### Algorithm 2 Observations
- This algorithm doesn't "sort" tiles as effectively as algorithm 1.
  - Some mosaics have multiple "clusters" of colors since there is sometimes no advantage to grouping them together.
- Very dense clusters of solid colors with very sometimes little "feathering" into other clusters.
- Only swapping two tiles at once severely limits the flexibility of the mosaic. For example, a piecewise shift of an entire row to the left by one tile may result in a final lower `delta_sum`, but would never be performed by the algorithm as long as an individual swap increases the `delta_sum`. (Note that adding multiple-step transformations would severely increase the complexity of the algorithm)

### Algorithm 3: Breadth First + Random Swaps
- Algorithm 2, but instead of starting with random mosaics, start with with results from algorithm 1

#### Sample Algorithm 3 results
<p float="left">
<img src="./output/algo3/mosaic_6731.png" width=400/>
<img src="./output/algo3/mosaic_6173.png" width=400/>
</p>

#### Algorithm 3 Observations
- Similar results to algorithm 1, just with less 'mistakes' (as expected).
- Starting with a greedy-generated canvas usually prevents the algorithm from splitting colors into multiple clusters.
