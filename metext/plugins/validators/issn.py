import re

from metext.plugin_base import BaseValidator


def is_issn(issn: str) -> bool:
    if not isinstance(issn, str):
        try:
            issn = str(issn)
        except:
            return False

    issn = re.sub(r"[^0-9xX]", "", issn)

    if len(issn) != 8:
        return False

    sum_ = sum(
        (index + 1) * int(value) if value.isdigit() else 10
        for index, value in enumerate(issn[::-1])
    )
    return sum_ % 11 == 0


class IssnValidator(BaseValidator):
    PLUGIN_NAME = "issn"

    @classmethod
    def run(cls, _input, **kwargs) -> bool:
        """Checks that the input string is a valid ISSN identifier.

        Input string should include only the identifier digits (with delimiter).

        :param _input: String to check
        :param kwargs:
        :return: True if input string is an ISSN identifier,
        else False
        """
        return is_issn(_input.split(":")[-1])
