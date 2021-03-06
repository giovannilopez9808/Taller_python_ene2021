import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
data_solution = pd.read_csv("Datos/solution.csv")
data_map = np.loadtxt("Datos/map_data.csv", delimiter=",")
print(data_map)
fig, (ax1, ax2) = plt.subplots(1, 2)
# Grafica de la izquierda
ax1.plot(data_solution["R"], data_solution["Solution"])
# Eliminacion de las etiquetas de la grafica dererecha
ax2.axis("off")
ax2.contourf(data_map, cmap="inferno_r")
plt.savefig("circulos.png", transparent=False)
plt.show()
