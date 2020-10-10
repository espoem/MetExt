from typing import List, Tuple, Union

from .decoder import Decodable, Decoder

ALPHABET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


class Bech32(Decoder):
    """https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py"""

    def decode(
        self, data: Decodable, *args, **kwargs
    ) -> Union[Tuple[None, None], Tuple[Union[int, bytes, str], List[int]]]:
        try:
            if not isinstance(data, str):
                data = data.decode("ascii")
        except Exception:
            return None, None

        if (any(ord(x) < 33 or ord(x) > 126 for x in data)) or (
            data.lower() != data and data.upper() != data
        ):
            return None, None
        data = data.lower()
        pos = data.rfind("1")
        if pos < 1 or pos + 7 > len(data) or len(data) > 90:
            return None, None
        if any(x not in ALPHABET for x in data[pos + 1 :]):
            return None, None
        hrp = data[:pos]
        data = [ALPHABET.find(x) for x in data[pos + 1 :]]
        if not self.verify_checksum(hrp, data):
            return None, None
        return hrp, data[:-6]

    def verify_checksum(self, hrp, data):
        """Verify a checksum given HRP and converted data characters."""
        return self.polymod(self.hrp_expand(hrp) + data) == 1

    def polymod(self, values):
        """Internal function that computes the Bech32 checksum."""
        generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
        chk = 1
        for value in values:
            top = chk >> 25
            chk = (chk & 0x1FFFFFF) << 5 ^ value
            for i in range(5):
                chk ^= generator[i] if ((top >> i) & 1) else 0
        return chk

    def hrp_expand(self, hrp):
        """Expand the HRP into values for checksum computation."""
        return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
