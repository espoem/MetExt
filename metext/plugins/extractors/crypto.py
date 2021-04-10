from typing import Iterable, List, Union

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
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Bitcoin addresses from a string or a list of strings.

        Looks for addresses on mainnet:
        - base58-encoded : must confirm to pattern /[13][a-km-zA-HJ-NP-Z1-9]{25,34}/
        - segwit (bech32-encoded) : must confirm to pattern /(?:[bB][cC])1[a-zA-HJ-NP-Z0-9]{25,39}/

        See:
        - https://en.bitcoin.it/wiki/Address

        :param _input: String or a list of strings to extract Bitcoin addresses from
        :return: Generator of found valid Bitcoin addresses
        """

        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_BTC.findall(part)
                if BitcoinValidator.run(address)
            )


class BitcoinWif(BaseExtractor):
    PLUGIN_NAME = "btc-wif"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        if not isinstance(_input, str):
            try:
                _input = _input.decode("utf-8")
            except:
                yield from ()

        global_pos_start = 0
        for part in _input.splitlines(keepends=True):
            matches = list(RE_BTC_WIF.finditer(part))
            for match in matches:
                wif = match.group(0)
                if not BitcoinWifValidator.run(wif):
                    continue
                yield {
                    "value": wif,
                    "position": (
                        global_pos_start + match.start(0),
                        global_pos_start + match.end(0),
                    ),
                }
            global_pos_start += len(part)


class BitcoinXKey(BaseExtractor):
    PLUGIN_NAME = "btc-bip32-xkey"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        if not isinstance(_input, str):
            try:
                _input = _input.decode("utf-8")
            except:
                yield from ()

        global_pos_start = 0
        for part in _input.splitlines(keepends=True):
            matches = list(RE_BTC_BIP32_XKEY.finditer(part))
            for match in matches:
                if has_btclib:
                    try:
                        slip132.address_from_xkey(match.group(0))
                    except:
                        continue

                yield {
                    "value": match.group(0),
                    "position": (
                        global_pos_start + match.start(0),
                        global_pos_start + match.end(0),
                    ),
                }
            global_pos_start += len(part)


class BitcoinPrivateKey(BaseExtractor):
    PLUGIN_NAME = "btc-privkey"
    PLUGIN_ACTIVE = False

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:

        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_BTC_PRIVKEY.findall(part)
                if BitcoinPrivKeyValidator.run(address)
            )


class EthereumAddressExtractor(BaseExtractor):
    PLUGIN_NAME = "eth"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Ethereum (ETH) addresses from a string or a list of strings.

        Looks for legacy addresses and EIP-55 addresses.

        :param _input: String or a list of strings
        :return: Generator of found valid Ethereum addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_ETH.findall(part)
                if EthereumValidator.run(address)
            )


class LitecoinAddress(BaseExtractor):
    PLUGIN_NAME = "ltc"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Litecoin addresses from a string or a list of strings.

        Looks for addresses that start with 'M', 'L', or '3' char.

        .. warning::
            An address starting with '3' may represent a Bitcoin address.

        :param _input: String or a list of strings
        :return: Generator of found valid Litecoin addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_LTC.findall(part)
                if LitecoinValidator.run(address)
            )


# TODO: Check X-format https://xrpaddress.info/
class RippleAddress(BaseExtractor):
    PLUGIN_NAME = "xrp"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Ripple (XRP) addresses from a string or a list of strings.

        See: https://xrpl.org/accounts.html#addresses

        :param _input: String or a list of strings to extract Ripple addresses from
        :return: Generator of found valid Ripple addresses
        """

        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_XRP.findall(part)
                if RippleValidator.run(address)
            )


class TetherAddress(BaseExtractor):
    PLUGIN_NAME = "usdt"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Tether (USDT) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid Tether addresses
        """

        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_USDT.findall(part)
                if TetherValidator.run(address)
            )


class BitcoinCashAddress(BaseExtractor):
    PLUGIN_NAME = "bch"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Bitcoin Cash (BCH) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :keyword include_legacy: Flag to include legacy addresses
        conforming to BTC address format. Defaults to True
        :return: Generator of formally valid Bitcoin Cash addresses
        """
        include_legacy = kwargs.get("include_legacy", True)
        re_ = RE_BCH_WITH_LEGACY if include_legacy else RE_BCH

        for part in _input if isinstance(_input, list) else [_input]:
            yield from (
                address
                for address in re_.findall(part)
                if BitcoinCashValidator.run(
                    "bitcoincash:" + address
                    if address[0].lower() in ["q", "p"]
                    else address
                )
            )


class ChainlinkAddress(BaseExtractor):
    PLUGIN_NAME = "chainlink"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Chainlink (LINK) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid chainlink addresses
        """

        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_LINK.findall(part)
                if ChainlinkValidator.run(address)
            )


class CardanoAddress(BaseExtractor):
    PLUGIN_NAME = "ada"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Cardano (ADA) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid Cardano addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_ADA.findall(part)
                if CardanoValidator.run(address)
            )


class PolkadotAddress(BaseExtractor):
    PLUGIN_NAME = "dot"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Cardano (ADA) addresses from a string or a list of strings.

        :param _input: String or a list of strings
        :return: Generator of formally valid Cardano addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_DOT.findall(part)
                if PolkadotValidator.run(address)
            )
