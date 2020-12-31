#!/usr/bin/env python3
import argparse

from Detector import plugin_base
from Detector import analyze
from Detector.utils import to_csv_printer_format, to_table_printer_format
from Detector.utils.fileinput import FileInputExtended


def build_parser():
    default_decoders = [
        plug.PLUGIN_NAME for plug in plugin_base.BaseDecoder.get_active_plugins()
    ]
    default_extractors = [
        plug.PLUGIN_NAME for plug in plugin_base.BaseExtractor.get_active_plugins()
    ]
    default_printers = [
        plug.PLUGIN_NAME for plug in plugin_base.BasePrinter.get_active_plugins()
    ]
    main_parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    main_parser.add_argument(
        "-i",
        "--input",
        action="append",
        help=(
            "File path to process. Wildcards can be used."
            " Reads from STDIN if no input files defined via arguments -i or -f."
            " If -f argument is used, the input file paths are extended with the list of paths from the file."
        ),
    )
    main_parser.add_argument(
        "-f",
        "--file",
        help="Read input file paths from a file. One file path per line.",
    )
    main_parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Enables recursive wildcards (**) for -i and -f arguments.",
    )
    main_parser.add_argument(
        "-o",
        "--output",
        nargs=1,
        help="File to write the output to. Outputs to STDOUT if no file given.",
        default=["-"],
    )
    main_parser.add_argument(
        "-d",
        "--decode",
        nargs="*",
        help=(
            "Select formats that should be tried for decoding from."
            " If no format selected, all will be tried."
        ),
        choices=default_decoders,
        # default=["_id"],
        # default=default_decoders,
        default=[p for p in default_decoders if p != "_id"],
    )
    main_parser.add_argument(
        "-e",
        "--extract",
        nargs="*",
        help=(
            "Select patterns that should be extracted."
            " If no pattern selected, all supported patterns will be tried."
        ),
        choices=default_extractors,
        # default=default_extractors,
        default=["btc", "ipv4", "ipv6", "email", "url"],
    )
    main_parser.add_argument(
        "-F",
        "--out-format",
        nargs=1,
        help="Select output format of found patterns.",
        choices=default_printers,
        default=["json"],
    )
    # main_parser.add_argument(
    #     "-p", "--plugins", nargs=1, help="Directory path to custom plugins."
    # )
    main_parser.add_argument(
        "--per-line",
        action="store_true",
        help=(
            "Read and process input files per line."
            " Otherwise, read and process all data in each file at once."
        ),
    )
    return main_parser


def unglob_filepaths(filepaths, recursive=False):
    import glob
    from os.path import isfile, abspath

    for path in filepaths or []:
        yield from (
            abspath(p) for p in glob.iglob(path, recursive=recursive) if isfile(p)
        )


def read_filepaths(file, recursive=False):
    if not file:
        return
    with open(file, "r") as f:
        yield from unglob_filepaths(f.readlines(), recursive=recursive)


def get_printer(_args):
    printers = [
        p
        for p in plugin_base.BasePrinter.get_active_plugins()
        if _args.out_format and _args.out_format[0] == p.PLUGIN_NAME
    ]
    if printers:
        return printers[0]
    return None


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    input_files = list(
        set(unglob_filepaths(args.input, args.recursive)).union(
            set(read_filepaths(args.file, args.recursive))
        )
    ) or [
        "-"  # STDIN
    ]

    with FileInputExtended(input_files, mode="rb") as f:
        res = analyze(
            f,
            [(dec, [], {}) for dec in args.decode],
            [(ex, [], {}) for ex in args.extract],
            args.per_line,
        )
    printer = get_printer(args)
    to_print = res
    if printer.PLUGIN_NAME == "csv":
        to_print = to_csv_printer_format(res)
    if printer.PLUGIN_NAME == "text":
        to_print = to_table_printer_format(res)
    printer.run(to_print, filename=args.output[0])
