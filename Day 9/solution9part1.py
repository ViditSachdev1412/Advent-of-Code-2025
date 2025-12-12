# Day 9 - Largest axis-aligned rectangle with opposite corners at red tiles
# Reads from ./Day 9/input-day9.md

import os

input_file = "./Day 9/input-day9.md"

if not os.path.exists(input_file):
    raise FileNotFoundError(f"File not found: {input_file}")

# Load all points
pts = []
with open(input_file) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Skip markdown code block markers
        if line.startswith('```'):
            continue
        # Skip lines that don't contain a comma (like markdown headers)
        if ',' not in line:
            continue
        try:
            x, y = map(int, line.split(","))
            pts.append((x, y))
        except ValueError:
            # Skip lines that can't be parsed as coordinates
            continue

print(f"Loaded {len(pts)} points")

best = 0
best_rect = None

# Check every pair of points as opposite corners
for i in range(len(pts)):
    x1, y1 = pts[i]
    for j in range(i + 1, len(pts)):
        x2, y2 = pts[j]

        # If they share x or y, they're on the same line (area would be 1D)
        if x1 == x2 or y1 == y2:
            continue

        # Calculate area - include both endpoints
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        if area > best:
            best = area
            best_rect = ((x1, y1), (x2, y2))

print(f"Largest rectangle area: {best}")
if best_rect:
    print(f"Between corners: {best_rect[0]} and {best_rect[1]}")