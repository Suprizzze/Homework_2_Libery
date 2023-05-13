
class Verify:
    @classmethod
    def verify_str(cls, inst):
        if not isinstance(inst, str):
            raise TypeError("Type must be a string")
        return inst

    @classmethod
    def verify_int(cls, inst):
        if not isinstance(inst, int):
            raise TypeError("Type must be an integer between 0 and 10 inclusive")
        return inst

    @classmethod
    def verify_isdigit(cls, inst):
        if not str(inst).isdigit():
            raise Exception("Can only be a digit as a string or an integer")
        return inst
