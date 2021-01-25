from numpy.random import random
from algorithm import *


def df(y, x, k=0.2, v=0.1):
    y1, y2 = y[0], y[1]
    dy1 = y2
    if 30 < x < 40:
        dy2 = 10
    else:
        dy2 = -y2/x-k*y1-v*y2
    return [dy1, dy2]


parameters = {
    "size": 100,
    "y0": [0, 1],
    "minimum": 0.01,
    "maximum": 100, }
wave_solution = wave(parameters["minimum"],
                     parameters["maximum"],
                     parameters["size"],
                     parameters["y0"])
wave_solution.solve_PDE(df)
wave_solution.plot_graphics()
