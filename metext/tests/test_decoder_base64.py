import pytest

from metext.plugins.decoders.base64 import Base64Decoder, CHARSETS_BASE64


@pytest.mark.parametrize(
    "value, expected",
    [
        ("MQ==", b"1"),
        ("MQ", b"1"),
        ("YmFzZTY0", b"base64"),
        ("ěšč", None),
        (
            "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZWxpdCwgc2VkIGRv\nIGVpdXNtb2QgdGVtcG9yIGluY2lkaWR1bnQgdXQgbGFib3JlIGV0IGRvbG9yZSBtYWdu\nYSBhbGlxdWEu",
            b"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        ),
    ],
)
def test_decode(value, expected):
    assert Base64Decoder.run(value) == expected
    assert Base64Decoder.run(value.encode()) == expected


@pytest.mark.parametrize(
    "encoded, expected",
    [("SGVsbG9Xb3JsZD8/Pw==", b"HelloWorld???")],
)
def test_decode_custom_charset(encoded, expected):
    for k, v in CHARSETS_BASE64.items():
        translated = encoded.translate(str.maketrans(CHARSETS_BASE64["std"], v))
        run = Base64Decoder.run(translated, charset=v)
        assert run == expected
