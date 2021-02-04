"""
Fields have the logic to serialize and validate the values to store
in the table. Each field defined a value with fixed tpe and size.
"""

import struct

from .errors import ValidationError, TooLongError, InvalidLengthError


class BaseField:
    """
    Base field class with the necessary methods to implement.
    """

    def __init__(self, default=None):
        assert default is not None, "no default value"
        self.default = default

    def stringify(self, value):
        """
        Represents the value as string.
        """
        return repr(value)

    def validate(self, value):
        """
        Validates the value.
        """
        if value is None:
            raise ValidationError(value)

    def sizeof(self):
        """
        Size of the value in bytes.
        """
        raise NotImplementedError()

    def to_bytes(self, value):
        """
        Serializes to bytes.
        """
        raise NotImplementedError()

    def from_bytes(self, block):
        """
        Deserializes from bytes.
        """
        raise NotImplementedError()


class Varchar(BaseField):
    """
    Strings with fixed length.
    """

    def __init__(self, length, **kwargs):
        super().__init__(**kwargs)
        self.length = length

    def stringify(self, value):
        return f'"{value}"'

    def validate(self, value):
        super().validate(value)
        if len(value) > self.length:
            raise TooLongError(value)

    def sizeof(self):
        return self.length

    def to_bytes(self, value):
        block = value.encode()
        block += b'\x00' * (self.length - len(block))
        return block

    def from_bytes(self, block):
        return block.decode()


class Bytes(BaseField):
    """
    Bytes with fixed length.
    """

    def __init__(self, length, **kwargs):
        super().__init__(**kwargs)
        self.length = length

    def stringify(self, value):
        return f'"{value}"'

    def validate(self, value):
        super().validate(value)
        if len(value) != self.length:
            raise InvalidLengthError(value)

    def sizeof(self):
        return self.length

    def to_bytes(self, value):
        return value

    def from_bytes(self, block):
        return block


class Uint8(BaseField):
    """
    Unsigned 8-bit integer.
    """

    def sizeof(self):
        return 1

    def to_bytes(self, value):
        return struct.pack('>B', value)

    def from_bytes(self, block):
        return struct.unpack('>B', block)[0]


class Uint16(BaseField):
    """
    Unsigned 16-bit integer.
    """

    def sizeof(self):
        return 2

    def to_bytes(self, value):
        return struct.pack('>H', value)

    def from_bytes(self, block):
        return struct.unpack('>H', block)[0]


class Uint32(BaseField):
    """
    Unsigned 32-bit integer.
    """

    def sizeof(self):
        return 4

    def to_bytes(self, value):
        return struct.pack('>I', value)

    def from_bytes(self, block):
        return struct.unpack('>I', block)[0]


class Uint64(BaseField):
    """
    Unsigned 64-bit integer.
    """

    def sizeof(self):
        return 8

    def to_bytes(self, value):
        return struct.pack('>Q', value)

    def from_bytes(self, block):
        return struct.unpack('>Q', block)[0]


class Int8(BaseField):
    """
    Signed 8-bit integer.
    """

    def sizeof(self):
        return 1

    def to_bytes(self, value):
        return struct.pack('>b', value)

    def from_bytes(self, block):
        return struct.unpack('>b', block)[0]


class Int16(BaseField):
    """
    Signed 16-bit integer.
    """

    def sizeof(self):
        return 2

    def to_bytes(self, value):
        return struct.pack('>h', value)

    def from_bytes(self, block):
        return struct.unpack('>h', block)[0]


class Int32(BaseField):
    """
    Signed 32-bit integer.
    """

    def sizeof(self):
        return 4

    def to_bytes(self, value):
        return struct.pack('>i', value)

    def from_bytes(self, block):
        return struct.unpack('>i', block)[0]


class Int64(BaseField):
    """
    Signed 64-bit integer.
    """

    def sizeof(self):
        return 8

    def to_bytes(self, value):
        return struct.pack('>q', value)

    def from_bytes(self, block):
        return struct.unpack('>q', block)[0]


class Boolean(BaseField):
    """
    Boolean.
    """

    def sizeof(self):
        return 1

    def to_bytes(self, value):
        return struct.pack('?', value)

    def from_bytes(self, block):
        return struct.unpack('?', block)[0]


class Float32(BaseField):
    """
    32-bit float.
    """

    def sizeof(self):
        return 4

    def to_bytes(self, value):
        return struct.pack('f', value)

    def from_bytes(self, block):
        return struct.unpack('f', block)[0]


class Float64(BaseField):
    """
    64-bit float (double).
    """

    def sizeof(self):
        return 8

    def to_bytes(self, value):
        return struct.pack('d', value)

    def from_bytes(self, block):
        return struct.unpack('d', block)[0]
