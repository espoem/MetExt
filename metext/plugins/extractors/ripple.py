import re
from typing import Iterable, List, Union

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.ripple import RippleValidator

PATTERN_XRP_BASE58 = r"\br[0-9a-zA-Z]{24,34}\b"
RE_XRP = re.compile(PATTERN_XRP_BASE58)

# TODO: Check X-format https://xrpaddress.info/


class RippleAddress(BaseExtractor):
    PLUGIN_NAME = "xrp"

    @classmethod
    def run(cls, _input: Union[str, List[str]], *args, **kwargs) -> Iterable[str]:
        """Extracts valid Ripple (XRP) addresses from a string or a list of strings.

        See: https://xrpl.org/accounts.html#addresses

        :param _input: String or a list of strings to extract Ripple addresses from
        :return: Generator of found valid Ripple addresses
        """

        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                address
                for address in RE_XRP.findall(part)
                if RippleValidator.run(address)
            )
