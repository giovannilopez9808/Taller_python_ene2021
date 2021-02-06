# Este programa fue elaborado por Jesús Loera

# GRAFICADORA DE VECTORES EN EL PLANO
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class colors:
    def __init__(self):
        self.blue = '#00bbf9'
        self.green = '#38b000'
        self.red = '#e71d36'
        self.purple = '#5a189a'


class vector_2d():
    def __init__(self, p_i, p_f, color):
        self.p_i = p_i
        self.p_f = p_f
        self.color = color

    def plot(self):
        x_i, y_i = self.p_i
        x_f, y_f = self.p_f
        color = self.color
        plt.quiver(x_i, x_f, y_i, y_f, angles='xy',
                   scale_units='xy', scale=1, color=color)


class vector_3d(vector_2d):
    def __init__(self, p_i, p_f, color):
        super().__init__(p_i, p_f, color)

    def plot(self, ax):
        x_i, y_i, z_i = self.p_i
        x_f, y_f, z_f = self.p_f
        color = self.color
        ax.quiver(x_i, y_i, z_i,
                  x_f, y_f, z_f, length=1, color=color)
    #########################################################################

    # Creemos las funciones que nos ayudarán a gráficar


def plot_vectors_3D(vectors, limits):
    lim_x_i, lim_x_f = limits[0]
    lim_y_i, lim_y_f = limits[1]
    lim_z_i, lim_z_f = limits[2]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.axes.set_xlim3d(left=lim_x_i, right=lim_x_f)
    ax.axes.set_ylim3d(bottom=lim_y_i, top=lim_y_f)
    ax.axes.set_zlim3d(bottom=lim_z_i, top=lim_z_f)
    for vector in vectors:
        vector.plot(ax)
    plt.grid()
    plt.show()


def plot_vectors_2D(vectors, limits):
    lim_x_i, lim_x_f = limits[0]
    lim_y_i, lim_y_f = limits[1]
    for vector in vectors:
        vector.plot()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(lim_x_i, lim_x_f)
    plt.ylim(lim_y_i, lim_y_f)
    plt.grid()
    plt.show()


colors = colors()
################### GRAFICADOR EN 2D ###################


# Creamos la lista de vectores a gráficar en el plano


#              origen   cabeza    color
#               del       del      del
#              vector    vector   vector
vector1 = vector_2d([0, 0], [1, 1], colors.blue)
vector2 = vector_2d([0, 1], [2, 1], colors.red)
vector3 = vector_2d([0, 0], [2, 1], colors.purple)

# Añada en esta lista los vectores que va gráficar
vectors = [vector1, vector2, vector3]

#  LIMITES EN:       EJE X     EJE Y
limits = [[-3, 3], [-3, 3]]

# LLAMEMOS AL GRAFICADOR 2D
plot_vectors_2D(vectors, limits)

################### GRAFICADOR EN 3D ###################
# Creamos la lista de vectores a gráficar en el plano
#              origen    dimensiones    color
#               del         del          del
#              vector      vector       vector
vector1 = vector_3d([0, 0, 0], [1, 1, 1],    colors.blue)
vector2 = vector_3d([0, 0, 0], [2, 0, 0],    colors.green)
vector3 = vector_3d([0, 0, 0], [-1, -1, -1], colors.red)

# Añada en esta lista los vectores que va a gráficar
Vectores_3D = [vector1, vector2, vector3]

#  LIMITES EN:   EJE X     EJE Y    EJE Z
Limites_ejes_3D = [[-3, 3], [-3, 3], [-3, 3]]

# LLAMEMOS AL GRAFICADOR 3D
# COMENTAR ESTA LINEA EN CASO DE NO QUERER GRAFICAR EN 3D
plot_vectors_3D(Vectores_3D, Limites_ejes_3D)

#########################################################################
