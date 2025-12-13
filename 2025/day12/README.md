# Day 12: Christmas Tree Farm

## Problem Summary

2D bin packing problem with polyomino shapes (presents) that need to fit into rectangular regions under Christmas trees.

## Key Requirements

1. Parse present shapes (polyominoes) from visual representation
2. Parse region specifications with required present counts
3. Determine if all required presents can fit in each region
4. Presents can be rotated and flipped
5. Shapes cannot overlap but can interlock (# parts can't overlap, . parts don't block)
6. Must align to grid perfectly

## Input Format

```
Shape definitions:
0: ### 
   ##. 
   ##.  

Region specifications:
4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2 1
```

## Algorithm Approach

This is a complex constraint satisfaction problem that will likely require:
1. Shape parsing and normalization
2. Generation of all rotations/reflections for each shape
3. Backtracking placement algorithm
4. Efficient collision detection

## Example

First region (4x4) with two shape-4 presents:
```
AAA.
ABAB
ABAB
.BBB
```

Result: Count regions where all presents fit.