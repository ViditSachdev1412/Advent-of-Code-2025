from typing import List

NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def part2_total_removed(grid: List[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    G = [list(r) for r in grid]

    total_removed = 0

    while True:
        to_remove = []

        # Find all accessible rolls in this round
        for r in range(rows):
            for c in range(cols):
                if G[r][c] != "@":
                    continue

                neigh = 0
                for dr, dc in NEIGHBORS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and G[nr][nc] == "@":
                        neigh += 1

                if neigh < 4:
                    to_remove.append((r, c))

        # Stop if no more can be removed
        if not to_remove:
            break

        # Remove rolls
        for r, c in to_remove:
            G[r][c] = "."

        total_removed += len(to_remove)

    return total_removed


# ---- Run PART 2 ----
def run_part2(path="./Day 4/input-day4.md"):
    with open(path) as f:
        grid = [line.strip() for line in f if line.strip()]
    ans = part2_total_removed(grid)
    print("Part 2:", ans)
    return ans


run_part2()
