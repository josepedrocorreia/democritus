from democritus.exceptions import SpecificationError


class TestSpecificationError(object):
    def test_default_message(self):
        exception = SpecificationError({})
        assert exception.args[0] is not None
