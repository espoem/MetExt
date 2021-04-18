from typing import Iterable
from urllib.parse import unquote_plus

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.plugins.validators.uri import (
    DataURIValidator,
    MagnetValidator,
    URIValidator,
    URLValidator,
)
from metext.utils.regex import RE_URI, RE_URI_REFERENCE, RE_URL_FORM_FIELDS
from metext.utils.uri import URI_SCHEMES


class URIExtractor(BaseExtractor):
    PLUGIN_NAME = "uri"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts URIs from a string or a list of strings.

        See https://tools.ietf.org/html/rfc3986

        .. warning::
            This method does no filtering on specific schemes. Therefore, it may return
            lots of noise patterns.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword strict: Flag to reduce the number of results,
        if True then only path-like results with "/" path parts delimiter are returned.
        Defaults to False
        :keyword relative: Flag to allow URI relative references,
        otherwise some scheme must be present, default to False
        :keyword schemes: List of lower-cased schemes (e.g. http, data) URI must contain.
        If empty list (not provided), then URI is not restricted by a scheme,
        defaults to registered schemes
        :return: Generator of URIs
        """
        include_relative = kwargs.get("relative", False)
        strict = kwargs.get("strict", False)
        schemes = kwargs.get(
            "schemes", URI_SCHEMES
        )  # https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml
        regex = RE_URI_REFERENCE if include_relative else RE_URI
        yield from _extract_with_regex(
            _input,
            regex,
            validator=lambda val: URIValidator.run(val, strict=strict, schemes=schemes),
            data_kind=URIExtractor.PLUGIN_NAME,
        )


class URLExtractor(BaseExtractor):
    PLUGIN_NAME = "url"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts URLs from a string or a list of strings. URL must contain one of the following schemes:
        `http`, `https`, `ftp`, `ftps`

        See https://tools.ietf.org/html/rfc3986

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with URLs
        """
        yield from _extract_with_regex(
            _input, RE_URI, validator=URLValidator.run, data_kind=URLExtractor.PLUGIN_NAME
        )


class URNExtractor(BaseExtractor):
    PLUGIN_NAME = "urn"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts URNs from a string or a list of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with URNs
        """
        yield from URIExtractor.run(
            _input, schemes=["urn"], strict=False, data_kind=URNExtractor.PLUGIN_NAME
        )


class DataURIExtractor(BaseExtractor):
    PLUGIN_NAME = "data_uri"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid data URIs from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with data URIs
        """
        yield from _extract_with_regex(
            _input, RE_URI, validator=DataURIValidator.run, data_kind=DataURIExtractor.PLUGIN_NAME
        )


class MagnetExtractor(BaseExtractor):
    PLUGIN_NAME = "magnet"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts MAC addresses

        :param _input: String or a list of strings to extract MAC address from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of MAC addresses
        """

        yield from (
            magnet
            for magnet in URIExtractor.run(_input, schemes=["magnet"], strict=False)
            if MagnetValidator.run(magnet["value"])
        )


class FormFieldsExtractor(BaseExtractor):
    PLUGIN_NAME = "form_fields"
    PLUGIN_ACTIVE = False

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts form fields data in HTTP, URL.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword min_len: Minimum length of extracted pattern.
        Defaults to 20.
        :keyword decode: Flag to percent (URL) decode the found pattern. Defaults to True
        :return: Generator of form fields in decoded format
        """
        min_len = kwargs.get("min_len", 20)
        decode = kwargs.get("decode", True)

        yield from _extract_with_regex(
            _input,
            RE_URL_FORM_FIELDS,
            validator=lambda val: len(val) >= min_len
            and not ("&" not in val and val.endswith("=")),
            postprocess=lambda val: unquote_plus(val) if decode else val,
            data_kind=FormFieldsExtractor.PLUGIN_NAME,
        )
