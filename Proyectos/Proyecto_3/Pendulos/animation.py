import moviepy.editor as mp
import imageio
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        pass


def create_gif(name, duration, path, delete):
    filenames = sorted(os.listdir(path))
    images = []
    for filename in filenames:
        images.append(imageio.imread(path+filename))
    output_file = path+name+".gif"
    imageio.mimsave(output_file, images, duration=duration)
    if delete:
        os.system("rm "+path+"*.png")


def clip_maker(output_file, path):
    loc = path+output_file
    clip = mp.VideoFileClip(loc+'.gif')
    os.system("rm "+path+"*.gif")
    clip.write_videofile(loc+".mp4")


def make_animation(name="animation", duration=0.1, path="", delete=True):
    create_gif(name,duration,path,delete)
    clip_maker(name,path)

def calc_alpha(walk,total):
    alpha=(walk-total+10)/10
    if alpha<0:
        alpha=0
    return alpha