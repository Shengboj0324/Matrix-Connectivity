import json

def graph_to_adjacency_matrix(graph_data):
    nodes = graph_data.get('nodes', [])
    edges = graph_data.get('edges', [])

    if not nodes:
        return [], {}

    node_ids = sorted([node['id'] for node in nodes])
    node_mapping = {node_id: i for i, node_id in enumerate(node_ids)}
    n = len(node_ids)

    adj_matrix = [[0] * n for _ in range(n)]

    for edge in edges:
        from_id, to_id = edge['from'], edge['to']
        if from_id in node_mapping and to_id in node_mapping:
            from_idx, to_idx = node_mapping[from_id], node_mapping[to_id]
            adj_matrix[from_idx][to_idx] = 1
            adj_matrix[to_idx][from_idx] = 1

    return adj_matrix, node_mapping

def load_graph_from_file(filename):
    with open(filename, 'r') as f:
        graph_data = json.load(f)
    adj_matrix, node_mapping = graph_to_adjacency_matrix(graph_data)
    return adj_matrix, node_mapping, graph_data

def adjacency_matrix_to_graph(adj_matrix, node_mapping=None):
    n = len(adj_matrix)
    if node_mapping is None:
        node_mapping = {i: i for i in range(n)}

    reverse_mapping = {v: k for k, v in node_mapping.items()}

    nodes = [{'id': reverse_mapping.get(i, i), 'x': 100 + (i % 10) * 80, 'y': 100 + (i // 10) * 80} for i in range(n)]
    edges = [{'from': reverse_mapping.get(i, i), 'to': reverse_mapping.get(j, j)}
             for i in range(n) for j in range(i + 1, n) if adj_matrix[i][j] > 0]

    return {'nodes': nodes, 'edges': edges}