import numpy as np
import matplotlib.pyplot as plt
import datetime
from os import listdir
import matplotlib.pyplot as plt
import moviepy.editor as mp
import math
import imageio
import os,sys
import time
def image(walk_real,pos_x,pos_y,walk):
    plt.yticks([]);plt.xticks([])
    plt.title("Walk N="+str(int(walk_real)))
    plt.scatter(pos_x,pos_y,c="#560bad",marker=".")
    plt.savefig(str(walk+1)+".png")
    plt.clf()
#<------------------------Funcion para generar el gif---------------------------->
def create_gif(filenames, duration):
	images = []
	for filename in filenames:
		images.append(imageio.imread(filename))
	output_file='dim.gif'
	imageio.mimsave(output_file, images, duration=duration)
#<---------------------Direccion de los archivos-------------------------->
dir_results="../Results/";dir_graphics="../Graphics/"
n=1
for i in range(n):
    #<---------------------------------Numero de particulas------------------------->
    pos_x,pos_y=np.loadtxt(dir_results+"5_Cor_in_"+str(i)+".dat",usecols=[1,2],unpack=True)
    image(0,pos_x,pos_y,-1)
    n_part=np.size(np.loadtxt(dir_results+"5_Cor_in_"+str(i)+".dat",usecols=0))
    #<----------------------------------Pasos-------------------------------->
    walks=np.loadtxt(dir_results+"8_T_U_P_0.dat",usecols=0)
    #<---------------------------Numero de pasos---------------------------->
    n_walks=np.size(walks)
    print("Creando graficas")
    for walk,walk_real in zip(range(n_walks),walks):
        #<--------------------------------Lectura de las posiciones------------------------------------->
        pos_x,pos_y=np.loadtxt(dir_results+"3_coor_"+str(i)+".dat",unpack=True,usecols=[0,1],skiprows=walk*(n_part+1)+1,max_rows=n_part)
        image(walk_real,pos_x,pos_y,walk)
    print("Creando gif")
    duration = 0.1
    #<-------------------------Nombres de las graficas--------------------------------->
    filenames = sorted(filter(os.path.isfile, [x for x in os.listdir() if x.endswith(".png")]), key=lambda p: os.path.exists(p) and os.stat(p).st_mtime or time.mktime(datetime.now().timetuple()))
    #<---------------------------Creacion del gif-------------------------->
    create_gif(filenames, duration)
    #<----------------------------Eliminacion de las grafias residuales--------------->
    os.system("rm *.png")
    clip = mp.VideoFileClip("dim.gif")
    os.system("rm *.gif")
    clip.write_videofile(dir_graphics+"video"+str(i)+".mp4")