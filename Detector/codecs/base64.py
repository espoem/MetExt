import base64
from typing import Optional

from .decoder import Decodable, Decoder


class Base64(Decoder):
    def decode(self, data: Decodable, *args, **kwargs) -> Optional[bytes]:
        """Decodes Base64 encoded bytes-like object or ASCII `data` string
        using the standard base64 charset with `+` and `/` characters.

        See https://tools.ietf.org/html/rfc4648#section-4

        :param data: Base64 encoded (bytes) string
        :param args: Variable arguments
        :param kwargs: Other keyword arguments
        :return: `None` if `data` couldn't be decoded, else decoded byte string
        """
        padding_len = (4 - len(data) & 3) & 3

        try:
            if isinstance(data, str):
                return base64.b64decode(data + "=" * padding_len)

            return base64.b64decode(data + b"=" * padding_len)
        except Exception:
            return None
