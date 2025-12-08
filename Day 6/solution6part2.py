import re
import math
import os

input_file = './Day 6/input-day6.md'

if not os.path.exists(input_file):
    raise FileNotFoundError(f"{input_file} not found in the current folder.")

with open(input_file) as f:
    input_text = f.read().rstrip('\n')

lines = input_text.split('\n')

# Pad all 5 lines to equal length
max_len = max(len(line) for line in lines[:5])
padded_lines = [line.ljust(max_len) for line in lines[:5]]

# Find split points where operators are placed (non-space characters on line 5)
split_points = [m.start() for m in re.finditer(r'\S', padded_lines[4])]
split_points.append(max_len)  # include end boundary

answerp2 = 0

for i in range(len(split_points) - 1):
    start = split_points[i]
    end = split_points[i + 1]

    arr = []

    for j in range(start, end):
        # Build the 4-digit number by stacking vertical digits
        num_str = (
            padded_lines[0][j] +
            padded_lines[1][j] +
            padded_lines[2][j] +
            padded_lines[3][j]
        ).strip()

        num = int(num_str or '0')
        if num > 0:
            arr.append(num)

    # Operator comes from padded_lines[4][start]
    if padded_lines[4][start] == '+':
        answerp2 += sum(arr)
    else:
        answerp2 += math.prod(arr)

print(answerp2)
