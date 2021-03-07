import gzip
from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable


class GzipDecoder(BaseDecoder):
    PLUGIN_NAME = "gzip"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decompress gzipped data

        :param _input: Bytes data
        :param kwargs:
        :return: Bytes if decompressed successfully, else None
        """
        if isinstance(_input, str):
            _input = bytes(_input, "utf8")

        try:
            return gzip.decompress(_input)
        except Exception:
            return None
