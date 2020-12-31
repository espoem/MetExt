import sys

from Detector.plugin_base import BasePrinter
import json


class JsonPrinter(BasePrinter):
    PLUGIN_NAME = "json"

    @classmethod
    def run(cls, _input, *args, **kwargs):
        """Prints to JSON format.

        :param _input:
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :keyword filename: Name of output file. If it is "-", then the output is printed to STDOUT, defaults to "-"
        :keyword indent: Indentation to pretty print, defaults to 2
        :return:
        """
        out_file = kwargs.get("filename", "-")
        indent = kwargs.get("indent", 2)
        sort_keys = kwargs.get("sort_keys", False)
        with (
            sys.stdout if out_file == "-" else open(out_file, "w", encoding="utf8")
        ) as f:
            json.dump(_input, f, indent=indent, sort_keys=sort_keys)