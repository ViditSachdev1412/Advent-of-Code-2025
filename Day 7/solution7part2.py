#!/usr/bin/env python3
"""
Quantum Tachyon Simulator (Part Two)

Reads the manifold from: ./Day 7/input-day7.md
Simulates a single quantum tachyon particle that branches at each '^'
and returns the total number of timelines (particles that exit the grid).

No animation (this is a counting simulation and is fast).
"""

from pathlib import Path

INPUT_PATH = Path("./Day 7/input-day7.md")


def count_timelines(grid_lines):
    R = len(grid_lines)
    C = max(len(line) for line in grid_lines) if R > 0 else 0

    # Normalize grid: fill with '.' for missing cells
    grid = [list(line.ljust(C, '.')) for line in grid_lines]

    # find S
    sr = sc = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                sr, sc = r, c
                break
        if sr is not None:
            break

    if sr is None:
        raise ValueError("No 'S' found in input")

    # particle counts per cell (r,c) -> count
    from collections import defaultdict
    cur = defaultdict(int)
    cur[(sr, sc)] = 1  # one quantum particle starts at S

    exit_count = 0

    # iterate until no particles remain
    while cur:
        nxt = defaultdict(int)
        for (r, c), cnt in cur.items():
            nr = r + 1
            if nr >= R:
                # particle exits the manifold (timeline ends)
                exit_count += cnt
            else:
                cell_below = grid[nr][c]
                if cell_below == '^':
                    # particle reaches splitter: it branches into left and right
                    # note: the splitter is at (nr, c); new particles appear at (nr, c-1) and (nr, c+1)
                    left = (nr, c - 1)
                    right = (nr, c + 1)
                    # Only add when indices are within horizontal bounds (consistent with earlier implementations)
                    # If a branch would be outside the grid horizontally, it's still a timeline that immediately leaves:
                    if 0 <= left[1] < C:
                        nxt[left] += cnt
                    else:
                        # if left branch would be outside, it effectively exits immediately
                        exit_count += cnt
                    if 0 <= right[1] < C:
                        nxt[right] += cnt
                    else:
                        exit_count += cnt
                else:
                    # particle continues downward into same column
                    nxt[(nr, c)] += cnt
        cur = nxt

    return exit_count


def main():
    if not INPUT_PATH.exists():
        print(f"Input file not found: {INPUT_PATH}")
        return

    with INPUT_PATH.open("r", encoding="utf-8") as f:
        grid_lines = [line.rstrip("\n") for line in f]

    total_timelines = count_timelines(grid_lines)
    print(f"Loaded input from: {INPUT_PATH}")
    print("Total timelines (particles that exit the manifold):", total_timelines)


if __name__ == "__main__":
    main()
