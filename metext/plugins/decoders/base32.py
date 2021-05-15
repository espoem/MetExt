import base64
import re
from typing import Optional

import base32_crockford

from metext.plugin_base import BaseDecoder, Decodable
from metext.utils import convert_to_bytes, str_from_bytes

CHARSETS = {
    "std": "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567",
    "hex": "0123456789ABCDEFGHIJKLMNOPQRSTUV",
    "z-base-32": "ybndrfg8ejkmcpqxot1uwisza345h769",
    "geohash": "0123456789bcdefghjkmnpqrstuvwxyz",
    "word-safe": "23456789CFGHJMPQRVWXcfghjmpqrvwx",
}


class Base32Decoder(BaseDecoder):
    PLUGIN_NAME = "base32"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base32 encoded bytes-like object or ASCII `data` string
        using the base32 chars set.

        Be default the standard chars set is used.

        See https://tools.ietf.org/html/rfc4648#section-6

        :param _input: Base32 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :keyword charset: Alphabet of 32 chars to use for decoding
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        charset = kwargs.get("charset", CHARSETS["std"])
        if len(charset) != 32:
            raise AssertionError("Only full chars set can be defined")

        _input = convert_to_bytes(_input)

        if (
            re.search(convert_to_bytes(r"[^{}=\r\n]".format(charset)), _input)
            is not None
        ):
            return None

        if charset != CHARSETS["std"]:
            # https://stackoverflow.com/questions/5537750/decode-base64-like-string-with-different-index-tables
            tbl = bytes.maketrans(
                bytes(charset, "utf8"), bytes(CHARSETS["std"], "utf8")
            )
            _input = _input.translate(tbl)

        _input += b"=" * ((8 - len(_input) & 7) & 7)

        try:
            return base64.b32decode(_input)
        except:
            return None


class Base32HexDecoder(BaseDecoder):
    PLUGIN_NAME = "base32hex"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base32 encoded bytes-like object or ASCII `data` string
        using the base32hex chars set.

        See https://tools.ietf.org/html/rfc4648#section-7

        :param _input: Base64 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        return Base32Decoder.run(_input, charset=CHARSETS["hex"])


class Base32CrockfordDecoder(BaseDecoder):
    PLUGIN_NAME = "base32crockford"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base32 encoded bytes-like object or ASCII `data` string
        using the chars set and rules as defined by Douglas Crockford.

        See https://www.crockford.com/base32.html

        :param _input: Base64 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        try:
            if not isinstance(_input, str):
                _input = str_from_bytes(_input)

            if (
                re.search(r"[^0123456789ABCDEFGHJKMNPQRSTVWXYZ]", _input.upper())
                is not None
            ):
                return None
            decoded = base32_crockford.decode(_input, strict=True)
            return decoded.to_bytes((decoded.bit_length() + 7) // 8, byteorder="big")
        except:
            return None
