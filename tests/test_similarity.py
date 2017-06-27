import numpy as np
import pytest

from democritus.exceptions import IncompatibilityInSpecification, InvalidValueInSpecification
from democritus.similarity import SimilarityFunctionReader, SimilarityFunctionFactory
from democritus.specification import Specification
from democritus.states import StatesFactory

states_spec = Specification.from_dict({'type': 'metric space', 'elements': {'type': 'numbered', 'size': 3}})
states = StatesFactory.create(states_spec)


# SimilarityFunctionFactory
def test_similarity_function_factory_create_identity():
    similarity = SimilarityFunctionFactory.create_identity(3)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0, 0]
    assert np.round(similarity[1], decimals=3).tolist() == [0, 1, 0]
    assert np.round(similarity[2], decimals=3).tolist() == [0, 0, 1]


def test_similarity_function_factory_create_nosofsky():
    similarity = SimilarityFunctionFactory.create_nosofsky(np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]]), 2)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0.779, 0.368]
    assert np.round(similarity[1], decimals=3).tolist() == [0.779, 1, 0.779]
    assert np.round(similarity[2], decimals=3).tolist() == [0.368, 0.779, 1]


# SimilarityFunctionReader
def test_similarity_function_reader_create_identity():
    similarity_spec = Specification.from_dict({'type': 'identity'})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0, 0]
    assert np.round(similarity[1], decimals=3).tolist() == [0, 1, 0]
    assert np.round(similarity[2], decimals=3).tolist() == [0, 0, 1]


def test_similarity_function_reader_create_nosofsky():
    similarity_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0.779, 0.368]
    assert np.round(similarity[1], decimals=3).tolist() == [0.779, 1, 0.779]
    assert np.round(similarity[2], decimals=3).tolist() == [0.368, 0.779, 1]


def test_similarity_function_reader_unknown_type_raises_exception():
    similarity_spec = Specification.from_dict({'type': '???????????'})
    with pytest.raises(InvalidValueInSpecification):
        SimilarityFunctionReader.create(similarity_spec, states)


def test_similarity_function_reader_missing_type_defaults_to_identity():
    similarity_spec = Specification.from_dict({'decay': 2})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0, 0]
    assert np.round(similarity[1], decimals=3).tolist() == [0, 1, 0]
    assert np.round(similarity[2], decimals=3).tolist() == [0, 0, 1]


def test_utility_factory_nosofsky_without_distance_raises_exception():
    states_spec_set = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered', 'size': 3}})
    states_set = StatesFactory.create(states_spec_set)
    utility_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
    with pytest.raises(IncompatibilityInSpecification):
        SimilarityFunctionReader.create(utility_spec, states_set)


def test_similarity_function_reader_nosofsky_missing_decay_defaults_to_1():
    similarity_spec = Specification.from_dict({'type': 'nosofsky'})
    similarity = SimilarityFunctionReader.create(similarity_spec, states)
    assert np.round(similarity[0], decimals=3).tolist() == [1, 0.368, 0.018]
    assert np.round(similarity[1], decimals=3).tolist() == [0.368, 1, 0.368]
    assert np.round(similarity[2], decimals=3).tolist() == [0.018, 0.368, 1]
