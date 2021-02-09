from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.ethereum import EthereumValidator
from metext.utils import RE_ETH


class EthereumAddressExtractor(BaseExtractor):
    PLUGIN_NAME = "eth"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid Ethereum (ETH) addresses from a string or a list of strings.

        Looks for legacy addresses and EIP-55 addresses.

        :param _input: String or a list of strings
        :return: Generator of found valid Ethereum addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_ETH.findall(part)
                if EthereumValidator.run(address)
            )
