import pytest

from Detector.codecs.base64 import Base64


@pytest.mark.parametrize(
    "encoded, expected",
    [(b"MQ==", b"1"), ("MQ", b"1"), ("YmFzZTY0", b"base64"), ("ěšč", None)],
)
def test_decode(encoded, expected):
    assert Base64().decode(encoded) == expected
