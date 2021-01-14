def LJ(r2,u,epot,cut=2.5**2):
    r1=1/r2
    r6=r1**3
    pot=4*r6*(r6-1)
    u+=pot
    epot+=pot
    rr=48*r6*r1*(r6-0.5)
    return rr,u,epot