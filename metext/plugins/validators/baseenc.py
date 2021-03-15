from metext.plugin_base import BaseValidator
from metext.plugins.decoders.base32 import Base32Decoder
from metext.plugins.decoders.base64 import Base64Decoder, Base64UrlDecoder
from metext.plugins.decoders.base85 import Base85Decoder, Ascii85Decoder


class Ascii85Validator(BaseValidator):
    PLUGIN_NAME = "ascii85"

    @classmethod
    def run(cls, _input, **kwargs):
        return Ascii85Decoder.run(_input, **kwargs) is not None


class Base32Validator(BaseValidator):
    PLUGIN_NAME = "base32"

    @classmethod
    def run(cls, _input: str, **kwargs) -> bool:
        """Checks if _input string is decodable base32 string.
        Custom charsets of 32 chars can be used.

        :param _input:
        :param kwargs:
        :keyword alt_chars: Chars set of 32 chars to use.
        If not defined, standard chars set is used
        :return:
        """
        return Base32Decoder.run(_input, **kwargs) is not None


class Base64Validator(BaseValidator):
    PLUGIN_NAME = "base64"

    @classmethod
    def run(cls, _input: str, **kwargs) -> bool:
        """Checks if _input string is decodable base64 string.
        Custom charsets of 64 chars can be used.

        :param _input:
        :param kwargs:
        :keyword alt_chars: Chars set of 64 chars or chars set of 2 special characters to use.
        If not defined, standard chars set is used
        :return:
        """
        return Base64Decoder.run(_input, **kwargs) is not None


class Base64UrlValidator(BaseValidator):
    PLUGIN_NAME = "base64url"

    @classmethod
    def run(cls, _input: str, **kwargs) -> bool:
        """Checks if _input string is decodable base64 urlsafe string.

        :param _input:
        :param kwargs:
        :return:
        """
        return Base64UrlDecoder.run(_input, **kwargs) is not None


class Base85Validator(BaseValidator):
    PLUGIN_NAME = "base85"

    @classmethod
    def run(cls, _input, **kwargs):
        return Base85Decoder.run(_input, **kwargs) is not None
