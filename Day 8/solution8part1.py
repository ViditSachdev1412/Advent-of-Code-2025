import math
from itertools import combinations
from collections import Counter

# -------------------------
# Read input from file
# -------------------------
INPUT_FILE = "./Day 8/input-day8.md"

points = []
with open(INPUT_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Accept lines like: 162,817,812
        try:
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
        except:
            # ignore any non-coordinate lines (if markdown has text)
            pass

n = len(points)
print(f"Loaded {n} points.")

# -------------------------
# Union–Find (DSU)
# -------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

    def component_sizes(self):
        roots = [self.find(i) for i in range(len(self.parent))]
        cnt = Counter(roots)
        return sorted(cnt.values(), reverse=True)

# -------------------------
# Build all pairwise distances
# -------------------------
edges = []
for (i, p), (j, q) in combinations(list(enumerate(points)), 2):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    dz = p[2] - q[2]
    dist2 = dx*dx + dy*dy + dz*dz
    edges.append((dist2, i, j))

# Sort by distance
edges.sort(key=lambda x: x[0])

# -------------------------
# Process the 1000 closest pairs
# -------------------------
K = 1000
max_pairs = len(edges)
K = min(K, max_pairs)

uf = UnionFind(n)

for k in range(K):
    _, a, b = edges[k]
    uf.union(a, b)

# -------------------------
# Output results
# -------------------------
sizes = uf.component_sizes()
print("Component sizes (largest first):", sizes)

if len(sizes) >= 3:
    ans = sizes[0] * sizes[1] * sizes[2]
elif len(sizes) == 2:
    ans = sizes[0] * sizes[1] * 1
elif len(sizes) == 1:
    ans = sizes[0]
else:
    ans = 0

print("Answer (product of 3 largest):", ans)
