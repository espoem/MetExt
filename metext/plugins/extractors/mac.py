from typing import Iterable

from metext.plugin_base import BaseExtractor

# https://www.geeksforgeeks.org/how-to-validate-mac-address-using-regular-expression/
from metext.plugins.extractors import _extract_with_regex
from metext.utils.regex import RE_MAC


class MACAddressExtractor(BaseExtractor):
    PLUGIN_NAME = "mac"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts MAC addresses

        :param _input: String or a list of strings to extract MAC address from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of MAC addresses
        """
        yield from _extract_with_regex(_input, RE_MAC)
