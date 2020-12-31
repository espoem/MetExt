import base64
from typing import Optional

from Detector.plugin_base import BaseDecoder, Decodable

CHARSETS_BASE32 = {
    "std": "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567",
    "hex": "0123456789ABCDEFGHIJKLMNOPQRSTUV",
}


class Base32Decoder(BaseDecoder):
    PLUGIN_NAME = "base32"

    @classmethod
    def run(cls, _input: Decodable, *args, **kwargs) -> Optional[bytes]:
        """Decodes Base32 encoded bytes-like object or ASCII `data` string
        using the base32 chars set.

        Be default the standard chars set is used.

        See https://tools.ietf.org/html/rfc4648#section-6

        :param _input: Base32 encoded (bytes) string
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :keyword alt_chars: Chars set of 32 chars to use
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        alt_chars = kwargs.get("alt_chars", CHARSETS_BASE32["std"])
        lalt_chars = len(alt_chars)
        if lalt_chars != 32:
            raise AssertionError("Only full chars set can be defined")

        if lalt_chars == 32 and alt_chars != CHARSETS_BASE32["std"]:
            # https://stackoverflow.com/questions/5537750/decode-base64-like-string-with-different-index-tables
            if isinstance(_input, str):
                tbl = str.maketrans(alt_chars, CHARSETS_BASE32["std"])
            else:
                tbl = bytes.maketrans(
                    bytes(alt_chars, "utf8"), bytes(CHARSETS_BASE32["std"], "utf8")
                )
            _input = _input.translate(tbl)

        padding_len = (8 - len(_input) & 7) & 7
        _input += ("=" if isinstance(_input, str) else b"=") * padding_len

        try:
            return base64.b32decode(_input)
        except Exception:
            return None


class Base32HexDecoder(BaseDecoder):
    PLUGIN_NAME = "base32hex"

    @classmethod
    def run(cls, _input: Decodable, *args, **kwargs) -> Optional[bytes]:
        """Decodes Base32 encoded bytes-like object or ASCII `data` string
        using the base32hex chars set.

        See https://tools.ietf.org/html/rfc4648#section-7

        :param _input: Base64 encoded (bytes) string
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        return Base32Decoder.run(_input, alt_chars=CHARSETS_BASE32["hex"])
