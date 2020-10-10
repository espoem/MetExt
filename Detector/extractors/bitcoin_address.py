import re
from typing import Iterable, List, Union

from Detector.validators.bitcoin_address import BitcoinAddress as Btc

from .extractor import Extractor

PATTERN_BTC_BASE58 = r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}"
PATTERN_BTC_SEGWIT = r"(?:[bB][cC])1[a-zA-HJ-NP-Z0-9]{25,39}"
RE_BTC = re.compile("{}|{}".format(PATTERN_BTC_SEGWIT, PATTERN_BTC_BASE58))


class BitcoinAddress(Extractor):
    btc = Btc()

    def extract_from(self, data: Union[str, List[str]]) -> Iterable[str]:
        btc_addresses = []
        for part in data if isinstance(data, list) else data.splitlines(keepends=False):
            btc_addresses.extend(RE_BTC.findall(part))
        yield from (address for address in btc_addresses if self.btc.is_valid(address))
