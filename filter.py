from tifffile import imread
from tqdm import tqdm
from csbdeep.utils import normalize
from stardist import fill_label_holes
import numpy as np
import matplotlib.pyplot as plt
import os.path

axis_norm = (0,1)
min_resolution = (256,256)

def _pad_image(image, min_resolution):
    height, width = image.shape

    pad_height = max(0, min_resolution[0] - height)
    pad_width = max(0, min_resolution[1] - width)

    return np.pad(image, ((0, pad_height), (0, pad_width)), mode='constant')


def load_images(image_paths):
    images = []
    for path in tqdm(image_paths[:30], desc="Loading images"):
        image = imread(path)
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = normalize(image, 1, 99.8, axis=axis_norm)
        image = _pad_image(image, min_resolution)
        images.append(image)

    return images

def load_masks(mask_paths):
    masks = []
    for path in tqdm(mask_paths[:30], desc="Loading masks"):
        mask = imread(path)
        mask = fill_label_holes(mask)
        mask = _pad_image(mask, min_resolution)
        masks.append(mask)

    return masks



