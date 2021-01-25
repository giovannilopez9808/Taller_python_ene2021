import numpy as np

class system:
    def __init__(self, min, max, size):
        self.min = min
        self.max = max
        self.size = size
        self.initialize_system()

    def initialize_system(self):
        self.r = np.sqrt(2)*np.linspace(self.min, self.max, self.size)
        self.map = np.zeros((2*self.size, 2*self.size))

    def print_r(self):
        print(self.r)
    
wave=system(0.01,100,100)
wave.print_r()