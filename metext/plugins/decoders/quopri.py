import quopri
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable


class QuoPriDecoder(BaseDecoder):
    PLUGIN_NAME = "quopri"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes quoted-printable encoded bytes-like object or a string.

        :param _input: String or bytes
        :param kwargs:
        :return: Bytes string if decoded successfully, else None
        """
        if isinstance(_input, str):
            _input = bytes(_input, "utf8")

        try:
            return quopri.decodestring(_input)
        except Exception:
            return None
