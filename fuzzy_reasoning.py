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

    for i, value in enumerate(fuzzy_sets):
        if i == 0:
            dom.append(reverse_grade(position, value[1][0], value[2][0], 1))
        elif i == len(distances) - 1:
            dom.append(grade(position, value[1][0], value[2][0], 1))
        else:
            dom.append(triangle(position, value[1][0], value[2][0], value[3][0], 1))
    return dom


# Distances (x)
distances = [
    [[0, 1], [1, 1], [2.5, 0], [10, 0]],  # A1 very_small
    [[0, 0], [1.5, 0], [3, 1], [4.5, 0], [10, 0]],  # A2 small
    [[0, 0], [3.5, 0], [5, 1], [6.5, 0], [10, 0]],  # A3 perfect
    [[0, 0], [5.5, 0], [7, 1], [8.5, 0], [10, 0]],  # A4 big
    [[0, 0], [7.5, 0], [8.5, 1], [10, 1]]  # A5
]

# Deltas (y)
deltas = [
    [[-5, 1], [-4, 1], [-2.5, 0], [5, 0]],  # B1 shrinking_fast
    [[-5, 0], [-3.5, 0], [-2, 1], [-0.5, 0], [5, 0]],  # B2 shrinking
    [[-5, 0], [-1.5, 0], [0, 1], [1.5, 0], [5, 0]],  # B3 stable
    [[-5, 0], [0.5, 0], [2, 1], [3.5, 0], [5, 0]],  # B4 growing
    [[-5, 0], [2.5, 0], [4, 1], [5, 1]]  # B5 growing_fast
]

# Actions (z)
actions = [
    [[-10, 1], [-7, 1], [-5, 0], [10, 0]],  # C1 brake_hard
    [[-10, 0], [-7, 0], [-4, 1], [-1, 0], [10, 0]],  # C2 slow_down
    [[-10, 0], [-3, 0], [0, 1], [3, 0], [10, 0]],  # C3 none
    [[-10, 0], [1, 0], [4, 1], [7, 0], [10, 0]],  # C4 speed_up
    [[-10, 0], [5, 0], [8, 1], [10, 1]]  # C5 floor_it
]

# Inputs
distance_input = 3.7  # x
delta_input = 1.2  # y

"""
Part 1: Fuzzification - Degree of membership (DOM)
"""
distance_dom = calculate_dom(distances, distance_input)
delta_dom = calculate_dom(deltas, delta_input)

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

actions_detailed = [
    [[-10, 1], [-9, 1.0], [-8, 1.0], [-7, 1], [-6, -0.5], [-5, 0], [-4, 0], [-3, 0], [-2, 0], [-1, 0], [0, 0], [1, 0],
     [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0]],
    [[-10, 0], [-9, 0], [-8, 0], [-7, 0], [-6, 0.33], [-5, 0.67], [-4, 1], [-3, 0.67], [-2, 0.33], [-1, 0], [0, 0],
     [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0]],
    [[-10, 0], [-9, 0], [-8, 0], [-7, 0], [-6, 0], [-5, 0], [-4, 0], [-3, 0], [-2, 0.33], [-1, 0.67], [0, 1], [1, 0.67],
     [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0]],
    [[-10, 0], [-9, 0], [-8, 0], [-7, 0], [-6, 0], [-5, 0], [-4, 0], [-3, 0], [-2, 0.33], [-1, 0], [0, 0], [1, 0],
     [2, 0.33], [3, 0.67], [4, 1], [5, 0.67], [6, 0.33], [7, 0], [8, 0], [9, 0], [10, 0]],
    [[-10, 0], [-9, 0], [-8, 0], [-7, 0], [-6, 0], [-5, 0], [-4, 0], [-3, 0], [-2, 0.33], [-1, 0], [0, 0], [1, 0],
     [2, 0], [3, 0], [4, 1], [5, 0], [6, 0.5], [7, 1], [8, 1], [9, 1], [10, 1]],
]

highest_arr = [0] * 21

for action_index, actions in enumerate(actions_detailed):
    for i, coordinates in enumerate(actions):
        if coordinates[1] > action_dom[action_index]:
            current_height = action_dom[action_index]
        else:
            current_height = coordinates[1]

        if current_height > highest_arr[i]:
            highest_arr[i] = current_height

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

print dividend / float(divisor)
