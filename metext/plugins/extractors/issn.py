from typing import Iterable

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.plugins.validators.issn import IssnValidator
from metext.utils.regex import RE_ISSN


class IssnExtractor(BaseExtractor):
    PLUGIN_NAME = "issn"

    valid_issns = set()

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid ISSN identifiers
        from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with ISSN identifiers
        """
        yield from _extract_with_regex(
            _input,
            RE_ISSN,
            validator=IssnValidator.run,
            cached_values=cls.valid_issns,
            data_kind=cls.PLUGIN_NAME,
        )
