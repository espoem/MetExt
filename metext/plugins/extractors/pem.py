from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.utils.regex import RE_PEM


class PemExtractor(BaseExtractor):
    PLUGIN_NAME = "pem"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts PEM objects delimited by header `-----BEGIN <label>-----`
        and trailer `-----END <label>-----`.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of PEM objects strings
        """
        for part in _input if isinstance(_input, list) else [_input]:
            yield from iter(RE_PEM.findall(part))
