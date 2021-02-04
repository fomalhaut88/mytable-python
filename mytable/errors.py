"""
Here are classes for errors in the library.
"""

class MytableError(Exception):
    pass


class StructError(MytableError):
    pass


class NotFoundError(StructError):
    pass


class IdError(StructError):
    pass


class FieldError(MytableError):
    pass


class NoFieldError(FieldError):
    pass


class ValidationError(FieldError):
    pass


class InvalidLengthError(ValidationError):
    pass


class TooLongError(InvalidLengthError):
    pass
