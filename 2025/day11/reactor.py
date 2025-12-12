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

def count_paths_with_required_nodes(graph, start, end, required_nodes, visited=None, required_visited=None, memo=None, debug=False, progress_tracker=None):
    """Count paths from start to end that visit all required nodes using memoization."""
    if visited is None:
        visited = set()
    if required_visited is None:
        required_visited = set()
    if memo is None:
        memo = {}
    if progress_tracker is None:
        progress_tracker = {'processed': 0, 'last_report': 0}
    
    # Create a state key for memoization
    state_key = (start, frozenset(visited), frozenset(required_visited))
    if state_key in memo:
        return memo[state_key]
    
    # Progress tracking
    progress_tracker['processed'] += 1
    if progress_tracker['processed'] % 1000 == 0 or progress_tracker['processed'] - progress_tracker['last_report'] >= 1000:
        # Estimate progress based on memo size and complexity
        memo_size = len(memo)
        estimated_total = max(10000, memo_size * 2)  # Rough estimate
        progress_pct = min(99, (memo_size * 100) // estimated_total)
        print(f"Progress: {progress_pct}% ({memo_size} states explored, {progress_tracker['processed']} nodes processed)")
        progress_tracker['last_report'] = progress_tracker['processed']
    
    # Add current node to visited set
    new_visited = visited | {start}
    new_required_visited = required_visited.copy()
    if start in required_nodes:
        new_required_visited.add(start)
    
    if debug and len(new_visited) <= 10:  # Only debug for short paths
        print(f"  At {start}, visited: {sorted(new_visited)}, required: {sorted(new_required_visited)}")
    
    # If we reached the end, check if we visited all required nodes
    if start == end:
        if len(new_required_visited) == len(required_nodes):
            if debug:
                print(f"  Found valid path ending at {start}")
            memo[state_key] = 1
            return 1
        else:
            memo[state_key] = 0
            return 0
    
    # If this device has no outputs, dead end
    if start not in graph:
        memo[state_key] = 0
        return 0
    
    # Early termination if path is getting too long
    if len(new_visited) > 50:
        memo[state_key] = 0
        return 0
    
    total_paths = 0
    for next_device in graph[start]:
        # Avoid cycles by not revisiting nodes
        if next_device not in new_visited:
            paths = count_paths_with_required_nodes(graph, next_device, end, required_nodes, 
                                                  new_visited, new_required_visited, memo, debug, progress_tracker)
            total_paths += paths
    
    memo[state_key] = total_paths
    return total_paths

def part2(data, debug=False):
    """Solve part 2: count paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    if debug:
        print("Graph structure:")
        for device, outputs in data.items():
            print(f"  {device}: {outputs}")
        print()
    
    required_nodes = ['dac', 'fft']
    
    print("Counting paths with memoization...")
    count = count_paths_with_required_nodes(data, 'svr', 'out', required_nodes, debug=debug)
    
    print(f"Found {count} paths from 'svr' to 'out' that visit both 'dac' and 'fft'")
    
    return count

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