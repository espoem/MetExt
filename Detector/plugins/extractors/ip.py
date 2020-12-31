import re
from typing import Iterable, List, Union

from Detector.plugin_base import BaseExtractor
from Detector.plugins.validators.ip import IPv4AddressValidator, IPv6AddressValidator
from Detector.utils.uri import IPv4address, IPv6address

# https://en.wikipedia.org/wiki/Wikipedia:Hyphens_and_dashes
SYMBOLS_HYPHEN_LIKE = [
    "-",  # hyphen
    "–",  # en-dash
    "—",  # em-dash
    "−",  # minus
]

RE_IPV4 = re.compile(r"\b{}\b".format(IPv4address), re.VERBOSE)
# RE_IPV4 = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
RE_IPV6 = re.compile(r"\b{}\b".format(IPv6address), re.VERBOSE)


class IPv4AddressExtractor(BaseExtractor):
    PLUGIN_NAME = "ipv4"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extract IPv4 addresses strings from a string or a list of strings.

        See https://tools.ietf.org/html/rfc3986#section-3.2.2 for the form of IPv4 address

        :param _input: String or a list of strings to extract IPv4 addresses from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of IPv4 addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            yield from (
                address
                for address in RE_IPV4.findall(part)
                if IPv4AddressValidator.run(address)
            )


class IPv6AddressExtractor(BaseExtractor):
    PLUGIN_NAME = "ipv6"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extract IPv6 addresses strings from a string or a list of strings.

        See https://tools.ietf.org/html/rfc3986#section-3.2.2 for the form of IPv6 address

        :param _input: String or a list of strings to extract IPv6 addresses from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of IPv6 addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_IPV6.findall(part)
                if IPv6AddressValidator.run(address)
            )
