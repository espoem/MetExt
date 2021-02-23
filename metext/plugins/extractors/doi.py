from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.doi import DoiValidator
from metext.utils.regex import RE_DOI


class DoiExtractor(BaseExtractor):
    PLUGIN_NAME = "doi"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid DOI identifiers
        from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with DOI identifiers
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue

            dois_ = RE_DOI.findall(part)
            yield from ("doi:" + doi for doi in (dois_) if DoiValidator.run(doi))
