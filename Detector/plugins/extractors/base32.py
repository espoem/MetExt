import re
from typing import Iterable, List, Union

from Detector.plugin_base import BaseExtractor
from Detector.plugins.validators.base32 import Base32Validator

# https://stackoverflow.com/a/27362880
PATTERN_BASE32 = (
    r"(?:[A-Z2-7]{8})*(?:[A-Z2-7]{2}={6}|[A-Z2-7]{4}={4}|[A-Z2-7]{5}={3}|[A-Z2-7]{7}=)?"
)
RE_BASE32 = re.compile(r"{}".format(PATTERN_BASE32))


class Base32Extractor(BaseExtractor):
    PLUGIN_NAME = "base32"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts (standard) padded Base32 strings.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: String or a list of strings
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of Base32 strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            yield from (
                b32
                for b32 in RE_BASE32.findall(part)
                if b32 and Base32Validator.run(b32)
            )
