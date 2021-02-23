from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.isbn import IsbnValidator
from metext.utils.regex import RE_ISBN10, RE_ISBN13


class IsbnExtractor(BaseExtractor):
    PLUGIN_NAME = "isbn"

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
            yield from (isbn for isbn in isbn10 + isbn13 if IsbnValidator.run(isbn))


class Isbn10Extractor(BaseExtractor):
    PLUGIN_NAME = "isbn10"

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
            yield from (
                isbn for isbn in RE_ISBN10.findall(part) if IsbnValidator.run(isbn)
            )


class Isbn13Extractor(BaseExtractor):
    PLUGIN_NAME = "isbn13"

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
            yield from (
                isbn for isbn in RE_ISBN13.findall(part) if IsbnValidator.run(isbn)
            )
