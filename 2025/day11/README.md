# Day 11: Reactor

## Problem Summary

Find all possible paths from device "you" to device "out" in a directed graph of electrical devices.

## Part 1

Given a list of devices and their outputs, count the total number of different paths from "you" to "out".

Example:
```
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
```

This creates a directed graph where we need to find all paths from "you" to "out".

## Part 2

Find all paths from "svr" to "out" that visit both "dac" and "fft" (in any order).

Example:
```
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
```

Of all the paths from "svr" to "out", only 2 visit both "dac" and "fft":
- svr → aaa → fft → ccc → eee → dac → fff → ggg → out
- svr → aaa → fft → ccc → eee → dac → fff → hhh → out

## Approach

### Original Solution (reactor.py)
1. Parse the input to build a directed graph (adjacency list)
2. Use DFS to find all paths from start to end
3. For part 2, use memoized DFS tracking visited required nodes

**Performance**: Works for examples but too slow for large inputs in Part 2.

### Optimized Solution (reactor_optimized.py)
1. Parse the input to build a directed graph
2. For Part 1: Simple memoized path counting
3. For Part 2: Key insight - split into segments and multiply counts
   - Count paths: svr → fft → dac → out
   - Since the graph is a DAG, only one direction (fft→dac or dac→fft) exists
   - Multiply segment counts: (svr→fft) × (fft→dac) × (dac→out)

**Performance**: Runs in milliseconds for both parts.

## Solutions

- Original: [reactor.py](reactor.py) 
- Optimized: [reactor_optimized.py](reactor_optimized.py)