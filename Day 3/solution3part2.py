def max_joltage_12(bank):
    k = 12
    stack = []
    to_remove = len(bank) - k

    for ch in bank:
        while stack and ch > stack[-1] and to_remove > 0:
            stack.pop()
            to_remove -= 1

        stack.append(ch)

    result = "".join(stack[:k])
    return int(result)


total = 0

with open("./Day 3/input-day3.md") as f:
    for line in f:
        line = line.strip()
        if line:
            total += max_joltage_12(line)

print("Total output joltage =", total)
