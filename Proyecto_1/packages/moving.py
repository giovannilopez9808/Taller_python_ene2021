import numpy as np


class game:

    def __init__(self, dim, lim):
        self.dim = dim
        self.lim = lim
        self.values = np.random.rand(self.dim, self.dim)

    def create(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if self.values[i, j] >= self.lim:
                    self.change_values(i, j, 1)
                else:
                    self.change_values(i, j, 0)

    def rules(self, i, j):
        value = self.values[i, j]
        live = np.sum(self.values[i-1:i+2, j-1:j+2])-value
        var = value
        if value == 1:
            if not(live in [2, 3]):
                var = 0
        else:
            if live == 3:
                var = 1
        return var

    def change_values(self, i, j, value):
        self.values[i, j] = value

    def copiar(self):
        return self
