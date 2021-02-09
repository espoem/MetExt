import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor

# https://stackoverflow.com/a/25231922
RE_MD5 = re.compile(r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b")


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
