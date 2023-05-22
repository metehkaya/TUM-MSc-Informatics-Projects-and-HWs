import os
import numpy as np


class Solver:
    """
    Class for Solver tasks
    Attributes:
        file_name:      Input file storing coordinates of the points
        folder_path:    Directory of the folder where the input file is stored
        n:              The number of points in the dataset
    """

    def __init__(self, file_name, folder_path=None):
        """
        Initializer of the class Solver
        :param file_name:     Input file storing coordinates of the points
        :param folder_path:   Directory of the folder where the input file is stored
        """
        self.file_name = file_name
        self.folder_path = folder_path
        self.n = None

    def read_data(self):
        """
        Reads coordinates of the points
        :returns:   X and Y coordinates of the points given in the file
        """
        data_x = []
        data_y = []
        if self.folder_path is None:
            file_path = self.file_name
        else:
            file_path = os.path.join(self.folder_path, self.file_name)
        with open(file_path) as f:
            lines = f.readlines()
            for line in lines:
                x,y = map (float,line.split())
                data_x.append(x)
                data_y.append(y)
        data_x = np.asarray(data_x)
        data_y = np.asarray(data_y)
        self.n = data_x.shape[0]
        return data_x, data_y

    def get_loss(self, y, y_pred):
        """
        Retrieves loss
        :param y:         Ground truth for y coordinates of the points
        :param y_pred:    Predicted y coordinates of the points
        :returns:         Loss value
        """
        diff = y - y_pred
        sum = np.sum(diff**2)
        loss = sum / self.n
        return loss
