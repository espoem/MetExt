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

import abc
import collections
import contextlib
import math
import re
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import quote_plus as urlquote  # noqa: F401

from . import _errors as error


def is_power_of_2(num):
    """Return whether `num` is a power of two"""
    if num == 0:
        return False
    log = math.log2(abs(num))
    return int(log) == float(log)


def iterable_startswith(a, b):
    a_len = len(a)
    for i, b_item in enumerate(b):
        if i >= a_len:
            # a can't start with b if b is longer than a
            return False
        if a[i] != b_item:
            return False
    return True


def flatten(items):
    for item in items:
        if isinstance(item, Iterable):
            yield from flatten(item)
        else:
            yield item


_md5sum_regex = re.compile(r"^[0-9a-fA-F]{32}$")


class MonitoredList(collections.abc.MutableSequence):
    """List with change callback"""

    def __init__(self, items=(), callback=None, type=None):
        self._items = []
        self._type = type
        self._callback = callback
        with self._callback_disabled():
            self.replace(items)

    @contextlib.contextmanager
    def _callback_disabled(self):
        cb = self._callback
        self._callback = None
        yield
        self._callback = cb

    def __getitem__(self, index):
        return self._items[index]

    def __delitem__(self, index):
        del self._items[index]
        if self._callback is not None:
            self._callback(self)

    def _coerce(self, value):
        if self._type is not None:
            return self._type(value)
        return value

    def _filter_func(self, item):
        if item not in self._items:
            return item

    def __setitem__(self, index, value):
        if isinstance(value, Iterable):
            value = map(self._filter_func, map(self._coerce, value))
        else:
            value = self._filter_func(self._coerce(value))
        self._items[index] = value
        if self._callback is not None:
            self._callback(self)

    def insert(self, index, value):
        value = self._filter_func(self._coerce(value))
        if value is not None:
            self._items.insert(index, value)
        if self._callback is not None:
            self._callback(self)

    def replace(self, items):
        if not isinstance(items, Iterable):
            raise ValueError("Not an iterable: {items!r}".format(items=items))
        # Don't clear list before we know all new values are valid
        items = tuple(map(self._coerce, items))
        self._items.clear()
        with self._callback_disabled():
            self.extend(items)
        if self._callback is not None:
            self._callback(self)

    def clear(self):
        self._items.clear()
        if self._callback is not None:
            self._callback(self)

    def __len__(self):
        return len(self._items)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return frozenset(other._items) == frozenset(self._items)
        if isinstance(other, collections.abc.Iterable):
            return len(other) == len(self._items) and all(
                item in self._items for item in other
            )
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, type(self)):
            items = self._items + other._items
        elif isinstance(other, Iterable):
            items = self._items + list(other)
        else:
            items = self._items + [other]
        return type(self)(items, callback=self._callback)

    def __repr__(self):
        return repr(self._items)


def is_url(url):
    """Return whether `url` is a valid URL"""
    try:
        u = urllib.parse.urlparse(url)
        u.port  # Trigger 'invalid port' exception
    except Exception:
        return False
    else:
        return bool(u.scheme and u.netloc)


class URL(str):
    def __new__(cls, s):
        return super().__new__(cls, str(s).replace(" ", "+"))

    def __init__(self, url):
        if not is_url(url):
            raise error.URLError(url)
        else:
            self._parsed = urllib.parse.urlparse(url)

    @property
    def scheme(self):
        return self._parsed.scheme

    @property
    def netloc(self):
        return self._parsed.netloc

    @property
    def hostname(self):
        return self._parsed.hostname

    @property
    def port(self):
        return self._parsed.port

    @property
    def path(self):
        return self._parsed.path

    @property
    def params(self):
        return self._parsed.params

    @property
    def query(self):
        return self._parsed.query

    @property
    def fragment(self):
        return self._parsed.fragment


class URLs(MonitoredList):
    """Auto-flattening list of `:class:URL` objects with change callback"""

    def __init__(self, urls, callback=None, _get_known_urls=lambda: ()):
        self._get_known_urls = _get_known_urls
        if isinstance(urls, str):
            urls = () if not urls.strip() else (urls,)
        else:
            urls = flatten(urls)
        super().__init__(urls, callback=callback, type=URL)

    def _filter_func(self, url):
        # _get_known_urls is a hack for the Trackers class to deduplicate across
        # multiple tiers.
        if url not in self._items and url not in self._get_known_urls():
            return url


class Iterable(abc.ABC):
    """
    Iterable that is not a :class:`str`

    This allows you to write

        isinstance(x, Iterable)

    instead of

        isinstance(x, collections.abc.Iterable) and not isinstance(x, str)
    """

    @classmethod
    def __subclasshook__(cls, C):
        return (
            cls is Iterable
            and issubclass(C, collections.abc.Iterable)
            and not issubclass(C, str)
        )
