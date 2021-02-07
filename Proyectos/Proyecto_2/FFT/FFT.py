from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import numpy as np


def plot_FFT_and_original(img, FFT, name, path=""):
    fig = plt.figure(figsize=(8, 8))
    axs = [fig.add_subplot(2, 2, i+1) for i in range(4)]
    ax1, ax2, ax3, ax4 = axs
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    plot_FFT(ax1, img, bar=False)
    plot_FFT(ax2, FFT, cmap="binary")
    plot_FFT(ax3, FFT, hexagon=True, cmap="binary")
    plot_FFT(ax4, FFT, hexagon=True)
    plt.savefig(path+name+".png", bbox_inches="tight",
                pad_inches=0)


def plot_FFT(ax, image, cmap=None, bar=True, hexagon=False):
    ax.axis("off")
    ax.set_aspect('equal')
    ax.imshow(image, cmap=cmap)
    if bar:
        ax.plot([6.5, 63.3], [247.4, 247.4], color="black", lw=4)
        ax.text(2, 238, "5  1nm$^{-1}$", fontsize=14)
    if hexagon:
        plot_hexagon(ax)


def FFT(im):
    f = np.fft.fft2(im)
    f = np.fft.fftshift(f)
    f = np.log(np.abs(f))*1000
    return f


def plot_hexagon(ax):
    x, y = np.loadtxt("Data/hexa.csv", delimiter=",", unpack=True)
    n = np.size(x)
    for i in range(n):
        j = i+1
        if j == n:
            j = 0
        pos = [i, j]
        ax.plot(x[pos], y[pos], lw=3, color="black")


im = Image.open("Imagen.tif")
FFT_image = FFT(im)
plot_FFT_and_original(im, FFT_image, name="FFT")
