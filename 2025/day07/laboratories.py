def parse_manifold(filename):
    """Parse the manifold diagram and return grid and start position."""
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
    
    # Find start position
    start_col = None
    for col, char in enumerate(lines[0]):
        if char == 'S':
            start_col = col
            break
    
    return lines, start_col


def simulate_beams(grid, start_col):
    """Simulate tachyon beams through the manifold and count splits."""
    splits = 0
    beams = {start_col}  # Set of active beam columns
    
    # Process each row
    for row_idx in range(1, len(grid)):
        row = grid[row_idx]
        new_beams = set()
        
        for beam_col in beams:
            # Check if this position has a splitter
            if beam_col < len(row) and row[beam_col] == '^':
                # Beam hits splitter - count it as a split
                splits += 1
                # Create two new beams (left and right)
                new_beams.add(beam_col - 1)
                new_beams.add(beam_col + 1)
            else:
                # Beam continues downward
                new_beams.add(beam_col)
        
        # Remove out-of-bounds beams
        beams = {col for col in new_beams if 0 <= col < len(row)}
        
        # If no beams remain, we're done
        if not beams:
            break
    
    return splits


def count_timelines(grid, row, col, memo=None):
    """Count the number of distinct timelines (paths) from this position."""
    if memo is None:
        memo = {}
    
    # Base case: particle exits the bottom
    if row >= len(grid):
        return 1
    
    # Check memo
    if (row, col) in memo:
        return memo[(row, col)]
    
    # Check if out of bounds horizontally
    if col < 0 or col >= len(grid[row]):
        return 0
    
    # Check if current position has a splitter
    if grid[row][col] == '^':
        # Timeline splits: count paths going left + paths going right
        left_paths = count_timelines(grid, row + 1, col - 1, memo)
        right_paths = count_timelines(grid, row + 1, col + 1, memo)
        result = left_paths + right_paths
    else:
        # Continue straight down
        result = count_timelines(grid, row + 1, col, memo)
    
    memo[(row, col)] = result
    return result


def solve_part1(filename):
    """Solve part 1: count total beam splits."""
    grid, start_col = parse_manifold(filename)
    return simulate_beams(grid, start_col)


def solve_part2(filename):
    """Solve part 2: count total timelines."""
    grid, start_col = parse_manifold(filename)
    # Start counting from row 1 (after S)
    return count_timelines(grid, 1, start_col)


if __name__ == '__main__':
    import sys
    
    # Check for --part2 flag
    if '--part2' in sys.argv:
        result = solve_part2('input.txt')
        print(f'Part 2: {result}')
    else:
        result = solve_part1('input.txt')
        print(f'Part 1: {result}')
