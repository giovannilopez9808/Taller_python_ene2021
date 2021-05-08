import matplotlib.pyplot as plt
import numpy as np
inputs = {
    "path results": "../Results/",
    "path graphics": "../Graphics/",
    "file data number": 8,
}
# <---------------------Direccion de los archivos-------------------------->
dir_results = "../Results/"
dir_graphics = "../Graphics/"
version = "3"
# <---------------------------------Numero de particulas------------------------->
n_part = np.size(np.loadtxt("{}5_Cor_in_{}.dat".format(inputs["path results"],
                                                       inputs["file data number"]),
                            usecols=0))
# <----------------------------------Pasos-------------------------------->
walks = np.loadtxt("{}8_T_U_P_{}.dat".format(inputs["path results"],
                                             inputs["file data number"]),
                   usecols=0)
n = np.size(walks)
# <---------------------------Numero de pasos---------------------------->
pos_walks = [0, int(n/3), int(2*n/3), n-1]
n_walks = walks[pos_walks]
# <----------------------------Limite de las posiciones------------------------->
lim = np.arange(-30, 35, 5)
# <--------------------------------Reposicion de las particulas---------------------->
lim_real = np.arange(0, 65, 5)
fig, axs = plt.subplots(2, 2,
                        figsize=(10, 8))
# <----------------------------Lista de axs------------------------->
axs = np.reshape(axs, 4)
plt.subplots_adjust(top=0.944,
                    bottom=0.03,
                    left=0.02,
                    right=0.985,
                    hspace=0.148,
                    wspace=0.042)
print("Creando graficas")
for walk, walk_real, ax in zip(pos_walks, n_walks, axs):
    # <--------------------------------Lectura de las posiciones------------------------------------->
    pos_x, pos_y = np.loadtxt("{}3_coor_{}.dat".format(inputs["path results"],
                                                       inputs["file data number"]),
                              unpack=True,
                              usecols=[0, 1],
                              skiprows=walk*(n_part+1)+1,
                              max_rows=n_part)
    # <----------------------------Renombramiento de los bordes--------------------------_>
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("Walk N={}".format(walk_real))
    ax.scatter(pos_x, pos_y,
               c="#6a040f",
               marker=".")
    ax.plot(pos_x, pos_y,
            color="#e85d04",
            ls="-")
#plt.savefig(dir_graphics+"dim.png", dpi=200)
plt.show()
