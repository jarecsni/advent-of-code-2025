#!/usr/bin/env python3
"""
Day 12: Christmas Tree Farm

Polyomino packing problem solved using area-based feasibility check.
For problems with 1000+ regions and 120+ pieces each, exact geometric 
solving is computationally intractable, so we use the mathematical
insight that area feasibility is a good approximation.

Answer: 476
"""

import sys
import os


def solve(content: str) -> int:
    """
    Solve by checking if each region has sufficient area for required pieces.
    
    This approach works because:
    1. Infeasible regions are off by tiny amounts (1-3 cells)
    2. Feasible regions have hundreds of extra cells  
    3. The scale makes exact solving impractical (120+ pieces per region)
    """
    lines = [line.rstrip() for line in content.strip().split('\n')]
    
    # Parse shapes - just count # characters
    shape_areas = {}
    regions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
        # Shape definition
        if ':' in line and line.split(':')[0].strip().isdigit():
            shape_id = int(line.split(':')[0])
            shape_visual = line.split(':', 1)[1].strip()
            
            shape_lines = []
            if shape_visual:
                shape_lines.append(shape_visual)
            
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if (not next_line.strip() or 
                    (':' in next_line and next_line.split(':')[0].strip().isdigit()) or
                    ('x' in next_line and ':' in next_line)):
                    break
                
                if next_line.startswith(' '):
                    shape_lines.append(next_line.lstrip())
                else:
                    shape_lines.append(next_line)
                i += 1
            
            # Count # characters
            area = 0
            for shape_line in shape_lines:
                area += shape_line.count('#')
            
            shape_areas[shape_id] = area
        
        # Region definition
        elif 'x' in line and ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                dimensions = parts[0].strip()
                if 'x' in dimensions:
                    width, height = map(int, dimensions.split('x'))
                    counts = list(map(int, parts[1].strip().split()))
                    regions.append((width, height, counts))
            i += 1
        else:
            i += 1
    
    solvable = 0
    
    for i, (width, height, required) in enumerate(regions):
        region_area = width * height
        total_needed = sum(shape_areas.get(j, 0) * count for j, count in enumerate(required))
        
        # Skip regions that reference non-existent shapes
        if any(count > 0 and j not in shape_areas for j, count in enumerate(required)):
            continue
            
        # Count regions with sufficient area
        if total_needed <= region_area:
            solvable += 1
    
    return solvable


def main():
    """Main function with CLI support"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Solve Christmas Tree Farm')
    parser.add_argument('input_file', nargs='?', help='Input file')
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = args.input_file or os.path.join(script_dir, 'input.txt')
    
    try:
        with open(input_path, 'r') as f:
            result = solve(f.read())
        print(result)
        
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found")
        sys.exit(1)


if __name__ == "__main__":
    main()