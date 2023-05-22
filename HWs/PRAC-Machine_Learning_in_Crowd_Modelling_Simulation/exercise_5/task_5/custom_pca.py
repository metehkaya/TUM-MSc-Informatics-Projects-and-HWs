import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt


class CustomPCA:
    """
    Class for PCA tasks
    Attributes:
        a_shape:    Shape (size) of matrix A to use during reconstruction
        a_mean:     Data mean calculated for each column of matrix A that SVD will be applied on
        u:          Matrix U in SVD decomposition
        s:          Values of diagonal matrix in SVD decomposition
        v:          Matrix V in SVD decomposition
        trace:      Sum of squares of values in diagonal matrix in SVD decomposition
    """

    def __init__(self, a):
        """
        Initializer of the class CustomPCA
        :param a:   Matrix A that SVD will be applied on
        """
        self.a_shape = a.shape
        self.a_mean = None
        self.u = None
        self.s = None
        self.v = None
        self.trace = None
        self.calc_svd(a)

    def calc_svd(self, a):
        """
        Makes SVD decomposition on matrix A
        :param a:   Matrix A that SVD will be applied on
        """
        self.a_mean = a.mean(axis=0)
        a_norm = a - self.a_mean
        self.u, self.s, self.v = np.linalg.svd(a_norm, full_matrices=True)
        self.trace = np.sum(self.s ** 2)
        print("Diagonal matrix values:", self.s)

    def get_importance(self, lower, upper):
        """
        Calculates importance of the principle components in range [lower, upper)
        :param lower:   ID of the principal component with higher importance
        :param upper:   ID of the principal component with less importance
        :returns:       Total importance of the principle components in range [lower, upper)
        """
        s_new = self.s[lower:upper]
        total = np.sum(s_new ** 2)
        importance = total / self.trace * 100
        return importance

    def get_importance_of_k(self, k):
        """
        Calculates importance of the k'th principle component
        :param k:   The index of principle component to calculate importance
        :returns:   Importance of the k'th principle
        """
        return self.get_importance(k, k+1)

    def get_importance_of_first_k(self, k):
        """
        Calculates importance of the first k principle components, i.e. [0, k)
        :param k:   The number of first principle components to calculate importance
        :returns:   Total importance of the first k principle, i.e. [0, k)
        """
        return self.get_importance(0, k)

    def reconstruct(self, lower, upper):
        """
        Calculates reconstruction of SVD with principle components in [lower, upper)
        :param lower:   ID of the principal component with higher importance
        :param upper:   ID of the principal component with less importance
        :returns:       Reconstructed matrix calculated based on normalized A
        """
        s_new = np.zeros(self.s.shape)
        s_new[lower:upper] = self.s[lower:upper]
        a_new = self.u @ la.diagsvd(s_new, *self.a_shape) @ self.v
        a_new = a_new + self.a_mean
        return a_new

    def reconstruct_first_k(self, k):
        """
        Calculates reconstruction of SVD with first k principle components, i.e. [0, k)
        :param k:   The number of first principle components to calculate reconstruction of SVD
        :returns:   Reconstructed matrix calculated based on normalized A
        """
        return self.reconstruct(0, k)

    def plot_reconstruct_first_k(self, k):
        """
        Plots reconstruction of SVD with first k principle components, i.e. [0, k)
        :param k:   The number of first principle components to plot reconstruction of SVD
        """
        importance = self.get_importance_of_first_k(k)
        print('First {} principal components has importance {}'.format(k, importance))
        a_new = self.reconstruct_first_k(k)
        plt.imshow(a_new.T, cmap='gray')

    def find_first_k_exceed_threshold(self, threshold):
        """
        Finds minimal k such that first k principal components has higher importance than the given threshold
        :param threshold:   The threshold of reconstruction in terms of importance
        :returns:           Minimal number of principal components that has higher importance than the given threshold
        """
        assert threshold is not None and 0. <= threshold <= 100., "Threshold is not valid!"
        k_min = 1
        k_max = int(self.a_shape[1])
        k_threshold = None
        importance_threshold = None
        while k_min <= k_max:
            k = int((k_min + k_max) / 2)
            importance = self.get_importance_of_first_k(k)
            if importance > threshold:
                k_threshold = k
                importance_threshold = importance
                k_max = k-1
            else:
                k_min = k+1
        print('First {} principal components has importance {} and exceed the threshold {}'.
              format(k_threshold, importance_threshold, threshold))
        return k_threshold
