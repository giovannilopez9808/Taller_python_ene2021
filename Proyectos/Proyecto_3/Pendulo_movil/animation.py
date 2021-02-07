import imageio
import os


def mkdir(name, path=""):
    try:
        os.mkdir(path+name)
    except FileExistsError:
        pass


def create_gif(name, duration=0.1, path="", delete=True):
    filenames = sorted(os.listdir(path))
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    output_file = path+name
    imageio.mimsave(output_file, images, duration=duration)
    if delete:
        os.system("rm "+path+"/*.png")
