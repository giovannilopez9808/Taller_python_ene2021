import matplotlib.pyplot as plt
import numpy as np


class julia():
    def __init__(self, size, c, zmax, kmax, min, max):
        self.size = size
        self.c = c
        self.zmax = zmax
        self.kmax = kmax
        self.min = min
        self.max = max
        self.init_system()

    def init_system(self):
        self.values = np.linspace(self.min, self.max, self.size)
        self.image = np.zeros((self.size, self.size))

    def julia_algorithm(self, f, z):
        self.k = 0
        while abs(z) <= self.zmax and self.k < self.kmax:
            z = f(z, self.c)
            self.k += 1
        return self.k

    def interact_system(self, f):
        for x, i in zip(self.values, range(self.size)):
            for y, j in zip(self.values, range(self.size)):
                z = complex(x, y)
                self.image[i, j] = self.julia_algorithm(f, z)
        self.image = self.image/np.max(self.image)

    def plot_system(self, name="image", path=""):
        plt.axis("off")
        plt.subplots_adjust(left=0, bottom=0.05, right=1, top=0.95)
        plt.imshow(self.image, cmap="inferno")
        plt.savefig(path+name+".png", bbox_inches="tight",
                    pad_inches=0, dpi=400)
