from metext.plugin_base import BaseValidator
from metext.plugins.decoders.ascii85 import Ascii85Decoder


class Ascii85Validator(BaseValidator):
    PLUGIN_NAME = "ascii85"

    @classmethod
    def run(cls, _input, **kwargs):
        return Ascii85Decoder.run(_input, **kwargs) is not None
