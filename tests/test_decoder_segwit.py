import binascii

import pytest

# tests credit https://github.com/sipa/bech32/blob/master/ref/python/tests.py
from metext.plugins.decoders.segwit import SegwitDecoder


def segwit_scriptpubkey(witver, witprog):
    """Construct a Segwit scriptPubKey for a given witness program."""
    return bytes([witver + 0x50 if witver else 0, len(witprog)] + witprog)


@pytest.mark.parametrize(
    "hrp, address, hexscript",
    [
        (
            "bc",
            "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4",
            "0014751e76e8199196d454941c45d1b3a323f1433bd6",
        ),
        (
            "tb",
            "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7",
            "00201863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262",
        ),
        (
            "bc",
            "bc1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7k7grplx",
            "5128751e76e8199196d454941c45d1b3a323f1433bd6751e76e8199196d454941c45d1b3a323f1433bd6",
        ),
        ("bc", "BC1SW50QA3JX3S", "6002751e"),
        (
            "bc",
            b"bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj",
            "5210751e76e8199196d454941c45d1b3a323",
        ),
        (
            "tb",
            b"tb1qqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesrxh6hy",
            "0020000000c4a5cad46221b2a187905e5266362b99d5e91c6ce24d165dab93e86433",
        ),
    ],
)
def test_valid_segwit_address(hrp, address, hexscript):
    segwit = SegwitDecoder()
    witness_version, witness_program = segwit.run(address, hrp=hrp)
    assert witness_version is not None
    scriptpubkey = segwit_scriptpubkey(witness_version, witness_program)
    assert scriptpubkey == binascii.unhexlify(hexscript)


@pytest.mark.parametrize(
    "address",
    [
        "tc1qw508d6qejxtdg4y5r3zarvary0c5xw7kg3g4ty",
        "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5",
        "BC13W508D6QEJXTDG4Y5R3ZARVARY0C5XW7KN40WF2",
        "bc1rw5uspcuh",
        "bc10w508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7kw5rljs90",
        "BC1QR508D6QEJXTDG4Y5R3ZARVARYV98GJ9P",
        "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sL5k7",
        b"bc1zw508d6qejxtdg4y5r3zarvaryvqyzf3du",
        b"tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3pjxtptv",
        b"bc1gmk9yu",
    ],
)
def test_invalid_segwit_address(address):
    witness_version, _ = SegwitDecoder.run(address, hrp="bc")
    assert witness_version is None
    witness_version, _ = SegwitDecoder.run(address, hrp="tb")
    assert witness_version is None
