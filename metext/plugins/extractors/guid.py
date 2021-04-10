from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.utils.regex import RE_GUID


class GuidExtractor(BaseExtractor):
    PLUGIN_NAME = "guid"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts GUIDs strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of GUID strings
        """
        yield from _extract_with_regex(_input, RE_GUID, per_line=True)
