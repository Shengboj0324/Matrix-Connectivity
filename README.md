# Matrix Connectivity Investigation: Discovering Graph Connectivity Through Matrix Multiplication

## Abstract

This investigation examines how matrix multiplication reveals graph connectivity information. Through experimentation and mathematical analysis, matrix powers A^k are shown to count walks of length k between nodes. When these powers are combined using Boolean operations, complete reachability information is obtained that matches traditional graph algorithms. The study compares the algebraic approach against breadth-first search, demonstrating mathematical equivalence while revealing significant performance differences.

## 1. Introduction and Learning Objectives

This investigation examines the relationship between matrix multiplication and graph connectivity. A discovery-based approach is used where patterns emerge from computational experiments rather than starting with theoretical formulas.

The investigation addresses three learning objectives:

1. Build and manipulate diverse graph structures to create a comprehensive test suite
2. Discover through experimentation what matrix multiplication reveals about connectivity
3. Compare the performance trade-offs between algebraic and traditional graph algorithms

Mathematical insights emerge from computational experiments on carefully constructed graph collections.

## 2. Graph Collection and Data Structure (20 points)

### 2.1 Graph Suite Composition

The investigation uses five distinct graph types, ranging from 10-node to 150-node structures:

- **Path Graph (10 nodes)**: Linear chain structure for testing basic connectivity
- **Cycle Graph (10 nodes)**: Circular structure demonstrating closed-loop connectivity
- **Star Graph (21 nodes)**: Hub-and-spoke pattern illustrating centralized connectivity
- **Grid Graph (100 nodes)**: 10×10 lattice representing spatial connectivity patterns
- **Clustered Graph (150 nodes)**: Five clusters connected by bridges, testing multi-component structures

### 2.2 Graph Representation Convention

There is a sustained mathematical convention maintained for all graph structures:
- **Undirected**: Every edge works both ways, creating symmetric adjacency matrices that reflect real-world network behavior
- **Unweighted**: Each connection has equal importance, represented simply as 1 in the adjacency matrices
- **Simple**: Complications like self-loops or multiple edges between the same pair of nodes are avoided
- **Connected Components**: Some graphs intentionally contain multiple components, allowing study of how the algorithms handle disconnected networks

### 2.3 Data Format Specification

Graphs are stored in JSON format with standardized structure:

```json
{
  "name": "graph_identifier",
  "description": "Graph type and properties",
  "nodes": [{"id": 0, "x": 100, "y": 200}],
  "edges": [{"from": 0, "to": 1}]
}
```

## 3. Interactive Editor and Visualization (20 points)

### 3.1 Editor Functionality

The web-based interactive editor transforms abstract graph theory into tangible objects:

- **Node Operations**: Click to add nodes anywhere on the canvas, drag them around to find the perfect layout, or remove them with a simple click
- **Edge Operations**: Connect any two nodes by clicking them in sequence, or remove unwanted connections just as easily
- **Import/Export**: Seamlessly work with JSON files that play nicely with all the analysis algorithms
- **Sample Generation**: Jump-start exploration with built-in templates for classic graph types
- **Real-time Analysis**: Watch connectivity properties update instantly as the graph is modified

### 3.2 Technical Implementation

HTML5 Canvas is leveraged for smooth rendering while JavaScript handles all the interactive functionality. The editor switches between different modes—adding nodes, creating edges, deleting elements, or simply moving things around—with clear visual cues so users always know what will happen when they click.

### 3.3 Integration with Analysis Pipeline

Here's where the editor: every graph created exports to the exact JSON format the analysis algorithms expect. This seamless integration means ideas can be sketched, immediately tested with the connectivity algorithms, and iterated rapidly without any tedious format conversions or data wrangling.

## 4. Discovery Statement and Mathematical Evidence (25 points)

### 4.1 Core Discovery

**Discovery Statement**: When A^k (the k-th power of the adjacency matrix A) is computed, each entry (A^k)_{ij} equals the number of walks of length k from node i to node j. The Boolean union of A^1, A^2, ..., A^{n-1} produces the complete reachability matrix, where R_{ij} = 1 indicates that node j is reachable from node i.

### 4.2 Mathematical Foundation

The mathematical basis follows from matrix multiplication properties:
(A^k)_{ij} = Σ_ℓ (A^{k-1})_{iℓ} × A_{ℓj}

This formula counts every possible (k-1)-step walk from i to intermediate node ℓ, then extends it with an edge from ℓ to j. The sum counts all possible k-step walks from i to j. The Boolean union captures complete reachability because in any connected component with n nodes, any reachable node can be reached in at most n-1 steps.

### 4.3 Empirical Evidence

**4-Node Path Example (0-1-2-3)**:
- A^1: Shows direct connections between adjacent nodes
- A^2: Shows 2-step walks between nodes separated by one intermediate
- A^3: Shows 3-step walks, completing connectivity across the entire path
- Reachability Matrix: All entries equal 1, confirming full connectivity

**10-Node Cycle Example**:
- Matrix powers exhibit symmetric patterns reflecting the cycle structure
- Even powers show return paths to starting positions
- Odd powers show forward progression around the cycle
- Reachability matrix confirms complete connectivity within the cycle

### 4.4 Theoretical Justification

The mathematical correctness follows from the associative property of matrix multiplication and the interpretation of adjacency matrices as linear transformations on the space of node distributions. Each multiplication step extends walks by exactly one edge, and the Boolean union operation captures the existence of paths regardless of length.

## 5. Implementation Correctness (20 points)

### 5.1 Matrix Multiplication Implementation

Matrix multiplication is implemented using triple-nested loops without external linear algebra libraries:

```python
def matrix_multiply(A, B):
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C
```

This implementation achieves O(n³) complexity per multiplication. Matrix powers are computed by repeatedly applying this operation.

### 5.2 Direct Graph Algorithm Implementation

The BFS-based approach explores the graph directly through traversal:

```python
def compute_reachability_matrix_bfs(adj_matrix):
    n = len(adj_matrix)
    reachability = [[0 for _ in range(n)] for _ in range(n)]
    for start in range(n):
        reachable_nodes = bfs_reachable(adj_matrix, start)
        for node in reachable_nodes:
            reachability[start][node] = 1
    return reachability
```

This approach achieves O(n²) complexity for dense graphs and O(n(n+m)) for sparse graphs, providing better performance than the matrix method.

### 5.3 Correctness Verification

All implementations undergo systematic verification:
- **Functional Testing**: Unit tests verify correct behavior on known inputs
- **Cross-Validation**: Matrix and BFS methods produce identical results on all test graphs
- **Edge Case Handling**: Proper behavior for empty graphs, single nodes, and disconnected components

## 6. Performance Study (20 points)

### 6.1 Experimental Methodology

**System Environment**:
- Platform: Python 3.9.13 on macOS 10.16 (x86_64)
- Timing: `time.perf_counter()` for high-precision measurements
- Test Suite: 28 carefully chosen graphs ranging from 5 to 36 nodes
- Trials: Single execution per graph (the algorithms are deterministic, so repeated trials would just confirm the same results)

**Graph Generation**:
- A systematic size progression was tested: 5, 8, 10, 12, 15, 20, 25, 30, 36 nodes
- Each size included multiple graph types: paths, cycles, stars, and grid structures
- Where randomness was involved, fixed seeds were used to ensure reproducible results

### 6.2 Performance Results

| Graph Size | Matrix Time (s) | BFS Time (s) | BFS Speedup |
|------------|----------------|--------------|-------------|
| 5 nodes    | 0.000149       | 0.000016     | 9.1x        |
| 10 nodes   | 0.004371       | 0.000070     | 62.3x       |
| 20 nodes   | 0.149653       | 0.000427     | 350.4x      |
| 30 nodes   | 1.155326       | 0.001252     | 922.6x      |
| 36 nodes   | 2.962572       | 0.002120     | 1397.5x     |

**Summary Statistics**:
- Total graphs tested: 28
- Success rate: 100% (both methods always agreed on the final answer)
- Average BFS speedup: 320.5x
- The performance gap grows dramatically as graphs get larger—exactly what complexity theory predicts

### 6.3 Complexity Analysis

**Matrix Method**: O(n³) per power × O(n) powers = O(n⁴) total complexity
**BFS Method**: O(n + m) per source × n sources = O(n²) for dense graphs

The empirical results confirm complexity theory predictions:
- Matrix computation times grow with the fourth power of graph size
- BFS times grow quadratically
- The performance gap widens as graph size increases

### 6.4 Algorithmic Comparison

The performance study reveals algorithmic trade-offs:
- **Matrix Approach**: Provides mathematical insight but is computationally expensive
- **BFS Approach**: More efficient for practical applications
- **Practical Implications**: Direct graph algorithms are superior for operational connectivity analysis
- **Educational Value**: Matrix methods provide theoretical understanding of connectivity structure

## 7. Reproducibility and Documentation (5 points)

### 7.1 Reproduction Instructions

Want to reproduce the entire investigation? Here's the roadmap:

```bash
# Execute discovery experiments
cd experiments && python discovery.py

# Run performance benchmarks
python quick_benchmark.py

# Generate analysis plots
python generate_plots.py

# Launch interactive editor
cd ../editor && python server.py
```

### 7.2 System Requirements

- Python 3.7+ with standard library modules (no exotic dependencies required)
- Any modern web browser for the interactive editor
- Optional: matplotlib and pandas for enhanced plotting capabilities

### 7.3 Code Organization

Everything has been organized with clarity in mind:
- `algorithms/`: The mathematical heart of the investigation
- `experiments/`: Scripts that drive discovery and performance analysis
- `editor/`: Interactive tools for creating and visualizing graphs
- `graphs/`: The curated collection of test graphs in JSON format

### 7.4 Verification Procedures

Worried about whether everything works correctly? The solution is provided:

```bash
# Verify complete system functionality
python test_complete_system.py
```

This comprehensive test suite checks every component and ensures all the pieces work together seamlessly.

## 8. Conclusions and Mathematical Insights

### 8.1 Theoretical Contributions

The investigation demonstrates that matrix multiplication provides a mathematical framework for understanding network connectivity. The discovery that matrix powers count walks of specific lengths connects linear algebra and graph theory.

### 8.2 Computational Implications

The matrix approach offers mathematical insight but has O(n⁴) complexity, making it impractical for large graphs. Direct graph algorithms achieve O(n²) complexity and outperform matrix methods for practical applications. This demonstrates the trade-off between mathematical insight and computational efficiency.
