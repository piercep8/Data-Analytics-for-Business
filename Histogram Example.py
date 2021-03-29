# Lists
from typing import List, Any, Union

import numpy as np
import matplotlib.pyplot as plt

Turnover = [711.5, 610.5, 604.7, 521, 513, 445.6, 216.4, 213, 200, 195.5, 174.5]
League_Positions = [[2,	1,	7,	6,	4,	9,	5,	8,	3,	13,	12],
                    [3,	2,	1,	6,	4,	8,	16,	12,	5,	7,	14],
                    [6,	1,	2,	4,	3,	5,	10,	8,	9,	7,	12]]
Attendance = [74498, 54130, 52983, 54216, 40437, 59899, 58336, 38780, 31851, 31030, 25455]


# Derive average league position for each team
np_league_pos = np.array(League_Positions)
np_ave_league_pos = np_league_pos.mean(axis=0)
np_display_attendance = np.array(Attendance) / 25


# Define parameters for a scatter graph
plt.scatter(Turnover, np_ave_league_pos, s=np_display_attendance, alpha=0.7)
plt.xlabel('Turnover £m')
plt.ylabel(' Average League Position')
plt.title('Highest Earning Premier League Teams - Turnover to Average League Position')
plt.grid(True)
plt.gca().invert_yaxis()

plt.show()
plt.clf()
