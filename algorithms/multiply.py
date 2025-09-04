def matrix_multiply(A, B):
    if not A or not B or not A[0] or not B[0]:
        raise ValueError("Empty matrices cannot be multiplied")

    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError(f"Cannot multiply {rows_A}x{cols_A} matrix with {rows_B}x{cols_B} matrix")

    C = [[0] * cols_B for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C

def matrix_power(A, n):
    if not A or len(A) != len(A[0]):
        raise ValueError("Matrix must be square")
    if n < 0:
        raise ValueError("Power must be non-negative")

    size = len(A)

    if n == 0:
        return [[1 if i == j else 0 for j in range(size)] for i in range(size)]
    if n == 1:
        return [row[:] for row in A]

    result = [row[:] for row in A]
    for _ in range(n - 1):
        result = matrix_multiply(result, A)
    return result

def matrix_add(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrices must have the same dimensions for addition")
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_boolean_or(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Matrices must have the same dimensions for boolean OR")
    return [[1 if A[i][j] > 0 or B[i][j] > 0 else 0 for j in range(len(A[0]))] for i in range(len(A))]

def matrix_to_boolean(A):
    return [[1 if A[i][j] > 0 else 0 for j in range(len(A[0]))] for i in range(len(A))]

def print_matrix(A, title="Matrix"):
    print(f"\n{title}:")
    for row in A:
        print("  " + " ".join(f"{x:3}" for x in row))
    print()