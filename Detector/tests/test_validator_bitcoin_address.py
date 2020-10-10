import pytest

from Detector.validators.bitcoin_address import BitcoinAddress


@pytest.mark.parametrize(
    "input_address, expected",
    [
        ("1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i", False),
        ("1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i", True),
        ("17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j", True),
        ("17NdbrSGoUotzeGCcMMC?nFkEvLymoou9j", False),
        ("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", True),
        ("4J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", False),
        ("BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4", True),
        ("tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7", False),
        ("bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj", True),
        ("tc1qw508d6qejxtdg4y5r3zarvary0c5xw7kg3g4ty", False),
        ("bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5", False),
        ("BC13W508D6QEJXTDG4Y5R3ZARVARY0C5XW7KN40WF2", False),
        ("tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3pjxtptv", False),
    ],
)
def test_is_valid(input_address, expected):
    assert BitcoinAddress().is_valid(input_address) == expected
