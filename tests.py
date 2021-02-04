import os
from unittest import TestCase

from mytable.struct import Struct
from mytable.fields import Uint64, Uint32, Varchar


class MytableTest(TestCase):
    table_path = "person.tbl"

    def setUp(self):
        class Person(Struct):
            id = Uint64(default=0)
            name = Varchar(32, default="")
            age = Uint32(default=0)
        Person.bind(self.table_path)
        self.Person = Person

    def tearDown(self):
        os.remove(self.table_path)

    def test_insert(self):
        person = self.Person(name='alex', age=32)
        person.insert()
        self.assertEqual(self.Person.__table__.size(), 1)

    def test_insert_many(self):
        for age in range(30, 35):
            person = self.Person(name='alex', age=32)
            person.insert()
        self.assertEqual(self.Person.__table__.size(), 5)

    def test_get(self):
        person = self.Person(name='alex', age=32)
        person_id = person.insert()
        self.assertEqual(person_id, 1)

        alex = self.Person.get(person_id)
        self.assertEqual(alex.name, "alex")
        self.assertEqual(alex.age, 32)

    def test_update(self):
        person = self.Person(name='alex', age=32)
        person_id = person.insert()
        self.assertEqual(person_id, 1)

        alex = self.Person.get(person_id)
        alex.age = 33
        alex.update()

        record = self.Person.get(person_id)
        self.assertEqual(alex.name, "alex")
        self.assertEqual(alex.age, 33)
