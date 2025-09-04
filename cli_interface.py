#!/usr/bin/env python3

import sys
import os
import json
from pathlib import Path

sys.path.append('algorithms')
sys.path.append('experiments')

from adjacency import graph_to_adjacency_matrix, load_graph_from_file
from reachability_matrix import demonstrate_connectivity_discovery, compare_reachability_methods
from bfs import compute_reachability_matrix_bfs
from graph_utils import generate_path_graph, generate_cycle_graph, generate_star_graph, generate_grid_graph
import time

class MatrixConnectivityCLI:
    def __init__(self):
        self.current_graph = None
        self.current_adj_matrix = None
        self.current_node_mapping = None
    
    def run(self):
        print("=== Matrix Connectivity Investigation CLI ===")
        print("Discover how matrix multiplication reveals graph connectivity")
        
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.load_graph()
            elif choice == '2':
                self.generate_sample_graph()
            elif choice == '3':
                self.show_graph_info()
            elif choice == '4':
                self.run_discovery_experiment()
            elif choice == '5':
                self.run_performance_benchmark()
            elif choice == '6':
                self.compare_methods()
            elif choice == '7':
                self.export_graph()
            elif choice == '8':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def show_menu(self):
        print("\n" + "="*50)
        print("MAIN MENU")
        print("="*50)
        print("1. Load graph from file")
        print("2. Generate sample graph")
        print("3. Show graph information")
        print("4. Run discovery experiment")
        print("5. Run performance benchmark")
        print("6. Compare matrix vs BFS methods")
        print("7. Export current graph")
        print("8. Exit")
        
        if self.current_graph:
            nodes = len(self.current_graph.get('nodes', []))
            edges = len(self.current_graph.get('edges', []))
            print(f"\nCurrent graph: {nodes} nodes, {edges} edges")
    
    def load_graph(self):
        print("\nAvailable graphs:")
        graphs_dir = Path('graphs')
        if graphs_dir.exists():
            graph_files = list(graphs_dir.glob('*.json'))
            for i, file in enumerate(graph_files, 1):
                print(f"  {i}. {file.name}")
            
            try:
                choice = int(input(f"Select graph (1-{len(graph_files)}): "))
                if 1 <= choice <= len(graph_files):
                    filename = graph_files[choice - 1]
                    self.current_adj_matrix, self.current_node_mapping, self.current_graph = load_graph_from_file(filename)
                    print(f"Loaded {filename.name} successfully!")
                else:
                    print("Invalid selection.")
            except (ValueError, FileNotFoundError) as e:
                print(f"Error loading graph: {e}")
        else:
            print("No graphs directory found.")
    
    def generate_sample_graph(self):
        print("\nSample graph types:")
        print("1. Path graph")
        print("2. Cycle graph") 
        print("3. Star graph")
        print("4. Grid graph")
        
        try:
            choice = int(input("Select type (1-4): "))
            size = int(input("Enter size: "))
            
            if choice == 1:
                self.current_graph = generate_path_graph(size)
            elif choice == 2:
                self.current_graph = generate_cycle_graph(size)
            elif choice == 3:
                self.current_graph = generate_star_graph(size)
            elif choice == 4:
                rows = int(input("Enter rows: "))
                cols = int(input("Enter columns: "))
                self.current_graph = generate_grid_graph(rows, cols)
            else:
                print("Invalid choice.")
                return
            
            self.current_adj_matrix, self.current_node_mapping = graph_to_adjacency_matrix(self.current_graph)
            print("Sample graph generated successfully!")
            
        except ValueError:
            print("Invalid input. Please enter numbers only.")
    
    def show_graph_info(self):
        if not self.current_graph:
            print("No graph loaded. Please load or generate a graph first.")
            return
        
        nodes = self.current_graph.get('nodes', [])
        edges = self.current_graph.get('edges', [])
        
        print(f"\nGraph Information:")
        print(f"  Name: {self.current_graph.get('name', 'Unknown')}")
        print(f"  Nodes: {len(nodes)}")
        print(f"  Edges: {len(edges)}")
        
        if self.current_adj_matrix:
            from bfs import is_connected
            connected = is_connected(self.current_adj_matrix)
            print(f"  Connected: {connected}")
            
            if len(self.current_adj_matrix) <= 10:
                print(f"\nAdjacency Matrix:")
                for row in self.current_adj_matrix:
                    print("  " + " ".join(f"{x:2}" for x in row))
    
    def run_discovery_experiment(self):
        if not self.current_adj_matrix:
            print("No graph loaded. Please load or generate a graph first.")
            return
        
        print("\n" + "="*60)
        print("DISCOVERY EXPERIMENT: Matrix Powers and Connectivity")
        print("="*60)
        
        results = demonstrate_connectivity_discovery(self.current_adj_matrix, verbose=True)
        comparison = compare_reachability_methods(self.current_adj_matrix)
        
        print(f"\nKEY DISCOVERY:")
        print(f"Matrix powers A^k count walks of length k between nodes.")
        print(f"Boolean OR of A^1, A^2, ..., A^(n-1) gives reachability matrix.")
        print(f"\nVerification:")
        print(f"  Matrix and BFS methods agree: {comparison['methods_agree']}")
        print(f"  Connectivity ratio: {results['connectivity_ratio']:.2%}")
    
    def run_performance_benchmark(self):
        if not self.current_adj_matrix:
            print("No graph loaded. Please load or generate a graph first.")
            return
        
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARK: Matrix vs BFS")
        print("="*60)
        
        from reachability_matrix import compute_reachability_matrix_powers
        
        print(f"Graph size: {len(self.current_adj_matrix)} nodes")
        
        start_time = time.perf_counter()
        matrix_result = compute_reachability_matrix_powers(self.current_adj_matrix)
        matrix_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        bfs_result = compute_reachability_matrix_bfs(self.current_adj_matrix)
        bfs_time = time.perf_counter() - start_time
        
        speedup = matrix_time / bfs_time if bfs_time > 0 else float('inf')
        
        print(f"\nResults:")
        print(f"  Matrix method: {matrix_time:.6f} seconds")
        print(f"  BFS method: {bfs_time:.6f} seconds")
        print(f"  BFS speedup: {speedup:.1f}x")
        print(f"  Results match: {matrix_result == bfs_result}")
        print(f"\nComplexity Analysis:")
        print(f"  Matrix method: O(n⁴) - computes A^1 through A^(n-1)")
        print(f"  BFS method: O(n²) - BFS from each node")
    
    def compare_methods(self):
        if not self.current_adj_matrix:
            print("No graph loaded. Please load or generate a graph first.")
            return
        
        comparison = compare_reachability_methods(self.current_adj_matrix)
        
        print(f"\nMethod Comparison:")
        print(f"  Methods produce identical results: {comparison['methods_agree']}")
        if not comparison['methods_agree']:
            print(f"  Differences found: {comparison['differences']}")
        
        print(f"\nMathematical Equivalence:")
        print(f"  Both methods compute the same reachability information")
        print(f"  Matrix method reveals the mathematical structure")
        print(f"  BFS method is computationally more efficient")
    
    def export_graph(self):
        if not self.current_graph:
            print("No graph loaded. Please load or generate a graph first.")
            return
        
        filename = input("Enter filename (without .json): ").strip()
        if filename:
            filepath = f"{filename}.json"
            try:
                with open(filepath, 'w') as f:
                    json.dump(self.current_graph, f, indent=2)
                print(f"Graph exported to {filepath}")
            except Exception as e:
                print(f"Export failed: {e}")

def main():
    cli = MatrixConnectivityCLI()
    cli.run()

if __name__ == "__main__":
    main()
