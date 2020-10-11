from hashlib import sha256
from typing import Union

from Detector.codecs.base58 import Base58
from Detector.codecs.segwit import Segwit

from .validator import Validator


class BitcoinAddress(Validator):
    base58 = Base58()
    segwit = Segwit()

    def is_valid(self, data: Union[bytes, str]) -> bool:
        """Checks that given data (bytes) string represents a valid Bitcoin mainnet address.

        Works with base58-encoded (starts with char 1 or 3) and segwit (bech32-encoded) (starts with "bc1")
        mainnet addresses.

        :param data: ASCII (bytes) string
        :return: True if given address string represents a valid Bitcoin address, otherwise False
        """
        try:
            if data[0] in ["1", "3"]:
                bc_bytes = self.base58.decode(data)
                return (
                    bc_bytes[-4:] == sha256(sha256(bc_bytes[:-4]).digest()).digest()[:4]
                )

            hrp, decoded = self.segwit.decode(data, hrp="bc")
            return hrp is not None and decoded is not None
        except Exception:
            return False
