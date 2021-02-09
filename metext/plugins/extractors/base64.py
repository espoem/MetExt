import re
from typing import List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.baseenc import Base64Validator

# https://www.rise4fun.com/Bek/tutorial/base64
PATTERN_BASE64 = r"(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/][AQgw]==|[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=)?"
RE_BASE64 = re.compile(r"{}".format(PATTERN_BASE64))


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
        for part in _input if isinstance(_input, list) else _input.splitlines():
            yield from (
                b64
                for b64 in RE_BASE64.findall(part)
                if len(b64) >= min_len and Base64Validator.run(b64)
            )
