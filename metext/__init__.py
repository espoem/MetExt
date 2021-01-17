import concurrent.futures as cf
from io import BufferedIOBase, BytesIO, StringIO, TextIOBase
from typing import Any, List, Optional, Tuple, Union

from metext import plugin_base
from metext.plugin_base import BaseDecoder, BaseExtractor, Decodable
from metext.plugins import load_plugin_modules
from metext.utils.fileinput import FileInputExtended

supported_decoders = {
    plug.PLUGIN_NAME: plug for plug in plugin_base.BaseDecoder.get_plugins()
}

supported_extractors = {
    plug.PLUGIN_NAME: plug for plug in plugin_base.BaseExtractor.get_plugins()
}

register_plugin_modules = load_plugin_modules


def list_decoders() -> dict:
    """Gets a dict of registered decoders

    :return: Dict of registered decoding plugins
    """
    return supported_decoders


def get_decoder(name) -> Optional[BaseDecoder]:
    return supported_decoders.get(name)


def get_extractor(name) -> Optional[BaseExtractor]:
    return supported_extractors.get(name)


def list_extractors() -> dict:
    """Gets a dict of registered extractors

    :return: Dict of registered extracting plugins
    """
    return supported_extractors


def _is_supported_decoder(decoder: str):
    return decoder in supported_decoders.keys()


def _is_supported_extractor(extractor: str):
    return extractor in supported_extractors.keys()


def decode(data: Decodable, decoder: str, *args, **kwargs) -> Optional[Any]:
    """Decode data with a chosen decoder. Decoder must be registered, i.e. it
    must be listed with :func:`list_decoders`.

    :param data: Data to decode
    :param decoder: Name of a registered decoder
    :param args: Variable args for the decoder
    :param kwargs: Arbitrary keyword arguments for the decoder
    :return: Decoded data, None if data couldn't be decoded
    """
    if not decoder:
        return data

    if not _is_supported_decoder(decoder):
        raise ValueError(
            "Invalid decoder. Supported values: {}".format(
                list(supported_decoders.keys())
            )
        )

    return supported_decoders[decoder].run(data, *args, **kwargs)


def extract_patterns(data: str, extractor: str, *args, **kwargs) -> List[Any]:
    """Finds patterns in input data via selected extractor. The type of pattern is defined by the extractor used.
     The extractor must be registered, i.e. it must be listed with :func:`list_extractors`.

    :param data: Data in which to look for patterns
    :param extractor: Name of a registered extractor
    :param args: Variable args for the extractor
    :param kwargs: Arbitrary keyword arguments for the extractor
    :return: List of found patterns
    """
    if not _is_supported_extractor(extractor):
        raise ValueError(
            "Invalid extractor name. Supported values: {}".format(
                list(supported_extractors.keys())
            )
        )

    return list(supported_extractors[extractor].run(data, *args, **kwargs))


def analyze(
    _input: Union[FileInputExtended, BufferedIOBase, TextIOBase],
    decoders: List[Tuple[str, list, dict]],
    extractors: List[Tuple[str, list, dict]],
    per_line: bool = False,
) -> List[dict]:
    """Common function to apply multiple decoders and multiple extractors on the input.

    :param _input: File-like input (text or binary), see :func:`input_for_analysis` to create a suitable input.
    :param decoders: List of decoder (`decoder_name`, `decoder_args`, `decoder_kwargs`) to apply
    :param extractors: List of extractors (`extractor_name`, `extractor_args`, `extractor_kwargs`) to apply
    :param per_line: Flag whether to analyze input per line
    :return: List of dictionaries with the results for each input source
    """
    out = {}

    with cf.ProcessPoolExecutor() as e:
        for data in _read(_input, per_line):
            for dec in decoders:
                dec1, dec_args, dec_kwargs = dec
                decoded = decode(data, dec1, *dec_args, **dec_kwargs)
                patterns = {}
                if decoded:
                    future_extracted = {
                        e.submit(_extract_single, decoded, extractor): extractor[0]
                        for extractor in extractors
                    }
                    for future in cf.as_completed(future_extracted):
                        pattern_type = future_extracted[future]
                        try:
                            patterns[pattern_type] = future.result()
                        except:
                            patterns.setdefault(pattern_type, [])
                _add_patterns_to_out(_input.name, dec1, patterns, out)

    return list(out.values())


def input_for_analysis(
    value: Union[List[str], bytes, str], mode="r"
) -> Union[FileInputExtended, StringIO, BytesIO]:
    """Helper function to create an input for the :func:`analyze` function.
    Takes either a list of file paths, a string, or a byte string.

    :param value: Data to wrap in a suitable input object
    :param mode: Supports "r" (text), "rb" (binary) modes if input value is a list of file paths.
    :return: IO object wrapper for the input value
    """
    if isinstance(value, list):
        return FileInputExtended(value, mode=mode)
    if isinstance(value, str):
        return StringIO(value)
    return BytesIO(value)


def _extract_single(_data, _executor):
    ex_name, ex_args, ex_kwargs = _executor
    return extract_patterns(
        _data.decode("utf8") if isinstance(_data, bytes) else _data,
        ex_name,
        *ex_args,
        **ex_kwargs,
    )


def _read(_input: Union[FileInputExtended, BufferedIOBase], per_line: bool = False):
    if per_line:
        return _input
    if isinstance(_input, FileInputExtended):
        return _input.read()
    return (_input.read(),)


def _add_patterns_to_out(_source: str, _format: str, _patterns: dict, _out: dict):
    item = _out.setdefault(_source, {})
    item.setdefault("name", _source)
    item_formats = item.setdefault("formats", {})
    if not _patterns and _format not in item_formats:
        item_formats[_format] = None
        return
    item_formats[_format] = item_formats.get(_format) or {}
    for k, v in _patterns.items():
        item_formats[_format].setdefault("patterns", {}).setdefault(k, []).extend(v)
