from typing import Iterable

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.utils.regex import RE_PEM


class PemExtractor(BaseExtractor):
    PLUGIN_NAME = "pem"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts PEM objects delimited by header `-----BEGIN <label>-----`
        and trailer `-----END <label>-----`.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of PEM objects strings
        """
        yield from _extract_with_regex(_input, RE_PEM, per_line=False)
