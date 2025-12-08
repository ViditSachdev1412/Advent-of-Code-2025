ranges = []
with open("./Day 5/input-day5.md") as f:
    lines = [line.strip() for line in f]

blank_index = lines.index("")

range_lines = lines[:blank_index]

for line in range_lines:
    a, b = line.split("-")
    ranges.append((int(a), int(b)))


def merge_ranges(ranges):
    ranges.sort(key=lambda x: x[0])

    merged = []

    for start, end in ranges:
        # If merged is empty OR no overlap
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            # Overlap: extend the last interval
            merged[-1][1] = max(merged[-1][1], end)

    return merged


merged = merge_ranges(ranges)


def count_total_ids(merged):
    total = 0
    for start, end in merged:
        total += end - start + 1
    return total


print(count_total_ids(merged))
