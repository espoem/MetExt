from typing import Optional

from .decoder import Decodable, Decoder

ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
ALPHABET_LENGTH = len(ALPHABET)


class Base58(Decoder):
    def decode(self, data: Decodable, *, length: int = 25, **kwargs) -> Optional[bytes]:
        """Decodes Base58 encoded bytes-like object or ASCII `data` string
        using the charset defined for Bitcoin addresses.

        Using https://rosettacode.org/wiki/Bitcoin/address_validation#Python

        :param data: Base58 encoded (bytes) string
        :param length: Number of bytes in which the decoded data should be represented
        :param kwargs: Other keyword arguments
        :return: Decode bytes string. Returns `None` if `data` couldn't be decoded.
        """
        try:
            n = 0
            for char in data if isinstance(data, str) else data.decode("ascii"):
                n = n * ALPHABET_LENGTH + ALPHABET.index(char)

            return n.to_bytes(length, "big")
        except Exception:
            return None
