import re
from typing import Iterable, List, Union

from Detector.plugin_base import BaseExtractor
from Detector.plugins.validators.uri import DataURIValidator, URIValidator, URLValidator
from Detector.utils.uri import URI, URI_reference, data_URI

RE_URI_REFERENCE = re.compile(r"\b{}\b".format(URI_reference), re.VERBOSE)
RE_URI = re.compile(r"\b{}\b".format(URI), re.VERBOSE)


class URIExtractor(BaseExtractor):
    PLUGIN_NAME = "uri"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts URIs from a string or a list of strings.

        See https://tools.ietf.org/html/rfc3986

        .. warning::
            This method does no filtering on specific schemes. Therefore, it may return
            lots of noise patterns.

        :param _input: String or a list of strings
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :keyword strict: Flag to reduce the number of results,
        if True then only path-like results with "/" path parts delimiter are returned, defaults to True
        :keyword relative: Flag to allow URI relative references,
        otherwise some scheme must be present, default to False
        :keyword schemes: List of lower-cased schemes (e.g. http, data) URI must contain.
        If empty list (not provided), then URI is not restricted by a scheme, defaults to empty list
        :return: Generator of URIs
        """
        include_relative = kwargs.get("relative", False)
        strict = kwargs.get("strict", True)
        schemes = kwargs.get("schemes", [])
        regex = RE_URI_REFERENCE if include_relative else RE_URI
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                uri
                for uri in regex.findall(part)
                if URIValidator.run(uri, strict=strict, schemes=schemes)
            )


class URLExtractor(BaseExtractor):
    PLUGIN_NAME = "url"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts URLs from a string or a list of strings. URL must contain one of the following schemes:
        `http`, `https`, `ftp`, `ftps`

        See https://tools.ietf.org/html/rfc3986

        :param _input: String or a list of strings
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with URLs
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (uri for uri in RE_URI.findall(part) if URLValidator.run(uri))


class DataURIExtractor(BaseExtractor):
    PLUGIN_NAME = "data_uri"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts valid data URIs from a string or a lists of strings.

        :param _input: String or a list of strings
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with data URIs
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                uri for uri in RE_URI.findall(part) if DataURIValidator.run(uri)
            )
