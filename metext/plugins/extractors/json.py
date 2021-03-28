import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.utils.regex import RE_JSON


class JsonExtractor(BaseExtractor):
    PLUGIN_NAME = "json"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts JSON.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of JSON strings
        """
        for part in _input if isinstance(_input, list) else [_input]:
            for p in re.split(r"(\r\n|\n|\r){2,}", part):
                if not re.search(r"[{[]", p):
                    continue

                yield from iter(RE_JSON.findall(p))
