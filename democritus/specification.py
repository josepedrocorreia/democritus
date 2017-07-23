from democritus.exceptions import MissingFieldInSpecification


class Specification(dict):
    @staticmethod
    def from_dict(dictionary):
        spec = Specification()
        for key in dictionary:
            value = dictionary[key]
            if type(value) is dict:
                value = Specification.from_dict(value)
            spec[key] = value
        return spec

    @staticmethod
    def empty():
        return Specification.from_dict({})

    def get_or_fail(self, field):
        if field not in self:
            raise MissingFieldInSpecification(self, field)
        else:
            return self[field]
