from typing import List, Tuple

# 8 directions (row_delta, col_delta)
NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def count_accessible_and_mark(grid: List[str]) -> Tuple[int, List[str]]:
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    # convert to list of lists for easy updates
    G = [list(row) for row in grid]
    accessible_marks = [["." if ch != "@" else "@" for ch in row] for row in grid]

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    accessible_count = 0

    for r in range(rows):
        for c in range(cols):
            if G[r][c] != "@":
                continue
            neigh_at = 0
            for dr, dc in NEIGHBORS:
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc) and G[nr][nc] == "@":
                    neigh_at += 1
            if neigh_at < 4:
                accessible_count += 1
                accessible_marks[r][c] = "x"
            else:
                accessible_marks[r][c] = "@"  # keep as @ if not accessible

    marked_lines = ["".join(row) for row in accessible_marks]
    return accessible_count, marked_lines


# --- Test with your example ---
example = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]

cnt, marked = count_accessible_and_mark(example)
print("Example accessible count:", cnt)  # should print 13
print("\nMarked grid (x = accessible):")
print("\n".join(marked))


# --- Run on real input file 'input.txt' (one line per row) ---
def run_on_file(path="input.txt"):
    with open(path, "r") as fh:
        grid = [line.rstrip("\n") for line in fh if line.strip() != ""]
    cnt, _ = count_accessible_and_mark(grid)
    print("\nInput file:", path)
    print("Accessible rolls count:", cnt)
    return cnt


run_on_file("./Day 4/input-day4.md")
