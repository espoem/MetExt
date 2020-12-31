import pytest

from Detector.plugins.decoders.base64 import Base64Decoder


@pytest.mark.parametrize(
    "encoded, expected",
    [(b"MQ==", b"1"), ("MQ", b"1"), ("YmFzZTY0", b"base64"), ("ěšč", None)],
)
def test_decode(encoded, expected):
    assert Base64Decoder.run(encoded) == expected
