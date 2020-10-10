from hashlib import sha256
from typing import Any

from Detector.codecs.base58 import Base58

from .validator import Validator


class BitcoinAddress(Validator):
    decoder = Base58()

    def is_valid(self, data: Any) -> bool:
        """
        https://rosettacode.org/wiki/Bitcoin/address_validation#Python
        """
        try:
            bcbytes = self.decoder.decode(data)
            return bcbytes[-4:] == sha256(sha256(
                bcbytes[:-4]).digest()).digest()[:4]
        except Exception:
            return False
