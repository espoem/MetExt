import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins import HEX_PATTERN_TEMPLATE
from metext.plugins.validators.baseenc import Base32Validator, Base64Validator
from metext.utils.regex import RE_BASE32, RE_BASE64


class Base32Extractor(BaseExtractor):
    PLUGIN_NAME = "base32"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts (standard) padded Base32 strings.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword min_len: Minimum length of base32 found strings
        :return: Generator of Base32 strings
        """
        min_len = kwargs.get("min_len", 50)
        for part in _input if isinstance(_input, list) else [_input]:
            part = part.replace(r"\r\n", "").replace(r"\n", "").replace(r"\r", "")
            yield from (
                b32
                for b32 in RE_BASE32.findall(part)
                if len(b32) >= min_len and Base32Validator.run(b32)
            )


class Base64Extractor(BaseExtractor):
    PLUGIN_NAME = "base64"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs):
        """Extracts (standard) padded Base64 strings.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword min_len: Minimum length of base64 found string, defaults to 50
        :return: Generator of Base64 strings
        """
        min_len = kwargs.get("min_len", 50)
        for part in _input if isinstance(_input, list) else [_input]:
            part = part.replace(r"\r\n", "").replace(r"\n", "").replace(r"\r", "")
            b64_found = [re.sub("\r\n|\n|\r", "", b) for b in RE_BASE64.findall(part)]
            yield from (
                b64
                for b64 in b64_found
                if len(b64) >= min_len and Base64Validator.run(b64)
            )


class HexExtractor(BaseExtractor):
    PLUGIN_NAME = "hex"
    PLUGIN_ACTIVE = False

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts sequences of hex strings, where each two hex chars are separated by
        a selected delimiter.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword delim: Delimiter separating 2-digit hex representation of a byte,
        can be regex pattern string. Defaults to empty string ("")
        :return: Generator of hex-representation strings
        """
        delim = kwargs.get("delim", "")
        regex = re.compile(HEX_PATTERN_TEMPLATE.format(delim=delim), re.IGNORECASE)
        for part in _input if isinstance(_input, list) else _input.splitlines():
            yield from iter(regex.findall(part))
