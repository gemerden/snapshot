```markdown
![example workflow](https://github.com/gemerden/snapshot/actions/workflows/python-app.yml/badge.svg)
```

# Snapshot

 Extract named tuples from classes with a simple descriptor.

## Introduction

This is a simple and fast descriptor to extract named tuples from instances of a class. It can do some by direct (or nested) attribute access and by defining function to get the value. Named tuples are an extension of normal tuples where the values can be accessed by name. There are in the Python standard library in 'collections'.

Some use cases and advantages of using 'Snapshot' to transform class instances into named tuples are:

- Snapshot can be used by adding a single class attribute to a class,
- Like tuples, named tuples are immutable, 
- Like tuples, they can be unwrapped (`a, b, c = some_snapshot`),
- They can be used to speed up algorithms, by 'flattening' the data in advance,
- They can be used to turn your classes into compatible arguments for functions and constructors (e.g. `some_func(*some_snapshot)`),
- Because named tuples support attribute access, they can often be used as drop-in replacements of the original class instances,
- Turning instances into named tuples is about as fast as python allows (a simple snapshot on my 6 year old computer in about 1 microsecond),
- Attribute access on a named tuple seems about 10% faster than on a class instance (same machine).

## Installation

To install the module you can use: `pip install snapshot`. It has only standard library dependencies. 

## Limitations

This module runs on Python >= 3.6. Earlier versions have not been tested, but probably work. Let me know if this is not the case.

## Code Sample

Here is a simple example of how to use 'Snapshot'.

```python
from snapshot import Snapshot

class Some(object):
    snapsy = Snapshot('a', x='b', y=lambda obj: obj.c, z=lambda obj: obj.d ** 2, ea='e.a')

    def __init__(self, a, b=None, c=None, d=None, e=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

some = Some(1, 2, 3, 4, Some(5))

snap = some.snapsy
assert (snap.a, snap.x, snap.y, snap.z, snap.ea) == (1, 2, 3, 16, 5)

a, x, y, z, ea = snap
assert (a, x, y, z, ea) == (1, 2, 3, 16, 5)
  
```

## Authors

Lars van Gemerden (rational-it) - initial code and documentation.

## License

See LICENSE.
