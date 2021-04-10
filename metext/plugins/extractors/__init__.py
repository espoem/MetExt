def _extract_with_regex(_input, regex, validator=None):
    if not isinstance(_input, str):
        try:
            _input = _input.decode("utf-8")
        except:
            yield from ()

    global_pos_start = 0
    for part in _input.splitlines(keepends=True):
        matches = list(regex.finditer(part))
        for match in matches:
            value = match.group(0)
            if validator is not None and not validator(value):
                continue
            yield {
                "value": value,
                "position": (
                    global_pos_start + match.start(0),
                    global_pos_start + match.end(0),
                ),
            }
        global_pos_start += len(part)
