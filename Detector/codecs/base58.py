from typing import Optional

from .decoder import Decodable, Decoder

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
ALPHABET_LENGTH = len(ALPHABET)


class Base58(Decoder):
    def decode(self, data: Decodable, *args, **kwargs) -> Optional[bytes]:
        """
        https://rosettacode.org/wiki/Bitcoin/address_validation#Python
        """
        length = kwargs.get("length", 25)
        try:
            n = 0
            for char in data if isinstance(data, str) else data.decode("ascii"):
                n = n * ALPHABET_LENGTH + ALPHABET.index(char)

            return n.to_bytes(length, "big")
        except Exception:
            return None
