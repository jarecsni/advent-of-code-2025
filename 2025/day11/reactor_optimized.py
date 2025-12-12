"""
Day 11: Reactor - Optimized solution for path counting
"""
import argparse
from functools import lru_cache

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

def count_paths_simple(graph, start, end, memo=None):
    """Count paths from start to end using simple memoization."""
    if memo is None:
        memo = {}
    
    if (start, end) in memo:
        return memo[(start, end)]
    
    if start == end:
        return 1
    
    if start not in graph:
        return 0
    
    total = 0
    for next_node in graph[start]:
        total += count_paths_simple(graph, next_node, end, memo)
    
    memo[(start, end)] = total
    return total

def part1(data, debug=False):
    """Solve part 1: count all paths from 'you' to 'out'."""
    count = count_paths_simple(data, 'you', 'out')
    
    if debug:
        print(f"Found {count} paths from 'you' to 'out'")
    
    return count

def part2(data, debug=False):
    """
    Solve part 2 using the key insight: split into segments and multiply.
    
    The insight is that we need paths svr -> out that visit both fft and dac.
    Since the graph is a DAG, either fft comes before dac or dac comes before fft.
    We can split this into segments and multiply the counts.
    """
    
    # Check which direction exists: fft->dac or dac->fft
    fft_to_dac = count_paths_simple(data, 'fft', 'dac')
    dac_to_fft = count_paths_simple(data, 'dac', 'fft')
    
    if debug:
        print(f"Paths fft->dac: {fft_to_dac}")
        print(f"Paths dac->fft: {dac_to_fft}")
    
    total_paths = 0
    
    # Case 1: svr -> fft -> dac -> out
    if fft_to_dac > 0:
        svr_to_fft = count_paths_simple(data, 'svr', 'fft')
        fft_to_dac_count = count_paths_simple(data, 'fft', 'dac')
        dac_to_out = count_paths_simple(data, 'dac', 'out')
        
        paths_via_fft_dac = svr_to_fft * fft_to_dac_count * dac_to_out
        total_paths += paths_via_fft_dac
        
        if debug:
            print(f"svr->fft: {svr_to_fft}, fft->dac: {fft_to_dac_count}, dac->out: {dac_to_out}")
            print(f"Paths via fft->dac: {paths_via_fft_dac}")
    
    # Case 2: svr -> dac -> fft -> out  
    if dac_to_fft > 0:
        svr_to_dac = count_paths_simple(data, 'svr', 'dac')
        dac_to_fft_count = count_paths_simple(data, 'dac', 'fft')
        fft_to_out = count_paths_simple(data, 'fft', 'out')
        
        paths_via_dac_fft = svr_to_dac * dac_to_fft_count * fft_to_out
        total_paths += paths_via_dac_fft
        
        if debug:
            print(f"svr->dac: {svr_to_dac}, dac->fft: {dac_to_fft_count}, fft->out: {fft_to_out}")
            print(f"Paths via dac->fft: {paths_via_dac_fft}")
    
    if debug:
        print(f"Total paths: {total_paths}")
    
    return total_paths

def main():
    parser = argparse.ArgumentParser(description="Day 11: Reactor - Optimized path counting")
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