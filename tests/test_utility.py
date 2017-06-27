import numpy as np
import pytest

from democritus.exceptions import IncompatibilityInSpecification, InvalidValueInSpecification
from democritus.specification import Specification
from democritus.states import StatesFactory
from democritus.utility import UtilityFactory, NosofskyUtility, IdentityUtility

states_spec = Specification.from_dict({'type': 'metric space', 'elements': {'type': 'numbered', 'size': 3}})
states = StatesFactory.create(states_spec)


def test_utility_factory_create_identity():
    utility_spec = Specification.from_dict({'type': 'identity'})
    utility = UtilityFactory.create(utility_spec, states)
    assert type(utility) is IdentityUtility
    assert np.round(utility.utilities[0], decimals=3).tolist() == [1, 0, 0]
    assert np.round(utility.utilities[1], decimals=3).tolist() == [0, 1, 0]
    assert np.round(utility.utilities[2], decimals=3).tolist() == [0, 0, 1]


def test_utility_factory_create_nosofsky():
    utility_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
    utility = UtilityFactory.create(utility_spec, states)
    assert type(utility) is NosofskyUtility
    assert np.round(utility.utilities[0], decimals=3).tolist() == [1, 0.779, 0.368]
    assert np.round(utility.utilities[1], decimals=3).tolist() == [0.779, 1, 0.779]
    assert np.round(utility.utilities[2], decimals=3).tolist() == [0.368, 0.779, 1]


def test_utility_factory_unknown_type_raises_exception():
    utility_spec = Specification.from_dict({'type': '???????????'})
    with pytest.raises(InvalidValueInSpecification):
        UtilityFactory.create(utility_spec, states)


def test_utility_factory_missing_type_defaults_to_identity():
    utility_spec = Specification.from_dict({'decay': 2})
    utility = UtilityFactory.create(utility_spec, states)
    assert type(utility) is IdentityUtility


def test_utility_factory_nosofsky_without_distance_raises_exception():
    states_spec_set = Specification.from_dict({'type': 'set', 'elements': {'type': 'numbered', 'size': 3}})
    states_set = StatesFactory.create(states_spec_set)
    utility_spec = Specification.from_dict({'type': 'nosofsky', 'decay': 2})
    with pytest.raises(IncompatibilityInSpecification):
        UtilityFactory.create(utility_spec, states_set)


def test_utility_factory_nosofsky_missing_decay_defaults_to_1():
    utility_spec = Specification.from_dict({'type': 'nosofsky'})
    utility = UtilityFactory.create(utility_spec, states)
    assert type(utility) is NosofskyUtility
    assert np.round(utility.utilities[0], decimals=3).tolist() == [1, 0.368, 0.018]
    assert np.round(utility.utilities[1], decimals=3).tolist() == [0.368, 1, 0.368]
    assert np.round(utility.utilities[2], decimals=3).tolist() == [0.018, 0.368, 1]
