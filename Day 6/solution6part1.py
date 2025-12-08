from functools import reduce
import operator
import math

def read_grid(path):
    with open(path, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    # remove any completely empty trailing lines
    while lines and lines[-1] == "":
        lines.pop()
    # ensure at least one line
    if not lines:
        return []
    # pad lines to same length
    maxlen = max(len(l) for l in lines)
    return [l.ljust(maxlen) for l in lines]

def find_separator_columns(grid):
    """Return a set of column indices that are full-space separators."""
    if not grid:
        return set()
    cols = len(grid[0])
    separators = set()
    for c in range(cols):
        if all(row[c] == " " for row in grid):
            separators.add(c)
    return separators

def extract_blocks(grid, separators):
    """Return list of (start_col, end_col) inclusive blocks that are not separators."""
    if not grid:
        return []
    cols = len(grid[0])
    blocks = []
    in_block = False
    start = None
    for c in range(cols):
        if c not in separators:
            if not in_block:
                in_block = True
                start = c
        else:
            if in_block:
                blocks.append((start, c - 1))
                in_block = False
    if in_block:
        blocks.append((start, cols - 1))
    return blocks

def read_block_as_problem(grid, start_col, end_col):
    """
    For columns start_col..end_col inclusive, read each row,
    strip spaces to form tokens. Last row is the operator, previous rows are numbers.
    Returns (op, [numbers]).
    """
    rows = []
    for r in grid:
        chunk = r[start_col:end_col+1]
        token = chunk.strip()
        rows.append(token)
    # last non-empty row should be op; but spec says operator is at bottom of problem
    # so last row is the operator (may be a single '+' or '*')
    if not rows:
        return None
    op = rows[-1]    # could be '' if weird input
    # collect numbers from all rows except the last; keep only non-empty
    numbers = [int(x) for x in (rows[:-1]) if x != ""]
    return op, numbers

def evaluate_problem(op, numbers):
    if op == "+":
        return sum(numbers)
    elif op == "*":
        # product (handle empty case: product of zero numbers -> 0? but spec will always have >=1)
        return math.prod(numbers)  # Python 3.8+
    else:
        raise ValueError(f"Unknown operator: {op!r}")

def grand_total_from_file(path):
    grid = read_grid(path)
    separators = find_separator_columns(grid)
    blocks = extract_blocks(grid, separators)
    total = 0
    for start, end in blocks:
        op, numbers = read_block_as_problem(grid, start, end)
        if op is None:
            continue
        # sanity: op might contain extra whitespace or stray chars; take first char
        op = op.strip()
        if op == "":
            raise ValueError(f"No operator found in block columns {start}-{end}")
        op = op[0]
        val = evaluate_problem(op, numbers)
        total += val
    return total

if __name__ == "__main__":
    path = "./Day 6/input-day6.md"   # change to your input path
    total = grand_total_from_file(path)
    print(total)
