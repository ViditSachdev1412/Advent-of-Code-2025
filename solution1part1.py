current = 50
countZero = 0


with open("./Day 1/input-day1.md", "r") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue
        direction = line[0]
        value = int(line[1:])

        if direction == "R":
            current = (current + value) % 100
        else:  # direction == "L"
            current = (current - value) % 100

        if current == 0:
            countZero += 1

print("Final value =", current)
print("No. of times value became 0 =", countZero)
