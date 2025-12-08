# solve_day8_part2.py
import sys
from itertools import combinations
from collections import Counter

INPUT_FILE = "./Day 8/input-day8.md"

# --- read points ---
points = []
with open(INPUT_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
        except:
            # ignore non-coordinate lines (markdown headings, etc.)
            pass

n = len(points)
if n == 0:
    print("No points found in", INPUT_FILE)
    sys.exit(1)

# --- Union-Find with component count tracking ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1]*n
        self.components = n

    def find(self, a):
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

# --- build all edges with squared distances ---
edges = []
for (i, p), (j, q) in combinations(list(enumerate(points)), 2):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    dz = p[2] - q[2]
    dist2 = dx*dx + dy*dy + dz*dz
    edges.append((dist2, i, j))

edges.sort(key=lambda x: x[0])

# --- process edges until single component ---
uf = UnionFind(n)
last_pair = None

for dist2, i, j in edges:
    merged = uf.union(i, j)
    if merged:
        # if this union made the graph fully connected, record pair and break
        if uf.components == 1:
            last_pair = (i, j, dist2)
            break

if last_pair is None:
    print("All edges processed but graph did not become fully connected (unexpected).")
    sys.exit(1)

i, j, dist2 = last_pair
xi, yi, zi = points[i]
xj, yj, zj = points[j]
product_x = xi * xj

print("Last pair indices:", i, j)
print("Point A (X,Y,Z):", (xi, yi, zi))
print("Point B (X,Y,Z):", (xj, yj, zj))
print("Squared distance between them:", dist2)
print("Answer (product of X coordinates):", product_x)
