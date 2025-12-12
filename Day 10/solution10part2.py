import re
from pathlib import Path

# Try importing pulp. If not available, error clearly.
try:
    import pulp
except ImportError:
    raise SystemExit("ERROR: pulp (python ILP solver) is required for part 2.")

input_file = Path("./Day 10/input-day10.md")
if not input_file.exists():
    raise FileNotFoundError("input-day10.md missing")

raw = input_file.read_text().strip().splitlines()

total_answer = 0

line_pattern = re.compile(
    r"\[(.*?)\]\s*((?:\([0-9,]*\)\s*)+)\s*\{(.*?)\}"
)

def parse_button_list(s):
    parts = re.findall(r"\((.*?)\)", s)
    res = []
    for p in parts:
        if p.strip() == "":
            res.append([])
        else:
            res.append(list(map(int, p.split(","))))
    return res

for line in raw:
    m = line_pattern.match(line)
    if not m:
        continue

    # lights_str = m.group(1)  # ignored for part 2
    buttons_str = m.group(2)
    joltage_str = m.group(3).strip()

    target = list(map(int, joltage_str.split(",")))
    T = len(target)

    buttons = parse_button_list(buttons_str)
    B = len(buttons)

    # Build ILP
    prob = pulp.LpProblem("MachineJoltage", pulp.LpMinimize)

    x = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(B)]

    # Minimize total presses
    prob += pulp.lpSum(x)

    # Constraints: For each counter j, sum(button impact) == target[j]
    # button[i] adds +1 for each index in its list
    for j in range(T):
        prob += pulp.lpSum(
            x[i] for i in range(B) if j in buttons[i]
        ) == target[j]

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != "Optimal":
        raise RuntimeError("No solution found for a machine.")

    presses = sum(v.value() for v in x)
    total_answer += presses

print("PART 2 ANSWER =", int(total_answer))
