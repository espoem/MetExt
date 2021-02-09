import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.baseenc import Base32Validator

# https://stackoverflow.com/a/27362880
PATTERN_BASE32 = (
    r"(?:[A-Z2-7]{8})*(?:[A-Z2-7]{2}={6}|[A-Z2-7]{4}={4}|[A-Z2-7]{5}={3}|[A-Z2-7]{7}=)?"
)
RE_BASE32 = re.compile(r"{}".format(PATTERN_BASE32))


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
        for part in _input if isinstance(_input, list) else _input.splitlines():
            yield from (
                b32
                for b32 in RE_BASE32.findall(part)
                if len(b32) >= min_len and Base32Validator.run(b32)
            )
