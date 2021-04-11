from typing import Iterable

from metext.plugins.extractors import _extract_with_regex

try:
    from btclib import slip132

    has_btclib = True
except ImportError:
    has_btclib = False

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.crypto import (
    BitcoinCashValidator,
    BitcoinPrivKeyValidator,
    BitcoinValidator,
    BitcoinWifValidator,
    CardanoValidator,
    ChainlinkValidator,
    EthereumValidator,
    LitecoinValidator,
    PolkadotValidator,
    RippleValidator,
    TetherValidator,
)
from metext.utils.regex import (
    RE_ADA,
    RE_BCH,
    RE_BCH_WITH_LEGACY,
    RE_BTC,
    RE_BTC_PRIVKEY,
    RE_BTC_WIF,
    RE_DOT,
    RE_ETH,
    RE_LINK,
    RE_LTC,
    RE_USDT,
    RE_XRP,
    RE_BTC_BIP32_XKEY,
)


class BitcoinAddress(BaseExtractor):
    PLUGIN_NAME = "btc"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Bitcoin addresses from a string or a list of strings.

        Looks for addresses on mainnet:
        - base58-encoded : must confirm to pattern /[13][a-km-zA-HJ-NP-Z1-9]{25,34}/
        - segwit (bech32-encoded) : must confirm to pattern /(?:[bB][cC])1[a-zA-HJ-NP-Z0-9]{25,39}/

        See:
        - https://en.bitcoin.it/wiki/Address

        :param _input: String or a list of strings to extract Bitcoin addresses from
        :return: Generator of found valid Bitcoin addresses
        """
        yield from _extract_with_regex(
            _input, RE_BTC, validator=BitcoinValidator.run, data_kind=cls.PLUGIN_NAME
        )


class BitcoinWif(BaseExtractor):
    PLUGIN_NAME = "btc-wif"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        yield from _extract_with_regex(
            _input,
            RE_BTC_WIF,
            validator=BitcoinWifValidator.run,
            data_kind=cls.PLUGIN_NAME,
        )


class BitcoinXKey(BaseExtractor):
    PLUGIN_NAME = "btc-bip32-xkey"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        yield from _extract_with_regex(
            _input,
            RE_BTC_BIP32_XKEY,
            validator=slip132.address_from_xkey if has_btclib else None,
            data_kind=cls.PLUGIN_NAME,
        )


class BitcoinPrivateKey(BaseExtractor):
    PLUGIN_NAME = "btc-privkey"
    PLUGIN_ACTIVE = False

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        yield from _extract_with_regex(
            _input,
            RE_BTC_PRIVKEY,
            validator=BitcoinPrivKeyValidator.run,
            data_kind=cls.PLUGIN_NAME,
        )


class EthereumAddressExtractor(BaseExtractor):
    PLUGIN_NAME = "eth"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Ethereum (ETH) addresses from a string or a list of strings.

        Looks for legacy addresses and EIP-55 addresses.

        :param _input: String or a list of strings
        :return: Generator of found valid Ethereum addresses
        """
        yield from _extract_with_regex(
            _input, RE_ETH, validator=EthereumValidator.run, data_kind=cls.PLUGIN_NAME
        )


class LitecoinAddress(BaseExtractor):
    PLUGIN_NAME = "ltc"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Litecoin addresses from a string or a list of strings.

        Looks for addresses that start with 'M', 'L', or '3' char.

        .. warning::
            An address starting with '3' may represent a Bitcoin address.

        :param _input: String or a list of strings
        :return: Generator of found valid Litecoin addresses
        """
        yield from _extract_with_regex(
            _input, RE_LTC, validator=LitecoinValidator.run, data_kind=cls.PLUGIN_NAME
        )


# TODO: Check X-format https://xrpaddress.info/
class RippleAddress(BaseExtractor):
    PLUGIN_NAME = "xrp"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Ripple (XRP) addresses from a string or a list of strings.

        See: https://xrpl.org/accounts.html#addresses

        :param _input: String or a list of strings to extract Ripple addresses from
        :return: Generator of found valid Ripple addresses
        """
        yield from _extract_with_regex(
            _input, RE_XRP, validator=RippleValidator.run, data_kind=cls.PLUGIN_NAME
        )


class TetherAddress(BaseExtractor):
    PLUGIN_NAME = "usdt"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Tether (USDT) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid Tether addresses
        """
        yield from _extract_with_regex(
            _input, RE_USDT, validator=TetherValidator.run, data_kind=cls.PLUGIN_NAME
        )


class BitcoinCashAddress(BaseExtractor):
    PLUGIN_NAME = "bch"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Bitcoin Cash (BCH) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :keyword include_legacy: Flag to include legacy addresses
        conforming to BTC address format. Defaults to True
        :return: Generator of formally valid Bitcoin Cash addresses
        """
        include_legacy = kwargs.get("include_legacy", True)
        re_ = RE_BCH_WITH_LEGACY if include_legacy else RE_BCH
        yield from _extract_with_regex(
            _input, re_, validator=BitcoinCashValidator.run, data_kind=cls.PLUGIN_NAME
        )


class ChainlinkAddress(BaseExtractor):
    PLUGIN_NAME = "chainlink"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Chainlink (LINK) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid chainlink addresses
        """
        yield from _extract_with_regex(
            _input, RE_LINK, validator=ChainlinkValidator.run, data_kind=cls.PLUGIN_NAME
        )


class CardanoAddress(BaseExtractor):
    PLUGIN_NAME = "ada"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Cardano (ADA) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid Cardano addresses
        """
        yield from _extract_with_regex(
            _input, RE_ADA, validator=CardanoValidator.run, data_kind=cls.PLUGIN_NAME
        )


class PolkadotAddress(BaseExtractor):
    PLUGIN_NAME = "dot"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid Cardano (ADA) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid Cardano addresses
        """
        yield from _extract_with_regex(
            _input, RE_DOT, validator=PolkadotValidator.run, data_kind=cls.PLUGIN_NAME
        )
