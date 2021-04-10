from typing import Iterable

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.utils.regex import RE_JSON


class JsonExtractor(BaseExtractor):
    PLUGIN_NAME = "json"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts JSON.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of JSON strings
        """
        yield from _extract_with_regex(_input, RE_JSON, per_line=False)
