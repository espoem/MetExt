from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.plugins.validators.doi import DoiValidator
from metext.utils.regex import RE_DOI


class DoiExtractor(BaseExtractor):
    PLUGIN_NAME = "doi"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts valid DOI identifiers
        from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with DOI identifiers
        """
        yield from _extract_with_regex(
            _input, RE_DOI, validator=DoiValidator.run, per_line=True
        )
