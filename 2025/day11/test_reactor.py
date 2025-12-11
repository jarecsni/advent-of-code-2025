"""
Tests for Day 11: Reactor
"""
import unittest
from reactor import parse_input, find_all_paths, part1

class TestParseInput(unittest.TestCase):
    """Test input parsing functionality."""
    
    def test_parse_simple_graph(self):
        """Test parsing a simple device graph."""
        # Create a temporary test file content
        test_content = [
            "you: bbb ccc",
            "bbb: out",
            "ccc: out"
        ]
        
        # Write to a temp file and parse
        with open("test_temp.txt", "w") as f:
            f.write("\n".join(test_content))
        
        graph = parse_input("test_temp.txt")
        
        expected = {
            "you": ["bbb", "ccc"],
            "bbb": ["out"],
            "ccc": ["out"]
        }
        
        self.assertEqual(graph, expected)
        
        # Clean up
        import os
        os.remove("test_temp.txt")
    
    def test_parse_ignores_comments_and_empty_lines(self):
        """Test that parsing ignores comments and empty lines."""
        test_content = [
            "# This is a comment",
            "",
            "you: bbb",
            "# Another comment",
            "bbb: out",
            ""
        ]
        
        with open("test_temp.txt", "w") as f:
            f.write("\n".join(test_content))
        
        graph = parse_input("test_temp.txt")
        
        expected = {
            "you": ["bbb"],
            "bbb": ["out"]
        }
        
        self.assertEqual(graph, expected)
        
        # Clean up
        import os
        os.remove("test_temp.txt")

class TestFindAllPaths(unittest.TestCase):
    """Test path finding functionality."""
    
    def test_single_path(self):
        """Test finding a single path."""
        graph = {
            "you": ["out"]
        }
        
        paths = find_all_paths(graph, "you", "out")
        expected = [["you", "out"]]
        
        self.assertEqual(paths, expected)
    
    def test_multiple_paths(self):
        """Test finding multiple paths."""
        graph = {
            "you": ["a", "b"],
            "a": ["out"],
            "b": ["out"]
        }
        
        paths = find_all_paths(graph, "you", "out")
        
        # Should find 2 paths
        self.assertEqual(len(paths), 2)
        
        # Convert to sets for comparison (order doesn't matter)
        path_sets = [set(path) for path in paths]
        expected_sets = [{"you", "a", "out"}, {"you", "b", "out"}]
        
        for expected_set in expected_sets:
            self.assertIn(expected_set, path_sets)
    
    def test_no_path_exists(self):
        """Test when no path exists."""
        graph = {
            "you": ["a"],
            "a": ["b"],
            "b": ["c"]
        }
        
        paths = find_all_paths(graph, "you", "out")
        
        self.assertEqual(paths, [])
    
    def test_cycle_avoidance(self):
        """Test that cycles are avoided within a single path."""
        graph = {
            "you": ["a"],
            "a": ["b", "you"],  # Creates a cycle back to you
            "b": ["out"]
        }
        
        paths = find_all_paths(graph, "you", "out")
        expected = [["you", "a", "b", "out"]]
        
        self.assertEqual(paths, expected)

class TestExampleInput(unittest.TestCase):
    """Test with the example input file."""
    
    def test_example_file(self):
        """Test that example file produces expected result."""
        try:
            result = part1(parse_input("example.txt"))
            self.assertEqual(result, 5)
        except FileNotFoundError:
            self.skipTest("example.txt not found")

if __name__ == "__main__":
    unittest.main()