#!/usr/bin/env python3
"""
Benchmark script to compare Python vs Prolog implementations
"""
import subprocess
import time
import os
from pathlib import Path

def time_python(day, script, args=""):
    """Time a Python script execution"""
    cmd = f"python {script} {args}"
    start = time.time()
    try:
        result = subprocess.run(cmd, shell=True, cwd=f"day{day:02d}", 
                              capture_output=True, text=True, timeout=30)
        end = time.time()
        if result.returncode == 0:
            return end - start, result.stdout.strip()
        else:
            return None, f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return None, "Timeout (>30s)"

def time_prolog(day, query):
    """Time a Prolog query execution"""
    cmd = f"swipl -g \"{query}, halt.\" -t 'halt(1).' *.pl"
    start = time.time()
    try:
        result = subprocess.run(cmd, shell=True, cwd=f"day{day:02d}",
                              capture_output=True, text=True, timeout=30)
        end = time.time()
        if result.returncode == 0:
            return end - start, result.stdout.strip()
        else:
            return None, f"Error: {result.stderr}"
    except subprocess.TimeoutExpired:
        return None, "Timeout (>30s)"

def benchmark_day04():
    """Benchmark Day 4: Printing Department"""
    print("=== Day 4: Printing Department ===")
    
    # Python
    py_time, py_result = time_python(4, "printing.py example.txt")
    print(f"Python: {py_time:.3f}s - {py_result}")
    
    # Prolog  
    pl_time, pl_result = time_prolog(4, "test_example")
    print(f"Prolog: {pl_time:.3f}s - {pl_result}")
    
    return py_time, pl_time

if __name__ == "__main__":
    os.chdir("2025")
    benchmark_day04()