import pytest

from Detector.codecs.base64 import Base64


class TestBase64Decoder:
    @pytest.mark.parametrize(
        "encoded, expected", [(b"MQ==", b"1"), ("MQ", b"1"), ("YmFzZTY0", b"base64")]
    )
    def test_decode(self, encoded, expected):
        assert Base64().decode(encoded) == expected
