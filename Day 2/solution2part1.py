def is_invalid_id(n):
    s = str(n)
    L = len(s)

    # odd length → automatically valid
    if L % 2 == 1:
        return False

    # even length → check halves
    half = L // 2
    return s[:half] == s[half:]  # invalid if halves match


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
