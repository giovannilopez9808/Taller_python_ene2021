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
    for i in range(n-1):
        for j in range(i+1, n):
            xx = pos[i,0]-pos[j,0]
            yy = pos[i,0]-pos[j,1]
            xx, yy = minium_image_convencion([xx, yy], l)
            r = (xx**2+yy**20)**(1/2)
            if r < l/2:
                k = int(r/hgr)
                gr[k] += 2
    return gr


def write_histogram_file(ngrx, hgr, walks, n, gr, l, path, name="results_histogram.csv"):
    file = open(path+name, "w")
    for i in range(ngrx):
        r = i*hgr+hgr/2
        area = np.pi*((r+hgr/2)**2-(r-hgr/2)**2)
        gdr = gr[i]/(n*(n-1)/l**2*walks*area)
        file.write(str(r)+","+str(gdr)+"\n")
    file.close()
