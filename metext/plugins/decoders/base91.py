import re
from typing import Optional

import base91

from metext.plugin_base import BaseDecoder, Decodable
from metext.utils import str_from_bytes, convert_to_bytes

CHARSET = "".join(base91.base91_alphabet)


class Base91Decoder(BaseDecoder):
    PLUGIN_NAME = "base91"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base91 encoded bytes-like object or ASCII string.

        See http://base91.sourceforge.net/

        :param _input: Base91 encoded (bytes) string
        :param kwargs:
        :keyword charset: Optional custom alphabet of 91 characters
        :return: `None` if `_input` couldn't be decoded, else decoded bytes string
        """
        charset = kwargs.get("charset", CHARSET)
        assert len(charset) == 91

        try:
            if not isinstance(_input, str):
                _input = str_from_bytes(_input).strip()
        except:
            return None

        if (
            re.search(
                "[^" + charset + "]",
                _input,
            )
            is not None
        ):
            return None

        if charset != CHARSET:
            _input = _input.translate(str.maketrans(charset, CHARSET))

        try:
            return convert_to_bytes(base91.decode(_input))
        except Exception:
            return None
