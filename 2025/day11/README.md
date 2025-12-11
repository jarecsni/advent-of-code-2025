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

## Approach

1. Parse the input to build a directed graph (adjacency list)
2. Use DFS to find all paths from "you" to "out"
3. Count the total number of paths

## Solution

- Part 1: [reactor.py](reactor.py)