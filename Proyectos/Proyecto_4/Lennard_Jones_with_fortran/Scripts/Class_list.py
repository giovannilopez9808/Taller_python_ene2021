import matplotlib.pyplot as plt
from functions import *
import numpy as np
import os


class MD:
    def __init__(self, path_input, program_name, repeat_run,):
        self.repeat_run = repeat_run
        self.program_name = program_name
        self.path_input = path_input
        self.create_all_folders()

    def create_all_folders(self):
        mkdir(name="Input",
              path="../")
        mkdir(name="Results",
              path="../")
        mkdir(name="Graphics",
              path="../")

    def run(self):
        print("Corriendo la dinamina molecular....")
        for time in range(self.repeat_run):
            print("{} repetición de {}".format(time+1,
                                               self.repeat_run))
            self.make_input_file(time)
            self.compile_MD()
            self.run_MD()

    def make_input_file(self, rho):
        file = open("{}rho.txt".format(self.path_input),
                    "w")
        file.write("{}".format(rho))
        file.close()

    def compile_MD(self):
        os.system("gfortran {}.f -o {}.out".format(self.program_name,
                                                   self.program_name))

    def run_MD(self):
        os.system("./{}.out".format(self.program_name))


class Graphics_LJ:
    def __init__(self):
        pass
