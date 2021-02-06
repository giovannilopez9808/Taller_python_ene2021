# Este programa fue elaborado por Jesús Loera con aportaciones de Giovanni López
from vectors_2d import *
from vectors_3d import *

# GRAFICADORA DE VECTORES EN EL PLANO


class colors:
    def __init__(self):
        self.blue = '#00bbf9'
        self.green = '#38b000'
        self.red = '#e71d36'
        self.purple = '#5a189a'


colors = colors()
################### GRAFICADOR EN 2D ###################
limits = [[-3, 3], [-3, 3]]
vectors_2d = vectors_2d(limits)
<<<<<<< HEAD
vectors_2d.create_vector([0, 0], [1, 1], colors.blue)
vectors_2d.create_vector([1, 1], [1, 1], colors.red)
vectors_2d.create_vector([0, 0], [2, 0], colors.purple)
=======
vector1 = vectors_2d.create_vector([0, 0], [1, 1], colors.blue)
vector2 = vectors_2d.create_vector([1, 1], [1, 1], colors.red)
vector3 = vectors_2d.create_vector([0, 0], [2, 0], colors.purple)
>>>>>>> c76e2a81d5cbe75c58befeafa8d1b55ab1dd45fc
vectors_2d.plot_vectors()

################### GRAFICADOR EN 3D ###################
# limits = [[-3, 3], [-3, 3], [-3, 3]]
# vectors_3d = vectors_3d(limits)
# vector1 = vectors_3d.create_vector([0, 0, 0], [1, 1, 1],    colors.blue)
# vector2 = vectors_3d.create_vector([0, 0, 0], [2, 0, 0],    colors.green)
# vector3 = vectors_3d.create_vector([0, 0, 0], [-1, -1, -1], colors.red)
# vectors_3d.plot_vectors()
#########################################################################
