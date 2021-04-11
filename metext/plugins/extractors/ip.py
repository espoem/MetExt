import re
from typing import Iterable

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.plugins.validators.ip import IPv4AddressValidator, IPv6AddressValidator
from metext.utils.uri import IPv4address, IPv6address

# https://en.wikipedia.org/wiki/Wikipedia:Hyphens_and_dashes
SYMBOLS_HYPHEN_LIKE = [
    "-",  # hyphen
    "–",  # en-dash
    "—",  # em-dash
    "−",  # minus
]

RE_IPV4 = re.compile(r"\b(?<!\.){}(?!\.)\b".format(IPv4address), re.VERBOSE)
# RE_IPV4 = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
RE_IPV6 = re.compile(r"\b(?<!:){}(?!:)\b".format(IPv6address), re.VERBOSE)


class IPv4AddressExtractor(BaseExtractor):
    PLUGIN_NAME = "ipv4"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extract IPv4 addresses strings from a string or a list of strings.

        See https://tools.ietf.org/html/rfc3986#section-3.2.2 for the form of IPv4 address

        :param _input: String or a list of strings to extract IPv4 addresses from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of IPv4 addresses
        """
        yield from _extract_with_regex(
            _input,
            RE_IPV4,
            validator=IPv4AddressValidator.run,
            per_line=True,
            data_kind=cls.PLUGIN_NAME,
        )


class IPv6AddressExtractor(BaseExtractor):
    PLUGIN_NAME = "ipv6"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extract IPv6 addresses strings from a string or a list of strings.

        See https://tools.ietf.org/html/rfc3986#section-3.2.2 for the form of IPv6 address

        :param _input: String or a list of strings to extract IPv6 addresses from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of IPv6 addresses
        """
        yield from _extract_with_regex(
            _input,
            RE_IPV6,
            validator=lambda val: len(val) > 6 and IPv6AddressValidator.run(val),
            per_line=True,
            data_kind=cls.PLUGIN_NAME,
        )
