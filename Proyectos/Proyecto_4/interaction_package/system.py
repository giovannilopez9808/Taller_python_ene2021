from .potential_list import *
from .conditions import *
import numpy as np


class gas():
    def __init__(self, ngrx, T, rho, dt, walks, n_print, nn=14, path=""):
        self.gr = np.zeros(ngrx)
        self.ngr = ngrx
        self.T = T
        self.dens = rho
        self.a = (4/self.dens)**(1/2)
        self.nn = nn
        self.n = 4*self.nn**2
        self.l = self.nn*self.a
        self.hgr = self.l/(2*self.ngr)
        self.dt = dt
        self.walks = walks
        self.ec = 0
        self.u = 0
        self.ap = 0
        self.epot = 0
        self.ekin = 0
        self.print = n_print
        self.positions = np.zeros((self.n, 2))
        self.velocities = np.random.random((self.n, 2))*2-1
        self.forces = np.zeros((self.n, 2))
        self.path = path

    def init_system(self):
        self.init_force()
        self.init_velocities()
        self.fcc_implementation()

    def init_force(self):
        self.forces = np.zeros((self.n, 2))

    def init_velocities(self):
        self.velocities *= int(3*self.T)

    def fcc_implementation(self):
        self.positions = fcc_lattice(self.positions, self.a, self.nn, self.l)

    def forces_calc(self, i, j, rr, xx, yy, r2):
        fxx = rr*xx
        fyy = rr*yy
        self.ap += rr*r2
        self.forces[i] += [fxx, fyy]
        self.forces[j] -= [fxx, fyy]

    def simulation(self, name="energy_results.csv"):
        file_energy = open(self.path+name, "w")
        for k in range(self.walks):
            print("Simulación en el paso ",k+1," de ",self.walks,self.ekin/(3*self.n),self.epot/(self.n*self.n))
            self.positions = periodic_boundary(self.positions, self.l)
            self.init_force()
            self.potential_calc()
            self.kinetic_calc()
            self.write_file_energy(k, file_energy)
        self.gr = histogram_values(
            self.positions, self.n, self.l, self.gr, self.hgr)
        write_histogram_file(self.ngr, self.hgr, self.walks,
                             self.n, self.gr, self.l, self.path)
        file_energy.close()

    def potential_calc(self):
        for i in range(self.n-1):
            xi, yi = self.positions[i]
            for j in range(i+1, self.n):
                xj, yj = self.positions[j]
                xx = xi-xj
                yy = yi-yj
                [xx, yy] = minium_image_convencion([xx, yy], self.l)
                r2 = xx**2+yy**2
                rr, self.u, self.epot = LJ(r2, self.u, self.epot)
                self.forces_calc(i, j, rr, xx, yy, r2)

    def kinetic_calc(self):
        for i in range(self.n):
            vi = self.velocities[i]+self.dt*self.forces[i]
            vxx, vyy = 0.5*(vi+self.velocities[i])
            en = vxx**2+vyy**2
            self.ekin += en
            self.ec += en
            self.velocities[i] = vi
            self.positions += self.dt*self.velocities[i]

    def write_file_energy(self, walk, file):
        if walk % self.print == 0:
            self.write_file_energy_format(walk, file)

    def write_file_energy_format(self, walk, file):
        file.write(str(walk)+","+str(self.ekin/(3*self.n))+"," +
                   str(self.epot/(self.n*self.n))+","+str(self.ap/(3*self.l**2))+"\n")
