#!/usr/bin/env python3

import http.server
import socketserver
import os
import webbrowser
import json
import sys
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs

sys.path.append(str(Path(__file__).parent.parent / 'algorithms'))
sys.path.append(str(Path(__file__).parent.parent / 'experiments'))

from adjacency import graph_to_adjacency_matrix
from reachability_matrix import demonstrate_connectivity_discovery, compare_reachability_methods
from bfs import compute_reachability_matrix_bfs
from multiply import matrix_multiply

class MatrixConnectivityHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/discovery':
            self.handle_discovery()
        elif self.path == '/api/benchmark':
            self.handle_benchmark()
        else:
            self.send_error(404)

    def handle_discovery(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        graph_data = json.loads(post_data.decode('utf-8'))

        try:
            adj_matrix, node_mapping = graph_to_adjacency_matrix(graph_data)
            results = demonstrate_connectivity_discovery(adj_matrix, verbose=False)
            comparison = compare_reachability_methods(adj_matrix)

            response_data = {
                'success': True,
                'results': {
                    'connectivity_ratio': results['connectivity_ratio'],
                    'is_strongly_connected': results['is_strongly_connected'],
                    'connected_pairs': results['connected_pairs'],
                    'total_pairs': results['total_pairs'],
                    'methods_agree': comparison['methods_agree'],
                    'matrix_powers': {str(k): v for k, v in results['matrix_powers'].items()},
                    'reachability_matrix': results['reachability_matrix']
                }
            }
        except Exception as e:
            response_data = {'success': False, 'error': str(e)}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def handle_benchmark(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        graph_data = json.loads(post_data.decode('utf-8'))

        try:
            adj_matrix, node_mapping = graph_to_adjacency_matrix(graph_data)

            start_time = time.perf_counter()
            from reachability_matrix import compute_reachability_matrix_powers
            matrix_result = compute_reachability_matrix_powers(adj_matrix)
            matrix_time = time.perf_counter() - start_time

            start_time = time.perf_counter()
            bfs_result = compute_reachability_matrix_bfs(adj_matrix)
            bfs_time = time.perf_counter() - start_time

            response_data = {
                'success': True,
                'results': {
                    'matrix_time': matrix_time,
                    'bfs_time': bfs_time,
                    'speedup_ratio': matrix_time / bfs_time if bfs_time > 0 else float('inf'),
                    'results_match': matrix_result == bfs_result,
                    'num_nodes': len(adj_matrix)
                }
            }
        except Exception as e:
            response_data = {'success': False, 'error': str(e)}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_server(port=8000):
    static_dir = Path(__file__).parent / 'static'
    os.chdir(static_dir)

    try:
        with socketserver.TCPServer(("", port), MatrixConnectivityHandler) as httpd:
            print(f"Matrix Connectivity Graph Editor")
            print(f"Server running at http://localhost:{port}")
            print(f"Open your browser and navigate to the URL above")
            print(f"Press Ctrl+C to stop the server")

            try:
                webbrowser.open(f'http://localhost:{port}')
            except:
                pass

            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if e.errno == 48:
            print(f"Port {port} is already in use. Try a different port:")
            print(f"python server.py --port 8001")
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Start the graph editor server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')

    args = parser.parse_args()
    start_server(args.port)
