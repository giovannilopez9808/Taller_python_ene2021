# Este programa fue elaborado por Jesús Loera con aportaciones de Giovanni López
from vectors_2d import *
from vectors_3d import *

# GRAFICADORA DE VECTORES EN EL PLANO


class colors_palette:
    def __init__(self):
        self.blue = '#00bbf9'
        self.green = '#38b000'
        self.red = '#e71d36'
        self.purple = '#5a189a'


colors = colors_palette()
################### GRAFICADOR EN 2D ###################
limits = [[-3, 3], [-3, 3]]
system_2d = vectors_2d(limits)
system_2d.create_vector([0, 0], [1, 1], colors.blue)
system_2d.create_vector([1, 1], [1, 1], colors.red)
system_2d.create_vector([0, 0], [2, 0], colors.purple)
system_2d.plot_vectors()
################### GRAFICADOR EN 3D ###################
limits = [[-3, 3], [-3, 3], [-3, 3]]
system_3d = vectors_3d(limits)
system_3d.create_vector([0, 0, 0], [1, 1, 1],    colors.blue)
system_3d.create_vector([0, 0, 0], [2, 0, 0],    colors.green)
system_3d.create_vector([0, 0, 0], [-1, -1, -1], colors.red)
system_3d.plot_vectors()
#########################################################################
