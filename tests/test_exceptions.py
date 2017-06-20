from democritus.exceptions import SpecificationError


def test_specification_error_default_message():
    exception = SpecificationError({})
    assert exception.args[0] is not None
