from abc import ABCMeta, abstractmethod
from typing import Iterable


class Extractor(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "extract_from") and callable(
            subclass.extract_from)

    @abstractmethod
    def extract_from(self, data: str) -> Iterable[str]:
        raise NotImplementedError("You should implement this")
