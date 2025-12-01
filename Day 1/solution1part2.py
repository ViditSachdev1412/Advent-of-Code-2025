current = 50
countZero = 0

with open("./Day 1/input-day1.md", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        direction = line[0]  # 'L' or 'R'
        value = int(line[1:])  # number of clicks to move

        # Simulate movement one click at a time
        for _ in range(value):
            if direction == "R":
                current = (current + 1) % 100
            else:  # "L"
                current = (current - 1) % 100

            # Count EVERY time dial lands on 0
            if current == 0:
                countZero += 1

print("Final value =", current)
print("Times dial hit 0 (including during rotations) =", countZero)
