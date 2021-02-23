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


class TorfError(Exception):
    """Base exception for all exceptions raised by torf"""

    def __init__(self, msg, *posargs, **kwargs):
        super().__init__(msg)
        self.posargs = posargs
        self.kwargs = kwargs


class URLError(TorfError):
    """Invalid URL"""

    def __init__(self, url):
        self._url = url
        super().__init__("{url}: Invalid URL".format(url=url), url)

    @property
    def url(self):
        """The invalid URL"""
        return self._url


class MagnetError(TorfError):
    """Invalid magnet URI or value"""

    def __init__(self, uri, reason=None):
        self._uri = uri
        self._reason = reason
        if reason is not None:
            super().__init__(
                "{uri}: {reason}".format(uri=uri, reason=reason), uri, reason=reason
            )
        else:
            super().__init__("{uri}: Invalid magnet URI".format(uri=uri), uri)

    @property
    def uri(self):
        """The invalid URI"""
        return self._uri

    @property
    def reason(self):
        """Why URI is invalid"""
        return self._reason
