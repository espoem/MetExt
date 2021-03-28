import base64
from typing import Optional

import pem

from metext.plugin_base import BaseDecoder, Decodable


class PemDecoder(BaseDecoder):
    PLUGIN_NAME = "pem"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Optional[bytes]:
        """Decodes PEM certificate as bytes containing
         certificate info in DER format.

        :param _input: String or bytes
        :param kwargs:
        :return: Bytes string if decoded successfully, else None
        """
        if isinstance(_input, str):
            _input = _input.encode("utf-8")

        try:
            pems = pem.parse(_input)
        except:
            return None

        res = []
        for p in pems:
            data = b"".join(p.as_bytes().splitlines()[1:-1])
            try:
                res.append(base64.b64decode(data))
            except:
                continue

        return b"\n\n".join(res)
