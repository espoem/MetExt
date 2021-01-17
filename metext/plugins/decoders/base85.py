import base64
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable


class Base85Decoder(BaseDecoder):
    PLUGIN_NAME = "base85"

    @classmethod
    def run(cls, _input: Decodable, *args, **kwargs) -> Optional[bytes]:
        """Decodes Base85 encoded bytes-like object or ASCII `data` string.

        :param _input: Base85 encoded (bytes) string
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        try:
            return base64.b85decode(_input)
        except Exception:
            return None
