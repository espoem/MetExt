import base64
import sys
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable
from metext.utils import z85


class Base85Decoder(BaseDecoder):
    PLUGIN_NAME = "base85"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base85 encoded bytes-like object or ASCII `data` string.

        :param _input: Base85 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        try:
            return base64.b85decode(_input)
        except Exception:
            return None


class Ascii85Decoder(BaseDecoder):
    PLUGIN_NAME = "ascii85"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Ascii85 encoded bytes-like object or ASCII `data` string.

        :param _input: Ascii85 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        if not _input:
            return None

        if isinstance(_input, str):
            _input = _input.encode("utf-8")

        _input = _input.strip()

        try:
            if _input[:2] == b"<~" and _input[-2:] == b"~>":
                return base64.a85decode(_input, adobe=True)
            return base64.a85decode(_input, adobe=False, foldspaces=True)
        except:
            return None


class Z85Decoder(BaseDecoder):
    PLUGIN_NAME = "z85"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Z85 encoded bytes-like object or ASCII `data` string.

        :param _input: Z85 encoded (bytes) string
        :param kwargs:
        :return: `None` if `data` couldn't be decoded, else decoded byte string'
        """
        try:
            return z85.decode(_input)
        except:
            return None
