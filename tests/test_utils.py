from democritus.utils import *


def test_make_stochastic_empty_vector():
    result = make_stochastic([])
    assert result.tolist() == []


def test_make_stochastic_zeroes_vector():
    result = make_stochastic([0, 0, 0, 0])
    assert result.tolist() == [0.25, 0.25, 0.25, 0.25]


def test_make_stochastic_some_vector():
    result = make_stochastic([0.8, 0.7, 0.9, 0.3, 0.1, 0.4, 0.8])
    assert np.sum(result) == 1
    assert result.tolist() == [0.2, 0.175, 0.225, 0.075, 0.025, 0.1, 0.2]


def test_make_row_stochastic_some_matrix():
    result = make_row_stochastic([[0, 0, 0, 0],
                              [0.8, 0.7, 0.9, 1.6],
                              [0, 0, 0, 0.1]])
    assert np.sum(result[0]) == 1
    assert np.sum(result[1]) == 1
    assert np.sum(result[2]) == 1
    assert result[0].tolist() == [0.25, 0.25, 0.25, 0.25]
    assert result[1].tolist() == [0.2, 0.175, 0.225, 0.4]
    assert result[2].tolist() == [0, 0, 0, 1]
