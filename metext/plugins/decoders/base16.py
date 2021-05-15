import base64
import itertools
import logging
import re
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable

logger = logging.getLogger(__name__)


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

        try:
            if isinstance(_input, str):
                _input = _input.encode("utf8")
            if re.search(rb"[g-wyz\x80-\xff]", _input, re.IGNORECASE) is not None:
                return None
            _input = re.sub(bytes(delim or regex_auto, "ascii"), b"", _input)
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

        if not _input:
            return None

        first = _input.splitlines()[0]
        cols = [c.strip() for c in first.split(b" ") if c.strip()]
        if not cols:
            return None

        if len(cols) == 1 or all(len(c) == cols[0] for c in cols):
            # assume no address column, nor ASCII column
            return HexDecoder.run(_input)

        _bytes = re.findall(
            rb"^(?:[a-f0-9]{4,}[:-]?){1,3}[ \t]+(?:((?:[a-f0-9]{2}[ \t]{,2}){,16}))",
            _input,
            re.IGNORECASE | re.MULTILINE,
        )

        if not (
            len(cols) > 2
            and (
                (
                    len(cols[-1]) > len(cols[1])
                    and len(cols[-1]) >= sum(len(c) for c in cols[1:-1]) // 2
                )  # assume ASCII column
                or all(
                    len(c) == 2 for c in cols[1:-1]
                )  # assume each byte in separate column
            )
        ):
            # GUESSING endianess !!!
            # assume address column, no ASCII column - swap bytes order in each bytes column
            _bytes = list(itertools.chain(*(b.split(b" ") for b in _bytes)))
            _bytes = [b.strip() for b in _bytes if b.strip()]
            _bytes = [
                b"".join(
                    map(
                        lambda x, y: x.to_bytes(1, "big") + y.to_bytes(1, "big"),
                        b[-2::-2],
                        b[-1::-2],
                    )
                )
                for b in _bytes
            ]

        _input = b"".join(_bytes)

        try:
            return HexDecoder.run(_input)
        except Exception as e:
            logger.exception(e)
            return None
