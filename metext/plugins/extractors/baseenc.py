import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.plugins.validators.baseenc import Base32Validator, Base64Validator
from metext.utils.regex import RE_BASE32, RE_BASE64


class Base32Extractor(BaseExtractor):
    PLUGIN_NAME = "base32"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts (standard) padded Base32 strings.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword min_len: Minimum length of base32 found strings,
        defaults to 25
        :return: Generator of Base32 strings
        """
        min_len = kwargs.get("min_len", 25)
        yield from _extract_with_regex(
            _input,
            RE_BASE32,
            validator=lambda val: len(val) >= min_len and Base32Validator.run(val),
            per_line=True,
            preprocess=lambda val: val.replace(r"\r\n", "")
            .replace(r"\n", "")
            .replace(r"\r", ""),
        )


class Base64Extractor(BaseExtractor):
    PLUGIN_NAME = "base64"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts (standard) padded Base64 strings.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword min_len: Minimum length of base64 found string,
        defaults to 25
        :return: Generator of Base64 strings
        """
        min_len = kwargs.get("min_len", 25)
        yield from _extract_with_regex(
            _input,
            RE_BASE64,
            validator=(lambda val: len(val) >= min_len and Base64Validator.run(val)),
            per_line=False,
            preprocess=(
                lambda val: val.replace(r"\r\n", "")
                .replace(r"\n", "")
                .replace(r"\r", "")
            ),
            postprocess=(lambda val: re.sub("\r\n|\n|\r", "", val)),
        )


class HexExtractor(BaseExtractor):
    PLUGIN_NAME = "hex"
    PLUGIN_ACTIVE = False

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
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
        yield from _extract_with_regex(
            _input,
            regex,
        )


HEX_DELIMITERS = {
    "None": "",
    "Space": " ",
    "Comma": ",",
    "Semicolon": ";",
    "Colon": ":",
    "LF": r"\n",
    "CRLF": r"\r\n",
    "0x": "0x",
    "comma-0x": ",0x",
    r"\x": r"[\]x",
}
HEX_PATTERN_TEMPLATE = r"[\dA-F]{{2}}(?:{delim}[\dA-F]{{2}})*"
