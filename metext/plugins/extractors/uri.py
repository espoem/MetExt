import re
from typing import Iterable, List, Union
from urllib.parse import unquote_plus

from metext.plugin_base import BaseExtractor
from metext.plugins.validators.uri import (
    DataURIValidator,
    MagnetValidator,
    URIValidator,
    URLValidator,
)
from metext.utils.regex import RE_URI, RE_URI_REFERENCE, RE_URL_FORM_FIELDS


class URIExtractor(BaseExtractor):
    PLUGIN_NAME = "uri"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts URIs from a string or a list of strings.

        See https://tools.ietf.org/html/rfc3986

        .. warning::
            This method does no filtering on specific schemes. Therefore, it may return
            lots of noise patterns.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword strict: Flag to reduce the number of results,
        if True then only path-like results with "/" path parts delimiter are returned.
        Defaults to False
        :keyword relative: Flag to allow URI relative references,
        otherwise some scheme must be present, default to False
        :keyword schemes: List of lower-cased schemes (e.g. http, data) URI must contain.
        If empty list (not provided), then URI is not restricted by a scheme,
        defaults to registered schemes
        :return: Generator of URIs
        """
        include_relative = kwargs.get("relative", False)
        strict = kwargs.get("strict", False)
        schemes = kwargs.get(
            "schemes", URI_SCHEMES
        )  # https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml
        regex = RE_URI_REFERENCE if include_relative else RE_URI
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                uri
                for uri in regex.findall(part)
                if URIValidator.run(uri, strict=strict, schemes=schemes)
            )


class URLExtractor(BaseExtractor):
    PLUGIN_NAME = "url"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts URLs from a string or a list of strings. URL must contain one of the following schemes:
        `http`, `https`, `ftp`, `ftps`

        See https://tools.ietf.org/html/rfc3986

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with URLs
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (uri for uri in RE_URI.findall(part) if URLValidator.run(uri))


class URNExtractor(BaseExtractor):
    PLUGIN_NAME = "urn"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts URNs from a string or a list of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with URNs
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from URIExtractor.run(part, schemes=["urn"], strict=False)


class DataURIExtractor(BaseExtractor):
    PLUGIN_NAME = "data_uri"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts valid data URIs from a string or a lists of strings.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :return: Generator with data URIs
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part:
                continue
            yield from (
                uri for uri in RE_URI.findall(part) if DataURIValidator.run(uri)
            )


class MagnetExtractor(BaseExtractor):
    PLUGIN_NAME = "magnet"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts MAC addresses

        :param _input: String or a list of strings to extract MAC address from
        :param kwargs: Arbitrary keyword arguments
        :return: Generator of MAC addresses
        """
        for part in _input if isinstance(_input, list) else _input.splitlines():
            if not part or not re.search(r"magnet:", part, re.IGNORECASE):
                continue
            uris = URIExtractor.run(part, schemes=["magnet"], strict=False)
            yield from (magnet for magnet in uris if MagnetValidator.run(magnet))


class FormFieldsExtractor(BaseExtractor):
    PLUGIN_NAME = "form_fields"

    @classmethod
    def run(cls, _input: Union[str, List[str]], **kwargs) -> Iterable[str]:
        """Extracts form fields data in HTTP, URL.

        :param _input: String or a list of strings
        :param kwargs: Arbitrary keyword arguments
        :keyword min_len: Minimum length of extracted pattern.
        Defaults to 20.
        :keyword decode: Flag to percent (URL) decode the found pattern. Defaults to True
        :return: Generator of form fields in decoded format
        """
        min_len = kwargs.get("min_len", 20)
        decode = kwargs.get("decode", True)
        for part in _input if isinstance(_input, list) else [_input]:
            for p in part.splitlines():
                if len(p) < min_len or "=" not in p:
                    continue
                res = (
                    unquote_plus(ff) if decode else ff
                    for ff in RE_URL_FORM_FIELDS.findall(p)
                    if not ("&" not in ff and ff.endswith("="))
                )
                yield from iter(res)


URI_SCHEMES = [
    "aaa",
    "aaas",
    "about",
    "acap",
    "acct",
    "acd",
    "acr",
    "adiumxtra",
    "adt",
    "afp",
    "afs",
    "aim",
    "amss",
    "android",
    "appdata",
    "apt",
    "ark",
    "attachment",
    "aw",
    "barion",
    "beshare",
    "bitcoin",
    "bitcoincash",
    "blob",
    "bolo",
    "browserext",
    "cabal",
    "calculator",
    "callto",
    "cap",
    "cast",
    "casts",
    "chrome",
    "chrome-extension",
    "cid",
    "coap",
    "coap+tcp",
    "coap+ws",
    "coaps",
    "coaps+tcp",
    "coaps+ws",
    "com-eventbrite-attendee",
    "content",
    "conti",
    "crid",
    "cvs",
    "dab",
    "dat",
    "data",
    "dav",
    "diaspora",
    "dict",
    "did",
    "dis",
    "dlna-playcontainer",
    "dlna-playsingle",
    "dns",
    "dntp",
    "doi",
    "dpp",
    "drm",
    "drop",
    "dtmi",
    "dtn",
    "dvb",
    "dweb",
    "ed2k",
    "elsi",
    "ens",
    "ethereum",
    "example",
    "facetime",
    "fax",
    "feed",
    "feedready",
    "file",
    "filesystem",
    "finger",
    "first-run-pen-experience",
    "fish",
    "fm",
    "ftp",
    "fuchsia-pkg",
    "geo",
    "gg",
    "git",
    "gizmoproject",
    "go",
    "gopher",
    "graph",
    "gtalk",
    "h323",
    "ham",
    "hcap",
    "hcp",
    "http",
    "https",
    "hxxp",
    "hxxps",
    "hydrazone",
    "hyper",
    "iax",
    "icap",
    "icon",
    "im",
    "imap",
    "info",
    "iotdisco",
    "ipfs",
    "ipn",
    "ipns",
    "ipp",
    "ipps",
    "irc",
    "irc6",
    "ircs",
    "iris",
    "iris.beep",
    "iris.lwz",
    "iris.xpc",
    "iris.xpcs",
    "isostore",
    "itms",
    "jabber",
    "jar",
    "jms",
    "keyparc",
    "lastfm",
    "lbry",
    "ldap",
    "ldaps",
    "leaptofrogans",
    "lorawan",
    "lvlt",
    "magnet",
    "mailserver",
    "mailto",
    "maps",
    "market",
    "matrix",
    "message",
    "microsoft.windows.camera",
    "microsoft.windows.camera.multipicker",
    "microsoft.windows.camera.picker",
    "mid",
    "mms",
    "modem",
    "mongodb",
    "moz",
    "ms-access",
    "ms-browser-extension",
    "ms-calculator",
    "ms-drive-to",
    "ms-enrollment",
    "ms-excel",
    "ms-eyecontrolspeech",
    "ms-gamebarservices",
    "ms-gamingoverlay",
    "ms-getoffice",
    "ms-help",
    "ms-infopath",
    "ms-inputapp",
    "ms-lockscreencomponent-config",
    "ms-media-stream-id",
    "ms-mixedrealitycapture",
    "ms-mobileplans",
    "ms-officeapp",
    "ms-people",
    "ms-project",
    "ms-powerpoint",
    "ms-publisher",
    "ms-restoretabcompanion",
    "ms-screenclip",
    "ms-screensketch",
    "ms-search",
    "ms-search-repair",
    "ms-secondary-screen-controller",
    "ms-secondary-screen-setup",
    "ms-settings",
    "ms-settings-airplanemode",
    "ms-settings-bluetooth",
    "ms-settings-camera",
    "ms-settings-cellular",
    "ms-settings-cloudstorage",
    "ms-settings-connectabledevices",
    "ms-settings-displays-topology",
    "ms-settings-emailandaccounts",
    "ms-settings-language",
    "ms-settings-location",
    "ms-settings-lock",
    "ms-settings-nfctransactions",
    "ms-settings-notifications",
    "ms-settings-power",
    "ms-settings-privacy",
    "ms-settings-proximity",
    "ms-settings-screenrotation",
    "ms-settings-wifi",
    "ms-settings-workplace",
    "ms-spd",
    "ms-sttoverlay",
    "ms-transit-to",
    "ms-useractivityset",
    "ms-virtualtouchpad",
    "ms-visio",
    "ms-walk-to",
    "ms-whiteboard",
    "ms-whiteboard-cmd",
    "ms-word",
    "msnim",
    "msrp",
    "msrps",
    "mss",
    "mtqp",
    "mumble",
    "mupdate",
    "mvn",
    "news",
    "nfs",
    "ni",
    "nih",
    "nntp",
    "notes",
    "num",
    "ocf",
    "oid",
    "onenote",
    "onenote-cmd",
    "opaquelocktoken",
    "openpgp4fpr",
    "otpauth",
    "pack",
    "palm",
    "paparazzi",
    "payment",
    "payto",
    "pkcs11",
    "platform",
    "pop",
    "pres",
    "prospero",
    "proxy",
    "pwid",
    "psyc",
    "pttp",
    "qb",
    "query",
    "quic-transport",
    "redis",
    "rediss",
    "reload",
    "res",
    "resource",
    "rmi",
    "rsync",
    "rtmfp",
    "rtmp",
    "rtsp",
    "rtsps",
    "rtspu",
    "secondlife",
    "secret-token",
    "service",
    "session",
    "sftp",
    "sgn",
    "shttp",
    "sieve",
    "simpleledger",
    "sip",
    "sips",
    "skype",
    "smb",
    "sms",
    "smtp",
    "snews",
    "snmp",
    "soap.beep",
    "soap.beeps",
    "soldat",
    "spiffe",
    "spotify",
    "ssb",
    "ssh",
    "steam",
    "stun",
    "stuns",
    "submit",
    "swh",
    "svn",
    "tag",
    "teamspeak",
    "tel",
    "teliaeid",
    "telnet",
    "tftp",
    "things",
    "thismessage",
    "tip",
    "tn3270",
    "tool",
    "turn",
    "turns",
    "tv",
    "udp",
    "unreal",
    "upt",
    "urn",
    "ut2004",
    "v-event",
    "vemmi",
    "ventrilo",
    "videotex",
    "vnc",
    "view-source",
    "vscode",
    "vscode-insiders",
    "vsls",
    "wais",
    "wcr",
    "webcal",
    "wifi",
    "wpid",
    "ws",
    "wss",
    "wtai",
    "wyciwyg",
    "xcon",
    "xcon-userid",
    "xfire",
    "xmlrpc.beep",
    "xmlrpc.beeps",
    "xmpp",
    "xri",
    "ymsgr",
    "z39.50",
    "z39.50r",
    "z39.50s",
]
