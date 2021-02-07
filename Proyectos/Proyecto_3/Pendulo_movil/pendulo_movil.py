# Este programa fue hecho por Jesus Eduardo Loera Casas
# con aportaciones de Giovanni López

# Importamos las librerías que vamos a necesitar
from double_pendulum_algorithm import *


def df(y, t, m1, m2, l1, g):
    # Se asiganan las condiciones iniciales
    x1, v1, theta1, omega1 = y
    # Se definen las nuevas variables
    x1dot = v1
    theta1dot = omega1
    # Se colocan las ecuaciones del movimiento en terminos de omega1 y omega2
    v1dot = ((m2*l1*np.cos(theta1)*(-(g*np.sin(theta1)/l1)) + m2*l1 *
              np.sin(theta1)*omega1**2)*(-1))/((m1+m2)-m2*(np.cos(theta1)**2))
    omega1dot = ((m2*np.sin(theta1)*np.cos(theta1)*(omega1**2))/(m1+m2) -
                 g*np.sin(theta1)/l1)/(1-(m2 * (np.cos(theta1))**2)/(m1+m2))
    return x1dot, v1dot, theta1dot, omega1dot


# Pedimos al usuario las condiciones iniciales del problema
input = {
    "posicion inicial 1": 2,
    "velocidad inicial 1": 0,
    "angulo inicial 1": 45,
    "angulo inicial 2": 0,
    "masa 1": 2,
    "masa 2": 2,
    "longitud": 2,
    "tiempo maximo": 40,
    "delta tiempo": 0.1,
}

system = double_pendulum(
    input["posicion inicial 1"],
    input["velocidad inicial 1"],
    input["angulo inicial 1"],
    input["angulo inicial 2"],
    input["masa 1"],
    input["masa 2"],
    input["longitud"],
    input["tiempo maximo"],
    input["delta tiempo"],
)
system.resolve_ED(df, g=9.81)
system.plot_velocity_and_position()
system.create_animation(path="Graphics/")