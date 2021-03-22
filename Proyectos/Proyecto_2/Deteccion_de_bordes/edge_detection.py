import matplotlib.pyplot as plt
from scipy import signal
from PIL import Image
import numpy as np
import cv2


class edge_detection:
    def __init__(self, kernel_name, path_image, name_image):
        self.kernel_name = kernel_name
        self.path_image = path_image
        self.name_image = name_image
        self.kernel_define()
        self.read_image()
        self.convolve_images()

    def kernel_define(self):
        """
        Kernel (matriz de transformacion) para la deteccion de bordes en imagenes
        de alta resolución
        """
        kernels = {
            "Sobel": [
                [-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1],
            ],
            "Prewitt": [
                [-1, -1, -1],
                [0, 0, 0],
                [1, 1, 1],
            ],
            "Feldman": [
                [10, 10, 20, 10, 10],
                [3, 3, 10, 3, 3],
                [0, 0, 0, 0, 0],
                [-3, -3, -10, -3, -3],
                [-10, -10, -20, -10, -10],
            ],
            "Scharr": [
                [47, 162, 47],
                [0, 0, 0],
                [-47, -162, -47],
            ],
        }
        self.kernel = np.array(kernels[self.kernel_name])

    def read_image(self):
        """
        Lectura de la imagen y aplicacion del filtro de alto contraste
        """
        img_original = cv2.imread(self.path_image + self.name_image, 1)
        self.img = self.high_contrast_image(img_original)[:, :, 0]
        self.img_original = Image.open(self.path_image +
                                       self.name_image).convert("RGB")

    def high_contrast_image(self, img):
        """
        Funcion que aplica el alto contraste a la imagen cargada.
        Este processo no ess necesario, es solo para obtener mejores
        resultados
        """
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8, 8))
        # convert from BGR to LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)  # split on 3 different channels
        l2 = clahe.apply(l)  # apply CLAHE to the L-channel
        lab = cv2.merge((l2, a, b))  # merge channels
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
        return img

    def convolve_images(self):
        """
        Proceso de convolución (multiplicacion de matrices) en la imagen con el kernel
        seleccionado
        """
        img_edge_x = signal.convolve2d(self.img,
                                       self.kernel,
                                       boundary='symm',
                                       mode='same')
        img_edge_y = signal.convolve2d(self.img,
                                       self.kernel.transpose(),
                                       boundary='symm',
                                       mode='same')
        self.img_edge = np.sqrt(img_edge_x**2 + img_edge_y**2)

    def plot_image(self, name_result="result.png", path_result="", save_image=False):
        """
        Función que grafica las dos imagenes en una sola, de lado izquierdo la original
        y de lado derecho con bordes
        """
        images = [self.img_original, self.img_edge]
        fig = plt.figure(figsize=(13, 5))
        axs = [fig.add_subplot(1, 2, i + 1) for i in range(2)]
        axs = np.reshape(axs, 2)
        plt.subplots_adjust(left=0,
                            bottom=0,
                            right=1,
                            top=0.957,
                            wspace=0,
                            hspace=0)
        for ax, image in zip(axs, images):
            self.individual_plots(ax, image)
        if save_image:
            plt.savefig(path_result + name_result,
                        bbox_inches="tight",
                        pad_inches=0)
        else:
            plt.show()

    def individual_plots(self, ax, image):
        # Ploteo de cada imagen
        ax.axis("off")
        ax.imshow(image, cmap="gray")


inputs = {
    "Image path": "",
    "Image name": "image.jpg",
    "Kernel name": "Sobel",
}
path = ""
name = "image.jpg"
kernel = "Sobel"
border = edge_detection(inputs["Kernel name"],
                        inputs["Image path"],
                        inputs["Image name"])
border.plot_image()
