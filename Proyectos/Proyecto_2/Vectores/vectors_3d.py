from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from vectors_2d import *


class vectors_3d(vectors_2d):
    def __init__(self, limits):
        super().__init__(limits)

    def create_vector(self, p_i, p_f, color):
        self.vectors.append(vector_3d(p_i, p_f, color))

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


class vector_3d(vector_2d):
    def __init__(self, p_i, p_f, color):
        super().__init__(p_i, p_f, color)

    def plot(self, ax):
        x_i, y_i, z_i = self.p_i
        x_f, y_f, z_f = self.p_f
        color = self.color
        ax.quiver(x_i, y_i, z_i,
                  x_f, y_f, z_f, length=1, color=color)
