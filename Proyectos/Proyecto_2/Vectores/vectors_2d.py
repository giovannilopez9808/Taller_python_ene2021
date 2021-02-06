import matplotlib.pyplot as plt


class vectors_2d():
    def __init__(self, limits):
        self.vectors = []
        self.limits = limits

    def create_vector(self, p_i, p_f, color):
        self.vectors.append(vector_2d(p_i, p_f, color))

    def plot_vectors(self):
        lim_x_i, lim_x_f = self.limits[0]
        lim_y_i, lim_y_f = self.limits[1]
        for vector in self.vectors:
            vector.plot()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.xlim(lim_x_i, lim_x_f)
        plt.ylim(lim_y_i, lim_y_f)
        plt.grid()
        plt.show()


class vector_2d():
    def __init__(self, p_i, p_f, color):
        self.p_i = p_i
        self.p_f = p_f
        self.color = color

    def plot(self):
        x_i, y_i = self.p_i
        x_f, y_f = self.p_f
        color = self.color
        plt.quiver(x_i, y_i, x_f, y_f, angles='xy',
                   scale_units='xy', scale=1, color=color)
