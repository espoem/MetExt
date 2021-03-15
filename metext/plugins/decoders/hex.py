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


class HexdumpDecoder(BaseDecoder):
    PLUGIN_NAME = "hexdump"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes hexdump format

        Tries to naively decode bytes basic hexdump format produced
        by programs such as hexdump, od, xdd.

        :param _input: String or bytes containing hex dump
        :param kwargs: Arbitrary keyword arguments
        :return: None if decoding failed, else bytes string
        """
        if isinstance(_input, str):
            _input = _input.encode("utf8")

        chunks = [c.strip() for c in _input.split(b" ", maxsplit=10)[:-1] if c.strip()]
        if not chunks:
            return None

        if len(chunks) == 1:
            return HexDecoder.run(_input)

        if len(chunks[0]) > 4 and len(chunks[0]) > len(chunks[1]):
            _input = b"".join(
                re.findall(
                    rb"^(?:[a-f0-9]{4,}[:-]?){1,3}[ \t]+(?:((?:[a-f0-9]{2}[ \t]{,2}){,32}))",
                    _input,
                    re.IGNORECASE | re.MULTILINE,
                )
            )

        try:
            return HexDecoder.run(_input)
        except:
            return None
