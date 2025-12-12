# Day 11 – All Paths From "you" to "out"

from pathlib import Path

def load_graph(path="./Day 11/input-day11.md"):
    graph = {}
    text = Path(path).read_text().strip().splitlines()

    for line in text:
        # Example line: 'bbb: ddd eee'
        name, outputs = line.split(":")
        outs = outputs.strip().split()
        graph[name.strip()] = outs

    return graph


def dfs(graph, node, target, path, all_paths):
    # If we reached "out", record the complete path
    if node == target:
        all_paths.append(path[:])
        return

    # Explore neighbors
    for nxt in graph.get(node, []):
        if nxt not in path:             # prevents cycles
            path.append(nxt)
            dfs(graph, nxt, target, path, all_paths)
            path.pop()                  # backtrack


def main():
    graph = load_graph()

    all_paths = []
    dfs(graph, "you", "out", ["you"], all_paths)

    # Print all paths (optional)
    print("All paths:\n")
    for p in all_paths:
        print(" -> ".join(p))

    print("\nTotal paths:", len(all_paths))


if __name__ == "__main__":
    main()
