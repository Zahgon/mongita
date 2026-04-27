from .errors import MongitaNotImplementedError, MongitaError, InvalidOperation
from .common import ASCENDING, DESCENDING, support_alert


def _validate_sort(key_or_list, direction=None):
    """
    Validate kwargs and return a proper sort list

    :param key_or_list str|[(str key, int direction), ...]
    :param direction int:
    :rtype: [(str key, int direction), ...]
    """
    pass


class Cursor():
    UNIMPLEMENTED = ['add_option', 'address', 'alive', 'allow_disk_use', 'batch_size',
                     'collation', 'collection', 'comment', 'cursor_id', 'distinct',
                     'explain', 'hint', 'max', 'max_await_time_ms',
                     'max_time_ms', 'min', 'remove_option', 'retrieved', 'rewind',
                     'session', 'where']
    DEPRECATED = ['count', 'max_scan']

    def __init__(self, _find, filter, sort, limit, skip):
        self._find = _find
        self._filter = filter
        self._sort = sort or []
        self._limit = limit or None
        self._skip = skip or None
        self._cursor = None

    def __getattr__(self, attr):
        if attr in self.DEPRECATED:
            raise MongitaNotImplementedError.create_depr("Collection", attr)
        if attr in self.UNIMPLEMENTED:
            raise MongitaNotImplementedError.create("Cursor", attr)
        raise AttributeError()

    def __getitem__(self, val):
        pass

    def __iter__(self):
        for el in self._gen():
            yield el

    def __next__(self):
        return next(self._gen())

    def _gen(self):
        """
        This exists so that we can maintain our position in the cursor and
        to not execute until we start requesting items
        """
        pass

    @support_alert
    def next(self):
        """
        Returns the next document in the Cursor. Raises StopIteration if there
        are no more documents.

        :rtype: dict
        """
        pass

    @support_alert
    def sort(self, key_or_list, direction=None):
        """
        Apply a sort to the cursor. Sorts have no impact until retrieving the
        first document from the cursor. If not sorting against indexes, sort can
        negatively impact performance.
        This returns the same cursor to allow for chaining. Only the last sort
        is applied.

        :param key_or_list str|[(key, direction)]:
        :param direction mongita.ASCENDING|mongita.DESCENDING:
        :rtype: cursor.Cursor
        """
        pass

    @support_alert
    def limit(self, limit):
        """
        Apply a limit to the number of elements returned from the cursor.
        This returns the same cursor to allow for chaining. Only the last limit
        is applied.

        :param limit int:
        :rtype: cursor.Cursor
        """
        pass

    @support_alert
    def skip(self, skip):
        """
        Skip the first [skip] results of this cursor.
        """
        pass

    @support_alert
    def clone(self):
        pass

    @support_alert
    def close(self):
        """
        Close this cursor to free the memory
        """
        pass
