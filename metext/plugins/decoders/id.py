from metext.plugin_base import BaseDecoder, Decodable


class IdDecoder(BaseDecoder):
    PLUGIN_NAME = "raw"

    @classmethod
    def run(cls, _input: Decodable, **kwargs) -> Decodable:
        """Helper plugin for convenience. Returns unaltered _input.

        :param _input:
        :param kwargs:
        :return:
        """
        return _input
