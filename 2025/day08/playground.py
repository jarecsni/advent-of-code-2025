"""Day 8: Playground - Junction box circuit connection problem."""
import math
from itertools import combinations
from pathlib import Path


def parse_input(filename):
    """Parse junction box coordinates from input file."""
    filepath = Path(__file__).parent / filename
    boxes = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                boxes.append((x, y, z))
    return boxes


def calculate_distance(box1, box2):
    """Calculate Euclidean distance between two 3D points."""
    return math.sqrt(
        (box1[0] - box2[0]) ** 2 +
        (box1[1] - box2[1]) ** 2 +
        (box1[2] - box2[2]) ** 2
    )


class UnionFind:
    """Union-Find data structure for tracking connected components."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        """Find root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union two sets. Returns True if they were different sets."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by size
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        
        return True
    
    def get_component_sizes(self):
        """Get sizes of all connected components."""
        components = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in components:
                components[root] = 0
            components[root] += 1
        return sorted(components.values(), reverse=True)


def solve_part1(filename, num_edges=1000):
    """
    Process the first num_edges shortest edges, connecting junction boxes
    that aren't already in the same circuit. Return the product of the
    three largest circuit sizes.
    
    Args:
        filename: Input file with junction box coordinates
        num_edges: Number of edges to process from sorted list
    
    Returns:
        Product of three largest circuit sizes
    """
    boxes = parse_input(filename)
    n = len(boxes)
    
    # Generate all edges with distances
    edges = []
    for i, j in combinations(range(n), 2):
        dist = calculate_distance(boxes[i], boxes[j])
        edges.append((dist, i, j))
    
    # Sort by distance
    edges.sort()
    
    # Process first num_edges edges using Union-Find
    uf = UnionFind(n)
    for edge_idx in range(min(num_edges, len(edges))):
        _, i, j = edges[edge_idx]
        uf.union(i, j)
    
    # Get circuit sizes and calculate result
    sizes = uf.get_component_sizes()
    return sizes[0] * sizes[1] * sizes[2]


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python playground.py <input_file> [num_edges] [-d|--debug]")
        print("Example: python playground.py example.txt 10")
        print("Example: python playground.py input.txt 1000 --debug")
        sys.exit(1)
    
    filename = sys.argv[1]
    debug = "-d" in sys.argv or "--debug" in sys.argv
    
    # Parse num_edges (skip debug flags)
    num_edges = 1000
    for arg in sys.argv[2:]:
        if arg not in ["-d", "--debug"]:
            num_edges = int(arg)
            break
    
    try:
        boxes = parse_input(filename)
        n = len(boxes)
        
        if debug:
            print(f"Parsed {n} boxes")
            print(f"First 3 boxes: {boxes[:3]}")
            print()
        
        # Generate and sort edges
        if debug:
            print("Generating all possible edges...")
        edges = []
        for i, j in combinations(range(n), 2):
            dist = calculate_distance(boxes[i], boxes[j])
            edges.append((dist, i, j))
        
        if debug:
            print(f"Generated {len(edges)} edges")
            print(f"Sorting edges by distance...")
        edges.sort()
        
        if debug:
            print(f"Shortest 5 edges:")
            for idx in range(min(5, len(edges))):
                dist, i, j = edges[idx]
                print(f"  {idx+1}. Distance {dist:.2f}: box{i} <-> box{j}")
            print()
        
        # Process edges
        if debug:
            print(f"Processing first {num_edges} edges...")
        uf = UnionFind(n)
        connections_made = 0
        skipped = 0
        
        for edge_idx in range(min(num_edges, len(edges))):
            dist, i, j = edges[edge_idx]
            if uf.union(i, j):
                connections_made += 1
                if debug and edge_idx < 10:
                    print(f"  Edge {edge_idx+1}: Connected box{i} <-> box{j} (dist {dist:.2f})")
            else:
                skipped += 1
                if debug and edge_idx < 10:
                    print(f"  Edge {edge_idx+1}: Skipped box{i} <-> box{j} (already connected)")
        
        if debug:
            print(f"\nConnections made: {connections_made}")
            print(f"Edges skipped: {skipped}")
            print()
        
        # Get sizes and result
        sizes = uf.get_component_sizes()
        result = sizes[0] * sizes[1] * sizes[2]
        
        print(f"Total boxes: {n}")
        print(f"Edges processed: {min(num_edges, len(edges))}")
        print(f"Circuits remaining: {len(sizes)}")
        print(f"Three largest circuits: {sizes[0]}, {sizes[1]}, {sizes[2]}")
        if debug and len(sizes) > 3:
            print(f"All circuit sizes: {sizes}")
        print(f"\nResult: {sizes[0]} × {sizes[1]} × {sizes[2]} = {result}")
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
