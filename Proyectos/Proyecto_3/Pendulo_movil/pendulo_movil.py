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
def f(y,t,m1,m2,l1,g):

    # Se asiganan las condiciones iniciales
    x1, v1, theta1, omega1 = y

    # Se definen las nuevas variables
    x1dot = v1
    theta1dot = omega1

    # Se colocan las ecuaciones del movimiento en terminos de omega1 y omega2
    v1dot = ((m2*l1*np.cos(theta1)*(-(g*np.sin(theta1)/l1)) + m2*l1*np.sin(theta1)*omega1**2)*(-1))/( (m1+m2)-m2*(np.cos(theta1)**2) )
    omega1dot=(( m2*np.sin(theta1)*np.cos(theta1)*(omega1**2) )/(m1+m2) - g*np.sin(theta1)/l1)/( 1-(m2* (np.cos(theta1))**2)/(m1+m2) ) 

    return x1dot, v1dot, theta1dot, omega1dot

#Pedimos al usuario las condiciones iniciales del problema
x1_i = 2
v1_i = 0
theta1_i = 45
omega1_i = 0
m1 = 2
m2 = 2
l1 = 2
g = 9.81
tmax = 40
dt = 0.1

#Intervalo total de tiempo como un arreglo

t=np.arange(0.00, tmax+dt, dt)

#Condiciones iniciales
theta1_i = theta1_i*np.pi/180.0
y0 = [x1_i, v1_i, theta1_i, omega1_i]

#Se resuelve la ecuacion diferencial usando odeint
print("Resolviendo ecuacion diferencial")
y = odeint(f, y0, t, args = (m1, m2, l1, g) )

#Graficamos las soluciones de la EDO
# plt.xlabel("Tiempo (s)")
# plt.ylabel("Angulo ($\Theta$)")
# plt.plot(t,y[   :,0],label="Péndulo 1",color="purple")
# plt.plot(t,y[:,2],label="Péndulo 2",color="black")
# plt.legend(frameon=False,ncol=2)
# plt.show()
# plt.clf()
# plt.xlabel("Tiempo (s)")
# plt.ylabel("Velocidad angular ($\omega$)")
# plt.plot(t,y[:,1],label="Péndulo 1",color="purple")
# plt.plot(t,y[:,3],label="Péndulo 2",color="black")
# plt.legend(frameon=False,ncol=2)
# plt.show()
# plt.clf()

#Se realizara la animación
k = len(y[:,0])
x1 = y[:,0]
x2 = x1 + l1*np.sin(y[:,2])
y1 = 0
y2 = -l1*np.cos(y[:,2])

print( x1, y1, x2, y2 )

#Maximos y minimos del grafico
ylim = [ -l1-0.3, 0.3 ]
xlim = [ x2.min()-0.3, x2.max()+0.3 ]

#Graficamos el pendulo en el plano cartesiano

print("Simulando y graficando la dinamica del pendulo doble")

for i in range (k):

    plt.xlim( xlim[0], xlim[1] )
    plt.ylim( ylim[0], ylim[1] )
    plt.axis( "off" )
    plt.scatter( x1[i], 0, c = "red" )
    plt.plot( [ x1[i], x2[i] ], [ 0, y2[i] ], 'b-' )
    plt.scatter( x2[i], y2[i], c = "red" )

    for n in range(i): 
        plt.plot( [ x1[n], x1[n+1] ], [ 0, 0 ], "g--" )
        plt.plot( [ x2[n], x2[n+1] ], [ y2[n], y2[n+1] ], "g--" )

    plt.title( 'Tiempo: ' + str(round(t[i],2)) )
    plt.savefig( "figura" + str(i) + ".png" ) 
    plt.clf()

#Creamos el gif
print("Creando Gif")
script = sys.argv.pop(0)
duration = 0.1
filenames = sorted(filter(os.path.isfile, [x for x in os.listdir() if x.endswith(".png")]), key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or time.mktime(datetime.now().timetuple()))
create_gif(filenames, duration)