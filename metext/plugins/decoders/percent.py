from typing import Optional
from urllib.parse import unquote_to_bytes

from metext.plugin_base import BaseDecoder, Decodable


class PercentDecoder(BaseDecoder):
    PLUGIN_NAME = "percent"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes percent encoded (URL encoded) bytes-like object or a string.

        :param _input: String or bytes
        :param kwargs:
        :return: Bytes string if decoded successfully, else None
        """
        try:
            return unquote_to_bytes(_input)
        except Exception:
            return None
