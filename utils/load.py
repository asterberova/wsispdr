import random
from pathlib import Path
from skimage.feature import peak_local_max
import numpy as np
import cv2


def to_cropped_imgs(ids, dir_img):
    """From a list of tuples, returns the correct cropped img"""
    for id in ids:
        yield cv2.imread(str(dir_img / id.name))[:, :, :1].astype(np.float32)


def hwc_to_chw(img):
    return np.transpose(img, axes=[2, 0, 1])


def normalize(x):
    return x / 255


def get_imgs_and_masks_boundaries(dir_img, dir_mask, dir_boundary):
    """Return all the couples (img, mask)"""
    paths = list(dir_img.glob("*.tif"))
    random.shuffle(list(paths))

    imgs = to_cropped_imgs(paths, dir_img)
    imgs_switched = map(hwc_to_chw, imgs)
    imgs_normalized = map(normalize, imgs_switched)

    masks = to_cropped_imgs(paths, dir_mask)
    masks_switched = map(hwc_to_chw, masks)
    masks_normalized = map(normalize, masks_switched)

    boundaries = to_cropped_imgs(paths, dir_boundary)
    boundaries_switched = map(hwc_to_chw, boundaries)
    boundaries_normalized = map(normalize, boundaries_switched)

    return zip(imgs_normalized, masks_normalized, boundaries_normalized)


def batch(iterable, batch_size):
    """Yields lists by batch"""
    b = []
    for i, t in enumerate(iterable):
        b.append(t)
        if (i + 1) % batch_size == 0:
            yield b
            b = []

    if len(b) > 0:
        yield b


def local_maxima(img, threshold=100, dist=2):
    assert len(img.shape) == 2
    data = np.zeros((0, 2))
    x = peak_local_max(img, threshold_abs=threshold, min_distance=dist)
    peak_img = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for j in range(x.shape[0]):
        peak_img[x[j, 0], x[j, 1]] = 255
    labels, _, _, center = cv2.connectedComponentsWithStats(peak_img)
    for j in range(1, labels):
        data = np.append(data, [[center[j, 0], center[j, 1]]], axis=0).astype(int)
    return data