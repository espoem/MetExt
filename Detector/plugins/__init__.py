import pkgutil

__all__ = []

HEX_DELIMITERS = {
    "None": "",
    "Space": " ",
    "Comma": ",",
    "Semicolon": ";",
    "Colon": ":",
    "LF": r"\n",
    "CRLF": r"\r\n",
    "0x": "0x",
    "comma-0x": ",0x",
    r"\x": r"[\]x",
}
HEX_PATTERN_TEMPLATE = r"[\dA-F]{{2}}(?:{delim}[\dA-F]{{2}})*"
HEX_PATTERNS = {
    name: HEX_PATTERN_TEMPLATE.format(delim=delim)
    for name, delim in HEX_DELIMITERS.items()
}


def load_plugin_modules(paths):
    """https://geoffsamuel.com/2020/03/31/plugin-class-architecture/

    :param paths:
    :return:
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(paths):
        __all__.append(module_name)
        module = loader.find_module(module_name).load_module(module_name)
        exec("{} = module".format(module_name))


load_plugin_modules(__path__)
