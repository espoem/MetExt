from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable

CHARSETS_BASE58 = {
    "bitcoin": "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz",
    "ripple": "rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz",
}


class Base58Decoder(BaseDecoder):
    PLUGIN_NAME = "base58"
    PLUGIN_ACTIVE = False

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base58 encoded bytes-like object or ASCII `data` string
        using the charset defined for Bitcoin addresses.

        Using https://rosettacode.org/wiki/Bitcoin/address_validation#Python

        :param _input: Base58 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :keyword length: Number of bytes in which the decoded data should be represented.
        Defaults to None, that means no restriction on output bytes length
        :keyword alt_chars: Alphabet for base58 decoding. Use Bitcoin alphabet by default
        :return: Decode bytes string. Returns `None` if `data` couldn't be decoded.
        """
        alt_chars = kwargs.get("alt_chars", CHARSETS_BASE58["bitcoin"])
        assert len(alt_chars) == 58
        length = kwargs.get("length", None)
        try:
            n = 0
            for char in _input if isinstance(_input, str) else _input.decode("ascii"):
                n = n * 58 + alt_chars.index(char)

            return n.to_bytes(
                length if length is not None else (n.bit_length() + 7) // 8, "big"
            )
        except:
            return None


class Base58BitcoinDecoder(BaseDecoder):
    PLUGIN_NAME = "base58btc"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base58 encoded bytes-like object or ASCII `data` string
        using the charset defined for Bitcoin addresses.

        Using https://rosettacode.org/wiki/Bitcoin/address_validation#Python

        :param _input: Base58 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :keyword length: Number of bytes in which the decoded data should be represented, defaults to 25
        :return: Decode bytes string. Returns `None` if `data` couldn't be decoded.
        """
        kwargs_ = {"length": 25}.update(kwargs)
        return Base58Decoder.run(
            _input, alt_chars=CHARSETS_BASE58["bitcoin"], **kwargs_
        )


class Base58RippleDecoder(BaseDecoder):
    PLUGIN_NAME = "base58ripple"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base58 encoded bytes-like object or ASCII `data` string
        using the charset defined for Bitcoin addresses.

        Using https://rosettacode.org/wiki/Bitcoin/address_validation#Python

        :param _input: Base58 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :keyword length: Number of bytes in which the decoded data should be represented, defaults to 25
        :return: Decode bytes string. Returns `None` if `data` couldn't be decoded.
        """
        kwargs_ = {"length": 25}.update(kwargs)
        return Base58Decoder.run(_input, alt_chars=CHARSETS_BASE58["ripple"], **kwargs_)
