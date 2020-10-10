import pytest
from Detector.extractors.bitcoin_address import BitcoinAddress


class TestBitcoinAddressExtractor:

    @pytest.mark.parametrize("input_data", [
        "", "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i",
        [
            "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i",
            "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i"
        ],
        "1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i\n1AGNa15ZQXAZUgFiqJ3i7Z2DPU2J6hW62i"
    ])
    def test_extract_from_returns_empty_collection(self, input_data):
        extracted = BitcoinAddress().extract_from(input_data)
        assert len(list(extracted)) == 0

    @pytest.mark.parametrize("input_data, expected",
                             [("17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
                               ["17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j"]),
                              ("17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j",
                               ["17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j", "17NdbrSGoUotzeGCcMMCqnFkEvLymoou9j"])
                              ])
    def test_extract_from(self, input_data, expected):
        extracted = list(BitcoinAddress().extract_from(input_data))
        assert len(extracted) == len(expected)
        assert not set(extracted).isdisjoint(expected)
