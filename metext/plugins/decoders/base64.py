import base64
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable

CHARSETS_BASE64 = {
    "std": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
    "urlsafe": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_",
    "filenamesafe": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_",
    "itoa64": "./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    "radix-64": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/",
}


class Base64Decoder(BaseDecoder):
    PLUGIN_NAME = "base64"

    @classmethod
    def run(cls, _input: Decodable, *args, **kwargs) -> Optional[bytes]:
        """Decodes Base64 encoded bytes-like object or ASCII `data` string
        using the base64 chars set.

        Be default the standard chars set with the special chars "+/" is used.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: Base64 encoded (bytes) string
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :keyword alt_chars: Defines alternative full chars set of 64 chars, or set of 2 special chars, defaults to "+/"
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        alt_chars = kwargs.get("alt_chars", "+/")
        lalt_chars = len(alt_chars)
        if lalt_chars not in [
            2,  # special chars set
            64,  # full chars set
        ]:
            raise AssertionError(
                "Only full chars set or special chars set can be defined"
            )

        if lalt_chars == 64 and alt_chars != CHARSETS_BASE64["std"]:
            # https://stackoverflow.com/questions/5537750/decode-base64-like-string-with-different-index-tables
            if isinstance(_input, str):
                tbl = str.maketrans(alt_chars, CHARSETS_BASE64["std"])
            else:
                tbl = bytes.maketrans(
                    bytes(alt_chars, "utf8"), bytes(CHARSETS_BASE64["std"], "utf8")
                )
            _input = _input.translate(tbl)

        padding_len = (4 - len(_input) & 3) & 3
        _input += ("=" if isinstance(_input, str) else b"=") * padding_len

        try:
            return base64.b64decode(_input, altchars=alt_chars[-2:])
        except Exception:
            return None


class Base64UrlDecoder(BaseDecoder):
    PLUGIN_NAME = "base64url"

    @classmethod
    def run(cls, _input: Decodable, *args, **kwargs) -> Optional[bytes]:
        """Decodes Base64 encoded bytes-like object or ASCII `data` string
        using the standard base64 charset with `-` and `_` characters.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param _input: Base64 encoded (bytes) string
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        return Base64Decoder.run(_input, *args, alt_chars="-_", **kwargs)
