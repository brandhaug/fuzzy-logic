def triangle(position, x0, x1, x2, clip):
    value = 0

    if x0 <= position <= x1:
        value = (position - x0) / (x1 - x0)
    elif x1 <= position <= x2:
        value = (x2 - position) / (x1 - x0)

    if value > clip:
        value = clip

    return value


def grade(position, x0, x1, clip):
    value = 0

    if position >= x1:
        value = 1.0
    elif position <= x0:
        value = 0
    else:
        value = (position - x0) / (x1 - x0)

    if value > clip:
        value = clip

    return value


def reverse_grade(position, x0, x1, clip):
    value = 0

    if position <= x0:
        value = 1.0
    elif position >= x1:
        value = 0
    else:
        value = (x1 - position) / (x1 - x0)

    if value > clip:
        value = clip

    return value


def calculate_dom(fuzzy_sets, position):
    dom = []

    for i, x in enumerate(fuzzy_sets):
        if i == 0:
            dom.append(reverse_grade(position, x[0], x[1], 1))
        elif i == len(distances) - 1:
            dom.append(grade(position, x[0], x[1], 1))
        else:
            dom.append(triangle(position, x[0], x[1], x[2], 1))
    return dom


# Distances (x)
distances = [
    [1, 2.5],  # A1 very_small
    [1.5, 3, 4.5],  # A2 small
    [3.5, 5, 6.5],  # A3 perfect
    [5.5, 7, 8.5],  # A4 big
    [7.5, 8.5, 1]  # A5
]

# Deltas (y)
deltas = [
    [-4, -25],  # B1 shrinking_fast
    [-3.5, -2, -0.5],  # B2 shrinking
    [-1.5, 0, 1.5],  # B3 stable
    [0.5, 2, 3.5],  # B4 growing
    [2.5, 4]  # B5 growing_fast
]

# Actions (z)
actions = [
    [-7, -5],  # C1 brake_hard
    [-7, -4, -1],  # C2 slow_down
    [-3, 0, 3],  # C3 none
    [1, 4, 7],  # C4 speed_up
    [5, 8]  # C5 floor_it
]

# Inputs
distance_input = 3.7  # x
delta_input = 1.2  # y

"""
Part 1: Fuzzification - Degree of membership (DOM)
"""
distance_dom = calculate_dom(distances, distance_input)
delta_dom = calculate_dom(deltas, delta_input)

print('Distance DOM', distance_dom)
print('Delta DOM', delta_dom)

"""
Part 2: Rule evaluation
"""
action_dom = [0, 0, 0, 0, 0]

if distance_dom[1] and delta_dom[3]:  # z = C3
    action_dom[2] = min(distance_dom[1], delta_dom[3])

if distance_dom[1] and delta_dom[2]:  # z = C2
    action_dom[1] = min(distance_dom[1], delta_dom[2])

if distance_dom[2] and delta_dom[3]:  # z = C4
    action_dom[3] = min(distance_dom[2], delta_dom[3])

if distance_dom[4] and (not delta_dom[3] or not delta_dom[4]):  # z = C5
    action_dom[4] = min(distance_dom[1], max(1 - delta_dom[3]), (1 - delta_dom[4]))

"""
Part 3: Rule aggregation
"""
min_x = -10
max_x = 10
step = 1

highest_arr = [0] * 21

for position in range(min_x, max_x + 1):
    for action_index, x in enumerate(actions):
        val = 0

        if action_index == 0:
            val = reverse_grade(position, x[0], x[1], action_dom[action_index])
        elif action_index == len(distances) - 1:
            val = grade(position, x[0], x[1], action_dom[action_index])
        else:
            val = triangle(position, x[0], x[1], x[2], action_dom[action_index])

        if val > highest_arr[position + 10]:
            highest_arr[position + 10] = val

print(highest_arr)

dividend = 0.0
divisor = 0.0
values = []
values_count = []

for i in range(min_x, max_x + 1):
    dividend += highest_arr[i + 10] * i

for val in highest_arr:
    if val not in values:
        values.append(val)
        values_count.append(1)
    else:
        index = values.index(val)
        values_count[index] += 1
    divisor += val

defuzzified_output = dividend / divisor
print('Defuzzified output', defuzzified_output)

highest_val = 0
highest_index = 0

for action_index, x in enumerate(actions):
    temp_val = 0

    if action_index == 0:
        temp_val = reverse_grade(defuzzified_output, x[0], x[1], 1)
    elif action_index == len(distances) - 1:
        temp_val = grade(defuzzified_output, x[0], x[1], 1)
    else:
        temp_val = triangle(defuzzified_output, x[0], x[1], x[2], 1)

    if temp_val > highest_val:
        highest_val = temp_val
        highest_index = action_index

print('Action: C%d' % (highest_index + 1))
