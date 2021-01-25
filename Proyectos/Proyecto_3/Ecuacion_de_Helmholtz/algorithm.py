from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np


class wave:
    def __init__(self, min, max, size, y0):
        self.min = min
        self.max = max
        self.size = size
        self.y0 = y0
        self.initialize_system()

    def initialize_system(self):
        self.r = np.sqrt(2)*np.linspace(self.min, self.max, self.size)
        self.map = np.zeros((2*self.size, 2*self.size))

    def solve_PDE(self, df):
        sol = odeint(df, self.y0, self.r)
        self.solution = sol[:, 0]
        self.fill_map()

    def fill_map(self):
        for i in range(self.size):
            pos_i = self.pos_values(i)
            for j in range(self.size):
                pos_j = self.pos_values(j)
                self.fill_pos(pos_i, pos_j, i, j)

    def pos_values(self, pos):
        return [self.size-pos, self.size+pos]

    def fill_pos(self, pos_i, pos_j, i, j):
        for ii in pos_i:
            for jj in pos_j:
                r_ij = (self.r[i]**2+self.r[j]**2)**(1/2)
                self.map[ii, jj] = self.fill_values(r_ij)

    def fill_values(self, r_ij):
        istrue = True
        n = 0
        value = 0
        while istrue and n < self.size:
            if r_ij-self.r[n] <= 0.001:
                value = self.solution[n]
                istrue = False
            else:
                n += 1
        return value

    def plot_graphics(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax2.axis("off")
        contour = ax2.contourf(self.map, cmap="inferno_r")
        ax1.plot(self.r, self.solution)
        fig.colorbar(contour)
        plt.show()
