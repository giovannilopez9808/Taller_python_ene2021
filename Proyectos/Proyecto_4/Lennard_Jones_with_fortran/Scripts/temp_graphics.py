import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import matplotlib.pyplot as plt
#<---------------------Direccion de los archivos-------------------------->
dir_results="../Results/";dir_graphics="../Graphics/"
colors=["b76935","a56336","935e38","6f523b","5c4d3c","4a473e","38413f","263c41","143642"]
n_part=50;n=9
fig,axs=plt.subplots(3,3,figsize=(12,8))
axs=np.reshape(axs,9)
for i,ax,color in zip(range(n),axs,colors):
    print("Calculando temperatura de "+str(i))
    #<----------------------------------Pasos-------------------------------->
    walks,ekin_list=np.loadtxt(dir_results+"8_T_U_P_"+str(i)+".dat",usecols=[0,1],unpack=True)
    file=open(dir_results+"temp_"+str(i)+".dat","w")
    for walk,ekin in zip(walks,ekin_list):
        temp=ekin/(3*n_part)
        file.write(str(walk)+" "+str(temp)+"\n")
    file.close()
    temp=np.loadtxt(dir_results+"temp_"+str(i)+".dat",usecols=1)
    print(np.round(np.mean(temp),4))
    ax.set_ylim(0.004,0.01)
    ax.set_xlim(0,2e5)
    ax.set_title("Simulacion N$^{\circ}$"+str(i+1))
    for j in np.arange(0.004,0.01+0.001,0.001):
        ax.plot([0,2e5],[j,j],ls="--",color="grey")
    for j in np.arange(0,2e5+0.4e5,0.4e5):
        ax.plot([j,j],[0.004,0.01],ls="--",color="grey")
    if ax in [axs[0],axs[3],axs[6]]:
        ax.set_yticks(np.arange(0.004,0.01+0.001,0.001))
        ax.set_yticklabels(np.arange(4,10+1,1))
    else:
        ax.set_yticks([])
    if ax in [axs[6],axs[7],axs[8]]:
        ax.set_xticks(np.arange(0,2e5+0.4e5,0.4e5))
        ax.set_xticklabels(np.round(np.arange(0,2+0.4,0.4),2))
    else:
        ax.set_xticks([])
    ax.plot(walks,temp,color="#"+color)
#<------------------------Label eje x---------------------------------------->
fig.text(0.5, 0.04, 'Walks (10$^{5}$)', ha='center',fontsize=13)
#<--------------------------Label en el eje y-------------------------------------------->
fig.text(0.04, 0.5, 'Temperatura (10$^{-3}$)', va='center', rotation='vertical',fontsize=13)
plt.subplots_adjust(left=0.107,bottom=0.11,right=0.945,top=0.952,wspace=0.105,hspace=0.214)
plt.savefig(dir_graphics+"temp.png",dpi=200)