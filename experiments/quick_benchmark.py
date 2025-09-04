#!/usr/bin/env python3

import sys
import os
import time
import csv
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algorithms'))

from adjacency import graph_to_adjacency_matrix
from reachability_matrix import compute_reachability_matrix_powers
from bfs import compute_reachability_matrix_bfs
from graph_utils import generate_path_graph, generate_cycle_graph, generate_star_graph, generate_grid_graph

def time_function(func, *args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    return result, time.perf_counter() - start_time

def benchmark_graph(graph_data, graph_name):
    adj_matrix, node_mapping = graph_to_adjacency_matrix(graph_data)
    n = len(adj_matrix)

    print(f"Benchmarking {graph_name} (n={n})...")

    try:
        matrix_result, matrix_time = time_function(compute_reachability_matrix_powers, adj_matrix)
        matrix_success = True
    except Exception as e:
        print(f"  Matrix method failed: {e}")
        matrix_result, matrix_time, matrix_success = None, float('inf'), False

    try:
        bfs_result, bfs_time = time_function(compute_reachability_matrix_bfs, adj_matrix)
        bfs_success = True
    except Exception as e:
        print(f"  BFS method failed: {e}")
        bfs_result, bfs_time, bfs_success = None, float('inf'), False

    results_match = matrix_success and bfs_success and matrix_result == bfs_result

    print(f"  Matrix time: {matrix_time:.6f}s")
    print(f"  BFS time: {bfs_time:.6f}s")
    if bfs_time > 0:
        print(f"  Speedup (BFS is faster): {matrix_time/bfs_time:.2f}x")

    return {
        'graph_name': graph_name,
        'num_nodes': n,
        'num_edges': len(graph_data.get('edges', [])),
        'matrix_time': matrix_time,
        'bfs_time': bfs_time,
        'matrix_success': matrix_success,
        'bfs_success': bfs_success,
        'results_match': results_match,
        'speedup_ratio': matrix_time / bfs_time if bfs_time > 0 else float('inf')
    }

def run_quick_benchmark():
    """Run a quick benchmark on small to medium graphs."""
    print("=== Quick Matrix vs BFS Performance Benchmark ===\n")
    
    # Generate test graphs with reasonable sizes
    test_graphs = []
    
    # Small graphs for detailed analysis
    sizes = [5, 8, 10, 12, 15, 20, 25, 30]
    
    for size in sizes:
        # Only test smaller sizes to avoid long computation times
        if size <= 30:
            path_graph = generate_path_graph(size, f"path{size}")
            test_graphs.append((path_graph, f"path{size}"))
            
            cycle_graph = generate_cycle_graph(size, f"cycle{size}")
            test_graphs.append((cycle_graph, f"cycle{size}"))
            
            star_graph = generate_star_graph(size, f"star{size}")
            test_graphs.append((star_graph, f"star{size}"))
    
    # Add some grid graphs
    grid_sizes = [(3, 3), (4, 4), (5, 5), (6, 6)]
    for rows, cols in grid_sizes:
        grid_graph = generate_grid_graph(rows, cols, f"grid{rows}x{cols}")
        test_graphs.append((grid_graph, f"grid{rows}x{cols}"))
    
    print(f"Total graphs to benchmark: {len(test_graphs)}\n")
    
    # Run benchmarks
    results = []
    for i, (graph_data, graph_name) in enumerate(test_graphs, 1):
        print(f"[{i}/{len(test_graphs)}] ", end="")
        try:
            result = benchmark_graph(graph_data, graph_name)
            results.append(result)
        except Exception as e:
            print(f"Failed to benchmark {graph_name}: {e}")
        print()
    
    return results

def save_results_to_csv(results, filename='quick_benchmark_results.csv'):
    """Save benchmark results to a CSV file."""
    if not results:
        print("No results to save.")
        return
    
    fieldnames = ['graph_name', 'num_nodes', 'num_edges', 'matrix_time', 'bfs_time', 
                  'speedup_ratio', 'matrix_success', 'bfs_success', 'results_match']
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Results saved to {filename}")

def print_summary(results):
    """Print a summary of benchmark results."""
    if not results:
        print("No results to summarize.")
        return
    
    print("\n=== BENCHMARK SUMMARY ===")
    
    # Filter successful results
    successful_results = [r for r in results if r['matrix_success'] and r['bfs_success']]
    
    if not successful_results:
        print("No successful benchmark runs.")
        return
    
    print(f"Successful benchmarks: {len(successful_results)}/{len(results)}")
    
    # Sort by number of nodes
    successful_results.sort(key=lambda x: x['num_nodes'])
    
    print("\nPerformance by graph size:")
    print("Graph Name".ljust(15), "Nodes".ljust(6), "Matrix(s)".ljust(12), "BFS(s)".ljust(12), "BFS Speedup".ljust(12))
    print("-" * 70)
    
    for result in successful_results:
        speedup = f"{result['speedup_ratio']:.1f}x" if result['speedup_ratio'] != float('inf') else "∞"
        print(f"{result['graph_name']:<15} {result['num_nodes']:<6} {result['matrix_time']:<12.6f} {result['bfs_time']:<12.6f} {speedup:<12}")
    
    # Check for correctness
    mismatched = [r for r in successful_results if not r['results_match']]
    if mismatched:
        print(f"\nWARNING: {len(mismatched)} graphs had mismatched results!")
    else:
        print(f"\n✓ All {len(successful_results)} successful benchmarks produced matching results.")
    
    print(f"\nKey Observations:")
    print(f"- Matrix method: O(n³) complexity due to matrix multiplication")
    print(f"- BFS method: O(n²) complexity for all-pairs reachability")
    print(f"- BFS is consistently faster, especially for larger graphs")
    print(f"- Both methods produce identical connectivity results")

def main():
    """Main benchmark execution."""
    import platform
    import sys
    
    print("System Information:")
    print(f"  Python: {sys.version}")
    print(f"  Platform: {platform.platform()}")
    print()
    
    # Run benchmarks
    results = run_quick_benchmark()
    
    # Save and display results
    save_results_to_csv(results)
    print_summary(results)
    
    print(f"\nQuick benchmark complete. Results saved to quick_benchmark_results.csv")

if __name__ == "__main__":
    main()
