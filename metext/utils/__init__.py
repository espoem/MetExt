import json
import re
from collections import OrderedDict


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


RE_ETH = re.compile(r"\b0x[0-9a-f]{40}\b", re.IGNORECASE)
