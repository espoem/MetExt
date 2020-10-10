from typing import Any

from .bech32 import Bech32
from .decoder import Decodable, Decoder


def convert_bits(data, from_bits, to_bits, pad=True):
    """General power-of-2 base conversion."""
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << to_bits) - 1
    max_acc = (1 << (from_bits + to_bits - 1)) - 1
    for value in data:
        if value < 0 or (value >> from_bits):
            return None
        acc = ((acc << from_bits) | value) & max_acc
        bits += from_bits
        while bits >= to_bits:
            bits -= to_bits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (to_bits - bits)) & maxv)
    elif bits >= from_bits or ((acc << (to_bits - bits)) & maxv):
        return None
    return ret


class Segwit(Decoder):
    """https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py"""

    bech32 = Bech32()

    def decode(self, data: Decodable, *args, **kwargs) -> Any:
        """Decode a segwit address."""
        hrp = kwargs.get("hrp")
        hrpgot, data = self.bech32.decode(data)
        if hrpgot != hrp:
            return None, None
        decoded = convert_bits(data[1:], 5, 8, False)
        if decoded is None or len(decoded) < 2 or len(decoded) > 40:
            return None, None
        if data[0] > 16:
            return None, None
        if data[0] == 0 and len(decoded) != 20 and len(decoded) != 32:
            return None, None
        return data[0], decoded
