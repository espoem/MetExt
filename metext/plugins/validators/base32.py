from metext.plugin_base import BaseValidator
from metext.plugins.decoders.base32 import Base32Decoder


class Base32Validator(BaseValidator):
    PLUGIN_NAME = "base32"

    @classmethod
    def run(cls, _input: str, *args, **kwargs) -> bool:
        """Checks if _input string is decodable base32 string.
        Custom charsets of 32 chars can be used.

        :param _input:
        :param args:
        :param kwargs:
        :keyword alt_chars: Chars set of 32 chars to use.
        If not defined, standard chars set is used
        :return:
        """
        return Base32Decoder.run(_input, *args, **kwargs) is not None
