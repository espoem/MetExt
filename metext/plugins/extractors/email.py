from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.email import EmailValidator
from metext.utils.regex import RE_EMAIL


class EmailExtractor(BaseExtractor):
    PLUGIN_NAME = "email"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts e-mail addresses from a string or a list of strings.

        :param _input: String or a list of strings to extract e-mail addresses from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of e-mail addresses
        """
        for part in _input if isinstance(_input, list) else [_input]:
            for line in part.splitlines():
                yield from (
                    address
                    for address in RE_EMAIL.findall(line)
                    if EmailValidator.run(address)
                )
