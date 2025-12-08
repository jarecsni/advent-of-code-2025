# Day 7: Laboratories

## Problem Description

You're in a teleporter lab with a malfunctioning tachyon manifold. A tachyon beam enters at position `S` and travels downward through the manifold.

### Rules
- Tachyon beams always move downward
- Beams pass freely through empty space (`.`)
- When a beam encounters a splitter (`^`), the beam stops and two new beams are emitted from the immediate left and right of the splitter
- Multiple beams can occupy the same position (they merge into one beam)

### Part 1
Count how many times the beam is split as it travels through the manifold.

### Example
```
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
```

In this example, the beam is split **21 times**.

## Solution Approach

This is a beam simulation problem where we need to:
1. Track active beams as they move downward
2. When a beam hits a splitter, stop it and create two new beams (left and right)
3. Handle beam merging when multiple beams occupy the same position
4. Count the total number of splits

Key considerations:
- Need to track beam positions and handle simultaneous movement
- Beams that move into the same column merge
- Need to detect when all beams have exited the manifold
