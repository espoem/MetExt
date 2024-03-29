# This file is part of torf.
#
# torf is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# torf is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with torf.  If not, see <https://www.gnu.org/licenses/>.

import re
import urllib
from collections import abc, defaultdict

from . import _errors as error
from . import _utils as utils


class Magnet:
    """
    BTIH Magnet URI

    :param str xt: eXact Topic: Info hash (Base 16 or 32)
    :param str dn: Display Name: Name of the torrent
    :param int xl: eXact Length: Size in bytes
    :param list tr: TRacker: Iterable of tracker URLs
    :param str xs: eXact Source: Torrent file URL
    :param str as\\_: Acceptable Source: Fallback torrent file URL
    :param list ws: WebSeeds: Iterable of webseed URLs (see BEP19)
    :param list kt: Keyword Topic: List of search keywords

    All keyword arguments that start with ``x_`` go into the :attr:`x`
    dictionary with the part after the underscore as the key.  They appear as
    "x.<name>" in the rendered URI.

    References:
        | https://www.bittorrent.org/beps/bep_0009.html
        | https://en.wikipedia.org/wiki/Magnet_URL
        | http://magnet-uri.sourceforge.net/magnet-draft-overview.txt
        | https://wiki.theory.org/index.php/BitTorrent_Magnet-URI_Webseeding
        | http://shareaza.sourceforge.net/mediawiki/index.php/Magnet_URI_scheme
    """

    _INFOHASH_REGEX = re.compile(
        r"^[0-9a-f]{40}|[a-z2-7]{32}|1220[a-f0-9]{64}$", flags=re.IGNORECASE
    )
    _XT_REGEX = re.compile(
        r"^(?:urn:btih:([0-9a-f]{40}|[a-z2-7]{32})|urn:btmh:1220[a-f0-9]{64})$",
        flags=re.IGNORECASE,
    )

    def __init__(
        self,
        xt,
        *,
        dn=None,
        xl=None,
        tr=None,
        xs=None,
        as_=None,
        ws=None,
        kt=None,
        **kwargs
    ):
        self._tr = utils.MonitoredList(type=utils.URL)
        self._ws = utils.MonitoredList(type=utils.URL)
        self.xt = xt
        self.dn = dn
        self.xl = xl
        self.tr = tr
        self.xs = xs
        self.as_ = as_
        self.ws = ws
        self.kt = kt

        self._x = defaultdict(lambda: None)
        for key in tuple(kwargs):
            if key.startswith("x_"):
                self._x[key[2:]] = kwargs.pop(key)

        if kwargs:
            key, value = next(iter(kwargs.items()))
            raise TypeError(
                "Unrecognized argument: {key}={value!r}".format(key=key, value=value)
            )

    @property
    def dn(self):
        """Display Name: Name of the torrent or ``None``"""
        return self._dn

    @dn.setter
    def dn(self, value):
        self._dn = str(value).replace("\n", " ") if value is not None else None

    @property
    def xt(self):
        """
        eXact Topic: URN containing the info hash as base 16 or base 32

        Example:

            urn:btih:3bb9561e35b06175bb6d2c2330578dc83846cc5d

        For convenience, this property may be set to the info hash without the
        ``urn:btih`` part.

        :raises MagnetError: if set to an invalid value
        """
        return "urn:btih:{}".format(self._infohash)

    @xt.setter
    def xt(self, value):
        value = str(value)
        if self._INFOHASH_REGEX.match(value):
            self._infohash = value
        else:
            match = self._XT_REGEX.match(value)
            if match:
                self._infohash = match.group(1)
        if not hasattr(self, "_infohash"):
            raise error.MagnetError(value, 'Invalid exact topic ("xt")')

    @property
    def infohash(self):
        """
        Info hash as base 16 or base 32

        :raises MagnetError: if set to an invalid value
        """
        return self._infohash

    @infohash.setter
    def infohash(self, value):
        value = str(value)
        match = self._INFOHASH_REGEX.match(value)
        if match:
            self._infohash = value
        else:
            raise error.MagnetError(value, "Invalid info hash")

    @property
    def xl(self):
        """
        eXact Length: Size in bytes or ``None``

        :raises MagnetError: if set to an invalid value
        """
        return self._xl

    @xl.setter
    def xl(self, value):
        if value is not None:
            try:
                value = int(value)
            except ValueError:
                raise error.MagnetError(value, 'Invalid exact length ("xl")')
            else:
                if value < 1:
                    raise error.MagnetError(value, "Must be 1 or larger")
                self._xl = value
        else:
            self._xl = None

    @property
    def tr(self):
        """
        TRackers: List of tracker URLs, single tracker URL or ``None``

        :raises URLError: if any of the URLs is invalid
        """
        return self._tr

    @tr.setter
    def tr(self, value):
        if value is None:
            self._tr.clear()
        elif isinstance(value, str):
            self._tr.replace((value,))
        else:
            self._tr.replace(value)

    @property
    def xs(self):
        """
        eXact Source: Torrent file URL or ``None``

        :raises URLError: if the URL is invalid
        """
        return self._xs

    @xs.setter
    def xs(self, value):
        self._xs = utils.URL(value) if value is not None else None

    @property
    def as_(self):
        """
        Acceptable Source: Fallback torrent file URL or ``None``

        (The trailing underscore is needed because "as" is a keyword in Python.)

        :raises URLError: if the URL is invalid
        """
        return self._as

    @as_.setter
    def as_(self, value):
        self._as = utils.URL(value) if value is not None else None

    @property
    def ws(self):
        """
        WebSeeds: List of webseed URLs, single webseed URL or ``None``

        See BEP19.

        :raises URLError: if any of the URLs is invalid
        """
        return self._ws

    @ws.setter
    def ws(self, value):
        if value is None:
            self._ws.clear()
        elif isinstance(value, str):
            self._ws.replace((value,))
        else:
            self._ws.replace(value)

    @property
    def kt(self):
        """Keyword Topic: List of search keywords or ``None``"""
        return self._kt

    @kt.setter
    def kt(self, value):
        if value is None:
            self._kt = []
        elif isinstance(value, str):
            self._kt = [value]
        elif isinstance(value, abc.Iterable):
            self._kt = [str(v) for v in value] if value is not None else None
        else:
            raise error.MagnetError(value, 'Invalid keyword topic ("kt")')

    @property
    def x(self):
        """
        Mapping of custom keys to their values

        For example, "x.pe" (a peer address) would be accessed as
        ``magnet.x['pe']``.
        """
        return self._x

    _KNOWN_PARAMETERS = ("xt", "dn", "xl", "tr", "xs", "as", "ws", "kt")

    @classmethod
    def from_string(cls, uri):
        """
        Create :class:`Magnet` URI from string

        :raises URLError: if `uri` contains an invalid URL (e.g. :attr:`tr`)
        :raises MagnetError: if `uri` is not a valid magnet URI
        """
        info = urllib.parse.urlparse(
            uri.strip(), scheme="magnet", allow_fragments=False
        )
        if info.scheme != "magnet":
            raise error.MagnetError(uri, "Not a magnet URI")
        query = urllib.parse.parse_qs(info.query)

        # Check for unknown parameters
        for key in query:
            if key not in cls._KNOWN_PARAMETERS and not key.startswith("x_"):
                raise error.MagnetError(uri, "{key}: Unknown parameter".format(key=key))

        if "xt" not in query:
            raise error.MagnetError(uri, 'Missing exact topic ("xt")')
        # if len(query["xt"]) > 1:
        #     raise error.MagnetError(uri, 'Multiple exact topics ("xt")')
        self = cls(xt=query["xt"][0])

        # Parameters that accept only one value
        for param, attr, name, parse in (
            ("dn", "dn", "display name", lambda v: v),
            ("xl", "xl", "exact length", lambda v: v),
            ("xs", "xs", "exact source", lambda v: v),
            ("as", "as_", "acceptable source", lambda v: v),
            ("kt", "kt", "keyword topic", lambda v: v.split()),
        ):
            if param in query:
                if len(query[param]) > 1:
                    raise error.MagnetError(
                        uri,
                        'Multiple {name}s ("{param}")'.format(name=name, param=param),
                    )
                setattr(self, attr, parse(query[param][0]))

        # Parameters that accept multiple values
        for param, name in (("tr", "tracker"), ("ws", "webseed")):
            if param in query:
                setattr(self, param, query[param])

        return self

    def __str__(self):
        uri = ["magnet:?xt={}".format(self.xt)]

        for key in ("dn", "xl", "xs", "as_"):
            value = getattr(self, str(key))
            if value is not None:
                if isinstance(value, str):
                    uri.append("{}={}".format(key, utils.urlquote(value)))
                else:
                    uri.append("{key}={value}".format(key=key, value=value))

        if self.kt:
            uri.append("kt={}".format("+".join(utils.urlquote(k) for k in self.kt)))

        for key in ("tr", "ws"):
            seq = getattr(self, str(key))
            if seq is not None:
                for item in seq:
                    uri.append("{}={}".format(key, utils.urlquote(item)))

        for key, value in self._x.items():
            uri.append("x.{}={}".format(key, utils.urlquote(value)))

        return "&".join(uri)

    def __repr__(self):
        clsname = type(self).__name__
        kwargs = {}
        for param in self._KNOWN_PARAMETERS:
            if param == "as":
                param = "as_"
            value = getattr(self, param)
            if value:
                kwargs[param] = value
        for k, v in self.x.items():
            kwargs["x_{k}".format(k=k)] = v
        kwargs_str = ", ".join("{}={}".format(k, repr(v)) for k, v in kwargs.items())
        return "{clsname}({kwargs_str})".format(clsname=clsname, kwargs_str=kwargs_str)
