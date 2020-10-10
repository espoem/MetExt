from typing import Optional

from .decoder import Decodable, Decoder

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
ALPHABET_LENGTH = len(ALPHABET)


class Base58(Decoder):
    def decode(self, data: Decodable, length: int = 25, **kwargs) -> Optional[bytes]:
        """
        https://rosettacode.org/wiki/Bitcoin/address_validation#Python
        """
        try:
            n = 0
            for char in data.decode("ascii") if isinstance(data, bytes) else data:
                n = n * ALPHABET_LENGTH + ALPHABET.index(char)

            return n.to_bytes(length, "big")
        except Exception:
            return None
