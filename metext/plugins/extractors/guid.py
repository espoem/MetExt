import re
import uuid
from typing import Iterable

from metext.plugin_base import BaseExtractor
from metext.plugins.extractors import _extract_with_regex
from metext.utils.regex import RE_GUID


class UuidExtractor(BaseExtractor):
    PLUGIN_NAME = "uuid"

    @classmethod
    def run(cls, _input: str, **kwargs) -> Iterable[dict]:
        """Extracts GUIDs strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of GUID strings
        """

        def validate(uuid, **kwargs):
            uuid = uuid.replace("-", "")
            return bool(re.match(r"[0-5]", uuid[12], re.IGNORECASE))

        def get_info(uuid_):
            try:
                res = uuid.UUID(uuid_)
                return {"variant": res.variant, "version": res.version}
            except:
                return None

        def normalize(uuid, **kwargs):
            uuid = uuid.replace(r"-", "").lower()
            return "{}-{}-{}-{}-{}".format(
                uuid[:8], uuid[8:12], uuid[12:16], uuid[16:20], uuid[20:]
            )

        for obj in _extract_with_regex(
            _input,
            RE_GUID,
            per_line=True,
            data_kind=cls.PLUGIN_NAME,
            validator=validate,
            postprocess=normalize,
        ):
            info = get_info(obj["value"])
            if info:
                if info["version"] is None:
                    continue
                obj.update({"info": info})
            yield obj
