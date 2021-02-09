import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.crypto import LitecoinValidator

PATTERN_LTC_BASE58 = r"\b[LM3][a-km-zA-HJ-NP-Z1-9]{26,33}\b"
RE_LTC = re.compile(PATTERN_LTC_BASE58)


class LitecoinAddress(BaseExtractor):
    PLUGIN_NAME = "ltc"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Litecoin addresses from a string or a list of strings.

        Looks for addresses that start with 'M', 'L', or '3' char.

        .. warning::
            An address starting with '3' may represent a Bitcoin address.

        :param _input: String or a list of strings
        :return: Generator of found valid Litecoin addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_LTC.findall(part)
                if LitecoinValidator.run(address)
            )
