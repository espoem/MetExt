from typing import List, Optional, Tuple, Union

from metext.plugin_base import BaseDecoder, Decodable
from metext.plugins.decoders.bech32 import Bech32Decoder


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


class SegwitDecoder(BaseDecoder):
    """Bitcoin Segwit address decoding class.

    Using https://github.com/sipa/bech32/blob/master/ref/python/segwit_addr.py
    """

    @classmethod
    def run(
        cls, _input: Decodable, **kwargs
    ) -> Union[Tuple[None, None], Tuple[str, List[int]]]:
        """Decodes Bech32 encoded bytes-like object or ASCII data string
        containing a (Bitcoin) Segwit address.

        See https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki#witness-program

        :param _input: Data to decode
        :param kwargs: Arbitrary keyword arguments
        :keyword hrp: Keyword argument for Human-readable part. Used as a check for an expected type of an address.
        Using "bc" for mainnet addresses and "tb" for testnet addresses, defaults to "bc"
        :return: Tuple (witness_version, witness_program), returns (None, None) if decoded program and version
        are not valid.
        """
        hrp = kwargs.get("hrp", "bc")
        hrpgot, _input = Bech32Decoder.run(_input)
        if hrp and hrpgot != hrp:
            return None, None
        decoded = convert_bits(_input[1:], 5, 8, False)
        if decoded is None or len(decoded) < 2 or len(decoded) > 40:
            return None, None
        if _input[0] > 16:
            return None, None
        if _input[0] == 0 and len(decoded) != 20 and len(decoded) != 32:
            return None, None
        return _input[0], decoded
