from megaman.embedding import SpectralEmbedding as SpectralEmbedding_Megaman
from megaman.embedding import LTSA, LocallyLinearEmbedding, Isomap
from sklearn.manifold import SpectralEmbedding as SpectralEmbedding_Default
import matplotlib.pyplot as plt
import datetime


class EmbeddingAlgorithms:
    """
    Class for the embedding algorithms
    Attributes:
        X:      Given data to embed
        geom:   Required Geometry object by Megaman algorithms
    """

    def __init__(self, X, geom):
        """
        Initializer of the class EmbeddingAlgorithms
        X:      Given data to embed
        geom:   Required Geometry object by Megaman algorithms
        """
        self.X = X
        self.geom = geom

    def run_all_algos(self, run_mm_se=True, run_mm_ltsa=False, run_mm_lle=False, run_mm_isomap=False,
                      run_sklearn_se=True):
        """
        Embeds the given data with some algorithm(s)
        :param run_mm_se:       Flag to run Megaman's SpectralEmbedding or not
        :param run_mm_ltsa:     Flag to run Megaman's LTSA or not
        :param run_mm_lle:      Flag to run Megaman's LocallyLinearEmbedding or not
        :param run_mm_isomap:   Flag to run Megaman's Isomap or not
        :param run_sklearn_se:  Flag to run Sklearn's SpectralEmbedding or not
        """
        if run_mm_se:
            try:
                self.megaman_se()
            except Exception as e:
                print(e)
        if run_mm_ltsa:
            try:
                self.megaman_ltsa()
            except Exception as e:
                print(e)
        if run_mm_lle:
            try:
                self.megaman_lle()
            except Exception as e:
                print(e)
        if run_mm_isomap:
            try:
                self.megaman_isomap()
            except Exception as e:
                print(e)
        if run_sklearn_se:
            try:
                self.sklearn_se()
            except Exception as e:
                print(e)

    @staticmethod
    def plot_embedding(Y):
        """
        Plots the embedded data
        :param Y:   Embedded data
        """
        plt.scatter(*Y.T)
        plt.show()

    def sklearn_se(self):
        """
        Runs Sklearn's SpectralEmbedding algorithm
        """
        print("sklearn - Spectral Embedding")
        embedding = SpectralEmbedding_Default(n_components=2)
        t0 = datetime.datetime.now()
        print("t0:", t0)
        Y = embedding.fit_transform(self.X)
        t1 = datetime.datetime.now()
        print("t1:", t1)
        t_diff = t1-t0
        print("Time diff:", t_diff)
        self.plot_embedding(Y)

    def megaman_se(self):
        """
        Runs Megaman's SpectralEmbedding algorithm
        """
        print("megaman - Spectral Embedding")
        SE = SpectralEmbedding_Megaman(
            n_components=2,
            eigen_solver='amg',
            geom=self.geom
        )
        t0 = datetime.datetime.now()
        print("t0:", t0)
        Y = SE.fit_transform(self.X)
        t1 = datetime.datetime.now()
        print("t1:", t1)
        t_diff = t1-t0
        print("Time diff:", t_diff)
        self.plot_embedding(Y)

    def megaman_ltsa(self):
        """
        Runs Megaman's LTSA algorithm
        """
        print("megaman - Local Tangent Space Alignment")
        ltsa = LTSA(
            n_components=2,
            eigen_solver='amg',
            geom=self.geom
        )
        t0 = datetime.datetime.now()
        print("t0:", t0)
        Y = ltsa.fit_transform(self.X)
        t1 = datetime.datetime.now()
        print("t1:", t1)
        t_diff = t1-t0
        print("Time diff:", t_diff)
        self.plot_embedding(Y)

    def megaman_lle(self):
        """
        Runs Megaman's LocallyLinearEmbedding algorithm
        """
        print("megaman - Locally Linear Embedding")
        lle = LocallyLinearEmbedding(
            n_components=2,
            eigen_solver='amg',
            geom=self.geom
        )
        t0 = datetime.datetime.now()
        print("t0:", t0)
        Y = lle.fit_transform(self.X)
        t1 = datetime.datetime.now()
        print("t1:", t1)
        t_diff = t1-t0
        print("Time diff:", t_diff)
        self.plot_embedding(Y)

    def megaman_isomap(self):
        """
        Runs Megaman's Isomap algorithm
        """
        print("megaman - Isomap")
        isomap = Isomap(
            n_components=2,
            eigen_solver='amg',
            geom=self.geom
        )
        t0 = datetime.datetime.now()
        print("t0:", t0)
        Y = isomap.fit_transform(self.X)
        t1 = datetime.datetime.now()
        print("t1:", t1)
        t_diff = t1-t0
        print("Time diff:", t_diff)
        self.plot_embedding(Y)
