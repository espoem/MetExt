import re

from metext.utils.uri import addr_spec


RE_MD5 = re.compile(
    r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b"
)  # https://stackoverflow.com/a/25231922
RE_EMAIL = re.compile(addr_spec, re.VERBOSE)
