import functools
import os
import re
import unicodedata

import bson
import sortedcontainers

from .errors import MongitaError

ASCENDING = 1
DESCENDING = -1


_windows_device_files = ('CON', 'AUX', 'COM1', 'COM2', 'COM3', 'COM4', 'LPT1',
                         'LPT2', 'LPT3', 'PRN', 'NUL')
_filename_ascii_strip_re = re.compile(r'[^A-Za-z0-9_.-]')
_invalid_names = re.compile(r'[/\. "$*<>:|?]')


def secure_filename(filename: str) -> str:
    """
    The idea of this is to ensure that the document_id doesn't do sketchy shit on
    the filesystem. This will probably be deleted soon.
    """
    pass


def ok_name(name):
    """
    In-line with MongoDB restrictions.
    https://docs.mongodb.com/manual/reference/limits/#std-label-restrictions-on-db-names
    https://docs.mongodb.com/manual/reference/limits/#Restriction-on-Collection-Names
    The prohibition on "system." names will be covered by the prohibition on '.'
    """
    pass


def support_alert(func):
    """
    Provide smart tips if the user tries to use un-implemented / deprecated
    known kwargs.
    """
    @functools.wraps(func)
    def inner(*args, **kwargs):
        pass
    pass


class MetaStorageObject(dict):
    """
    Subclass of the StorageObject with some extra handling for metadata.
    Specifically, indexes need extra steps to fully encode / decode.
    """

    def __init__(self, doc):
        super().__init__(doc)

    def to_storage(self, as_bson=False):
        """
        Makes sure that the SortedDict indexes are bson-compatible
        """
        pass

    @staticmethod
    def from_storage(obj, from_bson=False):
        pass

    def decode_indexes(self):
        """
        Changes the encoded indexes to SortedDicts
        """
        pass
