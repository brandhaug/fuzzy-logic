# added_actions = []
#
# for i, action_list in enumerate(actions):
#     actions_detail.append([])
#     added_actions = []
#
#     for j, action in enumerate(action_list):
#         if j > 0:
#             diffe = 0
#             x_distance = action[0] - actions[i][j - 1][0]
#             y_distance = action[1] - actions[i][j - 1][1]
#
#             if x_distance > 1:
#                 diffe = y_distance / float(x_distance)
#
#                 for k in range(x_distance, i, -1):
#                     if action[0] - k not in added_actions:
#                         actions_detail[i].append([action[0] - k, action[1] + (diffe * k)])
#                         added_actions.append(action[0] - k)
#
#         actions_detail[i].append(action)
#         added_actions.append(action[0])

# =====================================

# import matplotlib.pyplot as plt
# import numpy as np
#
#
#
# for temp in actions_detailed:
#     np_actions = np.array(temp)
#     plt.plot(np_actions[:, 0], np_actions[:, 1])
#     plt.show()