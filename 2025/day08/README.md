# Day 8: Playground

## Problem Summary

Connect junction boxes in 3D space by repeatedly connecting the two closest unconnected boxes. After making 1000 connections, find the product of the sizes of the three largest circuits.

## Approach

This is essentially Kruskal's algorithm for minimum spanning tree, but we stop after a specific number of edges rather than when we have a spanning tree.

Key components:
- Parse 3D coordinates
- Calculate Euclidean distances between all pairs
- Use Union-Find (Disjoint Set Union) to track circuits
- Sort edges by distance and connect the shortest ones
- Track circuit sizes and find the three largest

## Algorithm

1. Parse all junction box coordinates
2. Generate all possible pairs and calculate distances
3. Sort pairs by distance (ascending)
4. Use Union-Find to connect boxes:
   - For each pair in sorted order:
     - If boxes are in different circuits, connect them
     - Stop after 1000 connections
5. Count circuit sizes
6. Return product of three largest circuits

## Complexity

- Time: O(n² log n) for sorting all pairs
- Space: O(n²) for storing all distances
- With n junction boxes, we have n(n-1)/2 pairs

## Notes

- Union-Find with path compression and union by rank for efficiency
- Need to handle the case where boxes are already in the same circuit (no-op)
- After 1000 connections, we'll have (n - 1000) circuits remaining
