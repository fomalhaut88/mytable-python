"""
Struct class implements all the logic to work with objects in the table
such as get, iterate, insert, update. Field 'id' is required and must be
defined as id = Uint64(default=0).

Example:

    class Person(Struct):
        id = Uint64(default=0)
        name = Varchar(32, default="")
        age = Uint32(default=0)

    Person.bind("person.tbl")
"""

from .table import Table
from .fields import BaseField, Uint64
from .errors import IdError, NotFoundError, NoFieldError


class Struct:
    __table__ = None

    def __init_subclass__(cls):
        """
        Checks the field 'id' in the structure.
        """
        super().__init_subclass__()
        if 'id' not in cls.__dict__:
            raise NoFieldError(
                "Field 'id' is not provided. " \
                "Hint: add id = Uint64(default=0) " \
                "to the fields of the structure."
            )

    def __init__(self, **kwargs):
        """
        Constructs the object by its fields given in kwargs.
        """
        for name, field in self._iter_fields():
            value = kwargs.get(name, field.default)
            self.__setattr__(name, value)

    def __repr__(self):
        """
        Pretty string representation of the object.
        """
        attr_str = ", ".join(
            f"{name}={field.stringify(self.__dict__[name])}"
            for name, field in self._iter_fields()
        )
        return f"{self.__class__.__name__}({attr_str})"

    def __setattr__(self, name, value):
        """
        Sets attribute of the object with the validation.
        """
        field = self.__class__.__dict__[name]
        field.validate(value)
        self.__dict__[name] = value

    def as_bytes(self):
        """
        Serializes the object into bytes.
        """
        return b"".join(
            field.to_bytes(self.__dict__[name])
            for name, field in self._iter_fields()
        )

    def insert(self):
        """
        Inserts the object to the table in the end. 'id' must be equal to 0.
        The function returns 'id' that is assigned after insertion.
        """
        if self.id != 0:
            raise IdError("id must by 0 before insertion")
        idx = self.__table__.append(self.as_bytes())
        self.id = idx + 1
        self.__table__.update(self.as_bytes(), idx)
        return self.id

    def update(self):
        """
        Updates the data in the table related to the object.
        """
        idx = self.get_index_by_id(self.id)
        self.__table__.update(self.as_bytes(), idx)

    @classmethod
    def get(cls, id):
        """
        Gets object from the table by its 'id'.
        """
        idx = cls.get_index_by_id(id)
        block = cls.__table__.get(idx)
        return cls.from_bytes(block)

    @classmethod
    def block_size(cls):
        """
        Object size in bytes.
        """
        return sum(
            field.sizeof()
            for _, field in cls._iter_fields()
        )

    @classmethod
    def get_index_by_id(cls, id):
        """
        Gets index in the table by 'id'.
        """
        if id > 0 and id <= cls.__table__.size():
            return id - 1
        else:
            raise IdError(id)

    @classmethod
    def from_bytes(cls, block):
        """
        Deserializes bytes into object.
        """
        kwargs = {}
        offset = 0
        for name, field in cls._iter_fields():
            size = field.sizeof()
            kwargs[name] = field.from_bytes(block[offset:offset + size])
            offset += size
        return cls(**kwargs)

    @classmethod
    def bind(cls, path):
        """
        Binds structure to the table located by given path.
        """
        cls.__table__ = Table(path, cls.block_size())

    @classmethod
    def all(cls):
        """
        Iterates all objects in the table.
        """
        for block in cls.__table__.iter():
            yield cls.from_bytes(block)

    @classmethod
    def iter_between(cls, sorted_value_from, sorted_value_to,
                     get_sorted_value):
        """
        Iterates objects in the table between two values, if objects
        are sorted by it (for example: id, created_at, etc).
        get_sorted_value is a function that returns the value from the object.
        """
        get_value = lambda block: get_sorted_value(cls.from_bytes(block))
        idx_from = cls.__table__.find_sorted(sorted_value_from, get_value)
        idx_to = cls.__table__.find_sorted(sorted_value_to, get_value)
        for block in cls.__table__.iter_between(idx_from, idx_to):
            yield cls.from_bytes(block)

    @classmethod
    def _iter_fields(cls):
        """
        Iterates fields and names in the structure.
        """
        for name, field in cls.__dict__.items():
            if isinstance(field, BaseField):
                yield name, field
