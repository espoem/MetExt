import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor

RE_SHA1 = re.compile(r"\b[a-f0-9]{40}\b", re.IGNORECASE)


class SHA1Extractor(BaseExtractor):
    PLUGIN_NAME = "sha1"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts strings that is in accordance with the SHA-1 hash string.

        :param _input: String or a list of strings to extract SHA-1 hash string from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of MD5 hash strings
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_SHA1.findall(part))
