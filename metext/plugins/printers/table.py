import sys
from typing import List

from tabulate import tabulate

from metext.plugin_base import BasePrinter


class TextTablePrinter(BasePrinter):
    PLUGIN_NAME = "text"

    @classmethod
    def run(cls, _input: List[list], **kwargs):
        """Prints to JSON format.

        :param _input: List of rows
        :param kwargs: Arbitrary keyword arguments
        :keyword filename: Name of output file. If it is "-", then the output is printed to STDOUT, defaults to "-"
        :keyword tablefmt: Table format, see https://pypi.org/project/tabulate/ for supported values
        :keyword has_header: If True, then the first row is taken as a header
        :return:
        """
        out_file = kwargs.get("filename", "-")
        tablefmt = kwargs.get("tablefmt", "grid")
        has_header = kwargs.get("has_header", True)
        if not _input:
            return

        with (
            sys.stdout if out_file == "-" else open(out_file, "w", encoding="utf8")
        ) as f:
            if has_header:
                f.write(tabulate(_input[1:], headers=_input[0], tablefmt=tablefmt))
            else:
                f.write(tabulate(_input, tablefmt=tablefmt))
