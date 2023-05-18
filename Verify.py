import uuid
from string import ascii_letters


class ValidName:

    @classmethod
    def name_str_valid(cls, value):
        val = list(filter(lambda x: x not in ascii_letters, value))
        if len(val) > 0 or value != value.capitalize():
            raise TypeError("First name or last name must start with a capital letter and have only letters")
        return value

    @classmethod
    def __get_validators__(cls):
        yield cls.name_str_valid


class ValidUuid:

    @classmethod
    def uuid_str_valid(cls, value):
        if not isinstance(value, uuid.UUID):
            raise TypeError("Uuid must be of type uuid only")
        return value

    @classmethod
    def __get_validators__(cls):
        yield cls.uuid_str_valid
#






