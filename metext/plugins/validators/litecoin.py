from hashlib import sha256
from typing import Union

from metext.plugin_base import BaseValidator
from metext.plugins.decoders.base58 import Base58Decoder


class LitecoinValidator(BaseValidator):
    PLUGIN_NAME = "ltc"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        """Checks that given (bytes) string represents a valid
        Litecoin mainnet address.

        Works with addresses that start with 'L', 'M', or '3' char.

        :param _input: ASCII (bytes) string
        :return: True if address string is a valid Litecoin address, else False
        """
        try:
            if not isinstance(_input, str):
                _input = _input.decode("ascii")

            if _input[0] not in ["L", "M", "3"]:
                return False
            bc_bytes = Base58Decoder.run(_input)
            return bc_bytes[-4:] == sha256(sha256(bc_bytes[:-4]).digest()).digest()[:4]
        except Exception:
            return False
