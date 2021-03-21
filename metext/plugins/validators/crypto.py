from binascii import crc32
from hashlib import sha256
from typing import Optional, Union

import base58
import cashaddress
import cbor
import sha3

from metext.plugin_base import BaseValidator
from metext.plugins.decoders.base58 import CHARSETS_BASE58, Base58Decoder
from metext.plugins.decoders.bech32 import Bech32Decoder
from metext.plugins.decoders.segwit import SegwitDecoder
from metext.utils.regex import RE_ETH
from metext.utils.ss58 import ss58_decode


def is_valid_base58_address(
    address: Union[bytes, str],
    prefixes: Optional[list] = None,
    charset=CHARSETS_BASE58["bitcoin"],
    length=25,
    specs: Optional[list] = None,
) -> bool:
    """Checks validity of a address

    :param specs: List of version bytes, e.g. [b"\x00", b"\x05"] for bitcaoin
    :param address: Address to validate
    :param prefixes: First character of the address string,
    e.g. ["1", "3"] prefixes for bitcoin addresses
    :param charset: Base58 charset (different for bitcoin, ripple),
    defaults to bitcoin base58 charset
    :param length: Number of bytes in which the decoded data should be represented,
    defaults to 25
    :return: True if address is valid, else False
    """
    if prefixes is None and specs is None:
        specs = [b"\x00", b"\x05"]

    try:
        if not isinstance(address, str):
            address = address.decode("ascii")

        if prefixes and address[0] not in prefixes:
            return False
        bc_bytes = base58.b58decode(address, alphabet=charset.encode("ascii"))
        if specs and bc_bytes[0] not in (ord(s) for s in specs):
            return False
        return bc_bytes[-4:] == sha256(sha256(bc_bytes[:-4]).digest()).digest()[:4]
    except:
        return False


def is_valid_segwit_address(address, hrps=None) -> bool:
    """Checks validity of a segwit address

    :param address: Address to validate
    :param hrps: Human-readable part (e.g. "bc", "tb" for bitcoin mainnet and testnet),
    defaults to ["bc"]
    :return: True if address is valid, else False
    """
    if hrps is None:
        hrps = ["bc"]

    try:
        return any(SegwitDecoder.run(address, hrp=hrp) != (None, None) for hrp in hrps)
    except:
        return False


class BitcoinValidator(BaseValidator):
    PLUGIN_NAME = "btc"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        """Checks that given data (bytes) string represents a valid Bitcoin
        mainnet address.

        Works with base58-encoded (starts with char 1 or 3) and segwit (bech32-encoded) (starts with "bc1")
        mainnet addresses.

        :param _input: ASCII (bytes) string
        :return: True if given address string represents a valid Bitcoin address, otherwise False
        """
        return is_valid_base58_address(
            _input, prefixes=["1", "3"]
        ) or is_valid_segwit_address(_input, hrps=["bc"])


class BitcoinCashValidator(BaseValidator):
    PLUGIN_NAME = "bch"
    PLUGIN_ACTIVE = False

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        if not isinstance(_input, str):
            try:
                _input = _input.decode("ascii")
            except:
                return False

        return cashaddress.convert.is_valid(_input)


class EthereumValidator(BaseValidator):
    PLUGIN_NAME = "eth"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
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
        return is_valid_base58_address(
            _input, prefixes=["L", "M", "3"]
        ) or is_valid_segwit_address(_input, hrps=["ltc"])


class RippleValidator(BaseValidator):
    PLUGIN_NAME = "xrp"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        """Checks that given data (bytes) string represents a valid Ripple (XRP)
        address.

        Works with base58-encoded (starts with 'r') addresses.

        :param _input: ASCII (bytes) string
        :return: True if given address string represents a valid Ripple address, else False
        """
        return is_valid_base58_address(
            _input, prefixes=["r"], charset=CHARSETS_BASE58["ripple"]
        )


class TetherValidator(BaseValidator):
    PLUGIN_NAME = "usdt"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        """Checks that given data (bytes) string represents
        a valid Tether (USDT) address.

        Address may be omni-based (on Bitcoin blockchain)
         or erc20-based (on Ethereum blockchain).

        :param _input: ASCII (bytes) string
        :return: True if address string represents a valid Tether address, else False
        """
        return is_valid_base58_address(
            _input, charset=CHARSETS_BASE58["bitcoin"], specs=[b"\x00", b"\x05"]
        ) or EthereumValidator.run(_input)


class ChainlinkValidator(BaseValidator):
    PLUGIN_NAME = "chainlink"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        """Checks that given data (bytes) string represents
        a formally valid Chainlink (LINK) address.

        Conforms to ERC20-based address format.

        :param _input: ASCII (bytes) string
        :return: True if address string represents a valid Chainlink address,
        else False
        """
        return EthereumValidator.run(_input)


class CardanoValidator(BaseValidator):
    PLUGIN_NAME = "ada"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        """Checks that given data (bytes) string represents
        a Cardano (ADA) address.

        Checks address via CRC, should work with
        Yoroi and Daedalus address format as well as Shelley format.

        See: https://docs.cardano.org/projects/adrestia/en/latest/key-concepts/addresses-byron.html

        :param _input: ASCII (bytes) string
        :return: True if address string represents a valid Cardano address,
        else False
        """
        return cls.is_valid_address_byron(_input) or cls.is_valid_address_shelley(
            _input
        )

    @classmethod
    def is_valid_address_shelley(cls, address):
        hrp, decoded = Bech32Decoder.run(address)
        if decoded is None:
            return False

        return hrp in ["addr", "stake"]

    @classmethod
    def is_valid_address_byron(cls, address):
        decoded = cls._get_decoded(address)
        if not decoded or len(decoded) != 2:
            return False
        tag = decoded[0]
        expected_crc = decoded[1]
        return expected_crc == crc32(tag.value)

    @classmethod
    def _get_decoded(cls, address):
        decoded = base58.b58decode(address)
        if not decoded:
            return None
        decoded = decoded.lstrip(b"\x00")
        try:
            return cbor.loads(decoded)
        except:
            return None


class PolkadotValidator(BaseValidator):
    PLUGIN_NAME = "dot"

    @classmethod
    def run(cls, _input: Union[bytes, str], **kwargs) -> bool:
        """Checks that given data (bytes) string represents
        a Polkadot (DOT) address.

        :param _input: Address string to validate
        :return: True if address string represents a valid Polkadot address,
        else False
        """
        try:
            if not isinstance(_input, str):
                _input = _input.decode("ascii")

            if _input.startswith("0x"):
                return False

            ss58_decode(_input)
        except:
            return False

        return True
