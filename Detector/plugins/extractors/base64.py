import re
from typing import List, Union

from Detector.plugin_base import BaseExtractor
from Detector.plugins.validators.base64 import Base64Validator

# https://www.rise4fun.com/Bek/tutorial/base64
PATTERN_BASE64 = r"(?:[A-Za-z0-9+/]{4})+(?:[A-Za-z0-9+/][AQgw]==|[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=)?"
RE_BASE64 = re.compile(r"\b{}\b".format(PATTERN_BASE64))


class Base64Extractor(BaseExtractor):
    PLUGIN_NAME = "base64"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs):
        """Extracts (standard) padded Base64 strings.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: String or a list of strings
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of Base64 strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            yield from (
                b64 for b64 in RE_BASE64.findall(part) if Base64Validator.run(part)
            )
