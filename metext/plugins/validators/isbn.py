from is_isbn.is_isbn import is_isbn

from metext.plugin_base import BaseValidator


class IsbnValidator(BaseValidator):
    PLUGIN_NAME = "isbn"

    @classmethod
    def run(cls, _input, **kwargs) -> bool:
        """Checks that the input string is a valid ISBN-10
        or ISBN-13 identifier.

        Input string should include only the identifier digits (with delimiters).

        :param _input: String to check
        :param kwargs:
        :return: True if input string is a ISBN-10 or ISBN-13 identifier,
        else False
        """
        return is_isbn(_input.split(":")[-1])
