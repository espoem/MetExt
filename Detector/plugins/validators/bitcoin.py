from hashlib import sha256
from typing import Union

from Detector.plugin_base import BaseValidator
from Detector.plugins.decoders.base58 import Base58Decoder
from Detector.plugins.decoders.segwit import SegwitDecoder


class BitcoinValidator(BaseValidator):
    PLUGIN_NAME = "btc"

    @classmethod
    def run(cls, _input: Union[bytes, str], *args, **kwargs) -> bool:
        """Checks that given data (bytes) string represents a valid Bitcoin
        mainnet address.

        Works with base58-encoded (starts with char 1 or 3) and segwit (bech32-encoded) (starts with "bc1")
        mainnet addresses.

        :param _input: ASCII (bytes) string
        :return: True if given address string represents a valid Bitcoin address, otherwise False
        """
        try:
            if not isinstance(_input, str):
                _input = _input.decode("ascii")

            if _input[0] in ["1", "3"]:
                bc_bytes = Base58Decoder.run(_input)
                return (
                    bc_bytes[-4:] == sha256(sha256(bc_bytes[:-4]).digest()).digest()[:4]
                )

            hrp, decoded = SegwitDecoder.run(_input, hrp="bc")
            return hrp is not None and decoded is not None
        except Exception:
            return False
