from .post_processing_images import *
import matplotlib.pyplot as plt
from .formats import *
import numpy as np


def plot_image(images, name, titles, path=""):
    name = jpg2png(name)
    fig, axs = plt.subplots(2, 2, figsize=(8, 7))
    axs = np.reshape(axs, 4)
    plt.subplots_adjust(left=0, bottom=0, right=1,
                        top=0.957, wspace=0.05, hspace=0)
    for ax, image, title in zip(axs, images, titles):
        individual_plots(ax, image, title)
    date = pull_date(name)
    fig.text(0.4, 0.95, date, fontsize=20)
    plt.savefig(path+name)
    plt.clf()


def individual_plots(ax, image, title=""):
    ax.axis("off")
    ax.set_title(title, fontsize=16)
    ax.imshow(image, cmap="gray")


def kernel_plot(image, name, kernel_name, path=""):
    date = pull_date(name)
    fig_name = name_format_kernel(name, kernel_name)
    fig, ax = plt.subplots()
    individual_plots(ax, image, title=date)
    plt.savefig(path+fig_name)
    plt.clf()
