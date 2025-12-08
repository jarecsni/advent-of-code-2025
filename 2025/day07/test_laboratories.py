import pytest
from laboratories import parse_manifold, simulate_beams, solve_part1


def test_parse_manifold():
    """Test parsing the manifold diagram."""
    grid, start_col = parse_manifold('example.txt')
    assert start_col == 7
    assert len(grid) == 16
    assert grid[0][7] == 'S'


def test_example_part1():
    """Test part 1 with the example input."""
    result = solve_part1('example.txt')
    assert result == 21


def test_first_split():
    """Test that the first splitter creates a split."""
    grid = [
        '.......S.......',
        '...............',
        '.......^.......'
    ]
    result = simulate_beams(grid, 7)
    assert result == 1


def test_adjacent_splitters_with_merge():
    """Test two adjacent splitters that create merging beams."""
    grid = [
        '.......S.......',
        '...............',
        '.......^.......',
        '...............',
        '......^.^......'
    ]
    result = simulate_beams(grid, 7)
    # First split creates 2 beams, then 2 more splits (one for each beam)
    assert result == 3


def test_no_splitters():
    """Test beam passing through with no splitters."""
    grid = [
        '.......S.......',
        '...............',
        '...............',
        '...............'
    ]
    result = simulate_beams(grid, 7)
    assert result == 0


def test_beam_exits_bounds():
    """Test that beams exiting the grid don't cause issues."""
    grid = [
        'S..............',
        '^..............'
    ]
    result = simulate_beams(grid, 0)
    # Beam at col 0 hits splitter, creates beam at -1 (out of bounds) and 1
    assert result == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
