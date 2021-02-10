from edge_detection_package import *
# Obtención del Kernel a usar
kernel = edge_kernels()
# Localizacion de la imagen (eliminar dir_drive cuando se ejecuta en local)
file = "image.jpg"
final_images = []
# Lectura de la imagen y obtención de la misma con el alto contraste
img_original, img = read_image(file)
final_images.append(img_original)
# Aplicación de la convolución a la imagen
img_edge = convolve_images(img, kernel)
final_images.append(img_edge)
# Ploteo de la imagen original y con detección de bordes
plot_image(final_images)
