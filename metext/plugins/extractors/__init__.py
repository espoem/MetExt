import json

from metext.utils import decode_bytes


def _extract_with_regex(
    _input,
    regex,
    validator=None,
    per_line=True,
    preprocess=None,
    postprocess=None,
    cached_values=None,
    data_kind=None,
):
    def create_item(value_, position_=None, original_=None, value_kind_=None, **kwargs):
        res = {"value": value_}
        if position_ is not None:
            res.update({"position": position_})
        if original_ is not None:
            res.update({"original": original_})
        if value_kind_ is not None:
            res.update({"value_kind": value_kind_})
        if kwargs:
            res.update(kwargs)
        return res

    def add_update_item_to_out(item):
        key_ = json.dumps(item["value"])
        if key_ not in extracted_values:
            extracted_values[key_] = item
        if "frequency" not in extracted_values[key_]:
            extracted_values[key_]["frequency"] = 0
        extracted_values[key_]["frequency"] += 1
        if "positions" not in extracted_values[key_]:
            extracted_values[key_]["positions"] = []
        if item.get("position"):
            extracted_values[key_]["positions"].append(item["position"])
        if "position" in extracted_values[key_]:
            del extracted_values[key_]["position"]

    if not isinstance(_input, str):
        try:
            _input = decode_bytes(_input)
        except:
            yield from ()

    cur_pos = 0
    extracted_values = {}
    for part in _input.splitlines(keepends=True) if per_line else [_input]:
        if preprocess is not None:
            part = preprocess(part)
        matches = list(regex.finditer(part))
        for match in matches:
            value = match.group(0)
            if postprocess is not None:
                value = postprocess(value)
            orig_value = match.group(0) if match.group(0) != value else None
            if cached_values is not None and value in cached_values:
                add_update_item_to_out(
                    create_item(
                        value,
                        cur_pos + match.start(0),
                        orig_value,
                        value_kind_=data_kind,
                    )
                )
                continue
            if validator is not None and not validator(value):
                continue
            add_update_item_to_out(
                create_item(
                    value, cur_pos + match.start(0), orig_value, value_kind_=data_kind
                )
            )

            if isinstance(cached_values, list):
                cached_values.append(value)
            if isinstance(cached_values, set):
                cached_values.add(value)
        cur_pos += len(part)
    yield from extracted_values.values()
