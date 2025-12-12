"""
Tests for Day 11: Reactor
"""
import unittest
from reactor import parse_input, find_all_paths, part1, count_paths_with_required_nodes, part2

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

class TestRequiredNodePaths(unittest.TestCase):
    """Test path finding with required nodes."""
    
    def test_paths_with_required_nodes(self):
        """Test finding paths that visit specific required nodes."""
        graph = {
            "start": ["a", "b"],
            "a": ["req1"],
            "b": ["req2"],
            "req1": ["c"],
            "req2": ["c"],
            "c": ["end"]
        }
        
        # Should find no paths since no single path visits both req1 and req2
        count = count_paths_with_required_nodes(graph, "start", "end", ["req1", "req2"])
        self.assertEqual(count, 0)
        
        # Should find paths that visit req1
        count = count_paths_with_required_nodes(graph, "start", "end", ["req1"])
        self.assertEqual(count, 1)
    
    def test_paths_with_both_required_nodes(self):
        """Test finding paths that visit both required nodes."""
        graph = {
            "start": ["a"],
            "a": ["req1"],
            "req1": ["req2"],
            "req2": ["end"]
        }
        
        count = count_paths_with_required_nodes(graph, "start", "end", ["req1", "req2"])
        self.assertEqual(count, 1)

class TestExampleInput(unittest.TestCase):
    """Test with the example input files."""
    
    def test_example_file_part1(self):
        """Test that example file produces expected result for part 1."""
        try:
            result = part1(parse_input("2025/day11/example.txt"))
            self.assertEqual(result, 5)
        except FileNotFoundError:
            self.skipTest("example.txt not found")
    
    def test_example_file_part2(self):
        """Test that example2 file produces expected result for part 2."""
        try:
            result = part2(parse_input("2025/day11/example2.txt"))
            self.assertEqual(result, 2)
        except FileNotFoundError:
            self.skipTest("example2.txt not found")

if __name__ == "__main__":
    unittest.main()