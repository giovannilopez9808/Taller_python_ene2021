# Este programa fue hecho por Jesus Eduardo Loera Casas
from simple_pendulum_algorithm import *
import numpy as np

# Definimos la funcion derivada


def df(y, t, lon, g, approx):
    # Se asiganan las condiciones iniciales
    theta, omega = y
    # Se definen las nuevas variables
    thetadot = omega
    # Se colocan las ecuaciones del movimiento en terminos de omega1 y omega2
    if approx:
        omega1dot = -g/lon*theta
    else:
        omegadot = -g/lon*np.sin(theta)
    return thetadot, omegadot


inputs = {
    "Theta inicial": 40,
    "Omega inicial": 0,
    "longitud": 2,
    "tiempo maximo": 10,
    "delta tiempo": 0.1,
    "gravedad": 9.81,
    "aproximacion": False,
}
system = simple_pendulum(inputs["Theta inicial"],
                         inputs["Omega inicial"],
                         inputs["longitud"],
                         inputs["tiempo maximo"],
                         inputs["delta tiempo"],
                         inputs["gravedad"],
                         inputs["aproximacion"],
                         )
system.solve_DE(df)
system.plot_velocity_and_position()
system.create_animation(path="Graphics/")
