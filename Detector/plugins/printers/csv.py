import sys
from csv import DictWriter, writer as csvwriter, QUOTE_MINIMAL
from typing import List, Union

from Detector.plugin_base import BasePrinter


class CsvPrinter(BasePrinter):
    PLUGIN_NAME = "csv"

    @classmethod
    def run(cls, _input: Union[List[list], List[dict]], *args, **kwargs):
        """Prints to CSV format.

        Input can be either a list of dicts, or a list of lists.

        :param _input:
        :param args: Variable arguments
        :param kwargs: Arbitrary keyword arguments
        :keyword filename: Name of output file. If it is "-", then the output is printed to STDOUT, defaults to "-"
        :return:
        """
        out_file = kwargs.get("filename", "-")
        if not _input:
            return
        with (
            sys.stdout if out_file == "-" else open(out_file, "w", encoding="utf8")
        ) as f:
            if isinstance(_input[0], dict):
                fieldnames = list(_input[0].keys())
                writer = DictWriter(f, fieldnames=fieldnames, quoting=QUOTE_MINIMAL)
                writer.writeheader()
            else:
                writer = csvwriter(f, quoting=QUOTE_MINIMAL)
            writer.writerows(_input)