import matplotlib.pyplot as plt
import numpy as np
import os


class MD:
    def __init__(self, path_input, program_name, repeat_run,):
        self.repeat_run = repeat_run
        self.program_name = program_name
        self.path_input = path_input

    def run(self):
        for time in range(self.repeat_run):
            print("Corriendo la dinamina molecular....\n {} repetición de {}".format(time+1,
                                                                                     self.repeat_run))
            self.make_input_file(time)
            self.compile_MD()
            self.run_MD()

    def make_input_file(self, rho):
        file = open("{}rho.txt".format(self.path_input),
                    "w")
        file.write("{}", format(rho))
        file.close()

    def compile_MD(self):
        os.system("gfortan {}.f -o {}.out".format(self.program_name,
                                                  self.particle_number))

    def run_MD(self):
        os.system("./{}.out".format(self.particle_number))


class Graphics_LJ:
    def __init__(self):
        pass
