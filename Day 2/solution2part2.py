import re

pattern = re.compile(r"^(\d+)\1+$")


def is_invalid_id(n):
    s = str(n)
    return bool(pattern.fullmatch(s))


total_sum = 0

with open("./Day 2/input-day2.md") as f:
    data = f.read().strip()

ranges = data.split(",")

for r in ranges:
    start, end = map(int, r.split("-"))

    for num in range(start, end + 1):
        if is_invalid_id(num):
            total_sum += num

print("Sum of invalid IDs =", total_sum)
