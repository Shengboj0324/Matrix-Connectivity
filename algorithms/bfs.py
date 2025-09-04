from collections import deque

def bfs_reachable(adj_matrix, start_node):
    n = len(adj_matrix)
    if start_node < 0 or start_node >= n:
        raise ValueError(f"Start node {start_node} is out of range [0, {n-1}]")

    visited = set([start_node])
    queue = deque([start_node])

    while queue:
        current = queue.popleft()
        for neighbor in range(n):
            if adj_matrix[current][neighbor] > 0 and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited

def compute_reachability_matrix_bfs(adj_matrix):
    n = len(adj_matrix)
    reachability = [[0] * n for _ in range(n)]

    for start in range(n):
        reachable_nodes = bfs_reachable(adj_matrix, start)
        for node in reachable_nodes:
            reachability[start][node] = 1

    return reachability

def is_connected(adj_matrix):
    n = len(adj_matrix)
    if n <= 1:
        return True
    return len(bfs_reachable(adj_matrix, 0)) == n

def find_connected_components(adj_matrix):
    n = len(adj_matrix)
    visited = set()
    components = []

    for start in range(n):
        if start not in visited:
            component = bfs_reachable(adj_matrix, start)
            components.append(component)
            visited.update(component)

    return components