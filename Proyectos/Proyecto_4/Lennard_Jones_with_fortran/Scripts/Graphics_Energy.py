import matplotlib.pyplot as plt
import numpy as np
inputs = {
    "path results": "../Results/",
    "path graphics": "../Graphics/",
    "colors": ["b76935",
               "a56336",
               "935e38",
               "6f523b",
               "5c4d3c",
               "4a473e",
               "38413f",
               "263c41",
               "143642"],
    "repeat number": 9,
}
# <-------------Divisiones de las graficas---------------------------->
fig, axs = plt.subplots(3,
                        inputs["repeat number"]//3,
                        figsize=(12, 8),
                        sharex=True,
                        sharey=True)
axs = np.reshape(axs,
                 inputs["repeat number"])
for i, ax, color in zip(range(inputs["repeat number"]),
                        axs,
                        inputs["colors"]):
    # <------------------Lectura de los datos------------------------->
    walks, e_pot = np.loadtxt("{}8_T_U_P_{}.dat".format(inputs["path results"],
                                                        i),
                              unpack=True,
                              usecols=[0, 2])
    ax.plot(walks, e_pot,
            color="#{}".format(color))
    ax.set_xlim(0, 2e5)
    ax.set_title("Simulacion N$^\circ${}".format(i+1))
    ax.set_xticks(np.arange(0, 2e5+0.4e5, 0.4e5))
    ax.set_xticklabels(np.round(np.arange(0, 2+0.4, 0.4), 2))
    ax.grid(ls="--",
            color="#000000",
            alpha=0.5)
fig.text(0.5,
         0.04,
         'Walks (10$^{5}$)',
         ha='center',
         fontsize=13)
fig.text(0.04, 0.5,
         'U(10^{-2})',
         va='center',
         rotation='vertical',
         fontsize=13)
plt.subplots_adjust(left=0.107,
                    bottom=0.11,
                    right=0.945,
                    top=0.952,
                    wspace=0.105,
                    hspace=0.214)
plt.savefig("{}energy.png".format(inputs["path graphics"]),
            dpi=200)
plt.show()
