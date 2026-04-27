import collections
import itertools
import threading
from sys import intern as itrn

import bson

from ..common import MetaStorageObject
from .engine_common import Engine


class MemoryEngine(Engine):
    def __init__(self, strict=False):
        self._strict = strict
        self._cache = collections.defaultdict(dict)
        self._metadata = {}
        self.lock = threading.RLock()

    @staticmethod
    def create(strict=False):
        pass

    def put_doc(self, collection, doc, no_overwrite=False):
        pass

    def get_doc(self, collection, doc_id):
        pass

    def doc_exists(self, collection, doc_id):
        pass

    def list_ids(self, collection, limit=None):
        pass

    def delete_doc(self, collection, doc_id):
        pass

    def delete_dir(self, collection):
        pass

    def put_metadata(self, collection, doc):
        pass

    def get_metadata(self, collection):
        pass

    def create_path(self, collection):
        pass

    def close(self):
        pass
