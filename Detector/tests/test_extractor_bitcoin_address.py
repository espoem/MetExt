import pytest

from Detector.extractors.bitcoin_address import BitcoinAddress


@pytest.mark.parametrize(
    "input_data",
    [
        "",
        "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i",
        [
            "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i",
            "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i",
        ],
        "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i\n1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i",
        "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
        "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7",
        "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3pjxtptv",
        "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5",
    ],
)
def test_extract_from_returns_empty_collection(input_data):
    extracted = BitcoinAddress().extract_from(input_data)
    assert len(list(extracted)) == 0


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
            ["17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j"],
        ),
        (
            "-17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j-17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j-",
            [
                "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
                "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
            ],
        ),
        (
            [
                "-17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j-",
                "\n3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy\nabctest",
            ],
            [
                "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
                "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
            ],
        ),
        (
            "bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj",
            ["bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj"],
        ),
        (
            "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4",
            ["BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4"],
        ),
        (
            "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j-bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj",
            [
                "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
                "bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj",
            ],
        ),
    ],
)
def test_extract_from(input_data, expected):
    extracted = list(BitcoinAddress().extract_from(input_data))
    assert len(extracted) == len(expected)
    assert not set(extracted).isdisjoint(expected)
