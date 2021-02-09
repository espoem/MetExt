from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.utils.regex import (
    RE_MD5,
    RE_SHA1,
    RE_SHA224,
    RE_SHA256,
    RE_SHA384,
    RE_SHA512,
)


class MD5Extractor(BaseExtractor):
    PLUGIN_NAME = "md5"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts strings that conform to the MD5 hash string.

        :param _input: String or a list of strings to extract MD5 hash string from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of MD5 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_MD5.findall(part))


class SHA1Extractor(BaseExtractor):
    PLUGIN_NAME = "sha1"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-1 hash string.

        :param _input: String or a list of strings to extract SHA-1 hash string from
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
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-224 hash string.

        :param _input: String or a list of strings to extract SHA-224 hash string from
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
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-256 hash string.

        :param _input: String or a list of strings to extract SHA-256 hash string from
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
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-384 hash string.

        :param _input: String or a list of strings to extract SHA-384 hash string from
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
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-512 hash string.

        :param _input: String or a list of strings to extract SHA-512 hash string from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of SHA-512 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_SHA512.findall(part))
