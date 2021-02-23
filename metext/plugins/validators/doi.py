from metext.plugin_base import BaseValidator


class DoiValidator(BaseValidator):
    PLUGIN_NAME = "doi"

    @classmethod
    def run(cls, _input, **kwargs) -> bool:
        """Checks that the input string is a valid DOI identifier.

        Validating via <https://doi.org/api/handles/>

        :param _input: DOI to check (starts with "10.")
        :param kwargs:
        :return: True if input string is a resolvable DOI identifier,
        else False
        """
        import json
        import urllib.parse
        import urllib.request
        from urllib.error import HTTPError

        if not _input.startswith("10."):
            return False

        url = "https://doi.org/api/handles/{doi}".format(doi=_input)
        request = urllib.request.Request(url)

        try:
            result = json.loads(urllib.request.urlopen(request).read().decode())
        except HTTPError:
            raise ValueError("HTTP 404: DOI not found")

        return any(
            v["data"]["value"] for v in result["values"] if v.get("type") == "URL"
        )
