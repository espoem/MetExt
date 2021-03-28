from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.isbn import IsbnValidator
from metext.utils.regex import RE_ISBN10, RE_ISBN13


class IsbnExtractor(BaseExtractor):
    PLUGIN_NAME = "isbn"

    valid_isbns = set()

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid ISBN10 and ISBN13 identifiers
        from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with ISBN identifiers
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            isbn10 = RE_ISBN10.findall(part)
            isbn13 = RE_ISBN13.findall(part)
            isbn = isbn10 + isbn13
            for i in isbn:
                if i in cls.valid_isbns:
                    yield i
                    continue
                if IsbnValidator.run(i):
                    cls.valid_isbns.add(i)
                    yield i


class Isbn10Extractor(BaseExtractor):
    PLUGIN_NAME = "isbn10"

    valid_isbns = set()

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid ISBN10 identifiers from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with ISBN10 identifiers
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            isbn = RE_ISBN10.findall(part)
            for i in isbn:
                if i in cls.valid_isbns:
                    yield i
                    continue
                if IsbnValidator.run(i):
                    cls.valid_isbns.add(i)
                    yield i


class Isbn13Extractor(BaseExtractor):
    PLUGIN_NAME = "isbn13"

    valid_isbns = set()

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid ISBN13 identifiers from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with ISBN13 identifiers
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue

            isbn = RE_ISBN13.findall(part)
            for i in isbn:
                if i in cls.valid_isbns:
                    yield i
                    continue
                if IsbnValidator.run(i):
                    cls.valid_isbns.add(i)
                    yield i
