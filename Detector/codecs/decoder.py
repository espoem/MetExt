from abc import ABCMeta, abstractmethod
from typing import Any, Union

Decodable = Union[bytes, str]


class Decoder(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "decode") and callable(subclass.decode)

    @abstractmethod
    def decode(self, data: Decodable, *args, **kwargs) -> Any:
        raise NotImplementedError("You should implement this")
