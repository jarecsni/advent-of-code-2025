#!/usr/bin/env python3
"""
Tests for Day 12: Christmas Tree Farm
"""

import pytest
from farm import ChristmasTreeFarm, Shape, Region


def test_shape_parsing():
    """Test shape parsing from visual representation"""
    farm = ChristmasTreeFarm()
    
    example_input = """0: ###
   ##.
   ##.

4x4: 0 0 0 0 2 0"""
    
    farm.parse_input(example_input)
    
    assert len(farm.shapes) == 1
    shape = farm.shapes[0]
    assert shape.id == 0
    # Shape should be normalized to start at (0,0)
    expected_cells = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)}
    assert shape.cells == expected_cells


def test_region_parsing():
    """Test region parsing"""
    farm = ChristmasTreeFarm()
    
    example_input = """0: ###
   ##.

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2 1"""
    
    farm.parse_input(example_input)
    
    assert len(farm.regions) == 2
    
    region1 = farm.regions[0]
    assert region1.width == 4
    assert region1.height == 4
    assert region1.required_counts == [0, 0, 0, 0, 2, 0]
    
    region2 = farm.regions[1]
    assert region2.width == 12
    assert region2.height == 5
    assert region2.required_counts == [1, 0, 1, 0, 2, 2, 1]


def test_shape_properties():
    """Test shape width and height calculation"""
    # L-shaped piece
    cells = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0), (2, 1)}
    shape = Shape(0, cells)
    
    assert shape.width == 3
    assert shape.height == 3


if __name__ == "__main__":
    pytest.main([__file__])