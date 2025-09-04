from multiply import matrix_power, matrix_boolean_or, matrix_to_boolean, print_matrix

def compute_matrix_powers(adj_matrix, max_power=None):
    n = len(adj_matrix)
    if max_power is None:
        max_power = n - 1

    powers = {0: [[1 if i == j else 0 for j in range(n)] for i in range(n)]}

    if max_power >= 1:
        powers[1] = [row[:] for row in adj_matrix]

    for k in range(2, max_power + 1):
        powers[k] = matrix_power(adj_matrix, k)

    return powers

def compute_reachability_matrix_powers(adj_matrix):
    n = len(adj_matrix)
    if n == 0:
        return []

    powers = compute_matrix_powers(adj_matrix, n - 1)
    reachability = matrix_to_boolean(powers.get(1, [[0] * n for _ in range(n)]))

    for k in range(2, n):
        if k in powers:
            reachability = matrix_boolean_or(reachability, matrix_to_boolean(powers[k]))

    return reachability

def analyze_walk_counts(adj_matrix, max_length=5):
    n = len(adj_matrix)
    powers = compute_matrix_powers(adj_matrix, max_length)

    analysis = {'matrix_size': n, 'powers': powers, 'walk_counts': {}, 'reachability_by_length': {}}

    for k in range(1, max_length + 1):
        if k in powers:
            analysis['walk_counts'][k] = powers[k]
            analysis['reachability_by_length'][k] = sum(1 for i in range(n) for j in range(n)
                                                       if i != j and powers[k][i][j] > 0)

    return analysis

def demonstrate_connectivity_discovery(adj_matrix, verbose=True):
    n = len(adj_matrix)

    if verbose:
        print(f"\n=== Connectivity Discovery for {n}x{n} Graph ===")
        print_matrix(adj_matrix, "Adjacency Matrix A")

    analysis = analyze_walk_counts(adj_matrix, min(n - 1, 5))

    if verbose:
        for k in range(1, min(n, 6)):
            if k in analysis['powers']:
                print_matrix(analysis['powers'][k], f"A^{k} (walks of length {k})")

    reachability = compute_reachability_matrix_powers(adj_matrix)

    if verbose:
        print_matrix(reachability, "Reachability Matrix (Boolean OR of A^1 to A^(n-1))")

    total_pairs = n * (n - 1)
    connected_pairs = sum(1 for i in range(n) for j in range(n) if i != j and reachability[i][j] == 1)
    connectivity_ratio = connected_pairs / total_pairs if total_pairs > 0 else 0

    results = {
        'adjacency_matrix': adj_matrix,
        'matrix_powers': analysis['powers'],
        'reachability_matrix': reachability,
        'connected_pairs': connected_pairs,
        'total_pairs': total_pairs,
        'connectivity_ratio': connectivity_ratio,
        'is_strongly_connected': connectivity_ratio == 1.0,
        'walk_analysis': analysis
    }

    if verbose:
        print(f"\nConnectivity Analysis:")
        print(f"  Connected pairs: {connected_pairs}/{total_pairs}")
        print(f"  Connectivity ratio: {connectivity_ratio:.2%}")
        print(f"  Strongly connected: {results['is_strongly_connected']}")

    return results

def compare_reachability_methods(adj_matrix):
    from bfs import compute_reachability_matrix_bfs

    reachability_matrix = compute_reachability_matrix_powers(adj_matrix)
    reachability_bfs = compute_reachability_matrix_bfs(adj_matrix)

    n = len(adj_matrix)
    differences = sum(1 for i in range(n) for j in range(n) if reachability_matrix[i][j] != reachability_bfs[i][j])

    return {
        'matrix_method': reachability_matrix,
        'bfs_method': reachability_bfs,
        'methods_agree': differences == 0,
        'differences': differences
    }