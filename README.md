# mytable-python

Mytable implements an approach to store struct instances into a binary file. Generally, the file represents a database with one table with some limitations that are made for simplicity, minimization of the space and high performance on add a new record, search, update or iterate. So it can be successfully used for the purposes like logging. Notice: the library does not provide a way to delete records from the table, so if you need it you should implement it by your own.

## Installation

```
pip install git+https://github.com/fomalhaut88/mytable-python
```

## Basic example

### Define the structure

You can define the structure this way. Once you did it and started to insert the data you cannot modify the fields, otherwise the stored data will be broken.

```python
from mytable.struct import Struct
from mytable.fields import Uint32, Varchar, Uint64

class Person(Struct):
    id = Uint64(default=0)
    name = Varchar(32, default="")
    age = Uint32(default=0)

Person.bind("person.tbl")
```

### Work with the data

Insert a record:

```python
alex = Person("alex", 32)
alex.insert()
```

Update a record:

```python
alex.age = 33
alex.update()
```

Get record by id:

```python
person = Person.get(1)
```

Iterate all records:

```python
for person in Person.all():
    print(person)
```

Iterate the records between two values of a sorted field.

```python
for person in Person.iter_between(2, 6, lambda p: p.id):
    print(person)
```
