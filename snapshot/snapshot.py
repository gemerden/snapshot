from operator import attrgetter
from collections import namedtuple
from typing import Union, Callable, Type, Generic, TypeVar, Any, Iterable, Tuple

T = TypeVar('T')
Getter = Callable[[T], Any]


class Snapshot(Generic[T]):

    def __init__(self, *names: str, **named: Union[str, Getter]):
        """
        :param names: names of attributes of the owner to be copied to the namedtuple directly
        :param named: dict of name: string/callables:
            - if string: the dot separated location of the value in the object
            - if callable: called to get the tuple value from the object
        """
        self.names = names + tuple(named)  # all the attribute names in the namedtuple
        self.get_namedtuple = self._getter(names, named)
        self.tuple_type = lambda _: _  # satisfy mypy (could be None)

    def __set_name__(self, cls: Type[T], name: str):
        """ create the namedtuple class (subclass of tuple) """
        self.tuple_type = namedtuple(name, self.names)  # type: ignore

    def _getter(self, names, named) -> Getter:
        """ creates getters per attribute and returns a function that applies these getters """
        getters = [attrgetter(n) for n in names]
        for name, getter in named.items():
            if isinstance(getter, str):
                getters.append(attrgetter(getter))
            elif callable(getter):
                getters.append(getter)
            else:
                raise TypeError(f"{name} in {self.__class__.__name__} must either be string (attr name) or callable")

        def get_namedtuple(obj: T) -> Tuple:
            return self.tuple_type(*(g(obj) for g in getters))

        return get_namedtuple

    def __get__(self, obj: T, cls: Type[T]) -> Union['Snapshot', Tuple]:
        """ descriptors __get__ method: returns the namedtuple """
        if obj is None:
            return self
        return self.get_namedtuple(obj)

    def __call__(self, objs: Iterable[T]) -> Iterable[Tuple]:
        """ iterator over a number of named tuples created from 'objs' as in __get__"""
        return map(self.get_namedtuple, objs)

