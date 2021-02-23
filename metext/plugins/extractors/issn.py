from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.issn import IssnValidator
from metext.utils.regex import RE_ISSN


class IssnExtractor(BaseExtractor):
    PLUGIN_NAME = "issn"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid ISSN identifiers
        from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with ISSN identifiers
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                issn for issn in (RE_ISSN.findall(part)) if IssnValidator.run(issn)
            )
