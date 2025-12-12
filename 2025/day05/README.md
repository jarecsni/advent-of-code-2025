# Day 5: Cafeteria

## Problem Summary

The cafeteria's inventory system tracks ingredient freshness using ID ranges. Determine which available ingredients are fresh based on given ranges.

## Part 1: Fresh Ingredient Count

Given fresh ingredient ID ranges and available ingredient IDs, count how many available ingredients are fresh.

- Ranges are inclusive and can overlap
- An ingredient is fresh if it falls within any range

### Example

```
3-5 10-14 16-20 12-18

1 5 8 11 17 32
```

Analysis:
- ID 1: spoiled (not in any range)
- ID 5: fresh (in range 3-5)
- ID 8: spoiled (not in any range)
- ID 11: fresh (in range 10-14)
- ID 17: fresh (in ranges 16-20 and 12-18)
- ID 32: spoiled (not in any range)

Result: **3 fresh ingredients**

## Part 2: TBD

[Part 2 will be added when available]

## Algorithm

1. Parse fresh ID ranges from first line
2. Parse available ingredient IDs from second line
3. For each available ID, check if it falls within any fresh range
4. Count matches

## Key Insights

- Range intersection problem
- Overlapping ranges don't affect the result
- Simple linear scan is sufficient for reasonable input sizes

## Usage

```bash
python cafeteria.py example.txt
python cafeteria.py input.txt
```

Run tests:
```bash
python -m pytest test_cafeteria.py -v
```
