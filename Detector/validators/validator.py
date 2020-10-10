from abc import ABCMeta, abstractmethod
from typing import Any


class Validator(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "is_valid") and callable(subclass.is_valid)

    @abstractmethod
    def is_valid(self, data: Any) -> bool:
        raise NotImplementedError("You should implement this")
