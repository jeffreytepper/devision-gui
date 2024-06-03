from glob import glob
import os

import numpy as np
from tifffile import imread
from tqdm import tqdm

from csbdeep.utils import normalize
from stardist import fill_label_holes
from stardist.models import Config2D, StarDist2D

def pad_image(image, min_resolution):
    height, width = image.shape

    pad_height = max(0, min_resolution[0] - height)
    pad_width = max(0, min_resolution[1] - width)

    return np.pad(image, ((0, pad_height), (0, pad_width)), mode='constant')

def load_image(path):

    image = imread(path)
    if image.ndim == 3:
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
    image = normalize(image, 1, 99.8, axis=(0,1))
    image = pad_image(image, min_resolution=(256,256))

    return image

def load_mask(path):

    mask = imread(path)
    mask = fill_label_holes(mask)
    mask = pad_image(mask, min_resolution=(256,256))

    return mask

def random_fliprot(img, mask): 
    assert img.ndim >= mask.ndim
    axes = tuple(range(mask.ndim))
    perm = tuple(np.random.permutation(axes))
    img = img.transpose(perm + tuple(range(mask.ndim, img.ndim))) 
    mask = mask.transpose(perm) 
    for ax in axes: 
        if np.random.rand() > 0.5:
            img = np.flip(img, axis=ax)
            mask = np.flip(mask, axis=ax)
    return img, mask 

def random_intensity_change(img):
    img = img*np.random.uniform(0.6,2) + np.random.uniform(-0.2,0.2)
    return img


def augmenter(x, y):
    """Augmentation of a single input/label image pair.
    x is an input image
    y is the corresponding ground-truth label image
    """
    x, y = random_fliprot(x, y)
    x = random_intensity_change(x)
    # add some gaussian noise
    sig = 0.02*np.random.uniform(0,1)
    x = x + sig*np.random.normal(0,1,x.shape)
    return x, y



# def train(total_data, dataset_size, rays, train_split, testing_size, epochs, model_name, images_filepath, masks_filepath, output_filepath): 

def train(image_paths, mask_paths, train_split=0.15, epochs=3, rays=32, model_name='custom'):

    #Loading filepaths
    image_paths.sort()
    mask_paths.sort()

    #Preform preprocessing on images and masks
    images = list(map(load_image, image_paths[:10]))
    masks = list(map(load_mask, mask_paths[:10]))

    #Split into training and validation
    dataset_size = len(images)

    rng = np.random.default_rng(seed=42)
    indicies = rng.permutation(dataset_size)
    split_ind = max(1, int(train_split * dataset_size))

    val_images, train_images = [images[index] for index in indicies[:split_ind]], [images[index] for index in indicies[split_ind:]]
    val_masks, train_masks = [masks[index] for index in indicies[:split_ind]], [masks[index] for index in indicies[split_ind:]]

    #Initalize training configuration
    dataset_dir = os.path.join(os.getcwd(), f'datasize_{dataset_size}')
    os.makedirs(dataset_dir, exist_ok=True)

    config = Config2D (
        n_rays       = rays,
        grid         = (2,2),
        n_channel_in = 1
    )

    #Train and optimize model
    model = StarDist2D(config, name=model_name, basedir=dataset_dir)
    model.train(train_images, train_masks, validation_data=(val_images, val_masks), augmenter=augmenter, epochs=epochs)
    model.optimize_thresholds(val_images, val_masks)