import numpy as np


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
