import numpy as np


class DiffusionMap:
    """
    Class representing the diffusion map algorithm
    """

    def __init__(self, data, L):
        """
        Initiate attributes for the algorithm

        :param data: data itself
        :param L: number of eigenfunctions to be computed

        Attributes:
            m: corresponds to the number of rows of data (also named as N)
            n: corresponds to the number of columns of data
            D: corresponds to the distance matrix
            epsilon(ϵ): corresponds to 5% of the diameter of the dataset
            W: corresponds to the kernel matrix
            P: corresponds to the diagonal normalization matrix
            K: corresponds to the *normalized* kernel matrix
            Q: corresponds to the diagonal normalization matrix
            processed_Q: corresponds to Q^(-1/2)
            T_hat: corresponds to the symmetric matrix
            L:
            largest_eigenfunctions: dictionary with the following form where index 0 stores the largest eigenvalue
                {
                    index: (eigenvalue1, corresponding_eigenvector),
                    ...
                }
        """
        self.data = data
        self.m = data.shape[0]
        self.n = data.shape[1]
        self.D = None
        self.epsilon = None
        self.W = None
        self.P = None
        self.K = None
        self.Q = None
        self.processed_Q = None
        self.T_hat = None
        self.L = L
        self.largest_eigenfunctions = dict()
        self.final_eigenvalues = None
        self.final_eigenvectors = None
        self._form_dist_matrix()  # initiate the process to form ambient kernel

    def _form_dist_matrix(self):
        """
        Forms a distance matrix with the metric of Euclidean distance between rows
        """

        # initiate distance matrix with zeros
        self.D = np.zeros(shape=(self.m, self.m))

        def calculate_distance(row_i, row_j):
            """
            An inner method to calculate the Euclidean distance between two rows
            :param row_i: np array with n entries
            :param row_j: np array with n entries
            :return: distance between two rows
            """
            total_dist = np.sum([(row_i[ix] - row_j[ix]) ** 2 for ix in range(self.n)])
            return np.sqrt(total_dist)

        max_distance = 0
        for i in range(self.m):
            for j in range(self.m):
                self.D[i][j] = calculate_distance(self.data[i], self.data[j])
                max_distance = max(self.D[i][j], max_distance)

        self.epsilon = .05 * max_distance
        self._form_kernel_matrix()

    def _form_kernel_matrix(self):
        """
        Forms the kernel matrix W
        """
        # initiate kernel matrix with zeros
        self.W = np.zeros(shape=(self.m, self.m))

        for i in range(self.m):
            for j in range(self.m):
                self.W[i][j] = np.exp(-(self.D[i][j] ** 2) / self.epsilon)

        self._form_diagonal_normalization_matrix()

    def _form_diagonal_normalization_matrix(self):
        """
        Forms the diagonal normalization matrix P
        """

        # initiate diagonal normalization matrix with zeros
        self.P = np.zeros(shape=(self.m, self.m))

        for i in range(self.m):
            # for each row, sum up all values within that row
            self.P[i][i] = sum([self.W[i][j] for j in range(self.m)])

        self._normalize_kernel_matrix()

    def _normalize_kernel_matrix(self):
        """
        Forms the normalized the kernel matrix, i.e. K = P^-1 * W * P^-1
        """
        P_inverse = np.linalg.inv(self.P)
        self.K = P_inverse @ self.W @ P_inverse

        self._form_diagonal_normalization_matrix_q()

    def _form_diagonal_normalization_matrix_q(self):
        """
        Forms the diagonal normalization matrix Q, i.e. Q[i][i] = sum (K[i][j] for all j)
        """

        # initiate matrix with zeros
        self.Q = np.zeros(shape=(self.m, self.m))

        for i in range(self.m):
            # for each row, sum up all values within that row
            self.Q[i][i] = sum([self.K[i][j] for j in range(self.m)])

        self._form_symmetric_matrix()

    def _form_symmetric_matrix(self):
        """
        Forms the symmetric matrix T_hat, i.e. T_hat = Q^(-1/2) * K * Q^(-1/2)
        """

        processed_Q = np.zeros(shape=(self.m, self.m))

        for i in range(self.m):
            if self.Q[i][i] != 0:
                processed_Q[i][i] = 1 / np.sqrt(self.Q[i][i])

        self.processed_Q = processed_Q
        self.T_hat = processed_Q @ self.K @ processed_Q

        self._find_largest_eigenfunctions()

    def _find_largest_eigenfunctions(self):
        """
        Find the L+1 largest eigenvalues and associated eigenvectors of T_hat
        """

        eigenvalues, eigenvectors = np.linalg.eigh(self.T_hat)

        count = self.L
        # iterate through the largest L+1
        for eigval, eigvec in zip(eigenvalues[-(self.L + 1):], eigenvectors[-(self.L + 1):]):
            self.largest_eigenfunctions.update({count: (eigval, eigvec)})
            count -= 1

        # keep pairs on descending order of eigenvalues
        self.largest_eigenfunctions = dict(sorted(self.largest_eigenfunctions.items()))

        self._compute_final_eigenvalues()

    def _compute_final_eigenvalues(self):
        """
        Computes the eigenvalues of T_hat^(1/epsilon)
        """

        self.final_eigenvalues = np.zeros(shape=(self.L + 1))

        for ix in range(self.L + 1):
            eigenvalue, _ = self.largest_eigenfunctions[ix]
            self.final_eigenvalues[ix] = np.sqrt(eigenvalue ** (1 / self.epsilon))

        self._compute_final_eigenvectors()

    def _compute_final_eigenvectors(self):
        """
        Computes final eigenvectors of the matrix T = Q^-1 * K
        """
        self.final_eigenvectors = np.zeros(shape=(self.L + 1, self.m))

        for ix in range(self.L + 1):
            _, eigenvector = self.largest_eigenfunctions[ix]
            self.final_eigenvectors[ix] = self.processed_Q @ eigenvector
