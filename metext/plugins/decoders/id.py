from typing import Optional

from metext.plugin_base import BaseDecoder, Decodable


class IdDecoder(BaseDecoder):
    PLUGIN_NAME = "_id"

    @classmethod
    def run(cls, _input: Decodable, *args, **kwargs) -> Decodable:
        """Helper plugin for convenience. Returns unaltered _input.

        :param _input:
        :param args:
        :param kwargs:
        :return:
        """
        return _input
