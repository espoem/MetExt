import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor

RE_SHA1 = re.compile(r"\b[a-f0-9]{40}\b", re.IGNORECASE)
RE_SHA224 = re.compile(r"\b[a-f0-9]{56}\b", re.IGNORECASE)
RE_SHA256 = re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE)
RE_SHA384 = re.compile(r"\b[a-f0-9]{96}\b", re.IGNORECASE)
RE_SHA512 = re.compile(r"\b[a-f0-9]{128}\b", re.IGNORECASE)


class SHA1Extractor(BaseExtractor):
    PLUGIN_NAME = "sha1"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-1 hash string.

        :param _input: String or a list of strings to extract SHA-1 hash string from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of SHA-1 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_SHA1.findall(part))


class SHA224Extractor(BaseExtractor):
    PLUGIN_NAME = "sha224"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-224 hash string.

        :param _input: String or a list of strings to extract SHA-224 hash string from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of SHA-224 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_SHA224.findall(part))


class SHA256Extractor(BaseExtractor):
    PLUGIN_NAME = "sha256"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-256 hash string.

        :param _input: String or a list of strings to extract SHA-256 hash string from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of SHA-256 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_SHA256.findall(part))


class SHA384Extractor(BaseExtractor):
    PLUGIN_NAME = "sha384"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-384 hash string.

        :param _input: String or a list of strings to extract SHA-384 hash string from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of SHA-384 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_SHA384.findall(part))


class SHA512Extractor(BaseExtractor):
    PLUGIN_NAME = "sha512"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-512 hash string.

        :param _input: String or a list of strings to extract SHA-512 hash string from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of SHA-512 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_SHA512.findall(part))
