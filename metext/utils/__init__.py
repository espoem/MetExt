import json
import itertools
from collections import OrderedDict

import chardet

excluded = {
    "name",
    "value_kind",
    "frequency",
    "positions",
    "position",
    "value",
    "original",
    "contexts",
    "context",
}


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def _create_keys_list(analyzed_data):
    keys = set()
    for item in analyzed_data:
        for f_name, f_value in item.get("formats", {}).items():
            for p_type, p_values in f_value.get("patterns", {}).items():
                keys.update(set(itertools.chain(*[list(v.keys()) for v in p_values])))
    return sorted(keys)


def to_csv_printer_format(analyzed_data: list) -> list:
    out = []

    if not analyzed_data:
        return out

    for item in analyzed_data:
        source = item.get("name")
        for f_name, f_value in item.get("formats", {}).items():
            if not f_value:
                continue
            for p_type, p_values in f_value.get("patterns", {}).items():
                for v in p_values:
                    out.append(
                        OrderedDict(
                            [
                                ("source", str(source)),
                                ("format", str(f_name)),
                                ("pattern_type", str(p_type)),
                                (
                                    "pattern",
                                    json.dumps(v.get("value"), cls=CustomJsonEncoder),
                                ),
                                (
                                    "original",
                                    json.dumps(
                                        v.get("original"), cls=CustomJsonEncoder
                                    ),
                                ),
                                ("frequency", v.get("frequency", 1)),
                                (
                                    "positions",
                                    json.dumps(
                                        v.get("positions", []), cls=CustomJsonEncoder
                                    ),
                                ),
                                (
                                    "contexts",
                                    json.dumps(
                                        v.get("contexts", []), cls=CustomJsonEncoder
                                    ),
                                ),
                            ]
                        )
                    )
    return out


def to_table_printer_format(analyzed_data: list) -> list:
    csv_out = to_csv_printer_format(analyzed_data)
    if not csv_out:
        return []
    return [list(csv_out[0].keys())] + [list(item.values()) for item in csv_out]


def decode_bytes(bytes_):
    try:
        return bytes_.decode(
            "utf-8",
        )
    except UnicodeDecodeError:
        try:
            # Try using 8-bit ASCII, if came from Windows
            return bytes_.decode(
                "ISO-8859-1",
            )
        except ValueError:
            # Last resort we use the slow chardet package
            return bytes_.decode(
                chardet.detect(bytes_)["encoding"],
            )


def convert_to_bytes(obj):
    if isinstance(obj, bytes):
        return obj
    if isinstance(obj, str):
        return obj.encode()
    if isinstance(obj, int):
        return str(obj).encode()
    if isinstance(obj, dict):
        return str(obj).encode()
    if isinstance(obj, list):
        return str(obj).encode()
    if isinstance(obj, bool):
        return str(obj).encode()
    if isinstance(obj, bytearray):
        return bytes(obj)

    raise NotImplementedError
