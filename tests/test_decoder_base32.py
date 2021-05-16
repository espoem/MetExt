import pytest

from metext.plugins.decoders.base32 import CHARSETS, Base32Decoder


@pytest.mark.parametrize(
    "encoded, expected",
    [
        ("JBSWY3DPK5XXE3DE", b"HelloWorld"),
        ("GE======", b"1"),
        ("GE", b"1"),
        ("G.======", None),
    ],
)
def test_decode(encoded, expected):
    assert Base32Decoder.run(encoded) == expected
    assert Base32Decoder.run(encoded.encode()) == expected


@pytest.mark.parametrize(
    "encoded, expected",
    [("JBSWY3DPK5XXE3DE", b"HelloWorld")],
)
def test_decode_custom_charset(encoded, expected):
    for k, v in CHARSETS.items():
        translated = encoded.translate(str.maketrans(CHARSETS["std"], v))
        assert Base32Decoder.run(translated, charset=v) == expected
