from algorithm import *
import numpy as np


def f(z, c):
    return np.sinh(z)+c
    # return np.exp(z**2)+c


parameters = {
    "size": 1000,
    "c": -0.65,
    "zmax": 100,
    "kmax": 10,
    "min": -5,
    "max": 5, }

julia_image = julia(parameters["size"],
                    parameters["c"],
                    parameters["zmax"],
                    parameters["kmax"],
                    parameters["min"],
                    parameters["max"])
julia_image.interact_system(f)
julia_image.plot_system()
