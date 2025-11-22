def gaussian_elimination(A: list, b: list):
    """
    Solve Ax = b using manual Gaussian elimination with partial pivoting.
    Returns x as a list of floats.
    """
    n = len(A)
    # Forward elimination
    for i in range(n):
        # Partial pivot: find the row with max absolute value in column i
        # aka. best row to use as base
        # checks which row has highest value per row
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if abs(A[max_row][i]) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular")
            # disallows singular matrix
        # Swap rows
        # put best row on top
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        # Eliminate below
        # aka find the multiplier factor for each row.
        for k in range(i + 1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]
    # Back substitution
    # finds x, y, z
    x = [0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - sum_ax) / A[i][i]
    return x


# Test case 1: Original example
print("Test 1: Original system")
A1 = [[2, 1, -1], [-3, -1, -2], [-2, 1, 2]]
b1 = [8, -11, -3]
solution1 = gaussian_elimination(A1, b1)
print(f"Solution: {solution1}")

# Verify the solution by computing Ax
A_orig = [[2, 1, -1], [-3, -1, -2], [-2, 1, 2]]
result = [sum(A_orig[i][j] * solution1[j] for j in range(3)) for i in range(3)]
print(f"Verification Ax = {result}")
print(f"Expected b = [8, -11, -3]")
print(f"Match: {all(abs(result[i] - [8, -11, -3][i]) < 1e-10 for i in range(3))}")

# Test case 2: Simple system with known solution
print("\nTest 2: Simple system (x=1, y=2, z=3)")
A2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
b2 = [1, 2, 3]
solution2 = gaussian_elimination(A2, b2)
print(f"Solution: {solution2}")
print(f"Expected: [1, 2, 3]")
print(f"Match: {all(abs(solution2[i] - [1, 2, 3][i]) < 1e-10 for i in range(3))}")

# Test case 3: Another system
print("\nTest 3: Another system")
A3 = [[1, 2, 3], [2, -1, 1], [3, 0, -1]]
b3 = [11, 2, 5]
b3_expected = [11, 2, 5]  # Save original values
solution3 = gaussian_elimination(A3, b3)
print(f"Solution: {solution3}")

# Verify
A3_orig = [[1, 2, 3], [2, -1, 1], [3, 0, -1]]
result3 = [sum(A3_orig[i][j] * solution3[j] for j in range(3)) for i in range(3)]
print(f"Verification Ax = {result3}")
print(f"Expected b = {b3_expected}")
print(f"Match: {all(abs(result3[i] - b3_expected[i]) < 1e-10 for i in range(3))}")

# Test case 4: 2x2 system
print("\nTest 4: 2x2 system (x=3, y=2)")
A4 = [[2, 1], [1, 3]]
b4 = [8, 9]
solution4 = gaussian_elimination(A4, b4)
print(f"Solution: {solution4}")
print(f"Expected: [3, 2]")
print(f"Match: {all(abs(solution4[i] - [3, 2][i]) < 1e-10 for i in range(2))}")
