import re
from typing import Iterable, List, Union

from Detector.validators.bitcoin_address import BitcoinAddress as BTC

from .extractor import Extractor

PATTERN_BTC = r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}"
RE_BTC = re.compile(PATTERN_BTC)


class BitcoinAddress(Extractor):
    def extract_from(self, data: Union[str, List[str]]) -> Iterable[str]:
        btc_addresses = []
        for part in data if isinstance(data, list) else data.splitlines(keepends=False):
            btc_addresses.extend(RE_BTC.findall(part))
        btc = BTC()
        yield from (address for address in btc_addresses if btc.is_valid(address))
