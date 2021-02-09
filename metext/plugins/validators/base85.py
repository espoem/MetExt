from metext.plugin_base import BaseValidator
from metext.plugins.decoders.base85 import Base85Decoder


class Base85Validator(BaseValidator):
    PLUGIN_NAME = "base85"

    @classmethod
    def run(cls, _input, **kwargs):
        return Base85Decoder.run(_input, **kwargs) is not None
