from typing import List, Tuple, Union

from metext.plugin_base import BaseDecoder, Decodable
from metext.utils import str_from_bytes

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


class Bech32Decoder(BaseDecoder):
    """Bech32 decoders using base32 type of encoding.

    Using https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py
    """

    @classmethod
    def run(
        cls, _input: Decodable, **kwargs
    ) -> Union[Tuple[None, None], Tuple[str, List[int]]]:
        """Decodes Bech32 encoded bytes-like object or ASCII data string.

        :param _input: Data string to decode
        :param kwargs: Arbitrary keyword arguments
        :return: Tuple (hrp, data) with human-readable part and decoded data.
        Returns (None, None) if `data` is not valid bech32 encoded (bytes) string.
        """
        try:
            if not isinstance(_input, str):
                _input = str_from_bytes(_input)
        except Exception:
            return None, None

        max_length = kwargs.get("max_length", 90)
        if (any(ord(x) < 33 or ord(x) > 126 for x in _input)) or (
            _input.lower() != _input and _input.upper() != _input
        ):
            return None, None
        _input = _input.lower()
        pos = _input.rfind("1")
        if pos < 1 or pos + 7 > len(_input) or len(_input) > max_length:
            return None, None
        if any(x not in CHARSET for x in _input[pos + 1 :]):
            return None, None
        hrp = _input[:pos]
        result = [CHARSET.find(x) for x in _input[pos + 1 :]]
        if not cls.verify_checksum(hrp, result):
            return None, None
        return hrp, result[:-6]

    @classmethod
    def verify_checksum(cls, hrp, data):
        """Verify a checksum given HRP and converted data characters."""
        return cls.polymod(cls.hrp_expand(hrp) + data) in (1, 0x2BC830A3)

    @classmethod
    def polymod(cls, values):
        """Internal function that computes the Bech32 checksum."""
        generator = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
        chk = 1
        for value in values:
            top = chk >> 25
            chk = (chk & 0x1FFFFFF) << 5 ^ value
            for i in range(5):
                chk ^= generator[i] if ((top >> i) & 1) else 0
        return chk

    @classmethod
    def hrp_expand(cls, hrp):
        """Expand the HRP into values for checksum computation."""
        return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
