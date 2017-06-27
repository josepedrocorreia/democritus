class SpecificationError(Exception):
    def __init__(self, spec, msg=None):
        if msg is None:
            msg = 'Something is wrong with specification: %s' % spec
        Exception.__init__(self, msg)
        self.spec = spec


class MissingFieldInSpecification(SpecificationError):
    def __init__(self, spec, field):
        SpecificationError.__init__(self, spec,
                                    msg='Field \'%s\' missing from specification: %s'
                                        % (field, spec))
        self.field = field


class IncompatibilityInSpecification(SpecificationError):
    def __init__(self, spec, field1, field2):
        SpecificationError.__init__(self, spec,
                                    msg='Specification for field \'%s\''\
                                        ' is incompatible with specification for field \'%s\' in specification: %s'
                                        % (field1, field2, spec))
        self.field1 = field1
        self.field2 = field2


class InvalidValueInSpecification(SpecificationError):
    def __init__(self, spec, field, value):
        SpecificationError.__init__(self, spec,
                                    msg='Value \'%s\' for field \'%s\' invalid in specification: %s'
                                        % (value, field, spec))
        self.field = field
        self.value = value
