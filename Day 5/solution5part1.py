ranges = []
ids = []
count = 0

with open("./Day 5/input-day5.md") as f:
    lines = [line.strip() for line in f]

blank_index = lines.index("")

range_lines = lines[:blank_index]
id_lines = lines[blank_index + 1 :]

for line in range_lines:
    a, b = line.split("-")
    ranges.append((int(a), int(b)))

for line in id_lines:
    ids.append(int(line))


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


def binary_search(ranges, target):
    left, right = 0, len(ranges) - 1
    while left <= right:
        mid = (left + right) // 2
        start, end = ranges[mid]

        if start <= target <= end:
            return True
        elif target < start:
            right = mid - 1
        else:
            left = mid + 1
    return False


for i in ids:
    if binary_search(merged, i):
        count += 1

print(count)
