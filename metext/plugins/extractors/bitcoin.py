import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.crypto import BitcoinValidator

PATTERN_BTC_BASE58 = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"
PATTERN_BTC_SEGWIT = r"\b(?:[bB][cC])1[a-zA-HJ-NP-Z0-9]{25,39}\b"
RE_BTC = re.compile("{}|{}".format(PATTERN_BTC_SEGWIT, PATTERN_BTC_BASE58))


class BitcoinAddress(BaseExtractor):
    PLUGIN_NAME = "btc"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Bitcoin addresses from a string or a list of strings.

        Looks for addresses on mainnet:
        - base58-encoded : must confirm to pattern /[13][a-km-zA-HJ-NP-Z1-9]{25,34}/
        - segwit (bech32-encoded) : must confirm to pattern /(?:[bB][cC])1[a-zA-HJ-NP-Z0-9]{25,39}/

        See:
        - https://en.bitcoin.it/wiki/Address

        :param _input: String or a list of strings to extract Bitcoin addresses from
        :return: Generator of found valid Bitcoin addresses
        """

        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_BTC.findall(part)
                if BitcoinValidator.run(address)
            )
