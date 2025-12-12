data = open('Day 9/input-day9.md', 'r').read()

rows = data.splitlines()

inputs = [tuple([int(num) for num in row.split(',')]) for row in rows]

grid = {}
index = {}

def isValid(r1, r2):
    start = index[r1]
    # print('Checking', r1, r2, 'from', start)

    for i in range(start, start + len(inputs)):
        n1 = inputs[i % len(inputs)]
        n2 = inputs[(i + 1) % len(inputs)]
        
        # print('  Scan from', i, n1, n2)
        
        if (n1[0] == n2[0]):
            if (
                (n1[0] > r1[0] and n1[0] < r2[0])
                or (n1[0] > r2[0] and n1[0] < r1[0])
            ):
                for y in range(min(n1[1], n2[1]), max(n1[1], n2[1]) + 1):
                    if (
                        (y > r2[1] and y < r1[1])
                        or (y > r1[1] and y < r2[1])
                    ):
                        # print((n1[0],y), 'is between', r1[1], 'and', r2[1])
                        return False
                
        elif (n1[1] == n2[1]):
            if (
                (n1[1] > r1[1] and n1[1] < r2[1])
                or (n1[1] > r2[1] and n1[1] < r1[1])
            ):
                for x in range(min(n1[0], n2[0]), max(n1[0], n2[0]) + 1):
                    if (
                        (x > r2[0] and x < r1[0])
                        or (x > r1[0] and x < r2[0])
                    ):
                        # print((x,n1[1]), 'is between', r1[0], 'and', r2[0])
                        return False
                    
    return True

print('Building grid...')
queue = []

for i1 in range(len(inputs)):
    n1 = inputs[i1]
    n2 = inputs[i1 + 1] if i1 + 1 < len(inputs) else inputs[0]
    index[n1] = i1
    
    print(i1, n1, n2)
    
    grid[(n1[0], n1[1])] = '#'
    grid[(n2[0], n2[1])] = '#'
    
    if (n1[0] == n2[0]):
        for y in range(min(n1[1], n2[1]), max(n1[1], n2[1]) + 1):
            grid[(n1[0], y)] = grid[(n1[0], y)] if (n1[0], y) in grid else 'X'
    elif (n1[1] == n2[1]):
        for x in range(min(n1[0], n2[0]), max(n1[0], n2[0]) + 1):
            grid[(x,n1[1])] = grid[(x,n1[1])] if (x, n1[1]) in grid else 'X'

print('Grid built')

print('Calculating area...')

tests = []

max_area = 0
for i1 in range(len(inputs)):
    for i2 in range(i1 + 1, len(inputs)):
        n1 = inputs[i1]
        n2 = inputs[i2]
    
        area = (abs(n1[0] - n2[0]) + 1) * (abs(n1[1] - n2[1]) + 1) 
        tests.append((n1, n2, area))
        
        
        
tests.sort(key=lambda x: x[2], reverse=True)
        
for test in tests:
    n1, n2, area = test
    
    if not isValid(n1, n2):
        continue

    print(n1, n2, (abs(n1[0] - n2[0]) + 1), '*', (abs(n1[1] - n2[1]) + 1), '=', area)
    break
