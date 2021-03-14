import matplotlib.pyplot as plt
import numpy as np


class system:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.len_x = len(x)
        self.len_y = len(y)
        self.charges = []

    def append_particles(self, q, r):
        particle = charge(q, r)
        self.charges.append(particle)

    def calc_field(self):
        self.field = np.zeros((2, self.len_x, self.len_y))
        for i in range(self.len_x):
            for j in range(self.len_y):
                r_i = [self.x[i], self.y[j]]
                for charge in self.charges:
                    charge.calc_field(r_i)
                    self.field[:, i, j] += charge.field

    def plot_field(self):
        self.plot_charges()
        plt.quiver(self.x, self.y, self.field[1], self.field[0],
                   units="width", pivot='mid')
        plt.show()

    def plot_charges(self):
        for charge in self.charges:
            y, x = charge.r
            plt.scatter(x, y, color="red")


class charge:
    def __init__(self, q, r):
        self.r = np.array([r[1], r[0]])
        self.q = q

    def calc_field(self, r_i):
        r_i = np.array(r_i)
        dr = self.r-r_i
        norm = np.linalg.norm(dr)
        self.field = -self.q*dr/norm**3


inputs = {
    "limits": 6,
    "delta": 0.25,
}
x = np.arange(-inputs["limits"],
              inputs["limits"]+inputs["delta"],
              inputs["delta"],)
y = np.arange(-inputs["limits"],
              inputs["limits"]+inputs["delta"],
              inputs["delta"],)
system = system(x, y)
system.append_particles(1, [0, 3])
system.append_particles(-1, [0, -2])
# system.append_particles(1, [-2, 2])
# system.append_particles(-1, [-2, -2])
system.calc_field()
system.plot_field()
