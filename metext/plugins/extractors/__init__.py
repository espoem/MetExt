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
    if not isinstance(_input, str):
        try:
            _input = decode_bytes(_input)
        except:
            yield from ()

    cur_pos = 0
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
                yield _create_res_dict(
                    value, cur_pos + match.start(0), orig_value, value_kind=data_kind
                )
                continue
            if validator is not None and not validator(value):
                continue
            yield _create_res_dict(
                value, cur_pos + match.start(0), orig_value, value_kind=data_kind
            )
            if isinstance(cached_values, list):
                cached_values.append(value)
            if isinstance(cached_values, set):
                cached_values.add(value)
        cur_pos += len(part)


def _create_res_dict(value, position=None, original=None, value_kind=None):
    res = {"value": value}
    if position is not None:
        res.update({"position": position})
    if original is not None:
        res.update({"original": original})
    if value_kind is not None:
        res.update({"value_kind": value_kind})
    return res
