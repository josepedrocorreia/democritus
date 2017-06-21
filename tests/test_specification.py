import pytest

from democritus.exceptions import MissingFieldInSpecification
from democritus.specification import Specification


def test_from_dict_recursive():
    spec = Specification.from_dict({'a': 'b', 'c': {'d': 'e', 'f': {'g': 'h'}}})
    assert type(spec) is Specification
    assert 'a' in spec
    assert spec['a'] == 'b'
    assert type(spec['c']) is Specification
    assert spec['c']['d'] == 'e'
    assert type(spec['c']['f']) is Specification
    assert spec['c']['f']['g'] == 'h'


def test_get_or_fail_successful():
    spec = Specification.from_dict({'a': 'b'})
    assert spec.get_or_fail('a') == 'b'


def test_get_or_fail_unsuccessful():
    spec = Specification.from_dict({'a': 'b'})
    with pytest.raises(MissingFieldInSpecification):
        spec.get_or_fail('???????????')
