#!/usr/bin/env python3
"""
Test suite for Christmas Tree Farm solution
"""

import unittest
from fast_solution import ChristmasTreeFarm, Shape, generate_orientations, FastSolver


class TestChristmasTreeFarm(unittest.TestCase):
    
    def test_shape_parsing(self):
        """Test shape parsing from visual representation"""
        farm = ChristmasTreeFarm()
        test_input = """0: ###
   ##.
   ##.

1: ###
   #..
   ###"""
        
        farm.parse_input(test_input)
        
        self.assertEqual(len(farm.shapes), 2)
        self.assertEqual(farm.shapes[0].area, 7)
        self.assertEqual(farm.shapes[1].area, 7)
        
        # Check shape 0 coordinates (L-shape)
        expected_0 = {(0,0), (0,1), (0,2), (1,0), (1,1), (2,0), (2,1)}
        self.assertEqual(farm.shapes[0].cells, expected_0)
        
        # Check shape 1 coordinates (plus-like)
        expected_1 = {(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)}
        self.assertEqual(farm.shapes[1].cells, expected_1)
    
    def test_region_parsing(self):
        """Test region parsing"""
        farm = ChristmasTreeFarm()
        test_input = """4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2 1"""
        
        farm.parse_input(test_input)
        
        self.assertEqual(len(farm.regions), 2)
        self.assertEqual(farm.regions[0], (4, 4, [0, 0, 0, 0, 2, 0]))
        self.assertEqual(farm.regions[1], (12, 5, [1, 0, 1, 0, 2, 2, 1]))
    
    def test_shape_orientations(self):
        """Test orientation generation"""
        # Simple 2x1 rectangle
        cells = {(0, 0), (0, 1)}
        orientations = generate_orientations(cells)
        
        # Should have 2 unique orientations: horizontal and vertical
        self.assertGreaterEqual(len(orientations), 2)
        
        # Check we have both orientations
        horizontal = {(0, 0), (0, 1)}
        vertical = {(0, 0), (1, 0)}
        
        found_horizontal = any(o == horizontal for o in orientations)
        found_vertical = any(o == vertical for o in orientations)
        
        self.assertTrue(found_horizontal)
        self.assertTrue(found_vertical)
    
    def test_simple_placement(self):
        """Test simple piece placement"""
        # Create a simple 2x2 region with one 2x1 piece
        shapes = [Shape(0, {(0, 0), (0, 1)})]  # 2x1 rectangle
        solver = FastSolver(2, 2, shapes, [1])  # One piece in 2x2 grid
        
        # Should be solvable
        self.assertTrue(solver.solve())
    
    def test_impossible_placement(self):
        """Test impossible placement detection"""
        # Try to fit 5 cells in 4-cell region
        shapes = [Shape(0, {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)})]  # 5 cells
        solver = FastSolver(2, 2, shapes, [1])  # 4-cell region
        
        # Should be impossible
        self.assertFalse(solver.solve())
    
    def test_example_case(self):
        """Test the actual example case"""
        farm = ChristmasTreeFarm()
        
        # Use the actual example
        with open('example.txt', 'r') as f:
            farm.parse_input(f.read())
        
        result = farm.solve()
        
        # According to problem, should be 1 (only first region solvable)
        self.assertEqual(result, 1)
    
    def test_area_calculation(self):
        """Test area calculations"""
        shape = Shape(0, {(0, 0), (0, 1), (1, 0)})  # L-shape
        self.assertEqual(shape.area, 3)
        
        shape2 = Shape(1, {(0, 0), (0, 1), (0, 2), (1, 1)})  # T-shape
        self.assertEqual(shape2.area, 4)
    
    def test_normalization(self):
        """Test shape normalization"""
        # Shape not starting at (0,0)
        shape = Shape(0, {(2, 3), (2, 4), (3, 3)})
        
        # Should be normalized to start at (0,0)
        expected = {(0, 0), (0, 1), (1, 0)}
        self.assertEqual(shape.cells, expected)


if __name__ == '__main__':
    unittest.main()