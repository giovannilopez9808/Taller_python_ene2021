from edge_detection_package import *
import matplotlib.pyplot as plt
import os
# titles_kernel = ["Scharr", "Sobel", "Feldman"]
# titles=["Original"]+titles_kernel
titles_kernel = ["Sobel"]
titles = (["Original"]+titles_kernel)*2
kerneles = edge_kernels()
types_data = ["region_1/", "region_2/"]
folder_data = "../Data/"
folder_graphics = "../Graphics/"
files = listdir_sorted(folder_data+types_data[0])
for file in files:
    final_images = []
    for type_data in types_data:
        dir_data = folder_data+type_data
        dir_graphics = folder_graphics+type_data
        print(dir_data)
        img_original, img = read_image(file, path=dir_data)
        final_images.append(img_original)
        for kernel, title_kernel in zip(kerneles, titles_kernel):
            dir_fig = dir_graphics+title_kernel+"/"
            img_edge = convolve_images(img, kernel)
            kernel_plot(img_edge, file, title_kernel, dir_fig)
            final_images.append(img_edge)
    plot_image(final_images, file, titles, path=folder_graphics)
#animation_kernel(titles_kernel, path=dir_graphics)
files = listdir_sorted(folder_graphics)
create_gif(files, path=folder_graphics)
clip_maker(path=folder_graphics)
