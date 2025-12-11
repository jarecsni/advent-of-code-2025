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

1. Parse the input to build a directed graph (adjacency list)
2. Use DFS to find all paths from start to end
3. For part 2, filter paths that visit all required nodes

## Solution

- Part 1 & 2: [reactor.py](reactor.py)