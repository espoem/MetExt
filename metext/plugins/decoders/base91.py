from typing import Optional

import base91

from metext.plugin_base import BaseDecoder, Decodable

CHARSET = "".join(base91.base91_alphabet)


class Base91Decoder(BaseDecoder):
    PLUGIN_NAME = "base91"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes Base91 encoded bytes-like object or ASCII string.

        See http://base91.sourceforge.net/

        :param _input: Base91 encoded (bytes) string
        :param kwargs:
        :return: `None` if `_input` couldn't be decoded, else decoded bytes string
        """
        alt_chars = kwargs.get("alt_chars", CHARSET)
        if len(alt_chars) != 91:
            raise AssertionError(
                "Only full chars set or special chars set can be defined"
            )

        if alt_chars != CHARSET:
            if isinstance(_input, str):
                tbl = str.maketrans(alt_chars, CHARSET)
            else:
                tbl = bytes.maketrans(
                    bytes(alt_chars, "ascii"), bytes(CHARSET, "ascii")
                )
            _input = _input.translate(tbl)

        try:
            return bytes(base91.decode(str(_input, encoding="ascii")))
        except Exception:
            return None
