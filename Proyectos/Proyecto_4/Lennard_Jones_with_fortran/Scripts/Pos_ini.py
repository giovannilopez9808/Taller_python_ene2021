import numpy as np
import matplotlib.pyplot as plt
#<----------------------------Direcciones de los archivos-------------------->
dir_results="../Results/";dir_graphics="../Graphics/"
colors=["b76935","a56336","935e38","6f523b","5c4d3c","4a473e","38413f","263c41","143642"]
#<-_----------------------Grafica de la energía--------------------------------->
n=9
#<-------------Divisiones de las graficas---------------------------->
fig,axs=plt.subplots(3,3,figsize=(10,8))
axs=np.reshape(axs,9)
for i,ax,color in zip(range(n),axs,colors):
    #<------------------Lectura de los datos------------------------->
    pos_x,pos_y=np.loadtxt(dir_results+"5_Cor_in_"+str(i)+".dat",unpack=True,usecols=[1,2])
    ax.plot(pos_x,pos_y,color="#"+color)
    ax.scatter(pos_x,pos_y,color="black",marker=".")
    ax.set_title("Simulacion N$^{\circ}$"+str(i+1))
    ax.set_xticks([]);ax.set_yticks([])
plt.subplots_adjust(left=0.03,bottom=0.045,right=0.98,top=0.952,wspace=0.105,hspace=0.214)
plt.savefig(dir_graphics+"pos_ini.png",dpi=200)