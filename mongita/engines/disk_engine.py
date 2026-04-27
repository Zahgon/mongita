import collections
import itertools
import os
import pathlib
import shutil
import threading
from sys import intern as itrn

import bson

from ..common import MetaStorageObject, secure_filename
from .engine_common import Engine

DISK_ENGINE_INCUMBENTS = {}


class DiskEngine(Engine):
    def __init__(self, base_storage_path):
        if not os.path.exists(base_storage_path):
            os.mkdir(base_storage_path)
        self.base_storage_path = base_storage_path
        self._cache = collections.defaultdict(dict)
        self._collection_fhs = {}
        self._metadata = {}
        self._file_attrs = collections.defaultdict(dict)
        self.replaced = False
        self.lock = threading.RLock()

    @staticmethod
    def create(base_storage_path):
        pass

    def _get_full_path(self, collection, filename=''):
        pass

    def _get_coll_fh(self, collection):
        pass

    def _get_file_attrs(self, collection):
        pass

    def _set_file_attrs(self, collection, doc_id, pos):
        pass

    def doc_exists(self, collection, doc_id):
        pass

    def get_doc(self, collection, doc_id):
        pass

    def put_doc(self, collection, doc, no_overwrite=False):
        pass

    def delete_doc(self, collection, doc_id):
        pass

    def get_metadata(self, collection):
        pass

    # TODO disaster recovery rebuilds
    # def _rebuild_metadata(self, coll_path):
    #     fh = self._get_coll_fh(coll_path)
    #     pos = 0
    #     fh.seek(0)
    #     docs = []
    #     while True:
    #         doc_len_bytes = fh.read(4)
    #         if not doc_len_bytes:
    #             break
    #         doc_len = int.from_bytes(doc_len_bytes, 'little', signed=True)
    #         if not doc_len:
    #             continue
    #         doc = bson.decode(doc_len_bytes + fh.read(doc_len - 4))
    #         docs.append((pos, doc))
    #         pos += doc_len

    #     metadata = {}
    #     for pos, doc in docs:
    #         metadata['file_attrs'][doc['_id']] = pos
    #         self._cache[coll_path][doc['_id']] = doc
    #     self._metadata[coll_path] = metadata
    #     return metadata
    def _defrag(self, collection):
        pass

    def put_metadata(self, collection, metadata):
        pass

    def delete_dir(self, collection):
        pass

    def list_ids(self, collection, limit=None):
        pass

    def create_path(self, collection):
        pass

    def close(self):
        pass
