import numpy as np
import matplotlib.pyplot as plt
#<---------------------Direccion de los archivos-------------------------->
dir_results="../Results/";dir_graphics="../Graphics/";version="3"
#<---------------------------------Numero de particulas------------------------->
n_part=np.size(np.loadtxt(dir_results+"5_Cor_in_"+version+".dat",usecols=0))
#<----------------------------------Pasos-------------------------------->
walks=np.loadtxt(dir_results+"8_T_U_P_"+version+".dat",usecols=0)
n=np.size(walks)
#<---------------------------Numero de pasos---------------------------->
pos_walks=[0,int(n/3),int(2*n/3),n-1]
n_walks=walks[pos_walks]
#<----------------------------Limite de las posiciones------------------------->
lim=np.arange(-30,35,5)
#<--------------------------------Reposicion de las particulas---------------------->
lim_real=np.arange(0,65,5)
fig, ((ax1,ax2),(ax3,ax4))=plt.subplots(2, 2,figsize=(10,8))
#<----------------------------Lista de axs------------------------->
axs=[ax1,ax2,ax3,ax4]
plt.subplots_adjust(left=0.057,right=0.964,bottom=0.064,top= 0.912)
print("Creando graficas")
for walk,walk_real,ax in zip(pos_walks,n_walks,axs):
    #<--------------------------------Lectura de las posiciones------------------------------------->
    pos_x,pos_y=np.loadtxt(dir_results+"3_coor_"+version+".dat",unpack=True,usecols=[0,1],skiprows=walk*(n_part+1)+1,max_rows=n_part)
    #<----------------------------Renombramiento de los bordes--------------------------_>
    ax.set_yticks([]);ax.set_xticks([])
    ax.set_title("Walk N="+str(int(walk_real)))
    ax.scatter(pos_x,pos_y,c="#6a040f",marker=".")
    ax.plot(pos_x,pos_y,color="#e85d04",ls="-")
plt.savefig(dir_graphics+"dim.png",dpi=200)