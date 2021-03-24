from collections import OrderedDict

import chardet


def to_csv_printer_format(analyzed_data: list) -> list:
    out = []

    if not analyzed_data:
        return out

    for item in analyzed_data:
        source = item.get("name", "Unknown")
        for f_name, f_value in item.get("formats", {}).items():
            if not f_value:
                continue
            for p_type, p_value in f_value.get("patterns", {}).items():
                for val in p_value or ["NONE"]:
                    out.append(
                        OrderedDict(
                            [
                                ("source", str(source)),
                                ("format", str(f_name)),
                                ("pattern_type", str(p_type)),
                                ("pattern", val),
                            ]
                        )
                    )

    return out


def to_table_printer_format(analyzed_data: list) -> list:
    csv_out = to_csv_printer_format(analyzed_data)
    if not csv_out:
        return []
    return [list(csv_out[0].keys())] + [list(item.values()) for item in csv_out]


def to_xml_printer_format(analyzed_data: list) -> dict:
    return {"data": analyzed_data}


def decode_bytes(bytes_):
    try:
        return bytes_.decode("utf-8")
    except UnicodeDecodeError:
        try:
            # Try using 8-bit ASCII, if came from Windows
            return bytes_.decode("ISO-8859-1")
        except ValueError:
            # Last resort we use the slow chardet package
            return bytes_.decode(chardet.detect(bytes_)["encoding"])