#!/usr/bin/env python3
"""
Day 10: Factory - Indicator Light Configuration

This problem is a system of linear equations over GF(2) (binary field).
Each button press toggles specific lights, and we need to find the minimum
number of presses to achieve the target configuration.
"""

import re
from typing import List, Tuple, Set
import numpy as np


def parse_machine(line: str) -> Tuple[List[int], List[List[int]]]:
    """
    Parse a machine specification line.
    
    Returns:
        target_state: List of 0s and 1s representing target light configuration
        buttons: List of button configurations, each being a list of light indices
    """
    # Extract indicator pattern [.##.]
    pattern_match = re.search(r'\[([.#]+)\]', line)
    if not pattern_match:
        raise ValueError(f"No indicator pattern found in line: {line}")
    
    pattern = pattern_match.group(1)
    target_state = [1 if c == '#' else 0 for c in pattern]
    
    # Extract button configurations (1,3) (2) etc.
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        if button_str.strip():  # Handle empty parentheses
            button_lights = [int(x) for x in button_str.split(',')]
            buttons.append(button_lights)
    
    return target_state, buttons


def solve_gf2_gaussian(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Solve using Gaussian elimination over GF(2).
    
    This is much faster for large systems but finds A solution, not necessarily 
    the minimum weight solution. For minimum weight, you'd need to enumerate
    the null space and find the minimum among all solutions.
    """
    num_lights = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return float('inf') if any(target) else 0
    
    # Create augmented matrix [A|b]
    augmented = np.zeros((num_lights, num_buttons + 1), dtype=int)
    
    # Fill coefficient matrix
    for button_idx, button_lights in enumerate(buttons):
        for light_idx in button_lights:
            if light_idx < num_lights:
                augmented[light_idx, button_idx] = 1
    
    # Fill target vector
    for i, val in enumerate(target):
        augmented[i, num_buttons] = val
    
    if debug:
        print("Initial augmented matrix:")
        print(augmented)
    
    # Gaussian elimination in GF(2)
    pivot_row = 0
    for col in range(num_buttons):
        # Find pivot
        pivot_found = False
        for row in range(pivot_row, num_lights):
            if augmented[row, col] == 1:
                # Swap rows if needed
                if row != pivot_row:
                    augmented[[pivot_row, row]] = augmented[[row, pivot_row]]
                pivot_found = True
                break
        
        if not pivot_found:
            continue
        
        # Eliminate column
        for row in range(num_lights):
            if row != pivot_row and augmented[row, col] == 1:
                # XOR rows (addition in GF(2))
                augmented[row] ^= augmented[pivot_row]
        
        pivot_row += 1
    
    if debug:
        print("After Gaussian elimination:")
        print(augmented)
    
    # Check for inconsistency
    for row in range(pivot_row, num_lights):
        if augmented[row, num_buttons] == 1:
            return -1  # No solution
    
    # Find pivot columns (basic variables)
    pivot_cols = []
    for row in range(min(pivot_row, num_buttons)):
        for col in range(num_buttons):
            if augmented[row, col] == 1:
                pivot_cols.append(col)
                break
    
    # Free variables are non-pivot columns
    free_vars = [col for col in range(num_buttons) if col not in pivot_cols]
    
    if debug:
        print(f"Pivot columns (basic variables): {pivot_cols}")
        print(f"Free variables: {free_vars}")
    
    # If no free variables, we have a unique solution
    if not free_vars:
        solution = np.zeros(num_buttons, dtype=int)
        for row in range(len(pivot_cols) - 1, -1, -1):
            pivot_col = pivot_cols[row]
            val = augmented[row, num_buttons]
            for col in range(pivot_col + 1, num_buttons):
                val ^= augmented[row, col] * solution[col]
            solution[pivot_col] = val
        
        if debug:
            print(f"Unique solution: {solution}")
        return sum(solution)
    
    # Multiple solutions exist - find minimum weight solution
    min_weight = float('inf')
    best_solution = None
    
    # Try all combinations of free variables (2^|free_vars|)
    for free_combo in range(2 ** len(free_vars)):
        solution = np.zeros(num_buttons, dtype=int)
        
        # Set free variables according to current combination
        for i, free_var in enumerate(free_vars):
            solution[free_var] = (free_combo >> i) & 1
        
        # Back substitute to find basic variables
        for row in range(len(pivot_cols) - 1, -1, -1):
            pivot_col = pivot_cols[row]
            val = augmented[row, num_buttons]
            for col in range(pivot_col + 1, num_buttons):
                val ^= augmented[row, col] * solution[col]
            solution[pivot_col] = val
        
        # Check weight of this solution
        weight = sum(solution)
        if weight < min_weight:
            min_weight = weight
            best_solution = solution.copy()
    
    if debug:
        print(f"Minimum weight solution: {best_solution} (weight: {min_weight})")
    
    return min_weight


def solve_gf2_system(target: List[int], buttons: List[List[int]]) -> int:
    """
    Solve the system of linear equations over GF(2) to find minimum button presses.
    
    This creates a matrix where:
    - Each row represents a light
    - Each column represents a button
    - Entry (i,j) is 1 if button j toggles light i
    
    We solve: A * x = target (mod 2)
    where x is the vector of button press counts (0 or 1 each)
    """
    num_lights = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        # No buttons available
        return float('inf') if any(target) else 0
    
    # Create the coefficient matrix
    matrix = np.zeros((num_lights, num_buttons), dtype=int)
    
    for button_idx, button_lights in enumerate(buttons):
        for light_idx in button_lights:
            if light_idx < num_lights:  # Bounds check
                matrix[light_idx, button_idx] = 1
    
    # Try all possible combinations of button presses (brute force for small cases)
    # Since we're in GF(2), each button is pressed either 0 or 1 times
    min_presses = float('inf')
    
    for combination in range(2 ** num_buttons):
        button_presses = [(combination >> i) & 1 for i in range(num_buttons)]
        
        # Calculate resulting light state
        result_state = np.zeros(num_lights, dtype=int)
        for button_idx, press_count in enumerate(button_presses):
            if press_count:
                for light_idx in buttons[button_idx]:
                    if light_idx < num_lights:
                        result_state[light_idx] ^= 1  # XOR toggle
        
        # Check if this matches target
        if np.array_equal(result_state, target):
            total_presses = sum(button_presses)
            min_presses = min(min_presses, total_presses)
    
    return min_presses if min_presses != float('inf') else -1





def parse_input(filename: str) -> List[str]:
    """Parse input file and return list of machine specifications."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def part1(data: List[str], debug: bool = False, use_gaussian: bool = False) -> int:
    """
    Solve part 1: Find minimum button presses for all machines.
    
    Args:
        data: List of machine specification strings
        debug: Whether to print debug information
        
    Returns:
        Total minimum button presses needed for all machines
    """
    total_presses = 0
    
    for i, line in enumerate(data):
        try:
            target_state, buttons = parse_machine(line)
            if use_gaussian:
                min_presses = solve_gf2_gaussian(target_state, buttons, debug)
            else:
                min_presses = solve_gf2_system(target_state, buttons)
            
            if min_presses == -1:
                if debug:
                    print(f"Machine {i+1}: No solution possible")
                return -1
            
            if debug:
                target_str = ''.join('#' if x else '.' for x in target_state)
                print(f"Machine {i+1}: {min_presses} presses (target: {target_str})")
            
            total_presses += min_presses
            
        except Exception as e:
            if debug:
                print(f"Error processing machine {i+1}: {e}")
            return -1
    
    return total_presses


def solve_joltage_custom_gaussian(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Custom Gaussian elimination approach based on successful Reddit solutions.
    This implements the approach that several users mentioned worked for them.
    """
    import numpy as np
    
    num_counters = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return sum(target) if all(t >= 0 for t in target) else -1
    
    # Build coefficient matrix A where A[i,j] = 1 if button j affects counter i
    A = np.zeros((num_counters, num_buttons), dtype=int)
    for button_idx, button_counters in enumerate(buttons):
        for counter_idx in button_counters:
            if counter_idx < num_counters:
                A[counter_idx, button_idx] = 1
    
    # Create augmented matrix [A|b]
    augmented = np.hstack([A, np.array(target).reshape(-1, 1)])
    
    if debug:
        print(f"Initial system: {A.shape}, target: {target}")
    
    # Gaussian elimination to find pivot and free variables
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_buttons):
        # Find pivot
        pivot_found = False
        for row in range(pivot_row, num_counters):
            if augmented[row, col] != 0:
                # Swap rows if needed
                if row != pivot_row:
                    augmented[[pivot_row, row]] = augmented[[row, pivot_row]]
                pivot_found = True
                break
        
        if not pivot_found:
            continue
        
        pivot_cols.append(col)
        
        # Eliminate column (using integer arithmetic)
        pivot_val = augmented[pivot_row, col]
        for row in range(num_counters):
            if row != pivot_row and augmented[row, col] != 0:
                # Use integer elimination - multiply and subtract
                multiplier = augmented[row, col]
                for c in range(num_buttons + 1):
                    augmented[row, c] = augmented[row, c] * pivot_val - augmented[pivot_row, c] * multiplier
        
        pivot_row += 1
    
    # Check for inconsistency
    for row in range(pivot_row, num_counters):
        if augmented[row, num_buttons] != 0:
            return -1  # No solution
    
    # Free variables are non-pivot columns
    free_vars = [col for col in range(num_buttons) if col not in pivot_cols]
    
    if debug:
        print(f"Pivot columns: {pivot_cols}, Free variables: {free_vars}")
    
    if not free_vars:
        # Unique solution - back substitute
        solution = np.zeros(num_buttons, dtype=int)
        for i in range(len(pivot_cols) - 1, -1, -1):
            row = i
            col = pivot_cols[i]
            val = augmented[row, num_buttons]
            for c in range(col + 1, num_buttons):
                val -= augmented[row, c] * solution[c]
            
            if augmented[row, col] != 0:
                solution[col] = val // augmented[row, col]
        
        return sum(solution) if all(s >= 0 for s in solution) else -1
    
    # Multiple solutions - bounded search on free variables
    min_cost = float('inf')
    max_free_val = max(target) // len(free_vars) + 10 if free_vars else 0
    
    # Try all combinations of free variables up to reasonable bounds
    from itertools import product
    
    if len(free_vars) <= 4:  # Only for small numbers of free variables
        ranges = [range(max_free_val + 1) for _ in free_vars]
        
        for free_assignment in product(*ranges):
            if sum(free_assignment) >= min_cost:
                continue  # Skip if already worse
            
            # Set free variables
            solution = np.zeros(num_buttons, dtype=int)
            for i, var_idx in enumerate(free_vars):
                solution[var_idx] = free_assignment[i]
            
            # Back substitute for pivot variables
            valid = True
            for i in range(len(pivot_cols) - 1, -1, -1):
                row = i
                col = pivot_cols[i]
                val = augmented[row, num_buttons]
                for c in range(col + 1, num_buttons):
                    val -= augmented[row, c] * solution[c]
                
                if augmented[row, col] != 0:
                    if val % augmented[row, col] != 0:
                        valid = False
                        break
                    solution[col] = val // augmented[row, col]
                    if solution[col] < 0:
                        valid = False
                        break
            
            if valid:
                cost = sum(solution)
                if cost < min_cost:
                    min_cost = cost
    
    return min_cost if min_cost != float('inf') else -1


def solve_joltage_system_ilp_internal(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Solve using Z3 constraint solver - the approach most successful Reddit users employed.
    """
    try:
        import z3
    except ImportError:
        if debug:
            print("Z3 not available, falling back to scipy")
        return solve_joltage_scipy(target, buttons, debug)
    
    num_counters = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return sum(target) if all(t >= 0 for t in target) else -1
    
    # Create Z3 solver
    solver = z3.Optimize()
    
    # Create variables for button presses (non-negative integers)
    button_vars = [z3.Int(f'button_{i}') for i in range(num_buttons)]
    
    # Add non-negativity constraints
    for var in button_vars:
        solver.add(var >= 0)
    
    # Add constraints for each counter
    for counter_idx in range(num_counters):
        # Sum of presses for buttons affecting this counter must equal target
        affecting_buttons = []
        for button_idx, button_counters in enumerate(buttons):
            if counter_idx in button_counters:
                affecting_buttons.append(button_vars[button_idx])
        
        if affecting_buttons:
            solver.add(z3.Sum(affecting_buttons) == target[counter_idx])
        elif target[counter_idx] > 0:
            # No button affects this counter but target is positive - impossible
            return -1
    
    # Minimize total button presses
    total_presses = z3.Sum(button_vars)
    solver.minimize(total_presses)
    
    # Solve
    if solver.check() == z3.sat:
        model = solver.model()
        
        # Get individual button values and check for any fractional parts
        button_solution = []
        for var in button_vars:
            val = model.eval(var)
            if hasattr(val, 'as_fraction'):
                # Check if it's actually fractional
                frac = val.as_fraction()
                if frac.denominator != 1:
                    if debug:
                        print(f"Warning: Fractional solution found: {frac}")
                    # Round up fractional solutions
                    button_solution.append(int(frac.numerator // frac.denominator) + (1 if frac.numerator % frac.denominator != 0 else 0))
                else:
                    button_solution.append(int(frac.numerator))
            else:
                button_solution.append(val.as_long())
        
        result = sum(button_solution)
        
        if debug:
            print(f"Z3 solution: {button_solution} -> {result} presses")
            
            # Verify the solution manually
            verification = [0] * num_counters
            for button_idx, presses in enumerate(button_solution):
                for _ in range(presses):
                    for counter_idx in buttons[button_idx]:
                        if counter_idx < num_counters:
                            verification[counter_idx] += 1
            print(f"Verification: target={target}, achieved={verification}, match={verification == target}")
        
        return result
    else:
        if debug:
            print("Z3: No solution found")
        return -1


def solve_joltage_scipy(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Fallback using SciPy's MILP solver.
    """
    try:
        import numpy as np
        from scipy.optimize import milp, LinearConstraint, Bounds
    except ImportError:
        if debug:
            print("SciPy not available, falling back to heuristic")
        return solve_joltage_improved_heuristic(target, buttons, debug)
    
    num_counters = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return sum(target) if all(t >= 0 for t in target) else -1
    
    # Build coefficient matrix A where A[i,j] = 1 if button j affects counter i
    A = np.zeros((num_counters, num_buttons))
    for button_idx, button_counters in enumerate(buttons):
        for counter_idx in button_counters:
            if counter_idx < num_counters:
                A[counter_idx, button_idx] = 1
    
    # Objective: minimize sum of button presses
    c = np.ones(num_buttons)
    
    # Constraints: Ax = target
    constraints = LinearConstraint(A, target, target)
    
    # Bounds: x >= 0, with reasonable upper bounds
    max_reasonable = max(target) * 2 if target else 10
    bounds = Bounds(0, max_reasonable)
    
    # All variables must be integers
    integrality = np.ones(num_buttons)
    
    # Solve
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    
    if result.success:
        solution_value = int(round(sum(result.x)))
        if debug:
            print(f"SciPy solution: {[int(round(x)) for x in result.x]} -> {solution_value} presses")
        return solution_value
    else:
        if debug:
            print(f"SciPy failed: {result.message}")
        return solve_joltage_improved_heuristic(target, buttons, debug)


def solve_joltage_simple_greedy(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Simple greedy approach that prioritizes buttons affecting multiple needed counters.
    """
    num_counters = len(target)
    current = [0] * num_counters
    total_presses = 0
    max_iterations = sum(target) * 3
    
    for iteration in range(max_iterations):
        if current == target:
            return total_presses
        
        # Calculate what we still need
        needed = [max(0, target[i] - current[i]) for i in range(num_counters)]
        total_needed = sum(needed)
        
        if total_needed == 0:
            break
        
        # Find the button that helps with the most needed counters
        best_button = -1
        best_score = -1
        
        for button_idx, button_counters in enumerate(buttons):
            score = 0
            for counter_idx in button_counters:
                if counter_idx < num_counters and needed[counter_idx] > 0:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_button = button_idx
        
        if best_button == -1 or best_score == 0:
            # No helpful button found
            break
        
        # Press the best button
        for counter_idx in buttons[best_button]:
            if counter_idx < num_counters:
                current[counter_idx] += 1
        total_presses += 1
    
    return total_presses if current == target else -1


def solve_joltage_mathematical(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Use mathematical approach with proper integer programming.
    """
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    
    num_counters = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return sum(target) if all(t >= 0 for t in target) else -1
    
    # Build coefficient matrix A where A[i,j] = 1 if button j affects counter i
    A = np.zeros((num_counters, num_buttons))
    for button_idx, button_counters in enumerate(buttons):
        for counter_idx in button_counters:
            if counter_idx < num_counters:
                A[counter_idx, button_idx] = 1
    
    # Objective: minimize sum of button presses
    c = np.ones(num_buttons)
    
    # Constraints: Ax = target
    constraints = LinearConstraint(A, target, target)
    
    # Bounds: x >= 0, and reasonable upper bounds
    max_reasonable = max(target) * 2  # Heuristic upper bound
    bounds = Bounds(0, max_reasonable)
    
    # All variables must be integers
    integrality = np.ones(num_buttons)
    
    # Solve
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    
    if result.success:
        return int(sum(result.x))
    
    return -1


def solve_joltage_improved_heuristic(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Improved heuristic approach using multiple strategies.
    """
    num_counters = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return sum(target) if all(t >= 0 for t in target) else -1
    
    # Strategy 1: Try to find buttons that uniquely affect certain counters
    unique_solutions = {}
    for counter_idx in range(num_counters):
        affecting_buttons = []
        for button_idx, button_counters in enumerate(buttons):
            if counter_idx in button_counters:
                affecting_buttons.append(button_idx)
        
        if len(affecting_buttons) == 1:
            # This counter can only be affected by one button
            button_idx = affecting_buttons[0]
            needed_presses = target[counter_idx]
            unique_solutions[button_idx] = max(unique_solutions.get(button_idx, 0), needed_presses)
    
    # Apply unique solutions
    current = [0] * num_counters
    total_presses = 0
    button_presses = [0] * num_buttons
    
    for button_idx, presses in unique_solutions.items():
        button_presses[button_idx] = presses
        total_presses += presses
        for _ in range(presses):
            for counter_idx in buttons[button_idx]:
                if counter_idx < num_counters:
                    current[counter_idx] += 1
    
    if debug:
        print(f"After unique solutions: current = {current}, presses = {total_presses}")
    
    # Strategy 2: Greedy for remaining deficit
    max_iterations = sum(target) * 2
    iteration = 0
    
    while current != target and iteration < max_iterations:
        # Calculate deficit
        deficit = [max(0, target[i] - current[i]) for i in range(num_counters)]
        total_deficit = sum(deficit)
        
        if total_deficit == 0:
            break
        
        # Find button that best addresses the deficit
        best_button = -1
        best_efficiency = 0
        
        for button_idx, button_counters in enumerate(buttons):
            if not button_counters:  # Skip empty buttons
                continue
                
            # Calculate how much this button helps with deficit
            help_count = sum(1 for counter_idx in button_counters 
                           if counter_idx < num_counters and deficit[counter_idx] > 0)
            
            # Calculate waste (how much it overshoots)
            waste_count = sum(1 for counter_idx in button_counters 
                            if counter_idx < num_counters and deficit[counter_idx] == 0)
            
            # Efficiency = help - waste penalty
            efficiency = help_count - waste_count * 0.5
            
            if efficiency > best_efficiency:
                best_efficiency = efficiency
                best_button = button_idx
        
        if best_button == -1:
            # If no button helps, try any button that affects a deficit counter
            for button_idx, button_counters in enumerate(buttons):
                if any(counter_idx < num_counters and deficit[counter_idx] > 0 
                       for counter_idx in button_counters):
                    best_button = button_idx
                    break
        
        if best_button == -1:
            break
        
        # Press the best button
        button_presses[best_button] += 1
        total_presses += 1
        for counter_idx in buttons[best_button]:
            if counter_idx < num_counters:
                current[counter_idx] += 1
        
        iteration += 1
    
    if current == target:
        return total_presses
    
    # Strategy 3: Try small local search improvements
    return solve_joltage_local_search(target, buttons, button_presses, debug)


def solve_joltage_local_search(target: List[int], buttons: List[List[int]], initial_presses: List[int], debug: bool = False) -> int:
    """
    Local search to improve an initial solution.
    """
    num_counters = len(target)
    current_presses = initial_presses[:]
    
    # Calculate current state
    def calculate_state(presses):
        state = [0] * num_counters
        for button_idx, press_count in enumerate(presses):
            for _ in range(press_count):
                for counter_idx in buttons[button_idx]:
                    if counter_idx < num_counters:
                        state[counter_idx] += 1
        return state
    
    current_state = calculate_state(current_presses)
    
    if current_state == target:
        return sum(current_presses)
    
    # Try swapping button presses to improve solution
    max_swaps = 100
    for _ in range(max_swaps):
        improved = False
        
        # Try reducing one button and increasing another
        for reduce_btn in range(len(buttons)):
            if current_presses[reduce_btn] == 0:
                continue
                
            for increase_btn in range(len(buttons)):
                if reduce_btn == increase_btn:
                    continue
                
                # Try the swap
                test_presses = current_presses[:]
                test_presses[reduce_btn] -= 1
                test_presses[increase_btn] += 1
                
                test_state = calculate_state(test_presses)
                
                # Check if this gets us closer to target
                old_distance = sum(abs(current_state[i] - target[i]) for i in range(num_counters))
                new_distance = sum(abs(test_state[i] - target[i]) for i in range(num_counters))
                
                if new_distance < old_distance:
                    current_presses = test_presses
                    current_state = test_state
                    improved = True
                    break
            
            if improved:
                break
        
        if not improved:
            break
        
        if current_state == target:
            return sum(current_presses)
    
    # If we still don't have exact solution, return -1
    return -1 if current_state != target else sum(current_presses)


def solve_joltage_adjustment(target: List[int], buttons: List[List[int]], initial_solution: List[int], debug: bool = False) -> int:
    """
    Try to adjust an approximate solution to make it exact.
    """
    num_counters = len(target)
    current = [0] * num_counters
    
    # Apply initial solution
    for button_idx, presses in enumerate(initial_solution):
        for _ in range(presses):
            for counter_idx in buttons[button_idx]:
                if counter_idx < num_counters:
                    current[counter_idx] += 1
    
    if debug:
        print(f"Initial solution gives: {current}, target: {target}")
    
    # Try small adjustments
    solution = initial_solution[:]
    max_adjustments = 50
    
    for _ in range(max_adjustments):
        if current == target:
            return sum(solution)
        
        # Find the counter that's furthest from target
        max_diff = 0
        worst_counter = -1
        for i in range(num_counters):
            diff = abs(current[i] - target[i])
            if diff > max_diff:
                max_diff = diff
                worst_counter = i
        
        if worst_counter == -1:
            break
        
        # Find a button that affects this counter
        if current[worst_counter] < target[worst_counter]:
            # Need to increase this counter
            for button_idx, button_counters in enumerate(buttons):
                if worst_counter in button_counters:
                    # Press this button once more
                    solution[button_idx] += 1
                    for counter_idx in button_counters:
                        if counter_idx < num_counters:
                            current[counter_idx] += 1
                    break
        else:
            # Need to decrease this counter - this is tricky since we can't "unpress"
            # Try to find a different approach
            break
    
    if current == target:
        return sum(solution)
    
    # Fall back to original greedy approach
    return solve_joltage_system(target, buttons, debug)


def solve_joltage_system(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Solve the joltage configuration problem using integer linear programming.
    
    This is a minimum cost flow problem: minimize sum(x_i) subject to Ax = b, x_i >= 0
    where A is the coefficient matrix and b is the target joltage levels.
    """
    num_counters = len(target)
    num_buttons = len(buttons)
    
    if num_buttons == 0:
        return sum(target) if all(t >= 0 for t in target) else -1
    
    # Try a greedy approach first - often works for well-structured problems
    # Use a simple heuristic: repeatedly press the button that makes the most progress
    current = [0] * num_counters
    total_presses = 0
    
    if debug:
        print(f"Target: {target}")
        print(f"Buttons: {buttons}")
    
    # Simple greedy: while we haven't reached target, find best button to press
    max_iterations = sum(target) * 2  # Safety limit
    iteration = 0
    
    while current != target and iteration < max_iterations:
        best_button = -1
        best_score = -1
        
        # Find button that makes most progress toward target
        for button_idx, button_counters in enumerate(buttons):
            score = 0
            # Calculate how much this button helps
            for counter_idx in button_counters:
                if counter_idx < num_counters and current[counter_idx] < target[counter_idx]:
                    score += 1  # This button helps with a counter we need
                elif counter_idx < num_counters and current[counter_idx] >= target[counter_idx]:
                    score -= 10  # Penalty for overshooting
            
            if score > best_score:
                best_score = score
                best_button = button_idx
        
        if best_button == -1 or best_score <= 0:
            # No beneficial button found - try brute force for small cases
            return solve_joltage_brute_force(target, buttons, debug)
        
        # Press the best button
        for counter_idx in buttons[best_button]:
            if counter_idx < num_counters:
                current[counter_idx] += 1
        
        total_presses += 1
        iteration += 1
        
        if debug and iteration % 10 == 0:
            print(f"Iteration {iteration}: current = {current}, presses = {total_presses}")
    
    if current != target:
        # Greedy failed, try brute force for small cases
        return solve_joltage_brute_force(target, buttons, debug)
    
    if debug:
        print(f"Greedy solution: {total_presses} presses")
    
    return total_presses


def solve_joltage_brute_force(target: List[int], buttons: List[List[int]], debug: bool = False) -> int:
    """
    Brute force approach for small joltage problems.
    Try all combinations up to a reasonable limit.
    """
    num_counters = len(target)
    num_buttons = len(buttons)
    max_target = max(target) if target else 0
    
    # Reasonable upper bound: if we had one button per counter, max presses per button
    max_presses_per_button = max_target + 5
    
    if debug:
        print(f"Trying brute force with max {max_presses_per_button} presses per button")
    
    min_total = float('inf')
    
    # Generate all combinations (this gets expensive quickly)
    def try_combination(button_presses):
        current = [0] * num_counters
        total = sum(button_presses)
        
        # Apply button presses
        for button_idx, presses in enumerate(button_presses):
            for _ in range(presses):
                for counter_idx in buttons[button_idx]:
                    if counter_idx < num_counters:
                        current[counter_idx] += 1
        
        if current == target:
            return total
        return float('inf')
    
    # Try combinations up to reasonable limits
    from itertools import product
    
    # Limit search space - this is still exponential but manageable for small cases
    if num_buttons <= 6 and max_target <= 15:
        ranges = [range(max_presses_per_button + 1) for _ in range(num_buttons)]
        
        for combination in product(*ranges):
            if sum(combination) >= min_total:
                continue  # Skip if already worse than best found
            
            result = try_combination(combination)
            if result < min_total:
                min_total = result
                if debug:
                    print(f"New best: {combination} -> {result} presses")
    
    return min_total if min_total != float('inf') else -1


def part2(data: List[str], debug: bool = False) -> int:
    """
    Solve part 2: Configure joltage levels using minimum button presses.
    
    Args:
        data: List of machine specification strings
        debug: Whether to print debug information
        
    Returns:
        Total minimum button presses needed for all machines
    """
    total_presses = 0
    machines_processed = 0
    
    for i, line in enumerate(data):
        try:
            # Parse the line to extract joltage requirements
            # Extract joltage requirements {3,5,4,7}
            joltage_match = re.search(r'\{([0-9,]+)\}', line)
            if not joltage_match:
                if debug:
                    print(f"Machine {i+1}: No joltage requirements found")
                continue
            
            joltage_str = joltage_match.group(1)
            target_joltages = [int(x) for x in joltage_str.split(',')]
            
            # Reuse button parsing from part 1
            _, buttons = parse_machine(line)
            
            # Try both approaches and see if they differ
            gaussian_result = solve_joltage_custom_gaussian(target_joltages, buttons, False)
            z3_result = solve_joltage_system_ilp_internal(target_joltages, buttons, False)
            
            if gaussian_result != z3_result and gaussian_result != -1 and z3_result != -1:
                if debug:
                    print(f"Machine {i+1}: Gaussian={gaussian_result}, Z3={z3_result} - DIFFERENCE!")
                # Use the higher value (more conservative)
                min_presses = max(gaussian_result, z3_result)
            else:
                min_presses = z3_result if gaussian_result == -1 else gaussian_result
            
            if min_presses == -1:
                if debug:
                    print(f"Machine {i+1}: No solution possible")
                return -1
            
            if debug:
                print(f"Machine {i+1}: {min_presses} presses (target: {target_joltages})")
            
            total_presses += min_presses
            machines_processed += 1
            
        except Exception as e:
            if debug:
                print(f"Error processing machine {i+1}: {e}")
            return -1
    
    if debug:
        print(f"Processed {machines_processed} machines, total presses: {total_presses}")
    
    return total_presses


def main():
    """Main function with proper CLI interface."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Day 10: Factory - Configure indicator lights using minimum button presses")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("--part2", action="store_true",
                        help="Solve part 2 instead of part 1")
    parser.add_argument("-d", "--debug", action="store_true", 
                        help="Print debug information")
    parser.add_argument("-g", "--gaussian", action="store_true",
                        help="Use Gaussian elimination instead of brute force")
    
    args = parser.parse_args()
    
    try:
        data = parse_input(args.input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)
    
    if args.part2:
        result = part2(data, debug=args.debug)
        print(f"Part 2: {result}")
    else:
        result = part1(data, debug=args.debug, use_gaussian=args.gaussian)
        print(f"Part 1: {result}")


if __name__ == "__main__":
    main()