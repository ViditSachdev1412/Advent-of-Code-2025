from pathlib import Path
from functools import lru_cache

def load_graph(path="./Day 11/input-day11.md"):
    graph = {}
    text = Path(path).read_text().strip().splitlines()

    for line in text:
        name, outputs = line.split(":")
        outs = outputs.strip().split()
        graph[name.strip()] = outs

    return graph


def make_dp(graph):
    @lru_cache(None)
    def count_paths(start, target):
        if start == target:
            return 1
        total = 0
        for nxt in graph.get(start, []):
            total += count_paths(nxt, target)
        return total
    return count_paths


def main():
    graph = load_graph()

    count_paths = make_dp(graph)

    # Two valid orders:
    orderA = (
        count_paths("svr", "dac")
        * count_paths("dac", "fft")
        * count_paths("fft", "out")
    )

    orderB = (
        count_paths("svr", "fft")
        * count_paths("fft", "dac")
        * count_paths("dac", "out")
    )

    valid = orderA + orderB

    print("Paths svr → out that pass through dac and fft:", valid)


if __name__ == "__main__":
    main()
