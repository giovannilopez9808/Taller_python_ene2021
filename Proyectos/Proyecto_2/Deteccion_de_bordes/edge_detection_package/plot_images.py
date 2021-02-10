from .post_processing_images import *
import matplotlib.pyplot as plt
import numpy as np


def plot_image(images, name="result.png", titles=["Original","Bordes"], path=""):
    """
    Función que grafica las dos imagenes en una sola, de lado izquierdo la original
    y de lado derecho con bordes
    """
    fig, axs = plt.subplots(1, 2, figsize=(13, 5))
    axs = np.reshape(axs, 2)
    plt.subplots_adjust(left=0, bottom=0, right=1,
                        top=0.957, wspace=0.05, hspace=0)
    for ax, image, title in zip(axs, images, titles):
        individual_plots(ax, image, title)
    plt.savefig(path+name)
    plt.clf()


def individual_plots(ax, image, title=""):
    # Ploteo de cada imagen
    ax.axis("off")
    ax.set_title(title, fontsize=16)
    ax.imshow(image, cmap="gray")