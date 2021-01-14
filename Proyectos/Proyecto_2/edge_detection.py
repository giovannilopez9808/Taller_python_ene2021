from edge_detection_package import *
kernel = edge_kernels()
file = "image.jpg"
final_images = []
img_original, img = read_image(file)
final_images.append(img_original)
img_edge = convolve_images(img, kernel)
final_images.append(img_edge)
plot_image(final_images)
