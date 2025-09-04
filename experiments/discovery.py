#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'algorithms'))

from adjacency import graph_to_adjacency_matrix
from reachability_matrix import demonstrate_connectivity_discovery, compare_reachability_methods

def run_discovery_on_small_graphs():
    print("=== MATRIX CONNECTIVITY DISCOVERY EXPERIMENTS ===\n")

    graphs_dir = Path(__file__).parent.parent / 'graphs'
    small_graphs = ['path10.json', 'cycle10.json']

    for graph_file in small_graphs:
        filepath = graphs_dir / graph_file
        if not filepath.exists():
            print(f"Graph file {graph_file} not found, skipping...")
            continue

        print(f"{'='*60}")
        print(f"ANALYZING: {graph_file}")
        print(f"{'='*60}")

        try:
            with open(filepath, 'r') as f:
                graph_data = json.load(f)

            adj_matrix, node_mapping = graph_to_adjacency_matrix(graph_data)
            results = demonstrate_connectivity_discovery(adj_matrix, verbose=True)
            comparison = compare_reachability_methods(adj_matrix)

            print(f"\nMethod Comparison:")
            print(f"  Matrix and BFS methods agree: {comparison['methods_agree']}")
            if not comparison['methods_agree']:
                print(f"  Differences found: {comparison['differences']}")

            print(f"\nKey Insights for {graph_data.get('name', 'Unknown')}:")
            print(f"  - Graph has {len(adj_matrix)} nodes")
            print(f"  - Connectivity ratio: {results['connectivity_ratio']:.2%}")
            print(f"  - Strongly connected: {results['is_strongly_connected']}")

        except Exception as e:
            print(f"Error analyzing {graph_file}: {e}")

        print("\n" + "="*60 + "\n")

def demonstrate_walk_counting():
    """
    Demonstrate how matrix powers count walks of specific lengths.
    """
    print("=== WALK COUNTING DEMONSTRATION ===\n")
    
    # Create a simple 4-node path: 0-1-2-3
    simple_path = {
        'name': 'simple_path_4',
        'nodes': [
            {'id': 0, 'x': 100, 'y': 300},
            {'id': 1, 'x': 200, 'y': 300},
            {'id': 2, 'x': 300, 'y': 300},
            {'id': 3, 'x': 400, 'y': 300}
        ],
        'edges': [
            {'from': 0, 'to': 1},
            {'from': 1, 'to': 2},
            {'from': 2, 'to': 3}
        ]
    }
    
    adj_matrix, _ = graph_to_adjacency_matrix(simple_path)
    
    print("Simple 4-node path: 0-1-2-3")
    print("This will clearly show how matrix powers count walks.\n")
    
    # Demonstrate the discovery
    results = demonstrate_connectivity_discovery(adj_matrix, verbose=True)
    
    print("\nWalk Interpretation:")
    print("- A^1[i][j] = number of 1-step walks from node i to node j")
    print("- A^2[i][j] = number of 2-step walks from node i to node j")
    print("- A^3[i][j] = number of 3-step walks from node i to node j")
    print("- etc.")
    print("\nReachability Matrix = Boolean OR of A^1, A^2, ..., A^(n-1)")
    print("This tells us which nodes can reach which other nodes via ANY path.")

def analyze_connectivity_patterns():
    """
    Analyze different connectivity patterns in various graph types.
    """
    print("\n=== CONNECTIVITY PATTERN ANALYSIS ===\n")
    
    graphs_dir = Path(__file__).parent.parent / 'graphs'
    all_graphs = ['path10.json', 'cycle10.json', 'star21.json']
    
    connectivity_summary = []
    
    for graph_file in all_graphs:
        filepath = graphs_dir / graph_file
        if not filepath.exists():
            continue
            
        try:
            with open(filepath, 'r') as f:
                graph_data = json.load(f)
            
            adj_matrix, _ = graph_to_adjacency_matrix(graph_data)
            results = demonstrate_connectivity_discovery(adj_matrix, verbose=False)
            
            connectivity_summary.append({
                'name': graph_data.get('name', graph_file.stem),
                'type': graph_file.replace('.json', '').rstrip('0123456789'),
                'nodes': len(adj_matrix),
                'edges': len(graph_data.get('edges', [])),
                'connectivity_ratio': results['connectivity_ratio'],
                'strongly_connected': results['is_strongly_connected']
            })
            
        except Exception as e:
            print(f"Error analyzing {graph_file}: {e}")
    
    print("Connectivity Summary:")
    print("Graph Type".ljust(12), "Nodes".ljust(6), "Edges".ljust(6), "Connectivity".ljust(12), "Strongly Connected")
    print("-" * 60)
    
    for summary in connectivity_summary:
        connected_str = "Yes" if summary['strongly_connected'] else "No"
        print(f"{summary['type']:<12} {summary['nodes']:<6} {summary['edges']:<6} {summary['connectivity_ratio']:<12.2%} {connected_str}")
    
    print(f"\nObservations:")
    print(f"- Path graphs: Not strongly connected (can't go backwards)")
    print(f"- Cycle graphs: Strongly connected (can reach any node from any other)")
    print(f"- Star graphs: Not strongly connected (leaves can't reach each other directly)")

def main():
    """Main discovery experiment execution."""
    print("Matrix Connectivity Discovery Experiments")
    print("This script demonstrates how matrix multiplication reveals graph connectivity.\n")
    
    # Run experiments
    demonstrate_walk_counting()
    run_discovery_on_small_graphs()
    analyze_connectivity_patterns()
    
    print("\n=== DISCOVERY SUMMARY ===")
    print("KEY FINDING: Matrix powers A^k count the number of walks of length k between nodes.")
    print("CONNECTIVITY INSIGHT: The Boolean OR of A^1, A^2, ..., A^(n-1) gives the reachability matrix.")
    print("PRACTICAL MEANING: If R[i][j] = 1, then node j is reachable from node i via some path.")
    print("\nThis algebraic approach provides the same connectivity information as graph traversal")
    print("algorithms like BFS, but reveals the mathematical structure underlying connectivity.")

if __name__ == "__main__":
    main()
