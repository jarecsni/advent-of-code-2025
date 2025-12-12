"""
Tests for optimized Day 11: Reactor solution
"""
import unittest
from reactor_optimized import parse_input, count_paths_simple, part1, part2

class TestOptimizedSolution(unittest.TestCase):
    """Test the optimized reactor solution."""
    
    def test_count_paths_simple(self):
        """Test simple path counting."""
        graph = {
            "a": ["b", "c"],
            "b": ["d"],
            "c": ["d"],
            "d": ["end"]
        }
        
        # Should find 2 paths from a to end
        count = count_paths_simple(graph, "a", "end")
        self.assertEqual(count, 2)
        
        # Should find 1 path from b to end
        count = count_paths_simple(graph, "b", "end")
        self.assertEqual(count, 1)
        
        # Should find 0 paths from end to a
        count = count_paths_simple(graph, "end", "a")
        self.assertEqual(count, 0)
    
    def test_part1_example(self):
        """Test part 1 with example input."""
        data = parse_input("example.txt")
        result = part1(data)
        self.assertEqual(result, 5)
    
    def test_part2_example(self):
        """Test part 2 with example input."""
        data = parse_input("example2.txt")
        result = part2(data)
        self.assertEqual(result, 2)
    
    def test_part1_vs_original(self):
        """Test that optimized part 1 matches original."""
        from reactor import part1 as original_part1
        
        data = parse_input("example.txt")
        optimized_result = part1(data)
        original_result = original_part1(data)
        
        self.assertEqual(optimized_result, original_result)

if __name__ == "__main__":
    unittest.main()