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

class vectors_2d():
    def __init__(self,limits):
        self.vectors=[]
        self.limits=limits

    def create_vector(self,p_i,p_f,color):
        self.vectors.append(vector_2d(p_i,p_f,color))
    
    def plot_vectors(self):
        lim_x_i, lim_x_f = self.limits[0]
        lim_y_i, lim_y_f = self.limits[1]
        for vector in self.vectors:
            vector.plot()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(lim_x_i, lim_x_f)
        plt.ylim(lim_y_i, lim_y_f)
        plt.grid()
        plt.show()

class vectors_3d(vectors_2d):
    def __init__(self,limits):
        super().__init__(limits)

    def create_vector(self,p_i,p_f,color):
        self.vectors.append(vector_3d(p_i,p_f,color))

    def plot_vectors(self):
        lim_x_i, lim_x_f = self.limits[0]
        lim_y_i, lim_y_f = self.limits[1]
        lim_z_i, lim_z_f = self.limits[2]
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.axes.set_xlim3d(left=lim_x_i, right=lim_x_f)
        ax.axes.set_ylim3d(bottom=lim_y_i, top=lim_y_f)
        ax.axes.set_zlim3d(bottom=lim_z_i, top=lim_z_f)
        for vector in self.vectors:
            vector.plot(ax)
        plt.grid()
        plt.show()


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


colors = colors()
################### GRAFICADOR EN 2D ###################
limits = [[-3, 3], [-3, 3]]
vectors_2d=vectors_2d(limits)
vector1 = vectors_2d.create_vector([0, 0], [1, 1], colors.blue)
vector2 = vectors_2d.create_vector([0, 1], [2, 1], colors.red)
vector3 = vectors_2d.create_vector([0, 0], [2, 1], colors.purple)
vectors_2d.plot_vectors()

################### GRAFICADOR EN 3D ###################
limits = [[-3, 3], [-3, 3], [-3, 3]]
vectors_3d=vectors_3d(limits)
vector1 = vectors_3d.create_vector([0, 0, 0], [1, 1, 1],    colors.blue)
vector2 = vectors_3d.create_vector([0, 0, 0], [2, 0, 0],    colors.green)
vector3 = vectors_3d.create_vector([0, 0, 0], [-1, -1, -1], colors.red)
vectors_3d.plot_vectors()
#########################################################################