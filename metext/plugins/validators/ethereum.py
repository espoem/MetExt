from typing import Union

import sha3

from metext.plugin_base import BaseValidator
from metext.utils import RE_ETH


class EthereumValidator(BaseValidator):
    PLUGIN_NAME = "eth"

    @classmethod
    def run(cls, _input: Union[bytes, str], *args, **kwargs) -> bool:
        """Checks that given (bytes) string represents a valid Ethereum address.

        :param _input: ASCII (bytes) string
        :return: True if given string is a valid Ethereum address, else False
        """
        try:
            if not isinstance(_input, str):
                _input = _input.decode("ascii")

            if not RE_ETH.match(_input):
                return False

            _input = _input[2:]
            if _input.lower() == _input or _input.upper() == _input:
                return True

            # mixed-case address | https://github.com/ethereum/EIPs/blob/master/EIPS/eip-55.md
            # https://github.com/joeblackwaslike/coinaddr/blob/master/coinaddr/validation.py
            _hash = sha3.keccak_256(_input.lower().encode("ascii")).hexdigest()
            return not any(
                (int(_hash[i], 16) > 7 and _input[i].upper() != _input[i])
                or (int(_hash[i], 16) <= 7 and _input[i].lower() != _input[i])
                for i in range(len(_input))
            )
        except Exception:
            return False
