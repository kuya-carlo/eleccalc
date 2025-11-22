def gaussian_elimination(A: list, b: list):
    """
    Solve Ax = b using manual Gaussian elimination with partial pivoting.
    Returns x as a list of floats.
    """
    n = len(A)

    # Forward elimination
    for i in range(n):
        # Partial pivot: find the row with max absolute value in column i
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if abs(A[max_row][i]) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular")

        # Swap rows
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below
        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - sum_ax) / A[i][i]

    return x


A = [[2, 1, -1], [-3, -1, -2], [-2, 1, 2]]
b = [8, -11, -3]

solution = gaussian_elimination(A, b)
print(solution)
