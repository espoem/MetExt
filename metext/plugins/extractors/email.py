from typing import Iterable

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.plugins.validators.email import EmailValidator
from metext.utils.regex import RE_EMAIL


class EmailExtractor(BaseExtractor):
    PLUGIN_NAME = "email"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts e-mail addresses from a string or a list of strings.

        :param _input: String or a list of strings to extract e-mail addresses from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of e-mail addresses
        """
        yield from _extract_with_regex(
            _input,
            RE_EMAIL,
            validator=EmailValidator.run,
            per_line=True,
            data_kind=cls.PLUGIN_NAME,
        )
