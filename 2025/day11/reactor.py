"""
Day 11: Reactor - Find all paths through electrical devices
"""
import argparse

def parse_input(filename):
    """Parse device connections into a directed graph."""
    graph = {}
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if ': ' not in line:
                continue
                
            device, outputs = line.split(': ')
            connections = outputs.split()
            graph[device] = connections
    
    return graph

def find_all_paths(graph, start, end, path=None, debug=False):
    """Find all paths from start to end using DFS."""
    if path is None:
        path = []
    
    path = path + [start]
    
    if debug:
        print(f"  Exploring: {' -> '.join(path)}")
    
    # If we reached the end, return this path
    if start == end:
        if debug:
            print(f"  Found path: {' -> '.join(path)}")
        return [path]
    
    # If this device has no outputs, dead end
    if start not in graph:
        if debug:
            print(f"  Dead end at {start}")
        return []
    
    paths = []
    for next_device in graph[start]:
        # Avoid cycles by not revisiting nodes in current path
        if next_device not in path:
            new_paths = find_all_paths(graph, next_device, end, path, debug)
            paths.extend(new_paths)
        elif debug:
            print(f"  Skipping {next_device} (already in path)")
    
    return paths

def part1(data, debug=False):
    """Solve part 1: count all paths from 'you' to 'out'."""
    if debug:
        print("Graph structure:")
        for device, outputs in data.items():
            print(f"  {device}: {outputs}")
        print()
    
    paths = find_all_paths(data, 'you', 'out', debug=debug)
    
    if debug or len(paths) <= 20:  # Show paths if debugging or reasonable number
        print(f"Found {len(paths)} paths from 'you' to 'out':")
        for i, path in enumerate(paths, 1):
            print(f"  Path {i}: {' -> '.join(path)}")
    else:
        print(f"Found {len(paths)} paths from 'you' to 'out' (too many to display)")
    
    return len(paths)

def find_paths_with_required_nodes(graph, start, end, required_nodes, path=None, debug=False, max_paths=None):
    """Find all paths from start to end that visit all required nodes."""
    if path is None:
        path = []
    
    path = path + [start]
    
    # Early termination if path is getting too long (likely indicates cycles or inefficient graph)
    if len(path) > 50:
        if debug:
            print(f"  Path too long, terminating: {' -> '.join(path[:5])}...{' -> '.join(path[-5:])}")
        return []
    
    if debug:
        print(f"  Exploring: {' -> '.join(path)}")
    
    # If we reached the end, check if we visited all required nodes
    if start == end:
        visited_required = set(required_nodes) & set(path)
        if len(visited_required) == len(required_nodes):
            if debug:
                print(f"  Found valid path: {' -> '.join(path)} (visits {visited_required})")
            return [path]
        else:
            if debug:
                missing = set(required_nodes) - visited_required
                print(f"  Path reaches end but missing: {missing}")
            return []
    
    # If this device has no outputs, dead end
    if start not in graph:
        if debug:
            print(f"  Dead end at {start}")
        return []
    
    paths = []
    for next_device in graph[start]:
        # Avoid cycles by not revisiting nodes in current path
        if next_device not in path:
            new_paths = find_paths_with_required_nodes(graph, next_device, end, required_nodes, path, debug, max_paths)
            paths.extend(new_paths)
            
            # Early termination if we've found enough paths
            if max_paths and len(paths) >= max_paths:
                if debug:
                    print(f"  Reached max paths limit ({max_paths}), stopping search")
                break
        elif debug:
            print(f"  Skipping {next_device} (already in path)")
    
    return paths

def part2(data, debug=False):
    """Solve part 2: count paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    if debug:
        print("Graph structure:")
        for device, outputs in data.items():
            print(f"  {device}: {outputs}")
        print()
    
    required_nodes = ['dac', 'fft']
    
    # For large inputs, we might need to limit the search
    # Try with a reasonable limit first
    print("Searching for paths (this may take a while for large inputs)...")
    max_search_paths = 100000  # Reasonable limit to prevent infinite search
    paths = find_paths_with_required_nodes(data, 'svr', 'out', required_nodes, debug=debug, max_paths=max_search_paths)
    
    if debug or len(paths) <= 20:  # Show paths if debugging or reasonable number
        print(f"Found {len(paths)} paths from 'svr' to 'out' that visit both 'dac' and 'fft':")
        for i, path in enumerate(paths, 1):
            # Highlight the required nodes in the path
            path_str = ' -> '.join(path)
            for node in required_nodes:
                if node in path:
                    path_str = path_str.replace(node, f"[{node}]")
            print(f"  Path {i}: {path_str}")
    else:
        print(f"Found {len(paths)} paths from 'svr' to 'out' that visit both 'dac' and 'fft' (too many to display)")
    
    return len(paths)

def main():
    parser = argparse.ArgumentParser(description="Day 11: Reactor - Find all paths through electrical device network")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("part", type=int, nargs="?", default=1, 
                        choices=[1, 2], help="Puzzle part (1 or 2, default: 1)")
    parser.add_argument("-d", "--debug", action="store_true", 
                        help="Print debug information")
    args = parser.parse_args()
    
    data = parse_input(args.input_file)
    
    if args.part == 1:
        result = part1(data, debug=args.debug)
        print(f"Part 1: {result}")
    else:
        result = part2(data, debug=args.debug)
        print(f"Part 2: {result}")

if __name__ == "__main__":
    main()