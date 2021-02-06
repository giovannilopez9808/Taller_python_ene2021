# Este programa fue elaborado por Jesús Loera

# GRAFICADORA DE VECTORES EN EL PLANO

# Para el curso de Mecánica Teórica 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import linalg



############################### COLORES #################################
############################ DE VECTORES ################################

AZUL = 'b'
VERDE = 'g'
ROJO = 'r'
CELESTE = 'c'
MORADO = 'm'
AMARILLO = 'y'
NEGRO = 'k'

#########################################################################


# Creemos las funciones que nos ayudarán a gráficar

def Vectores3D(lista, limites ):

    size = len(lista)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.axes.set_xlim3d(left=limites[0][0], right=limites[0][1]) 
    ax.axes.set_ylim3d(bottom=limites[1][0], top=limites[1][1]) 
    ax.axes.set_zlim3d(bottom=limites[2][0], top=limites[2][1]) 

    for i in range (size):

        ax.quiver( lista[i][0][0] , lista[i][0][1] , lista[i][0][2], \
                    lista[i][1][0] , lista[i][1][1] , lista[i][1][2], length=1, color = lista[i][2] )

    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.show()

def Vectores2D(lista, limites):

    size = len(lista)
 

    for i in range (size):

        plt.quiver( lista[i][0][0] , lista[i][0][1] , \
                    lista[i][1][0] , lista[i][1][1], angles='xy', scale_units='xy', scale=1, color = lista[i][2] )

    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(limites[0][0],limites[0][1])
    plt.ylim(limites[1][0],limites[1][1])
    plt.grid()
    plt.show()


########################################################
########################################################

################### GRAFICADOR EN 2D ###################


# Creamos la lista de vectores a gráficar en el plano


#              origen   cabeza    color
#               del       del      del
#              vector    vector   vector
vector1_2D = ( [0, 0], [1, 1],    AZUL  )
vector2_2D = ( [1, 1], [1, 1],    ROJO  )
vector3_2D = ( [0, 0], [2 ,0 ],   NEGRO )


# Añada en esta lista los vectores que va gráficar
Vectores_2D = [ vector1_2D, vector2_2D, vector3_2D ]

#  LIMITES EN:       EJE X     EJE Y    
Limites_ejes_2D = [ [-3, 3], [-3, 3] ]


# LLAMEMOS AL GRAFICADOR 2D
Vectores2D(Vectores_2D, Limites_ejes_2D)       # COMENTAR ESTA LINEA EN CASO DE NO QUERER GRAFICAR EN 2D




########################################################
########################################################

################### GRAFICADOR EN 3D ###################

# Creamos la lista de vectores a gráficar en el plano


#              origen    dimensiones    color
#               del         del          del
#              vector      vector       vector
vector1_3D = ( [0, 0, 0], [1, 1, 1],    AZUL )
vector2_3D = ( [0, 0, 0], [2 ,0 ,0],    VERDE )
vector3_3D = ( [0, 0, 0], [-1, -1, -1], ROJO )

# Añada en esta lista los vectores que va a gráficar
Vectores_3D = [ vector1_3D, vector2_3D, vector3_3D ]


#  LIMITES EN:   EJE X     EJE Y    EJE Z
Limites_ejes_3D = [ [-3, 3], [-3, 3], [-3, 3] ]


# LLAMEMOS AL GRAFICADOR 3D
Vectores3D(Vectores_3D, Limites_ejes_3D)       # COMENTAR ESTA LINEA EN CASO DE NO QUERER GRAFICAR EN 3D


#########################################################################