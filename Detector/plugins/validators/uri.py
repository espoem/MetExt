from urllib.parse import urlparse

from Detector.plugin_base import BaseValidator


class URIValidator(BaseValidator):
    PLUGIN_NAME = "uri"

    @classmethod
    def run(cls, _input, *args, **kwargs) -> bool:
        """Checks that _input is valid, non-empty URI string, doesn't have to contain a scheme.

        :param _input:
        :param args:
        :param kwargs:
        :keyword strict: If True then _input is required to contain path-like delimiter "/"
        :return:
        """
        strict = kwargs.get("strict", True)
        parsed = urlparse(_input)
        return bool(parsed.netloc) or (
            bool(parsed.path) and ("/" in parsed.path) if strict else True
        )


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
