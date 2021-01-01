from urllib.parse import urlparse

from Detector.plugin_base import BaseValidator
from Detector.plugins.validators.base64 import Base64Validator


class URIValidator(BaseValidator):
    PLUGIN_NAME = "uri"

    @classmethod
    def run(cls, _input, *args, **kwargs) -> bool:
        """Checks that _input is valid, non-empty URI string, doesn't have to contain a scheme.

        :param _input:
        :param args:
        :param kwargs:
        :keyword strict: If True then _input is required to contain path-like delimiter "/"
        :keyword schemes: List of lower-cased schemes (e.g. http, data) that URI must have (one of).
        If schemes is an empty list (none provided), then there is no scheme restriction, defaults to empty list
        :return:
        """
        strict = kwargs.get("strict", True)
        schemes = kwargs.get("schemes", [])
        parsed = urlparse(_input)
        is_path_like = ("/" in parsed.path) if strict else True
        has_selected_scheme = parsed.scheme in schemes if schemes else True
        return (
            bool(parsed.netloc) or (bool(parsed.path) and is_path_like)
        ) and has_selected_scheme


class URLValidator(BaseValidator):
    PLUGIN_NAME = "url"

    @classmethod
    def run(cls, _input, *args, **kwargs) -> bool:
        """Checks that _input conforms to URL with either of the following schemes:
        http, https, ftp, ftps

        :param _input:
        :param args:
        :param kwargs:
        :return: True if _input is URL
        """
        parsed = urlparse(_input)
        return parsed.scheme in ("http", "https", "ftp", "ftps") and bool(parsed.netloc)


class DataURIValidator(BaseValidator):
    PLUGIN_NAME = "data_uri"

    @classmethod
    def run(cls, _input: str, *args, **kwargs) -> bool:
        """Checks that _input is a valid data URI string.
        If it contains data in base64 format, it checks that the data
        is valid base64.

        :param _input:
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: True if _input is valid data URI string
        """
        parsed = urlparse(_input)
        base64_valid = (
            "base64," not in _input
            or Base64Validator.run(_input.split("base64,")[-1])
            or True
        )
        return parsed.scheme == "data" and bool(parsed.path) and base64_valid
