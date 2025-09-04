import json
import math
import random

def generate_path_graph(n, name=None):
    if name is None:
        name = f"path{n}"

    nodes = []
    edges = []

    for i in range(n):
        nodes.append({
            'id': i,
            'x': 50 + i * 100,
            'y': 300
        })

    for i in range(n - 1):
        edges.append({
            'from': i,
            'to': i + 1
        })

    return {
        'name': name,
        'description': f"Path graph with {n} nodes",
        'nodes': nodes,
        'edges': edges
    }

def generate_cycle_graph(n, name=None):
    if name is None:
        name = f"cycle{n}"

    nodes = []
    edges = []

    center_x, center_y = 400, 300
    radius = 150

    for i in range(n):
        angle = 2 * math.pi * i / n
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        nodes.append({
            'id': i,
            'x': int(x),
            'y': int(y)
        })

    for i in range(n):
        edges.append({
            'from': i,
            'to': (i + 1) % n
        })

    return {
        'name': name,
        'description': f"Cycle graph with {n} nodes",
        'nodes': nodes,
        'edges': edges
    }

def generate_star_graph(n, name=None):
    if name is None:
        name = f"star{n}"

    center_x, center_y = 400, 300
    nodes = [{'id': 0, 'x': center_x, 'y': center_y}]
    edges = []

    radius = 150
    for i in range(1, n):
        angle = 2 * math.pi * (i - 1) / (n - 1)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        nodes.append({'id': i, 'x': int(x), 'y': int(y)})
        edges.append({'from': 0, 'to': i})

    return {
        'name': name,
        'description': f"Star graph with {n} nodes (1 center + {n-1} leaves)",
        'nodes': nodes,
        'edges': edges
    }

def generate_grid_graph(rows, cols, name=None):
    if name is None:
        name = f"grid{rows}x{cols}"

    spacing = 60
    start_x, start_y = 50, 50

    nodes = [{'id': r * cols + c, 'x': start_x + c * spacing, 'y': start_y + r * spacing}
             for r in range(rows) for c in range(cols)]

    edges = []
    for r in range(rows):
        for c in range(cols):
            node_id = r * cols + c
            if c < cols - 1:
                edges.append({'from': node_id, 'to': r * cols + (c + 1)})
            if r < rows - 1:
                edges.append({'from': node_id, 'to': (r + 1) * cols + c})

    return {
        'name': name,
        'description': f"{rows}x{cols} grid graph with {rows * cols} nodes",
        'nodes': nodes,
        'edges': edges
    }

