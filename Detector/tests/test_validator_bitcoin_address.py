import pytest

from Detector.validators.bitcoin_address import BitcoinAddress


class TestBitcoinAddressValidator:
    @pytest.mark.parametrize(
        "input_address, expected",
        [
            ("1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i", False),
            ("17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j", True),
            ("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", True),
            ("4J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", False),
        ],
    )
    def test_is_valid(self, input_address, expected):
        assert BitcoinAddress().is_valid(input_address) == expected
