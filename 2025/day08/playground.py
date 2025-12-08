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


def solve_part2(filename):
    """
    Connect junction boxes until all are in one circuit. Return the product
    of the X coordinates of the last two boxes connected.
    
    Args:
        filename: Input file with junction box coordinates
    
    Returns:
        Product of X coordinates of last connection
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
    
    # Process edges until we have one circuit
    uf = UnionFind(n)
    uf.num_components = n  # Track number of components
    last_connection = None
    
    for dist, i, j in edges:
        if uf.union(i, j):
            last_connection = (i, j)
            uf.num_components -= 1
            
            # Stop when all boxes are in one circuit
            if uf.num_components == 1:
                break
    
    # Get X coordinates and multiply
    box_i, box_j = last_connection
    x1 = boxes[box_i][0]
    x2 = boxes[box_j][0]
    return x1 * x2


def _generate_sorted_edges(boxes):
    """Helper to generate and sort all edges."""
    edges = []
    for i, j in combinations(range(len(boxes)), 2):
        dist = calculate_distance(boxes[i], boxes[j])
        edges.append((dist, i, j))
    edges.sort()
    return edges


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python playground.py <input_file> [num_edges] [-d|--debug] [--part2]")
        print("Example: python playground.py example.txt 10")
        print("Example: python playground.py input.txt 1000 --debug")
        print("Example: python playground.py input.txt --part2")
        sys.exit(1)
    
    filename = sys.argv[1]
    debug = "-d" in sys.argv or "--debug" in sys.argv
    part2 = "--part2" in sys.argv
    num_edges = 1000
    for arg in sys.argv[2:]:
        if arg not in ["-d", "--debug", "--part2"]:
            num_edges = int(arg)
            break
    
    try:
        boxes = parse_input(filename)
        n = len(boxes)
        edges = _generate_sorted_edges(boxes)
        
        if part2:
            # Part 2: Connect until one circuit
            uf = UnionFind(n)
            num_components = n
            last_connection = None
            
            for edge_idx, (dist, i, j) in enumerate(edges):
                if uf.union(i, j):
                    last_connection = (i, j, dist)
                    num_components -= 1
                    if num_components == 1:
                        break
            
            box_i, box_j, dist = last_connection
            x1, x2 = boxes[box_i][0], boxes[box_j][0]
            result = x1 * x2
            
            print(f"Last connection: box{box_i} {boxes[box_i]} <-> box{box_j} {boxes[box_j]}")
            print(f"X coordinates: {x1}, {x2}")
            print(f"Result: {x1} × {x2} = {result}")
        else:
            # Part 1: Process fixed number of edges
            uf = UnionFind(n)
            for edge_idx in range(min(num_edges, len(edges))):
                _, i, j = edges[edge_idx]
                uf.union(i, j)
            
            sizes = uf.get_component_sizes()
            result = sizes[0] * sizes[1] * sizes[2]
            
            print(f"Total boxes: {n}")
            print(f"Circuits remaining: {len(sizes)}")
            print(f"Three largest: {sizes[0]}, {sizes[1]}, {sizes[2]}")
            print(f"Result: {sizes[0]} × {sizes[1]} × {sizes[2]} = {result}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
