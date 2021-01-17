import pytest

# tests credit https://github.com/sipa/bech32/blob/master/ref/python/tests.py
from metext.plugins.decoders.bech32 import Bech32Decoder


@pytest.mark.parametrize(
    "checksum",
    [
        "A12UEL5L",
        "an83characterlonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1tt5tgs",
        "abcdef1qpzry9x8gf2tvdw0s3jn54khce6mua7lmqqqxw",
        "11qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqc8247j",
        "split1checkupstagehandshakeupstreamerranterredcaperred2y9e3w",
        b"A12UEL5L",
        b"an83characterlonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1tt5tgs",
        b"abcdef1qpzry9x8gf2tvdw0s3jn54khce6mua7lmqqqxw",
        b"11qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqc8247j",
        b"split1checkupstagehandshakeupstreamerranterredcaperred2y9e3w",
    ],
)
def test_valid_checksum(checksum):
    bech32 = Bech32Decoder()
    hrp, decoded = bech32.run(checksum)
    assert hrp is not None
    assert decoded is not None


@pytest.mark.parametrize(
    "checksum",
    [
        " 1nwldj5",
        "\x7F" + "1axkwrx",
        "an84characterslonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1569pvx",
        "pzry9x0s0muk",
        "1pzry9x0s0muk",
        "x1b4n0q5v",
        "li1dgmt3",
        "de1lg7wt\xff",
        b" 1nwldj5",
        b"\x7F" + b"1axkwrx",
        b"an84characterslonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1569pvx",
        b"pzry9x0s0muk",
        b"1pzry9x0s0muk",
        b"x1b4n0q5v",
        b"li1dgmt3",
        b"de1lg7wt\xff",
    ],
)
def test_invalid_checksum(checksum):
    hrp, decoded = Bech32Decoder.run(checksum)
    assert hrp is None
    assert decoded is None
