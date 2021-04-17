import bz2
import concurrent.futures as cf
import gzip
import io
import lzma
import os
import zipfile
from io import BufferedIOBase, BytesIO, StringIO, TextIOBase
from typing import Any, Callable, List, Optional, Tuple, Union

import brotli
from filetype import guess_mime

from metext import plugin_base
from metext.plugin_base import BaseDecoder, BaseExtractor, Decodable
from metext.plugins import load_plugin_modules
from metext.utils import convert_to_bytes, decode_bytes
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


def get_decoder(name) -> Optional[Callable]:
    """Get decoder execution function

    :param name: Decoder name
    :return: Decoding function
    """
    try:
        return supported_decoders.get(name).run
    except:
        return None


def get_extractor(name) -> Optional[Callable]:
    """Get extractor execution function

    :param name: Extractor name
    :return: Extracting function
    """
    try:
        return supported_extractors.get(name).run
    except:
        return None


def list_extractors() -> dict:
    """Gets a dict of registered extractors

    :return: Dict of registered extracting plugins
    """
    return supported_extractors


def _is_supported_decoder(decoder: str):
    return decoder in supported_decoders.keys()


def _is_supported_extractor(extractor: str):
    return extractor in supported_extractors.keys()


def decode(data: Decodable, decoder: str, **kwargs) -> Optional[Any]:
    """Decode data with a chosen decoder. Decoder must be registered, i.e. it
    must be listed with :func:`list_decoders`.

    :param data: Data to decode
    :param decoder: Name of a registered decoder
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

    return get_decoder(decoder)(data, **kwargs)


def extract_patterns(data: str, extractor: str, **kwargs) -> List[Any]:
    """Finds patterns in input data via selected extractor.
    The type of pattern is defined by the extractor used.
    The extractor must be registered, i.e. it must be listed with :func:`list_extractors`.

    :param data: Data in which to look for patterns
    :param extractor: Name of a registered extractor
    :param kwargs: Arbitrary keyword arguments for the extractor
    :return: List of found patterns
    """
    if not _is_supported_extractor(extractor):
        raise ValueError(
            "Invalid extractor name. Supported values: {}".format(
                list(supported_extractors.keys())
            )
        )

    return list(get_extractor(extractor)(data, **kwargs))


def analyze(
    _input: Union[FileInputExtended, BufferedIOBase, TextIOBase],
    decoders: List[Tuple[str, dict]],
    extractors: List[Tuple[str, dict]],
) -> List[dict]:
    """Common function to apply multiple decoders and multiple extractors on the input.
    Tries to decompress data first if recognized compression is applied.

    :param _input: File-like input (text or binary), see :func:`input_for_analysis` to create a suitable input.
    :param decoders: List of decoder (`decoder_name`, `decoder_args`, `decoder_kwargs`) to apply
    :param extractors: List of extractors (`extractor_name`, `extractor_args`, `extractor_kwargs`) to apply
    :return: List of dictionaries with the results for each input source
    """
    out = {}

    max_workers = max([min([len(extractors), os.cpu_count() - 1]), 1])
    with cf.ProcessPoolExecutor(max_workers=max_workers) as e:
        for data_read in _read(_input):
            for data in _try_decompress_to_data_list(data_read):
                for dec in decoders:
                    dec_name, dec_kwargs = dec
                    decoded = decode(data, dec_name, **dec_kwargs)
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
                    _add_patterns_to_out(_input.name, dec_name, patterns, out)

    return list(out.values())


def input_for_analysis(
    value: Union[List[str], bytes, str], mode="rb"
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
    ex_name, ex_kwargs = _executor
    return extract_patterns(
        _data if isinstance(_data, str) else decode_bytes(_data), ex_name, **ex_kwargs
    )


def _read(_input):
    if isinstance(_input, str):
        _input = StringIO(_input)
    elif isinstance(_input, (bytes, bytearray)):
        _input = BytesIO(_input)
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


def _try_decompress_to_data_list(data):
    data = convert_to_bytes(data)
    mime = guess_mime(data)
    try:
        if mime == "application/gzip":
            return [gzip.decompress(data)]
        if mime == "application/zip":
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                return [zf.read(f) for f in zf.infolist()]
        if mime == "application/x-brotli":
            return [brotli.decompress(data)]
        if mime == "application/x-bzip2":
            return [bz2.decompress(data)]
        if mime in ["application/x-lzip", "application/x-lzma", "application/x-xz"]:
            return [lzma.decompress(data)]
    except:
        return [data]

    return [data]
