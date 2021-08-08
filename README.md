![example workflow](https://github.com/gemerden/snapshot/actions/workflows/python-app.yml/badge.svg)

# Snapshot

 Extract named tuples from classes with a simple descriptor.

## Introduction

This is a simple and fast descriptor to transform a class instance into a `namedtuple`. It can do direct (or nested) attribute access get nametuple attributes by function. Named tuples are an extension of normal tuples where the values can be accessed by name. 


## Properties 
Some use cases and advantages of using 'Snapshot' to transform class instances into named tuples are:

- Snapshot can be used by adding a single class attribute to a class,
- Like tuples, named tuples are immutable, 
- Like tuples, they can be unwrapped (`a, b, c = some_snapshot`),
- They can be used to speed up algorithms, by 'flattening' the data in advance,
- They can be used to turn your classes into compatible arguments for functions and constructors (e.g. `some_func(*some_snapshot)`),
- Because named tuples support attribute access, they can often be used as drop-in replacements of the original class instances, 
- Namedtuples support nice printing out-of-the-box,
- Turning instances into named tuples is about as fast as python allows (a simple snapshot on my 6 year old PC in about 1 microsecond),
- Attribute access on a named tuple seems about 10% faster than on a class instance (same machine).

## Installation

To install the module you can use: `pip install snapshot`. It has only standard library dependencies. 

## Limitations

This module runs on Python >= 3.6. Earlier versions have not been tested, but probably work. Let me know if this is not the case.

## Code Sample

Here is a basic example of how to use 'Snapshot'.

```python
from snapshot import Snapshot

class Some:
    snapshot = Snapshot('a', x='b', y=lambda obj: obj.c, z=lambda obj: obj.d ** 2, ea='e.a')

    def __init__(self, a, b=None, c=None, d=None, e=None):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

some = Some(1, 2, 3, 4, Some(a=5))

snapshot = some.snapshot
assert (snapshot.a, snapshot.x, snapshot.y, snapshot.z, snapshot.ea) == (1, 2, 3, 16, 5)

a, x, y, z, ea = snapshot
assert (a, x, y, z, ea) == (1, 2, 3, 16, 5)
  
```

## Use Case
A simple use case, where instances odf a class are transformed to be able to use an existing library:

```python
import math
from snapshot import Snapshot

def some_distance(p1, p2):
    """ some distance function as an example of an external API to call"""
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class GeoLocation(object):
    point2d = Snapshot(x='latitude', y='longitude')  # transformation

    def __init__(self, latitude, longitude, altitude):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

geoloc1 = GeoLocation(latitude=10, longitude=50, altitude=17)
geoloc2 = GeoLocation(latitude=12, longitude=60, altitude=-23)

# turn the geolocations into points and calculate the distance
dist = some_distance(geoloc1.point2d, geoloc2.point2d)
print(geoloc1.point2d, geoloc2.point2d, 'distance =', dist)
```
prints:

`>>> point2d(x=10, y=50) point2d(x=12, y=60) distance = 10.198039027185569`

## Authors

Lars van Gemerden (rational-it) - initial code and documentation.

## License

See LICENSE.
