import moviepy.editor as mp
from .formats import *
import imageio
import os


def create_gif(filenames, duration=1, output_file="animation", path=""):
    images = []
    for filename in filenames:
        images.append(imageio.imread(path+filename))
    imageio.mimsave(path+output_file+".gif", images, duration=duration)
    #os.system("rm "+path+"*.png")


def clip_maker(output_file="animation", path=""):
    loc = path+output_file
    clip = mp.VideoFileClip(loc+'.gif')
    os.system("rm "+path+"*.gif")
    clip.write_videofile(loc+".mp4")


def animation_kernel(list_kernel, path="",):
    for kernel in list_kernel:
        dir_fig = path+kernel+"/"
        files = listdir_sorted(dir_fig)
        output = "animation_"+kernel
        create_gif(files, output_file=output, path=dir_fig)
        clip_maker(output_file=output, path=dir_fig)
