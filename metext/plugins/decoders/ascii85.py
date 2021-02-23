import base64
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable
from metext.utils import z85


class Ascii85Decoder(BaseDecoder):
    PLUGIN_NAME = "ascii85"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Ascii85 encoded bytes-like object or ASCII `data` string.

        :param _input: Ascii85 encoded (bytes) string
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        try:
            return base64.a85decode(_input)
        except Exception:
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
