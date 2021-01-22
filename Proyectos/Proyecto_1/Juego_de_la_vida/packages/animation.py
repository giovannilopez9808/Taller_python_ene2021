import matplotlib.pyplot as plt
import moviepy.editor as mp
from .name_list import *
import imageio


def image_plot(data, number, lim):
    name = name_format(number, lim)
    plt.subplots_adjust(bottom=0.024, top=0.917)
    plt.axis("off")
    plt.title("Walk number "+name)
    plt.imshow(data, cmap="gist_gray")
    plt.savefig(name+".png")
    plt.clf()


def create_gif(duration=0.1, output_file="animation"):
    images = []
    filenames = files()
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(output_file+".gif", images, duration=duration)
    os.system("rm *.png")


def clip_maker(output_file="animation"):
    clip = mp.VideoFileClip(output_file+'.gif')
    os.system("rm *.gif")
    clip.write_videofile(output_file+".mp4")
