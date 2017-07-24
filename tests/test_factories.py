import numpy as np

from democritus.factories import SimilarityFunctionFactory


class TestSimilarityFunctionFactory(object):
    def test_create_identity(self):
        similarity = SimilarityFunctionFactory.create_identity(3)
        assert np.round(similarity[0], decimals=3).tolist() == [1, 0, 0]
        assert np.round(similarity[1], decimals=3).tolist() == [0, 1, 0]
        assert np.round(similarity[2], decimals=3).tolist() == [0, 0, 1]

    def test_create_nosofsky(self):
        similarity = SimilarityFunctionFactory.create_nosofsky(np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]]), 2)
        assert np.round(similarity[0], decimals=3).tolist() == [1, 0.779, 0.368]
        assert np.round(similarity[1], decimals=3).tolist() == [0.779, 1, 0.779]
        assert np.round(similarity[2], decimals=3).tolist() == [0.368, 0.779, 1]
