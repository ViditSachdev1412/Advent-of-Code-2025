def max_two_digit(bank):
    digits = list(map(int, bank))
    n = len(digits)

    M = max(digits)

    idxs = [i for i, d in enumerate(digits) if d == M]

    best = -1

    for idx in idxs:
        if idx < n - 1:
            X = M
            Y = max(digits[idx + 1 :])
            best = max(best, 10 * X + Y)

        else:
            Y = M
            X = max(digits[:idx])
            best = max(best, 10 * X + Y)

    return best


total = 0

with open("./Day 3/input-day3.md") as f:
    for line in f:
        bank = line.strip()
        if bank:
            total += max_two_digit(bank)

print("Total output joltage =", total)
