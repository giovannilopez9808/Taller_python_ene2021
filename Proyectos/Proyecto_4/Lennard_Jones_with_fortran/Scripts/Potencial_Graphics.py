import numpy as np
import matplotlib.pyplot as plt
#<-----------------------------Potencial--------------------->
def potential_lj(r,e,sigma):
    v=4*e*((sigma/r)**12-(sigma/r)**6)
    return v
#<----------------------------Fuerza--------------------->
def force_lj(r,e,sigma):
    f=4*e*(12*sigma**12/r**13-6*sigma**6/r**7)
    return f
#
def potencial_fene(r,e,ra):
    k=10*e
    v=-k*ra**2*np.log(1-(r/ra)**2)/2
    return v
#
def force_fene(r,e,ra):
    k=10*e
    f=k*r/((1-(r/ra)**2))
    return f
#
def graphic(r,sum,lj,fene,ylim,label,name):
    #<----------------------------Direcciones de los archivos-------------------->
    dir_graphics="../Graphics/"
    plt.xlim(r[0],1.3);plt.ylim(-5,ylim)
    plt.plot(r,sum,lw=3,color="#7400b8",label=label+"$(r)$")
    plt.plot(r,lj,lw=3,color="#5390d9",label=label+"$_{LJ}$",ls="--")
    plt.plot(r,fene,lw=3,color="#64dfdf",label=label+"$_{FENE}$",ls="--")
    plt.ylabel(label+"(r)");plt.xlabel("Distancia radial (r)")
    plt.legend(frameon=False,ncol=1,loc="upper center",fontsize=12)
    plt.subplots_adjust(left=0.121,bottom=0.11,right=0.924,top=0.943)
    plt.savefig(dir_graphics+name+".png")
    plt.clf()

#<------------------------Parametros-------------------->
sigma=1;e=1;ra=1.3
#<------------------------------Valores para el radio---------------------->
r=np.arange(0.8,1.29+0.01,0.01);n=np.size(r)
v=np.zeros(np.size(r));v_lj=np.zeros(np.size(r));v_fene=np.zeros(np.size(r))
f=np.zeros(np.size(r));f_lj=np.zeros(np.size(r));f_fene=np.zeros(np.size(r))
#<----------------------------Potencial-------------------->
for i in range(n):
    r_i=r[i]
    if r_i<2.5:
        v_lj[i]+=potential_lj(r_i,e,sigma)
        f_lj[i]+=force_lj(r_i,e,sigma)
        if r_i<ra:
            v_fene[i]+=potencial_fene(r_i,e,ra)
            f_fene[i]+=force_fene(r_i,e,ra)
v=v_lj+v_fene
f=f_lj+f_fene
graphic(r,v,v_lj,v_fene,30,"V","potential")
graphic(r,f,f_lj,f_fene,150,"F","force")