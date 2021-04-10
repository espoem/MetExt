from metext.utils import decode_bytes


def _extract_with_regex(
    _input, regex, validator=None, per_line=True, preprocess=None, postprocess=None
):
    if not isinstance(_input, str):
        try:
            _input = decode_bytes(_input)
        except:
            yield from ()

    global_pos_start = 0
    for part in _input.splitlines(keepends=True) if per_line else [_input]:
        if preprocess is not None:
            part = preprocess(part)
        matches = list(regex.finditer(part))
        for match in matches:
            value = match.group(0)
            if postprocess is not None:
                value = postprocess(value)
            if validator is not None and not validator(value):
                continue
            yield {
                "value": value,
                "pos_span": (
                    global_pos_start + match.start(0),
                    global_pos_start + match.end(0),
                ),
            }
        global_pos_start += len(part)
