from scipy.integrate import odeint
import matplotlib.pyplot as plt
from animation import *
import numpy as np


class simple_pendulum:
    def __init__(self, theta_i, omega_i, lon, t_max, dt, g, approx):
        self.y0 = [theta_i*np.pi/180, omega_i*np.pi/180]
        self.lon = lon
        self.t = np.arange(0, t_max+dt, dt)
        self.g = g
        self.approx = approx

    def solve_DE(self, df):
        self.solve = odeint(df, self.y0, self.t, args=(
            self.lon, self.g, self.approx))
        self.x = self.lon*np.sin(self.solve[:, 0])
        self.y = -self.lon*np.cos(self.solve[:, 0])

    def plot_velocity_and_position(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        plt.xlabel("Tiempo (s)")
        plt.xlim(self.t.min(), self.t.max())
        ax1.set_title("Angulo ($\\theta$)")
        ax1.plot(self.t, self.solve[:, 0])
        ax2.set_title("Velocidad angular")
        ax2.plot(self.t, self.solve[:, 1])
        plt.show()

    def create_animation(self, path=""):
        self.k = np.size(self.solve[:, 0])
        self.y_lim_i, self.y_lim_f = [-self.lon-0.3, 0.3]
        self.x_lim_i, self.x_lim_f = [self.x.min()-0.3, self.x.max()+0.3]
        print("Simulando y graficando la dinamica del pendulo simple")
        for i in range(self.k):
            self.plot_pendulum(path, i)
        make_animation(path=path, name="simple_pendulum")

    def plot_pendulum(self, path, i):
        name = "0"*(len(str(self.k))-len(str(i+1)))+str(i+1)+".png"
        plt.xlim(self.x_lim_i, self.x_lim_f)
        plt.ylim(self.y_lim_i, self.y_lim_f)
        plt.axis("off")
        plt.scatter(self.x[i],  self.y[i], c="red")
        plt.plot([0, self.x[i]], [0, self.y[i]], c="blue", ls="-")
        self.plot_past(i)
        plt.title("Tiempo "+str(round(self.t[i], 2)))
        plt.savefig(path+name)
        plt.clf()

    def plot_past(self, i):
        for n in range(i):
            alpha = calc_alpha(n, i)
            plt.plot([self.x[n], self.x[n+1]],
                     [self.y[n], self.y[n+1]], c="green", ls="--", alpha=alpha)
