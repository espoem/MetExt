import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor

# https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
RE_MAC = re.compile(
    r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}|(?:[0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}\b"
)


class MACAddressExtractor(BaseExtractor):
    PLUGIN_NAME = "mac"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts MAC addresses

        :param _input: String or a list of strings to extract MAC address from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of MAC addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from iter(RE_MAC.findall(part))
