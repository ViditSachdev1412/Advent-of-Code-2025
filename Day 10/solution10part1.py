import re
from itertools import product

def parse_machine(line):
    # Extract indicator pattern
    pattern = re.search(r"\[(.*?)\]", line).group(1)
    target = [1 if c == '#' else 0 for c in pattern]
    n = len(target)

    # Extract button toggles
    buttons = [tuple(map(int, grp.split(',')))
               for grp in re.findall(r"\((.*?)\)", line)]

    # Build matrix A (lights × buttons)
    m = len(buttons)
    A = [[0]*m for _ in range(n)]
    for j, btn in enumerate(buttons):
        for x in btn:
            A[x][j] = 1

    return A, target, m

def gaussian_elim_gf2(A, b):
    """Return row-reduced matrix, solution basis, free vars, rank."""
    n = len(A)
    m = len(A[0])
    A = [row[:] for row in A]
    b = b[:]

    row = 0
    pivots = [-1]*n

    for col in range(m):
        pivot = None
        for r in range(row, n):
            if A[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            continue

        A[row], A[pivot] = A[pivot], A[row]
        b[row], b[pivot] = b[pivot], b[row]
        pivots[row] = col

        # Eliminate
        for r in range(n):
            if r != row and A[r][col] == 1:
                for c in range(col, m):
                    A[r][c] ^= A[row][c]
                b[r] ^= b[row]
        row += 1

    rank = row

    # Check inconsistency
    for r in range(rank, n):
        if b[r] == 1:
            return None, None, None, None  # No solution

    # Free variables
    free = [c for c in range(m) if c not in pivots]

    # Particular solution (set free variables = 0)
    x0 = [0]*m
    for r in range(rank):
        pc = pivots[r]
        val = b[r]
        for c in range(pc+1, m):
            if A[r][c] == 1:
                val ^= x0[c]
        x0[pc] = val

    # Nullspace basis vectors
    basis = []
    for f in free:
        v = [0]*m
        v[f] = 1
        for r in range(rank):
            pc = pivots[r]
            val = A[r][f]
            if val == 1:
                v[pc] = 1
        basis.append(v)

    return x0, basis, free, rank

def min_solution_gf2(x0, basis):
    """Enumerate all combinations of nullspace basis to find min weight."""
    if not basis:
        return sum(x0)

    k = len(basis)
    best = float('inf')

    for mask in product([0,1], repeat=k):
        x = x0[:]
        for bit, vec in zip(mask, basis):
            if bit:
                x = [a^b for a,b in zip(x, vec)]
        best = min(best, sum(x))

    return best

def solve_machine(line):
    A, target, m = parse_machine(line)
    x0, basis, free, rank = gaussian_elim_gf2(A, target)
    presses = min_solution_gf2(x0, basis)
    return presses

def solve_file(path="./Day 10/input-day10.md"):
    total = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                total += solve_machine(line)
    return total

# ---- RUN ----
print("Total minimum presses:", solve_file())
