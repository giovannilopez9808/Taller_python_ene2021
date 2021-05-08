import numpy as np
from ase.atoms import Atoms
from ase.optimize import BFGS
from ase.build import bulk
from ase.dft.kpoints import *
from math import cos, sin, pi, sqrt
from ase.calculators.calculator import Calculator, all_changes
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from pymatgen.core import Structure
import time
import os

Bohr = 0.52917721
Ry = 13.60569253
Ha = 2*Ry


def struct2at(struct):
    formula = str(struct.composition.formula.replace(' ', ''))
    pos = struct.cart_coords
    cell = struct.lattice.matrix
    return Atoms(formula, positions=pos, cell=cell, pbc=True)


def at2struct(atoms):
    sp = atoms.get_chemical_symbols()
    pos = atoms.positions
    cell = atoms.cell
    return Structure(cell, sp, pos, coords_are_cartesian=True)


def super_cell(atoms, newsize):
    struct = at2struct(atoms)
    struct.make_supercell(newsize)
    return struct2at(struct)


class PWSCF (Calculator):
    implemented_properties = ['energy', 'forces']
    pwbindir = 'mpirun -np 4 /opt/quantumexpresso/bin/'
    pwexe = pwbindir+'pw.x'
    pseudodir = '/opt/verano2018/pseudos/'

    control_dic = {'calculation': 'scf',
                   'tprnfor': True,
                   'tstress': False,
                   'pseudo_dir': pseudodir}

    system_dic = {'ibrav': 0,
                  'nat': 0,
                  'ecutwfc': 30.0,
                  'ecutrho': 120.0,
                  'occupations': 'smearing',
                  'smearing': 'gauss',
                  'degauss': 0.001}

    electrons_dic = {'conv_thr': 1e-10}

    ions_dic = {'ion_dynamics': 'none'}

    cell_dic = {'cell_dynamics': 'none'}

    pseudos = []

    celldm = None

    kpts = np.array([1, 1, 1])
    kpts_flag = 'automatic'

    label = 'pwscf'
    constraint = None

    def __init__(self, **kwargs):
        Calculator.__init__(self, **kwargs)
        if 'system' in kwargs:
            self.system_dic.update(kwargs['system'])
        if 'control' in kwargs:
            self.control_dic.update(kwargs['control'])
        if 'electrons' in kwargs:
            self.electrons_dic.update(kwargs['electrons'])
        if 'ions' in kwargs:
            self.ions_dic.update(kwargs['ions'])
        if 'cell' in kwargs:
            self.cell_dic.update(kwargs['cell'])
        if 'label' in kwargs:
            self.label = kwargs['label']
        if 'pseudos' in kwargs:
            self.pseudos = kwargs['pseudos']
        if 'kpts' in kwargs:
            self.kpts = np.array(kwargs['kpts'])
        if 'kpts_flag' in kwargs:
            self.kpts_flag = kwargs['kpts_flag']

    def write_pw_input(self, atoms):

        f = open(self.label+'.in', 'w')

        self.control_dic.update({'title': self.label, 'prefix': self.label,
                                 'outdir': './'+self.label})

        f.write('&control\n')
        for k, v, in self.control_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')

        self.system_dic.update({'nat': atoms.get_number_of_atoms(),
                                'ntyp': len(set(atoms.get_chemical_symbols()))})

        # Find ibrav and celldm
        if self.celldm == None:
            res = self.sym_ibav_celldm(atoms)
            ibv = res[0]
        #    cdm = res[1]
            struct = at2struct(atoms)
        # else:
        #    res   = self.sym_ibav_celldm(atoms)
        #    ibv = res[0]
        #    cdm = self.celldm
        #    struct = res[2]

        # self.system_dic.update(cdm)
        # print ibv
        self.system_dic['ibrav'] = 0

        f.write('&system\n')
        for k, v, in self.system_dic.items():
            if type(v) == bool:
                if v:
                    line = "    {} = {},\n".format(k, '.true.')
                else:
                    line = "    {} = {},\n".format(k, '.false.')
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')

        f.write('&electrons\n')
        for k, v, in self.electrons_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')

        f.write('&ions\n')
        for k, v, in self.ions_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')

        f.write('&cell\n')
        for k, v, in self.cell_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')

        f.write('ATOMIC_SPECIES\n')
        for itype in self.pseudos:
            f.write('%s  %4.2f  %s \n' % (itype[0], itype[1], itype[2]))

        f.write('ATOMIC_POSITIONS crystal \n')
        # np.dot(atoms.positions,np.linalg.inv(atoms.cell))
        scaled = struct.frac_coords
        sp = atoms.get_chemical_symbols()
        if self.constraint == None:
            for iat in range(np.shape(scaled)[0]):
                f.write('%s  %12.9f %12.9f %12.9f \n' % (struct.species[iat].symbol, scaled[iat, 0],
                                                         scaled[iat, 1], scaled[iat, 2]))
        else:
            for iat in range(np.shape(scaled)[0]):
                f.write('%s  %12.9f %12.9f %12.9f %6.3f %6.3f %6.3f \n' % (struct.species[iat].symbol,
                                                                           scaled[iat, 0], scaled[iat,
                                                                                                  1], scaled[iat, 2],
                                                                           self.constraint[iat, 0,
                                                                                           ], self.constraint[iat, 1],
                                                                           self.constraint[iat, 2]))

        if self.system_dic['ibrav'] == 0:
            f.write('CELL_PARAMETERS angstrom \n')
            for ic in range(3):
                f.write('%12.9f %12.9f %12.9f \n' %
                        (atoms.cell[ic, 0], atoms.cell[ic, 1], atoms.cell[ic, 2]))

        f.write('K_POINTS '+self.kpts_flag+'\n')
        # print np.shape(kpts)[0]

        if self.control_dic['calculation'] == 'bands':
            kk = self.kpts[0]
            nkk = self.kpts[1]
            f.write('%3d \n' % (np.shape(kk)[0]))
            for ik in range(np.shape(kk)[0]):
                f.write('%12.9f %12.9f %12.9f %d \n' %
                        (kk[ik, 0], kk[ik, 1], kk[ik, 2], int(nkk[ik])))
        else:
            if np.shape(self.kpts.flatten())[0] == 3:
                f.write('%3d %3d %3d %3d %3d %3d' % (self.kpts[0], self.kpts[1], self.kpts[2],
                                                     0, 0, 0))
            else:
                f.write('%3d \n' % (np.shape(self.kpts)[0]))
                for ik in range(np.shape(self.kpts)[0]):
                    f.write('%12.9f %12.9f %12.9f  \n' % (
                        self.kpts[ik, 0], self.kpts[ik, 1], self.kpts[ik, 2]))

        f.close()

    def parse_E(self):
        import subprocess
        cmd = "grep '!' " + self.label + ".out  |tail -1 | awk '{print $5}'"
        E = subprocess.check_output(cmd, shell=True)
        E = float(E)*Ry
        return E

    def parse_Efermi(self):
        import subprocess
        try:
            cmd = "grep  'Fermi energy' "+self.label+".out |  awk '{print $5}'"
            Ef = subprocess.check_output(cmd, shell=True)
            Ef = float(Ef)
        except:
            print('No fermi energy found')
            Ef = 0

        return Ef

    def parse_numPW(self):
        import subprocess
        cmd = "cat "+self.label + \
            ".out | grep -A5 'Parallelization' | tail -1 |awk '{print $7}'"
        npw = subprocess.check_output(cmd, shell=True)
        npw = int(npw)
        return npw

    def parse_F(self, atoms):
        import subprocess
        outname = self.label+'.out'
        nats = atoms.get_number_of_atoms()
        cmd = "grep  'Forces' -A"+str(nats+1)+" " + outname+" "
        cmd += " | tail -"+str(nats)+" | awk '{print $7, $8, $9}'"
        force = subprocess.check_output(cmd, shell=True)
        force = np.array(force.split(), dtype=float)
        force = force.reshape(nats, 3)
        force = force*Ry/Bohr
        return force

    def parse_Stress(self):
        import subprocess
        outname = self.label+'.out'
        cmd = "grep  'total   stress' -A3 " + outname+" "
        cmd += " | tail -3 | awk '{print $1, $2, $3}'"
        stress = subprocess.check_output(cmd, shell=True)
        stress = np.array(stress.split(), dtype=float)
        stress = stress*Ry/(Bohr**3)
        stress = stress.reshape(3, 3)
        return stress

    def run_pw(self, verbose=False):
        import subprocess
        import time
        fname = self.label+'.in'
        outname = self.label+'.out'
        cmd = self.pwexe + ' -inp '+fname + '> '+outname
        if verbose:
            print(self.pwexe)
            print(self.label)
            print(cmd)
        t0 = time.time()
        subprocess.call(cmd, shell=True)
        t1 = time.time()
        if verbose:
            print('Elapsed time: ', t1-t0, 's')

    def get_bands(self, path):
        Ef = self.parse_Efermi()
        self.control_dic.update({'calculation': 'bands'})
        self.kpts_flag = 'crystal'
        self.kpts = path
        kpath = path[0]
        nk = np.shape(kpath)[0]

        self.write_pw_input(self.atoms)
        self.run_pw()

        Ene, ekn = self.treat_bands()

        nb = np.shape(ekn)[0]/nk
        ekn = ekn.reshape(nb, nk)
        self.control_dic.update({'calculation': 'scf'})

        return Ene[0:nk], ekn-Ef

    def treat_bands(self):
        import subprocess
        bandx = self.pwbindir+'bands.x'
        label = self.label
        bandfile = self.label+'_bands'
        outdir = './'+self.label+'/'
        bandin = label+'.bandx.in'
        f = open(bandin, 'w')
        band_dic = {'prefix': label,
                    'outdir': outdir,
                    'filband': bandfile,
                    'lsym': True}
        f.write('&bands\n')
        for k, v, in band_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')
        f.close()
        cmd = bandx+' <  '+bandin + '> log.bandx.out'
        subprocess.call(cmd, shell=True)
        data = np.loadtxt(bandfile+'.gnu')
        ene = data[:, 0]
        ekn = data[:, 1]
        return ene, ekn

    def phonons_gamma(self):
        import subprocess
        phx = 'mpirun -np 2 /home/ucl/naps/botello/codes/espresso-5.4.0/bin/ph.x'
        phin = self.label+'.phG.in'
        f = open(phin, 'w')
        ph_dic = {'prefix': self.label,
                  'outdir': './'+self.label,
                  'fildyn': self.label+'.dyn',
                  'tr2_ph': 1e-14,
                  'verbosity': 'high',
                  'asr': True,
                  }
        f.write(self.label+' \n')
        f.write('&inputph\n')
        for k, v, in ph_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')
        f.write('0.0 0.0 0.0\n')

        f.close()

        cmd = phx+' < '+phin + '> log.ph.out'

        subprocess.call(cmd, shell=True)

    def get_force_constants(self, atoms, qpts=None):
        import subprocess
        if qpts == None:
            qpts = self.kpts

        phx = 'mpirun -np 2 /home/ucl/naps/botello/codes/espresso-5.4.0/bin/ph.x'
        q2r = 'mpirun -np 2 /home/ucl/naps/botello/codes/espresso-5.4.0/bin/q2r.x'
        phin = self.label+'.phG.in'
        f = open(phin, 'w')
        ph_dic = {'prefix': self.label,
                  'outdir': './'+self.label,
                  'fildyn': self.label+'.dyn',
                  'tr2_ph': 1e-14,
                  'ldisp': True,
                  'nq1': qpts[0],
                  'nq2': qpts[1],
                  'nq3': qpts[2],
                  'verbosity': 'high',
                  'asr': True,
                  }
        f.write(self.label+' \n')
        f.write('&inputph\n')
        for k, v, in ph_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')
        f.close()

        cmd = phx+' < '+phin + '> log.ph.out'
        subprocess.call(cmd, shell=True)
        qr_dic = {'fildyn': self.label+'.dyn',
                  'zasr': 'simple',
                  'flfrc': self.label+'.fc'}

        fq = open(self.label+'_qr.in', 'w')
        fq.write('&input\n')
        for k, v, in qr_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            fq.write(line)
        fq.write('/\n \n')
        fq.close()

        cmd = q2r + ' < '+self.label + '_qr.in > log.qr.out'
        subprocess.call(cmd, shell=True)

        fcfile = open(self.label+'.fc', 'r')
        flines = fcfile.readlines()
        head = 13+atoms.get_number_of_atoms()+len(set(atoms.get_chemical_symbols()))

        qpts = []
        qpts = np.array([float(l) for l in flines[head].split()], dtype=int)
        flines = flines[head+1:]

        fcmat = np.zeros((3, 3, 2, 2, 64))
        il = 0
        while il < len(flines):
            indexes = np.array([float(l)
                                for l in flines[il].split()], dtype=int)
            idir = indexes[0]-1
            jdir = indexes[1]-1
            iat = indexes[2]-1
            jat = indexes[3]-1
            # print indexes, im, iat
            for ictr in range(1, 65):
                s = flines[il+ictr].split()
                indexes = np.array([float(l) for l in s[0:3]], dtype=int)
                jm = (indexes[0]-1)+(indexes[1]-1) * \
                    qpts[0]+(indexes[2]-1)*qpts[0]*qpts[1]
                val = float(s[3])*Ry/(Bohr**2)
                # print indexes, jm , val
                # print type(im), type(jm), type(iat)
                fcmat[idir, jdir, iat, jat, jm] = val
            il += 65

        return fcmat

    def conv_ecut(self, ethr=1e-3):
        def convfun(x, a, b):
            return a/x**3+b

        conv = False
        conv0 = False
        ecut = self.system_dic['ecutwfc']
        data = []
        E0 = 0
        ctr = 0
        asympt = 0

        print(u'        Ecut    #PWs  Energia total   dE = E_n-E_{n-1} ')
        while not conv:
            self.system_dic.update({'ecutwfc': ecut})
            self.system_dic.update({'ecutrho': ecut*4})
            self.write_pw_input(self.atoms)
            self.run_pw()
            E = self.parse_E()
            npw = self.parse_numPW()
            # if ctr > 3:
            #    popt, pcov = curve_fit(convfun, np.array(data)[-3:,0], np.array(data)[-3:,1])
            #    asympt = popt[1]
            dE = abs(E - E0)
            if (dE < ethr):
                if conv0:
                    conv = True
                else:
                    conv0 = True
            # else:
            #    dE = abs(E - E0)
            print('%12.1f  %6d  %12.6f   %12.6f' % (ecut, npw, E, dE))
            data.append([ecut, npw, E])
            ecut += 5
            ctr += 1
            E0 = E

        data = np.array(data)

        plt.figure(figsize=(10, 10))
        plt.plot(data[:, 1], data[:, 2], 'ko-')
        plt.plot([data[0, 1], data[-1, 1]], [E, E], 'b--')
        plt.xlabel('# de ondas planas', fontsize=15)
        plt.ylabel('Energia total (eV)', fontsize=15)
        plt.show()
        # return ecut, data

    def conv_kpts(self, ethr=1e-3, is2d=False):
        conv = False
        fconv = False
        conv0 = False
        fconv0 = False
        sconv = False
        sconv0 = False

        a = np.linalg.norm(self.atoms.cell[0, :])
        b = np.linalg.norm(self.atoms.cell[1, :])
        c = np.linalg.norm(self.atoms.cell[2, :])

        ecut = self.system_dic['ecutwfc']/2.0
        if is2d:
            kpts = np.array([2, 2, 1], dtype=int)
        else:
            kpts = np.array([2, 2, 2], dtype=int)

        self.kpts = kpts

        data = []
        E0 = 0
        F0 = 0
        S0 = 0
        ctr = 0
        print(u'    kpoints     Energia total   dE= E_n-E_{n-1} ')
        self.kpts_flag = 'automatic'
        while not conv:
            self.write_pw_input(self.atoms)
            self.run_pw()
            E = self.parse_E()
            dE = abs(E - E0)
            F = max(abs(self.parse_F(self.atoms).flatten()))
            dF = abs(F - F0)
            #S = max(abs(self.parse_Stress().flatten()))
            #dS = abs(S - S0)
            if (dE < ethr):
                if conv0:
                    conv = True
                else:
                    conv0 = True
            else:
                conv0 = False
            data.append([kpts[0], E, F])  # , S])
            print('%2d x %2d x %2d   %12.6f  %12.6f' %
                  (kpts[0], kpts[1], kpts[2], E, dE))
            if is2d:
                kpts += np.array([2, int(2*a/b), 0], dtype=int)
            else:
                kpts += np.array([2, int(2*a/b), int(2*a/c)], dtype=int)

            self.kpts = kpts

            ctr += 1
            E0 = E
        data = np.array(data)
        #kdata = np.array(data[:,0])
        # print kdata
        plt.figure(figsize=(10, 10))
        plt.plot(data[:, 0], data[:, 1], 'ko-')
        plt.plot([data[0, 0], data[-1, 0]], [E, E], 'b--')
        plt.xlabel(u'puntos $k$ ($n$ x $n$ x $n$) ', fontsize=15)
        plt.ylabel('Energia total (eV)', fontsize=15)
        plt.show()

        # return  kpts, data

    def get_dos(self, kpts, emin=-10, emax=10, deltaE=0.1, degauss=0.01):
        import subprocess

        dosx = self.pwbindir+'dos.x'
        Ef = self.parse_Efermi()
        self.kpts = kpts
        self.control_dic.update({'calculation': 'nscf'})
        self.write_pw_input(self.atoms)
        self.run_pw()

        dosin = self.label+'.dos.in'
        f = open(dosin, 'w')
        dos_dic = {'prefix': self.label,
                   'outdir': './'+self.label,
                   'fildos': self.label+'_dos.dat',
                   'degauss': degauss,
                   'Emin': emin+Ef,
                   'Emax': emax+Ef,
                   'DeltaE': deltaE}

        f.write(self.label+' \n')
        f.write('&dos\n')
        for k, v, in dos_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')
        f.close()

        cmd = dosx+' < ' + dosin + ' > dos.out'
        subprocess.call(cmd, shell=True)

        dosdata = np.loadtxt(self.label+'_dos.dat')
        dosdata[:, 0] = dosdata[:, 0]-Ef
        self.control_dic.update({'calculation': 'scf'})
        return dosdata

    def get_stm(self, bias=0.01, z=1.0, imx=1, imy=1, nx=200, ny=200):
        import subprocess

        ppx = self.pwbindir+'pp.x'
        Ef = self.parse_Efermi()

        ppin = self.label+'.pp.in'
        f = open(ppin, 'w')
        inputpp_dic = {'prefix': self.label,
                       'outdir': './'+self.label,
                       'filplot': self.label+'_stm.dat',
                       'plot_num': 5,
                       'sample_bias': bias/Ry}

        plot_dic = {'output_format': 7,
                    'iflag': 2,
                    'e1(1)': imx,
                    'e1(2)': 0,
                    'e1(3)': 0,
                    'e2(1)': 0,
                    'e2(2)': imy,
                    'e2(3)': 0,
                    'x0(1)': 0,
                    'x0(2)': 0,
                    'x0(3)': z/np.linalg.norm(self.atoms.cell[0, :]),
                    'nx': nx,
                    'ny': ny}

        f.write(self.label+' \n')
        f.write('&inputpp\n')
        for k, v, in inputpp_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')
        f.write('&plot\n')
        for k, v, in plot_dic.items():
            if type(v) == str:
                line = "    {} = '{}',\n".format(k, v)
            else:
                line = "    {} = {}, \n".format(k, v)
            f.write(line)
        f.write('/\n \n')
        f.close()

        cmd = ppx+' < ' + ppin + ' > pp.out'
        subprocess.call(cmd, shell=True)

        file1 = open("pp.out", "r")
        file2 = open("stm_data.dat", "w")
        always_print = False
        lines = file1.readlines()
        for line in lines:
            if "Plot Type" in line:
                always_print = False

            if always_print:

                file2.write(line)

            if "imaginary charge" in line:
                always_print = True

        file1.close()
        file2.close()

        #stmdata = np.loadtxt(self.label+'_stm.dat')
        stmdata = np.loadtxt('stm_data.dat')
        X = np.reshape(stmdata[:, 0], (nx, ny))
        Y = np.reshape(stmdata[:, 1], (nx, ny))
        Z = np.reshape(stmdata[:, 2], (nx, ny))

        return X*Bohr, Y*Bohr, Z

    def calculate(self, atoms=None, properties=['energy'],
                  system_changes=all_changes):

        Calculator.calculate(self, atoms, properties, system_changes)

        self.write_pw_input(atoms)

        self.run_pw()
        Ep = self.parse_E()
        F = self.parse_F(atoms)
#        s = self.parse_Stress()
        self.results['energy'] = Ep
        self.results['forces'] = F
#        self.results['stress']=s

    def parse_xml_relax(self):
        outdir = self.label+'/'
        label = self.label
        from xml.dom import minidom
        out = minidom.parse(outdir+label+'.save/data-file.xml')

        alat = np.zeros((3, 3))
        lv = out.getElementsByTagName('DIRECT_LATTICE_VECTORS')[0]
        a1 = lv.getElementsByTagName('a1')[0]
        a1s = a1.firstChild.data.split()
        for i in range(3):
            anode = lv.getElementsByTagName('a'+str(i+1))[0]
            astr = anode.firstChild.data.split()
            for j in range(3):
                alat[i, j] = float(astr[j])

        a_ang = alat*Bohr

        nats = out.getElementsByTagName('NUMBER_OF_ATOMS')[0]
        nat = int(nats.firstChild.data)

        new_ats = np.zeros((nat, 3))
        for i in range(nat):
            at1 = out.getElementsByTagName('ATOM.'+str(i+1))[0]
            pos_s = at1.getAttribute('tau').split()
            for j in range(3):
                new_ats[i, j] = float(pos_s[j])
        new_frac = np.dot(new_ats, np.linalg.inv(alat))

        return a_ang, new_frac

    def sym_ibav_celldm(self, atoms):
        from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
        from math import sin, cos, pi, sqrt

        def at2struct(atoms):
            sp = atoms.get_chemical_symbols()
            pos = atoms.positions
            cell = atoms.cell
            return Structure(cell, sp, pos, coords_are_cartesian=True)

        struct = at2struct(atoms)

        sga = SpacegroupAnalyzer(struct, symprec=0.03, angle_tolerance=5)
        # print sga.get_space_group_symbol()
        # print sga.get_space_group_number()

        a = sga.get_conventional_standard_structure().lattice.a/Bohr
        b = sga.get_conventional_standard_structure().lattice.b/Bohr
        c = sga.get_conventional_standard_structure().lattice.c/Bohr

        alpha = sga.get_conventional_standard_structure().lattice.alpha
        beta = sga.get_conventional_standard_structure().lattice.beta
        gamma = sga.get_conventional_standard_structure().lattice.gamma

        if (sga.get_space_group_number() >= 195):
            # 1This means it's cubic
            if ('P' in sga.get_space_group_symbol()):
                # Simple cubic
                ibrav = 1
                celldm_dic = {'celldm(1)': a}
            if ('F' in sga.get_space_group_symbol()):
                # FCC
                ibrav = 2
                celldm_dic = {'celldm(1)': a}
            if ('I' in sga.get_space_group_symbol()):
                # FCC
                ibrav = 3
                celldm_dic = {'celldm(1)': a}

        elif (168 <= sga.get_space_group_number() < 195):
            ibrav = 4
            celldm_dic = {'celldm(1)': a,
                          'celldm(3)': c/a}

        elif (143 <= sga.get_space_group_number() < 168):
            ibrav = 5
            celldm_dic = {'celldm(1)': a,
                          'celldm(4)': cos(alpha*pi/180)}

        elif (75 <= sga.get_space_group_number() < 143):
            # this means it's Tetragonal
            if ('P' in sga.get_space_group_symbol()):
                # Simple cubic
                ibrav = 6
                celldm_dic = {'celldm(1)': a,
                              'celldm(3)': c/a}

            if ('I' in sga.get_space_group_symbol()):
                # FCC
                ibrav = 7
                celldm_dic = {'celldm(1)': a,
                              'celldm(3)': c/a}

        elif (16 <= sga.get_space_group_number() < 75):
            # this means it's Tetragonal
            if ('P' in sga.get_space_group_symbol()):
                # Simple cubic
                ibrav = 8
                celldm_dic = {'celldm(1)': a,
                              'celldm(2)': b/a,
                              'celldm(3)': c/a}

            if ('A' in sga.get_space_group_symbol() or 'C' in sga.get_space_group_symbol()):
                # Base centered
                ibrav = 9
                celldm_dic = {'celldm(1)': a,
                              'celldm(2)': b/a,
                              'celldm(3)': c/a}

            if ('F' in sga.get_space_group_symbol()):
                # Face centered
                ibrav = 10
                celldm_dic = {'celldm(1)': a,
                              'celldm(2)': b/a,
                              'celldm(3)': c/a}

            if ('I' in sga.get_space_group_symbol()):
                # Body centered
                ibrav = 11
                celldm_dic = {'celldm(1)': a,
                              'celldm(2)': b/a,
                              'celldm(3)': c/a}

        elif (3 <= sga.get_space_group_number() < 15):
            # this means it's Monoclinic
            if ('P' in sga.get_space_group_symbol()):
                # Simple cubic
                ibrav = 12
                celldm_dic = {'celldm(1)': a,
                              'celldm(2)': b/a,
                              'celldm(3)': c/a,
                              'celldm(4)': cos(gamma*pi/180.0)}
            if ('C' in sga.get_space_group_symbol()):
                # base centered
                ibrav = 13
                celldm_dic = {'celldm(1)': a,
                              'celldm(2)': b/a,
                              'celldm(3)': c/a,
                              'celldm(4)': cos(gamma*pi/180.0)}

        else:
            ibrav = 14
            celldm_dic = {'celldm(1)': a,
                          'celldm(2)': b/a,
                          'celldm(3)': c/a,
                          'celldm(4)': cos(alpha*pi/180.0),
                          'celldm(5)': cos(beta*pi/180.0),
                          'celldm(6)': cos(gamma*pi/180.0)}

        # print ibrav
        # if self.system_dic['ibrav'] == 0 :
        return [ibrav, celldm_dic, sga.get_conventional_standard_structure()]
        # else:

        # a = struct.lattice.a/Bohr
        # b = struct.lattice.b/Bohr
        # c = struct.lattice.c/Bohr

        # alpha = struct.lattice.alpha
        # beta = struct.lattice.beta
        # gamma =struct.lattice.gamma
        # celldm_dic = {'celldm(1)':a,
        #               'celldm(2)':b/a,
        #               'celldm(3)':c/a,
        #               'celldm(4)':cos(alpha*pi/180.0),
        #               'celldm(5)':cos(beta*pi/180.0),
        #               'celldm(6)':cos(gamma*pi/180.0)}
        # return [self.system_dic['ibrav'], celldm_dic, struct]
