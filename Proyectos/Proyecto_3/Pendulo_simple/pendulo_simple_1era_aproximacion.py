# -*- coding: utf-8 -*-

#Este programa fue hecho por Jesus Eduardo Loera Casas

#Importamos las librerías que vamos a necesitar
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import os,sys
import datetime
import imageio
from pprint import pprint
import time

#DEFINIMOS LAS FUNCIONES QUE VAMOS A USAR EN EL PROGRAMA

#Funcion para general el Gif
def create_gif(filenames, duration):

	images = []

	for filename in filenames:
		images.append(imageio.imread(filename))

	output_file='Gif.gif'
	imageio.mimsave(output_file, images, duration=duration) 
    
# Definimos la funcion derivada
def f(y,t,l1,g):

    # Se asiganan las condiciones iniciales
    theta1, omega1 = y

    # Se definen las nuevas variables
    theta1dot = omega1

    # Se colocan las ecuaciones del movimiento en terminos de omega1 y omega2
    omega1dot = -g/l1*theta1

    return theta1dot, omega1dot

#Pedimos al usuario las condiciones iniciales del problema
theta1_i = 2
omega1_i = 0
l1 = 2
g = 9.81
tmax = 10
dt = 0.1

#Intervalo total de tiempo como un arreglo

t=np.arange(0.00, tmax+dt, dt)

#Condiciones iniciales
theta1_i = theta1_i*np.pi/180.0
y0 = [theta1_i, omega1_i]

#Se resuelve la ecuacion diferencial usando odeint
print("Resolviendo ecuacion diferencial")
y = odeint(f, y0, t, args = (l1, g) )


#Se realizara la animación
k = len(y[:,0])
x1 = l1*np.sin(y[:,0])
y1 = -l1*np.cos(y[:,0])

# Graficamos las soluciones de la EDO
plt.xlabel("Tiempo (s)")
plt.ylabel("Angulo ($\Theta$)")
plt.plot(t,y[   :,0],label="Péndulo 1",color="purple")
plt.legend(frameon=False,ncol=2)
plt.show()
plt.clf()
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad angular ($\omega$)")
plt.plot(t,y[:,1],label="Péndulo 1",color="purple")
plt.legend(frameon=False,ncol=2)
plt.show()
plt.clf()

# Graficamos las soluciones de la EDO
plt.xlabel("Angulo ($\Theta$)")
plt.ylabel("Velocidad angular ($\Omega$)")
plt.plot(y[   :,0],y[   :,1],label="Péndulo 1",color="purple")
plt.legend(frameon=False,ncol=2)
plt.show()
plt.clf()

print(y[:,1].min(), y[:,1].max())
print(y[:,0].min(), y[:,0].max())


#Maximos y minimos del grafico
ylim = [ -l1-0.3, 0.3 ]
xlim = [ x1.min()-0.3, x1.max()+0.3 ]

#Graficamos el pendulo en el plano cartesiano

print("Simulando y graficando la dinamica del pendulo doble")

# for i in range (k):

#     plt.xlim( xlim[0], xlim[1] )
#     plt.ylim( ylim[0], ylim[1] )
#     plt.axis( "off" )
#     plt.scatter( x1[i], y1[i], c = "red" )
#     plt.plot( [ 0, x1[i] ], [ 0, y1[i] ], 'b-' )

#     for n in range(i): 
#         plt.plot( [ x1[n], x1[n+1] ], [ y1[n], y1[n+1] ], "g--" )

#     plt.title( 'Tiempo: ' + str(round(t[i],2)) )
#     plt.savefig( "figura" + str(i) + ".png" ) 
#     plt.clf()

# #Creamos el gif
# print("Creando Gif")
# script = sys.argv.pop(0)
# duration = 0.1
# filenames = sorted(filter(os.path.isfile, [x for x in os.listdir() if x.endswith(".png")]), key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or time.mktime(datetime.now().timetuple()))
# create_gif(filenames, duration)
