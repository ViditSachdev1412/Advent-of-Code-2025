# solve_day12.py
import sys
from collections import defaultdict

# --- SHAPE HELPERS ---------------------------------------------------------

def coords_from_pattern(pattern):
    pts = []
    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            if ch == '#':
                pts.append((r, c))
    return pts

def normalize(coords):
    minr = min(r for r,c in coords)
    minc = min(c for r,c in coords)
    return tuple(sorted(((r-minr, c-minc) for r,c in coords)))

def rotations_and_flips(pattern):
    pts = coords_from_pattern(pattern)
    variants = set()
    for fr in (False, True):
        for fc in (False, True):
            for rot in (0, 1, 2, 3):
                out = []
                for (r,c) in pts:
                    rr, cc = r, c
                    if fr: rr = -rr
                    if fc: cc = -cc
                    for _ in range(rot):
                        rr, cc = cc, -rr
                    out.append((rr, cc))
                variants.add(normalize(out))
    final = []
    for var in variants:
        maxr = max(r for r,c in var)
        maxc = max(c for r,c in var)
        final.append((var, maxr+1, maxc+1))
    return final

def generate_placements(variants, W, H):
    out = []
    for coords, h, w in variants:
        if h > H or w > W:
            continue
        for top in range(H - h + 1):
            for left in range(W - w + 1):
                mask = 0
                for (r,c) in coords:
                    rr = top + r
                    cc = left + c
                    mask |= 1 << (rr * W + cc)
                out.append(mask)
    return out

# --- BACKTRACK --------------------------------------------------------------

def can_pack(W, H, shapes, counts):
    shape_order = []
    cell_size = {}
    variants = {}

    total = 0
    for idx, pat in shapes.items():
        pts = coords_from_pattern(pat)
        cell_size[idx] = len(pts)
        total += counts.get(idx,0) * len(pts)
        variants[idx] = rotations_and_flips(pat)

    if total > W * H:
        return False

    placements = {idx: generate_placements(variants[idx], W, H)
                  for idx in shapes}

    seq = []
    for idx, cnt in counts.items():
        seq.extend([idx]*cnt)

    seq.sort(key=lambda i: len(placements[i]) or 10**9)
    for s in seq:
        if len(placements[s]) == 0:
            return False

    need = [0]*(len(seq)+1)
    s = 0
    for i in range(len(seq)-1, -1, -1):
        s += cell_size[seq[i]]
        need[i] = s

    occupied = 0
    WH = W*H

    sys.setrecursionlimit(10000)

    def dfs(i):
        nonlocal occupied
        if i == len(seq):
            return True
        free = WH - bin(occupied).count("1")
        if free < need[i]:
            return False

        idx = seq[i]
        for m in placements[idx]:
            if m & occupied == 0:
                occupied ^= m
                if dfs(i+1):
                    return True
                occupied ^= m
        return False

    return dfs(0)

# --- PARSE INPUT FILE -------------------------------------------------------

def solve(filename="./Day 12/input-day12.md"):
    text = open(filename).read().strip().splitlines()

    shapes = {}
    i = 0
    # parse shapes
    while i < len(text):
        line = text[i].strip()
        if line.endswith(":"):
            idx = int(line[:-1])
            i += 1
            block = []
            while i < len(text) and text[i].strip().startswith((".", "#")):
                block.append(text[i].rstrip())
                i += 1
            shapes[idx] = block
        else:
            i += 1
            if ":" in line and "x" in line:
                i -= 1
                break

    # parse regions
    regions = []
    while i < len(text):
        line = text[i].strip()
        i += 1
        if not line:
            continue
        if ":" not in line:
            continue

        left, right = line.split(":")
        W, H = map(int, left.split("x"))
        nums = list(map(int, right.split()))
        counts = {idx: nums[idx] if idx < len(nums) else 0 for idx in shapes.keys()}
        regions.append((W, H, counts))

    # check each region
    ans = 0
    for W, H, counts in regions:
        if can_pack(W, H, shapes, counts):
            ans += 1

    print(ans)

# ---- RUN -------------------------------------------------------------------

if __name__ == "__main__":
    solve()
