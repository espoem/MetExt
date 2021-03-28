from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
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
        for part in _input if isinstance(_input, list) else [_input]:
            yield from iter(RE_GUID.findall(part))
