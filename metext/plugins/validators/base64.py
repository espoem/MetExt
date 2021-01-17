from metext.plugin_base import BaseValidator
from metext.plugins.decoders.base64 import Base64Decoder, Base64UrlDecoder


class Base64Validator(BaseValidator):
    PLUGIN_NAME = "base64"

    @classmethod
    def run(cls, _input: str, *args, **kwargs) -> bool:
        """Checks if _input string is decodable base64 string.
        Custom charsets of 64 chars can be used.

        :param _input:
        :param args:
        :param kwargs:
        :keyword alt_chars: Chars set of 64 chars or chars set of 2 special characters to use.
        If not defined, standard chars set is used
        :return:
        """
        return Base64Decoder.run(_input, *args, **kwargs) is not None


class Base64UrlValidator(BaseValidator):
    PLUGIN_NAME = "base64url"

    @classmethod
    def run(cls, _input: str, *args, **kwargs) -> bool:
        """Checks if _input string is decodable base64 urlsafe string.

        :param _input:
        :param args:
        :param kwargs:
        :return:
        """
        return Base64UrlDecoder.run(_input, *args, **kwargs) is not None
