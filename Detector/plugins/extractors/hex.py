import re
from typing import Iterable, List, Union

from Detector.plugin_base import BaseExtractor
from Detector.plugins import HEX_PATTERN_TEMPLATE


class HexExtractor(BaseExtractor):
    PLUGIN_NAME = "hex"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts sequences of hex strings, where each two hex chars are separated by
        a selected delimiter.

        :param _input: String or a list of strings
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :keyword delim: Delimiter separating 2-digit hex representation of a byte,
        can be regex pattern string. Defaults to empty string ("")
        :return: Generator of hex-representation strings
        """
        delim = kwargs.get("delim", "")
        regex = re.compile(HEX_PATTERN_TEMPLATE.format(delim=delim), re.IGNORECASE)
        for part in _input if isinstance(_input, list) else _input.splitlines():
            yield from iter(regex.findall(part))
