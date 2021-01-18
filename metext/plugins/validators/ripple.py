from hashlib import sha256
from typing import Union

from metext.plugin_base import BaseValidator
from metext.plugins.decoders.base58 import CHARSETS_BASE58, Base58Decoder


class RippleValidator(BaseValidator):
    PLUGIN_NAME = "xrp"

    @classmethod
    def run(cls, _input: Union[bytes, str], *args, **kwargs) -> bool:
        """Checks that given data (bytes) string represents a valid Ripple (XRP)
        address.

        Works with base58-encoded (starts with 'r') addresses.

        :param _input: ASCII (bytes) string
        :return: True if given address string represents a valid Ripple address, else False
        """
        try:
            if not isinstance(_input, str):
                _input = _input.decode("ascii")

            if _input[0] != "r":
                return False
            bc_bytes = Base58Decoder.run(_input, alt_chars=CHARSETS_BASE58["ripple"])
            return bc_bytes[-4:] == sha256(sha256(bc_bytes[:-4]).digest()).digest()[:4]
        except Exception:
            return False
