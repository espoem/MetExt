import base64
import re
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable


class HexDecoder(BaseDecoder):
    PLUGIN_NAME = "hex"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes hex (base16) encoded bytes string or ASCII string

        :param _input: String or bytes in hex representation
        :param kwargs: Arbitrary keyword arguments
        :keyword delim: String delimiter separating 2-digit hex representation of a byte.
        If `delim` is empty, then it will remove any char outside hex charset and 0x pairs.
        Defaults to empty string ("")
        :return:
        """
        delim = kwargs.get("delim", "")
        regex_auto = r"[^a-fA-F\d]|(0x)"
        if isinstance(_input, str):
            _input = re.sub(delim or regex_auto, "", _input)
        else:
            _input = re.sub(bytes(delim or regex_auto, "ascii"), b"", _input)

        try:
            return base64.b16decode(_input, casefold=True)
        except:
            return None
