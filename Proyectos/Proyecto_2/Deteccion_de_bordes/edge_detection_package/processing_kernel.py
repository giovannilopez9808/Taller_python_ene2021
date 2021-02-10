from scipy import signal
import numpy as np


def edge_kernels():
    """
    Kernel (matriz de transformacion) para la deteccion de bordes en imagenes
    de alta resolución
    """
    # sobel = np.array([
    #     [2, 2, 4, 2, 2],
    #     [1,  1,  2,  1, -1],
    #     [0,  0,  0,  0, -0],
    #     [-1,  -1,  -2,  -1, -1],
    #     [-2, -2, -4, -2, -2], ])
    # scharr = np.array([
    #     [162, 162, 324, 162, 162],
    #     [47, 47, 162, 47, 47],
    #     [0, 0, 0, 0, 0],
    #     [-47, -47, -162, -47, -47],
    #     [-162, -162, -324, -162, -162], ])
    feldman = np.array([
        [10, 10, 20, 10, 10],
        [3, 3, 10, 3, 3],
        [0, 0, 0, 0, 0],
        [-3, -3, -10, -3, -3],
        [-10, -10, -20, -10, -10], ])
    # sobel = np.array([
    #     [1,  2,  1],
    #     [0,  0,  0],
    #     [-1, -2, 1], ])
    # scharr = np.array([
    #     [47, 162, 47],
    #     [0, 0, 0],
    #     [-47, -162, -47], ])
    # feldman = np.array([
    #     [3, 10, 3],
    #     [0, 0, 0],
    #     [-3, -10, -3], ])
    # return [scharr, sobel, feldman]
    return feldman


def convolve_images(img, kernel):
    """
    Proceso de convolución (multiplicacion de matrices) en la images con el kernel
    seleccionado
    """
    img_edge_x = signal.convolve2d(
        img, kernel, boundary='symm', mode='same')
    img_edge_y = signal.convolve2d(
        img, kernel.transpose(), boundary='symm', mode='same')
    img_edge = np.sqrt(img_edge_x**2+img_edge_y**2)
    return img_edge
