import numpy as np
import cv2


def read_text(file_path):
    """
    Reads txt file
    :param file_path:   Path to the text file containing matrix A that SVD will be applied on
    :returns:           Matrix A that SVD will be applied on
    """
    with open(file_path) as f:
        lines = f.readlines()
    rows = [l.rstrip('\n').split(' ') for l in lines]
    a = np.array(rows, float)
    return a


def get_image(file_path, mode, img_size):
    """
    Gets image
    :param file_path:   Path to the image file containing matrix A that SVD will be applied on
    :param mode:        Type of the image like black-white to use while reading the image
    :param img_size:    Size of the image
    :returns:           Image that SVD will be applied on
    """
    img = cv2.imread(file_path, mode)
    img = cv2.resize(img, img_size)
    return img
