import pytest

from democritus.elements import *


def test_elements_factory_missing_type_defaults_to_numbered():
    elements = ElementsFactory.create({'size': 2})
    assert elements == [1, 2]


def test_elements_factory_numbered():
    elements_spec = {'type': 'numbered', 'size': 5}
    elements = ElementsFactory.create(elements_spec)
    assert elements == [1, 2, 3, 4, 5]


def test_elements_factory_interval():
    elements_spec = {'type': 'interval', 'size': 5, 'start': 5, 'end': 9}
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [5, 6, 7, 8, 9]


def test_elements_factory_numbered_missing_size_raises_exception():
    elements_spec = {'type': 'numbered'}
    with pytest.raises(ValueError):
        ElementsFactory.create(elements_spec)


def test_elements_factory_interval_missing_size_raises_exception():
    elements_spec = {'type': 'interval', 'start': 5, 'end': 9}
    with pytest.raises(ValueError):
        ElementsFactory.create(elements_spec)


def test_elements_factory_interval_missing_start_defaults_to_0():
    elements_spec = {'type': 'interval', 'size': 5, 'end': 4}
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [0, 1, 2, 3, 4]


def test_elements_factory_interval_missing_end_defaults_to_1():
    elements_spec = {'type': 'interval', 'size': 3, 'start': 0.5}
    elements = ElementsFactory.create(elements_spec)
    assert elements.tolist() == [0.5, 0.75, 1]


def test_elements_factory_unknown_type_raises_exception():
    elements_spec = {'type': '????????'}
    with pytest.raises(ValueError):
        ElementsFactory.create(elements_spec)
