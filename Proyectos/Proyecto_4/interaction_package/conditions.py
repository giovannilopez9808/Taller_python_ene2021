import numpy as np


def fcc_lattice(pos, a, nn, l):
    sx = [0, 0.5, 0.5, 0]
    sy = [0, 0.5, 0, 0.5]
    sh = 0.01
    m = 0
    for i in range(nn):
        for j in range(nn):
            for k in range(4):
                pos[m, 0] = (i+sx[k]+sh)*a-l/2
                pos[m, 1] = (j+sy[k]+sh)*a-l/2
                m += 1
    return pos


def periodic_boundary(r, l):
    cond = np.abs(r) > l
    r[cond] += -l*np.array(r[cond]/l, dtype=int)
    return r


def minium_image_convencion(pos, l):
    for i in range(2):
        pos[i] += -l*int(pos[i]/l)
    return pos


def histogram_values(pos, n, l, gr, hgr):
    x, y = pos
    for i in range(n-1):
        for j in range(i+1, n):
            xx = x[i]-x[j]
            yy = y[i]-y[j]
            xx, yy = minium_image_convencion([xx, yy], l)
            r = (xx**2+yy**20)**(1/2)
            if r < l/2:
                k = int(r/hgr)
                gr[k] += 2
    return gr
