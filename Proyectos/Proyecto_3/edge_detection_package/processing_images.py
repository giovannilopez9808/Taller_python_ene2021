from .post_processing_images import *
from PIL import Image
import numpy as np
import cv2


def read_image(name, path=""):
    img_original = cv2.imread(path+name, 1)
    img = high_contrast_image(img_original)[:, :, 0]
    img_original = Image.open(path+name).convert("RGB")
    return img_original, img
