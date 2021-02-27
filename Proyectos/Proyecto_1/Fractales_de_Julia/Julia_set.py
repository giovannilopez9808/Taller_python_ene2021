from algorithm import *
import numpy as np


def f(z, c):
    # Julia y Mandelbrot
    # return z**2+c
    return z**3+c
    # Biologic 1
    # return np.exp(z**2)+c
    # Biologic 2
    # return np.sinh(z)+c


# parameters = {
#     "size": 1000,
#     "c": -0.8,
#     "zmax": 3,
#     "kmax": 100,
#     "min": -2,
#     "max": 2,
#     "name": "mandelbrot"}

# parameters = {
#     "size": 1000,
#     "c":  0.291811+0.0144686j,
#     "zmax": 4,
#     "kmax": 100,
#     "min": -2,
#     "max": 2,
#     "name": "mandelbrot2"}

parameters = {
    "size": 1000,
    "c":  0.5+0.2j,
    "zmax": 4,
    "kmax": 10,
    "min": -2,
    "max": 2,
    "name": "mandelbrot3"}

# parameters = {
#     "size": 1000,
#     "c": -0.4+0.65j,
#     "zmax": 4,
#     "kmax": 100,
#     "min": -2,
#     "max": 2,
#     "name": "julia"}

# parameters = {
#     "size": 1000,
#     "c": 0.92j,
#     "zmax": 4,
#     "kmax": 1000,
#     "min": -2,
#     "max": 2,
#     "name": "julia2"}


# parameters = {
#     "size": 1000,
#     "c": -0.65,
#     "zmax": 100,
#     "kmax": 10,
#     "min": -5,
#     "max": 5,
#     "name": "biologic"}

# parameters = {
#     "size": 1000,
#     "c": -0.65,
#     "zmax": 100,
#     "kmax": 10,
#     "min": -5,
#     "max": 5,
#     "name": "biologic2"}

julia_image = julia(parameters["size"],
                    parameters["c"],
                    parameters["zmax"],
                    parameters["kmax"],
                    parameters["min"],
                    parameters["max"])
julia_image.interact_system(f)
julia_image.image = np.transpose(julia_image.image)
julia_image.plot_system(parameters["name"])
