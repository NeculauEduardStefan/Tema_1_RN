import pathlib
import math

print("Ex. 1 - Parsing the System of Equations")
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []

    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue

        left, right = line.split("=")
        row = [0.0, 0.0, 0.0]
        sign = 1

        for term in left.split():
            if term == "+":
                sign = 1
            elif term == "-":
                sign = -1
            else:
                var = term[-1]
                coef = term[:-1]
                if coef == "" or coef == "+":
                    value = 1.0
                elif coef == "-":
                    value = -1.0
                else:
                    value = float(coef)

                if var == "x":
                    row[0] = sign * value
                elif var == "y":
                    row[1] = sign * value
                elif var == "z":
                    row[2] = sign * value
                sign = 1

        A.append(row)
        B.append(float(right.strip()))

    return A, B

A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} {B=}")

print(" ")
print("Ex. 2 - Matrix and Vector Operations")

print(" ")
print("Ex. 2.1 - Determinant")

def determinant(matrix: list[list[float]]) -> float:
    a11, a12, a13 = matrix[0]
    a21, a22, a23 = matrix[1]
    a31, a32, a33 = matrix[2]

    return a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)

print(f"{determinant(A)=}")

print(" ")
print("Ex. 2.2 - Trace")

def trace(matrix: list[list[float]]) -> float:
    return matrix[0][0] + matrix[1][1] + matrix[2][2]

print(f"{trace(A)=}")

print(" ")
print("Ex. 2.3 - Vector norm")

def norm(vector: list[float]) -> float:
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)

print(f"{norm(B)=}")

print(" ")
print("Ex. 2.4 - Transpose of matrix")

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    transposed = []
    for j in range(len(matrix[0])):
        new_row = []
        for i in range(len(matrix)):
            new_row.append(matrix[i][j])
        transposed.append(new_row)
    return transposed

print(f"{transpose(A)=}")

print(" ")
print("Ex. 2.5 - Matrix-vector multiplication")

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    multiplication = []
    for i in range(len(matrix)):
        total = 0.0
        for j in range(len(vector)):
            total += matrix[i][j] * vector[j]
        multiplication.append(total)
    return multiplication

print(f"{multiply(A, B)=}")

print(" ")
print("Ex. 3 - Solving using Cramer's Rule")

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("Sistemul nu are solutie unica!")
    solutions = []

    for col in range(3):
        modified = []
        for i in range(3):
            row = list(matrix[i])
            row[col] = vector[i]
            modified.append(row)
        solutions.append(determinant(modified) / det_a)

    return solutions

print(f"{solve_cramer(A, B)=}")

print(" ")
print("Ex. 4 - Solving using Inversion")

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    minor_matrix = []
    for row_idx in range(len(matrix)):
        if row_idx == i:
            continue
        row = []
        for col_idx in range(len(matrix[row_idx])):
            if col_idx == j:
                continue
            row.append(matrix[row_idx][col_idx])
        minor_matrix.append(row)
    return minor_matrix

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cofactor_matrix = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            sign = (-1) ** (i + j)
            m = minor(matrix, i, j)
            det_m = m[0][0] * m[1][1] - m[0][1] * m[1][0]
            row.append(sign * det_m)
        cofactor_matrix.append(row)
    return cofactor_matrix

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_a = determinant(matrix)
    if det_a == 0:
        raise ValueError("Sistemul nu are solutie unica!")

    adj = adjoint(matrix)

    inverse = []
    for i in range(len(adj)):
        new_row = []
        for j in range(len(adj[i])):
            new_row.append(adj[i][j] / det_a)
        inverse.append(new_row)

    return multiply(inverse, vector)

print(f"{solve(A, B)=}")