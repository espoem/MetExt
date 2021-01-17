import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.email import EmailValidator


class EmailExtractor(BaseExtractor):
    PLUGIN_NAME = "email"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts e-mail addresses from a string or a list of strings.

        :param _input: String or a list of strings to extract e-mail addresses from
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of e-mail addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part or re.search(r"\w[^@]@[^@]\w", part) is None:
                continue
            yield from (
                address
                for address in (re.findall(r"\S+[^@]@[^@]\S+", part))
                if EmailValidator.run(address)
            )
