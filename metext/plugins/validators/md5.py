import re

from metext.plugin_base import BaseValidator

# https://stackoverflow.com/a/25231922
RE_MD5 = re.compile(r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b")


class MD5Validator(BaseValidator):
    PLUGIN_NAME = "md5"

    @classmethod
    def run(cls, _input, **kwargs) -> bool:
        """Checks that the input string is a MD5 hash string.

        :param _input:
        :param kwargs:
        :return: True if input string is a MD5 hash string, else False
        """
        return RE_MD5.match(_input) is not None
