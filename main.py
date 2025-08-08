#!/usr/bin/env python3
"""
Logic Reduction Main Program

This program analyzes source code files with if/else statements and finds
the minimal set of test cases needed to achieve 100% branch coverage.
"""

import argparse
import sys
import json
from pathlib import Path
from logic_parser import LogicParser
from coverage_analyzer import CoverageAnalyzer
from test_reducer import TestReducer


def main():
    parser = argparse.ArgumentParser(
        description="Reduce test cases for 100% logic coverage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -f program.py
  python main.py -f code.c --domains domains.json
  python main.py -f script.js --algorithm greedy
  python main.py -f program.py --compare-all
        """
    )
    
    parser.add_argument('-f', '--file', required=True,
                       help='Source file to analyze')
    parser.add_argument('--domains', 
                       help='JSON file specifying variable domains')
    parser.add_argument('--algorithm', 
                       choices=['greedy', 'heuristic', 'intelligent', 'optimal'],
                       default='intelligent',
                       help='Reduction algorithm to use (default: intelligent)')
    parser.add_argument('--compare-all', action='store_true',
                       help='Compare all available algorithms')
    parser.add_argument('--output', 
                       help='Output file for results (JSON format)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not Path(args.file).exists():
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    try:
        # Parse the source file
        print(f"Analyzing file: {args.file}")
        parser = LogicParser()
        branches = parser.parse_file(args.file)
        
        if not branches:
            print("No if/else branches found in the file")
            sys.exit(1)
        
        print(f"Found {len(branches)} branches")
        print(f"Found {len(parser.variables)} variables: {sorted(parser.variables)}")
        
        if args.verbose:
            print("\nBranches found:")
            for i, branch in enumerate(branches, 1):
                print(f"  {i}. {branch}")
        
        # Load variable domains if provided
        domains = None
        if args.domains:
            try:
                with open(args.domains, 'r') as f:
                    domains = json.load(f)
                print(f"Loaded variable domains from {args.domains}")
            except Exception as e:
                print(f"Warning: Could not load domains file: {e}")
        
        # Analyze coverage
        print("\nGenerating test cases...")
        analyzer = CoverageAnalyzer(branches, parser.variables)
        
        if domains:
            test_cases = analyzer.generate_all_test_cases(domains)
        else:
            test_cases = analyzer.generate_smart_test_cases()
        
        if not test_cases:
            print("No test cases could be generated")
            sys.exit(1)
        
        print(f"Generated {len(test_cases)} test cases")
        
        if args.verbose:
            analyzer.print_coverage_report()
        
        # Reduce test cases
        reducer = TestReducer(analyzer)
        
        if args.compare_all:
            print(f"\nComparing all reduction algorithms...")
            results = reducer.compare_algorithms()
            
            print(f"\nComparison Results:")
            print("-" * 80)
            for result in results:
                print(result)
                print("-" * 80)
            
            # Find best result
            best_result = min(results, key=lambda r: r.reduction_ratio)
            print(f"\nBest Algorithm: {best_result.algorithm_used}")
            
        else:
            print(f"\nReducing test cases using {args.algorithm} algorithm...")
            
            if args.algorithm == 'greedy':
                result = reducer.reduce_greedy()
            elif args.algorithm == 'heuristic':
                result = reducer.reduce_heuristic()
            elif args.algorithm == 'intelligent':
                result = reducer.reduce_intelligent()
            elif args.algorithm == 'optimal':
                result = reducer.reduce_optimal_small()
                if result is None:
                    print("Optimal algorithm failed (problem too large), falling back to intelligent")
                    result = reducer.reduce_intelligent()
            
            print(f"\n{result}")
            best_result = result
        
        # Show final test cases
        print(f"\nMinimal Test Set ({len(best_result.minimal_test_cases)} test cases):")
        print("=" * 60)
        for i, test_case in enumerate(best_result.minimal_test_cases, 1):
            print(f"Test {i}: {dict(test_case.values)}")
            if args.verbose:
                print(f"    Covers: {sorted(test_case.covered_branches)}")
        
        # Save results if requested
        if args.output:
            output_data = {
                'file': args.file,
                'algorithm': best_result.algorithm_used,
                'original_test_count': len(test_cases),
                'reduced_test_count': len(best_result.minimal_test_cases),
                'coverage_percentage': best_result.coverage_percentage,
                'reduction_percentage': (1 - best_result.reduction_ratio) * 100,
                'execution_time': best_result.execution_time,
                'test_cases': [
                    {
                        'values': dict(tc.values),
                        'covered_branches': list(tc.covered_branches)
                    }
                    for tc in best_result.minimal_test_cases
                ],
                'branches': [
                    {
                        'id': branch.branch_id,
                        'conditions': [
                            {
                                'variable': c.variable,
                                'operator': c.operator,
                                'value': c.value
                            }
                            for c in branch.conditions
                        ]
                    }
                    for branch in branches
                ]
            }
            
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"\nResults saved to {args.output}")
    
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()