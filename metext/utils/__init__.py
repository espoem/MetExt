try:
    import orjson as json
except ImportError:
    try:
        import ujson as json
    except ImportError:
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
}


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
                    val = v.get("value")
                    out.append(
                        OrderedDict(
                            [
                                ("source", str(source)),
                                ("format", str(f_name)),
                                ("pattern_type", str(p_type)),
                                ("pattern", json.dumps(val)),
                                ("frequency", v.get("frequency", 1)),
                                ("positions", v.get("positions", [])),
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
