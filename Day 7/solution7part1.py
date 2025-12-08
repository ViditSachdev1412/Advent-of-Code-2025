import time
import os

# ----------------------------------------
# CONFIG
# ----------------------------------------
ANIMATION_DELAY = 0.05   # seconds between frames
CLEAR = True             # clear screen between frames
SHOW_ANIMATION = True    # set False if you only want the split count
# ----------------------------------------


def print_grid(grid, beams):
    """Render the grid with beams drawn on top."""
    disp = [list(row) for row in grid]

    for r, c in beams:
        if 0 <= r < len(disp) and 0 <= c < len(disp[0]):
            disp[r][c] = "|"

    for row in disp:
        print("".join(row))


def simulate_tachyons(grid_lines):
    R = len(grid_lines)
    C = max(len(line) for line in grid_lines)

    grid = [list(line.ljust(C, '.')) for line in grid_lines]

    # Find S
    sr = sc = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                sr, sc = r, c
                break
        if sr is not None:
            break

    if sr is None:
        raise ValueError("No 'S' found in input file")

    active = {(sr, sc)}
    split_count = 0
    frame = 0

    while active:
        if SHOW_ANIMATION:
            if CLEAR:
                os.system("cls" if os.name == "nt" else "clear")
            print(f"Frame {frame} | Active: {len(active)} | Splits: {split_count}")
            print_grid(grid, active)
            time.sleep(ANIMATION_DELAY)
            frame += 1

        next_active = set()

        for (r, c) in active:
            nr = r + 1

            if nr >= R:
                # Beam leaves the manifold
                continue

            if grid[nr][c] == '^':
                # Split event
                split_count += 1
                left = (nr, c - 1)
                right = (nr, c + 1)

                if 0 <= left[1] < C:
                    next_active.add(left)
                if 0 <= right[1] < C:
                    next_active.add(right)

            else:
                # Continue downward
                next_active.add((nr, c))

        active = next_active

    return split_count


# ----------------------------------------
# Load input from file and run
# ----------------------------------------
if __name__ == "__main__":
    input_path = "./Day 7/input-day7.md"

    with open(input_path, "r", encoding="utf-8") as f:
        grid_lines = [line.rstrip("\n") for line in f]

    print(f"Loaded input from: {input_path}")
    print("Starting simulation...\n")

    result = simulate_tachyons(grid_lines)

    print("\n----------------------------------------")
    print("Simulation complete!")
    print("Total split count:", result)
    print("----------------------------------------")
