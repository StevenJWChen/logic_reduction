# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the `logic_reduction` project - a Python tool for finding minimal test case sets to achieve 100% code coverage of if/else statements. The tool solves the Set Cover problem to reduce potentially thousands of test cases to a minimal set that still covers all branches.

## Core Architecture

### Main Components
- `logic_parser.py` - Parses source files to extract if/else conditions and branches
- `coverage_analyzer.py` - Generates test cases and analyzes coverage 
- `test_reducer.py` - Implements multiple reduction algorithms (greedy, heuristic, intelligent, optimal)
- `main.py` - Command-line interface and orchestration

### Key Data Structures
- `Condition` - Represents a single boolean condition (variable, operator, value)
- `Branch` - Represents a code branch with associated conditions
- `TestCase` - Test case with variable values and covered branches
- `ReductionResult` - Algorithm results with metrics

## Common Commands

### Basic Usage
```bash
# Analyze a Python file
python main.py -f program.py

# Use custom variable domains
python main.py -f program.py --domains domains.json

# Compare all algorithms
python main.py -f program.py --compare-all

# Save results to JSON
python main.py -f program.py --output results.json
```

### Algorithm Options
- `--algorithm greedy` - Fast greedy algorithm
- `--algorithm heuristic` - Greedy + local optimization  
- `--algorithm intelligent` - Efficiency-based selection (default)
- `--algorithm optimal` - Exhaustive search (small problems only)

## Project Permissions

Claude Code has been configured with specific permissions in `.claude/settings.local.json`:
- Allowed: `Bash(find:*)` - Permission to use find commands for file discovery
- Allowed: `Bash(python:*)` - Permission to run Python commands

## Development Notes

The parser currently supports Python AST parsing with regex fallback for other languages. The reduction algorithms solve the NP-hard Set Cover problem using various heuristics, with the optimal algorithm limited to small problem sizes.