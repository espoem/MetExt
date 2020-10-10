import base64
from typing import Optional

from .decoder import Decodable, Decoder


class Base64(Decoder):

    def decode(self, data: Decodable, **kwargs) -> Optional[bytes]:
        padding_len = ((4 - len(data) % 4) % 4)

        try:
            if isinstance(data, str):
                return base64.b64decode(data + "=" * padding_len)

            return base64.b64decode(data + b"=" * padding_len)
        except Exception:
            return None
