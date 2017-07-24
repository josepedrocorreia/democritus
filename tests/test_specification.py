import pytest

from democritus.exceptions import MissingFieldInSpecification
from democritus.specification import Specification


class TestSpecification(object):
    def test_from_dict_recursive(self):
        spec = Specification.from_dict({'a': 'b', 'c': {'d': 'e', 'f': {'g': 'h'}}})
        assert type(spec) is Specification
        assert 'a' in spec
        assert spec['a'] == 'b'
        assert type(spec['c']) is Specification
        assert spec['c']['d'] == 'e'
        assert type(spec['c']['f']) is Specification
        assert spec['c']['f']['g'] == 'h'

    def test_empty(self):
        spec = Specification.empty()
        assert len(spec) == 0

    def test_get_or_fail_successful(self):
        spec = Specification.from_dict({'a': 'b'})
        assert spec.get_or_fail('a') == 'b'

    def test_get_or_fail_unsuccessful(self):
        spec = Specification.from_dict({'a': 'b'})
        with pytest.raises(MissingFieldInSpecification):
            spec.get_or_fail('???????????')
