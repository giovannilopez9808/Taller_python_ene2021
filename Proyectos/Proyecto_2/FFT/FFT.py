import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


class FFT_algorithm:
    def __init__(self, path_image, name_image):
        self.path_image = path_image
        self.name_image = name_image
        self.read_image()
        self.apply_FFT()

    def read_image(self):
        self.img = Image.open(self.path_image + self.name_image)

    def apply_FFT(self):
        f = np.fft.fft2(self.img)
        f = np.fft.fftshift(f)
        self.FFT_image = np.log(np.abs(f)) * 1000

    def plot_FFT_and_original(self):
        fig = plt.figure(figsize=(6, 8))
        axs = [fig.add_subplot(2, 2, i + 1) for i in range(4)]
        ax1, ax2, ax3, ax4 = axs
        plt.subplots_adjust(left=0,
                            bottom=0,
                            right=1,
                            top=1,
                            wspace=0,
                            hspace=0)
        self.plot_FFT(ax1, self.img, bar=False)
        self.plot_FFT(ax2, self.FFT_image)
        self.plot_FFT(ax3, self.FFT_image, hexagon=True)
        self.plot_FFT(ax4, self.FFT_image, hexagon=True, cmap="inferno_r")
        plt.subplots_adjust(top=0.978,
                            bottom=0.022,
                            left=0.025,
                            right=0.975,
                            hspace=0.0,
                            wspace=0.054)
        plt.show()

    def plot_FFT(self, ax, image, cmap="Greys_r", bar=True, hexagon=False):
        ax.axis("off")
        ax.set_aspect('equal')
        ax.imshow(image, cmap=cmap)
        if bar:
            ax.plot([6.5, 63.3], [247.4, 247.4], color="black", lw=4)
            ax.text(2, 238, "5  1nm$^{-1}$", fontsize=14)
        if hexagon:
            self.read_plot_hexagon(ax)

    def read_plot_hexagon(self, ax):
        x, y = np.loadtxt("Data/hexa.csv", delimiter=",", unpack=True)
        n = np.size(x)
        for i in range(n):
            j = i + 1
            if j == n:
                j = 0
            pos = [i, j]
            ax.plot(x[pos], y[pos], lw=3, color="black")


inputs = {
    "Image path": "",
    "Image name": "Imagen.tif",
}
FFT = FFT_algorithm(inputs["Image path"],
                    inputs["Image name"])
FFT.plot_FFT_and_original()
