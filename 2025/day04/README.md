# Day 4: Printing Department

## Problem Summary

The printing department has paper rolls (`@`) on a grid. Forklifts can only access rolls that have **fewer than 4** neighbouring rolls in the 8 adjacent positions (Moore neighbourhood).

## Part 1: Count Accessible Rolls

Count how many rolls can be accessed by forklifts based on the neighbourhood rule.

## Part 2: Iterative Removal

After removing all accessible rolls, some previously inaccessible rolls may become accessible. Repeat the process until no more rolls can be removed. Count total removed rolls.

## Example

```
..@@.
@@@@.
.@@@.@.
@.@@@
.@@@@@.@.
@@
.@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

### Part 1 Analysis
- Each `@` is checked against its 8 neighbours
- If fewer than 4 neighbours are `@`, the roll is accessible
- In this example: 13 rolls are accessible

### Part 2 Process
1. Remove all accessible rolls
2. Check remaining rolls for new accessibility
3. Repeat until no changes occur
4. Count total rolls removed across all iterations

## Algorithm

**Part 1**: Single pass neighbourhood counting
**Part 2**: Iterative simulation with convergence detection

## Key Insights

- Moore neighbourhood: 8 directions including diagonals
- Boundary handling: positions outside grid count as empty
- Convergence: process stops when no rolls can be removed in an iteration
