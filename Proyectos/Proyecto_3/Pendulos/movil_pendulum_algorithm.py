from scipy.integrate import odeint
import matplotlib.pyplot as plt
from animation import *
import numpy as np


class double_pendulum:
    def __init__(self, pos_i, vel_i, theta_i, omega_i, m_1, m_2, lon, t_max, dt):
        self.pos_i = pos_i
        self.vel_i = vel_i
        self.theta_i = theta_i*np.pi/180
        self.omega_i = omega_i
        self.m_1 = m_1
        self.m_2 = m_2
        self.lon = lon
        self.time = np.arange(0, t_max+dt, dt)

    def initial_conditions(self):
        y0 = [self.pos_i, self.vel_i, self.theta_i, self.omega_i]
        return y0

    def resolve_ED(self, df, g):
        print("Resolviendo ecuacion diferencial")
        y0 = self.initial_conditions()
        self.solve = odeint(df, y0, self.time,
                            args=(self.m_1, self.m_2, self.lon, g))

    def plot_velocity_and_position(self):
        fig, (ax1, ax2) = plt.subplots(2, 1)
        axs = [ax1, ax2]
        data_list = [[self.solve[:, 0], self.solve[:, 2]],
                     [self.solve[:, 1], self.solve[:, 3]]]
        ylabels = ["Angulo ($\Theta$)", "Velocidad angular ($\omega$)"]
        for ax, data, ylabel in zip(axs, data_list, ylabels):
            ax.set_xlim(0, self.time.max())
            ax.set_ylabel(ylabel)
            ax.plot(self.time, data[0], label="Péndulo 1", color="purple")
            ax.plot(self.time, data[1], label="Péndulo 2", color="black")
            if ax == ax1:
                ax1.set_xticks([])
                ax.legend(frameon=False, ncol=2, bbox_to_anchor=(
                    0, 1, 1, 0.02), mode="expand")
        plt.show()
        plt.clf()

    def create_animation(self, path=""):
        # Se realizara la animación
        self.k = np.size(self.solve[:, 0])
        self.x1 = self.solve[:, 0]
        self.x2 = self.x1 + self.lon*np.sin(self.solve[:, 2])
        self.y1 = 0
        self.y2 = -self.lon*np.cos(self.solve[:, 2])

        # Maximos y minimos del grafico
        self.ylim = [-self.solve.max()-0.3, 0.3]
        self.xlim = [self.x2.min()-0.3, self.x2.max()+0.3]
        # Graficamos el pendulo en el plano cartesiano
        print("Simulando y graficando la dinamica del pendulo doble")
        for i in range(self.k):
            self.plot_pendulum(path, i)
        make_animation(path=path,name="movil_pendulum")

    def plot_pendulum(self, path, i):
        name = "0"*(len(str(self.k))-len(str(i+1)))+str(i+1)
        x_lim_i,x_lim_f=self.xlim
        y_lim_i,y_lim_f=self.ylim
        plt.xlim(x_lim_i, x_lim_f)
        plt.ylim(y_lim_i, y_lim_f)
        plt.axis("off")
        plt.scatter(self.x1[i], 0, c="red")
        plt.plot([self.x1[i], self.x2[i]], [
                 0, self.y2[i]], ls="-", color='blue')
        plt.scatter(self.x2[i], self.y2[i], c="red")
        self.plot_past(i)
        plt.title('Tiempo: ' + str(round(self.time[i], 2)))
        plt.savefig(path+name+".png")
        plt.clf()

    def plot_past(self, i):
        for n in range(i):
            plt.plot([self.x1[n], self.x1[n+1]],
                     [0, 0], ls="--", color="green")
            plt.plot([self.x2[n], self.x2[n+1]], [self.y2[n], self.y2[n+1]],
                     ls="--", color="green")
