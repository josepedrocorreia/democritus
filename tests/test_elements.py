import pytest

from democritus.elements import *
from democritus.exceptions import *
from democritus.specification import Specification


def test_elements_factory_missing_type_defaults_to_numbered():
    elements_spec = Specification.from_dict({'size': 2})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [1, 2]


def test_elements_factory_numbered():
    elements_spec = Specification.from_dict({'type': 'numbered', 'size': 5})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [1, 2, 3, 4, 5]


def test_elements_factory_interval():
    elements_spec = Specification.from_dict({'type': 'interval', 'size': 5, 'start': 5, 'end': 9})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [5, 6, 7, 8, 9]


def test_elements_factory_numbered_missing_size_raises_exception():
    elements_spec = Specification.from_dict({'type': 'numbered'})
    with pytest.raises(MissingFieldInSpecification):
        ElementsFactory.create(elements_spec)


def test_elements_factory_interval_missing_size_raises_exception():
    elements_spec = Specification.from_dict({'type': 'interval', 'start': 5, 'end': 9})
    with pytest.raises(MissingFieldInSpecification):
        ElementsFactory.create(elements_spec)


def test_elements_factory_interval_missing_start_defaults_to_0():
    elements_spec = Specification.from_dict({'type': 'interval', 'size': 5, 'end': 4})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [0, 1, 2, 3, 4]


def test_elements_factory_interval_missing_end_defaults_to_1():
    elements_spec = Specification.from_dict({'type': 'interval', 'size': 3, 'start': 0.5})
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [0.5, 0.75, 1]


def test_elements_factory_unknown_type_raises_exception():
    elements_spec = Specification.from_dict({'type': '????????'})
    with pytest.raises(InvalidValueInSpecification):
        ElementsFactory.create(elements_spec)
