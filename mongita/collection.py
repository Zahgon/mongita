import collections
import copy
import datetime
import functools
import re

import bson
import sortedcontainers

from .cursor import Cursor, _validate_sort
from .common import support_alert, ASCENDING, DESCENDING, MetaStorageObject
from .errors import (MongitaError, MongitaNotImplementedError, DuplicateKeyError,
                     InvalidName, OperationFailure)
from .read_concern import ReadConcern
from .results import InsertOneResult, InsertManyResult, DeleteResult, UpdateResult
from .write_concern import WriteConcern


_SUPPORTED_FILTER_OPERATORS = ('$in', '$eq', '$gt', '$gte', '$lt', '$lte', '$ne', '$nin')
_SUPPORTED_UPDATE_OPERATORS = ('$set', '$inc', '$push')
_DEFAULT_METADATA = {
    'options': {},
    'indexes': {},
    '_id': str(bson.ObjectId()),
}


# FROM docs.mongodb.com/manual/reference/bson-type-comparison-order/#comparison-sort-order
SORT_ORDER = {
    int: b'\x02',
    float: b'\x02',
    str: b'\x03',
    object: b'\x04',
    list: b'\x05',
    bytes: b'\x06',
    bson.ObjectId: b'\x07',
    bool: b'\x08',
    datetime.datetime: b'\t',
    re.Pattern: b'\n',
}


def _validate_filter(filter):
    """
    Validate the 'filter' parameter.
    This is near the top of most public methods.

    :param filter dict:
    :rtype: None
    """
    pass


def _validate_update(update):
    """
    Validate the 'update' parameter.
    This is near the top of the public update methods.

    :param update dict:
    :rtype: None
    """
    pass


def _validate_doc(doc):
    """
    Validate the 'doc' parameter.
    This is near the top of the public insert / replace methods.

    :param doc dict:
    :rtype: None
    """
    pass


def _overlap(iter_a, iter_b):
    """
    Return if there is any overlap between iter_a and iter_b
    from https://stackoverflow.com/questions/3170055

    :param iter_a list:
    :param iter_b list:
    :rtype: bool
    """
    pass


def _doc_matches_agg(doc_v, query_ops):
    """
    Return whether an individual document value matches a dict of
    query operations. Usually there will be one query_op but sometimes there
    are many.

    e.g. collection.find({'path.to.doc_v': {'$query_op': query_val}})

    The loop returns False whenever we know for sure that the document is
    not part of the query. At the end return True

    :param doc_v: The value in the doc to compare against
    :param query_ops {$query_op: query_val}:
    :returns: Whether the document value matches all query operators
    :rtype: bool
    """
    pass


def _doc_matches_slow_filters(doc, slow_filters):
    """
    Given an entire doc, return whether that doc matches every filter item in the
    slow_filters dict. A slow_filter is just the set of filters that we didn't
    have an index for.

    :param doc dict:
    :param slow_filters dict:
    :rtype: bool
    """
    pass


def _ids_given_irange_filters(matched_keys, idx, **kwargs):
    """
    Given an existing set of matched_keys, a SortedDict (idx), and
    a set of kwargs to apply to SortedDict.irange,
    return all keys that match both the irange and the existing matched_keys

    :param matched_keys set:
    :param idx sortedcontainers.SortedDict:
    :param kwargs dict: irange filters
    :rtype set:
    """
    pass


def _idx_filter_sort(query_op_tup):
    """
    For performance, the order of filtering matters. It's best to do
    equality first before comparsion. Not-equal should be last becase a lot
    of values are liable to be returned.
    In and nin vary in how much they matter so go with not-equal

    :param query_op_tup (query_op, query_val):
    :rtype: bool
    """
    pass


def _get_ids_from_idx(idx, query_ops):
    """
    Returns the ids that match a set of query_ops in an index.

    :param idx SortedDict:
    :param query_ops str|dict:
    :rtype: set
    """
    pass


def _failed_update_error(update_op, update_op_dict, doc, msg):
    """Helper for raising errors on update"""
    pass


def _update_item_in_doc(update_op, update_op_dict, doc):
    """
    Given an $update_op, a {doc_key: value} update_op_dict, and a doc,
    Update the doc in-place at doc_key with the update operation.

    e.g.
    doc = {'hi': 'ma'}
    update_op = '$set'
    update_op_dict {'ma': 'pa'}
    -> {'hi': 'pa'}

    :param update_op str:
    :param update_op_dict {str: value}:
    :param doc dict:
    :rtype: None
    """
    pass
        # Should never get an update key we don't recognize b/c _validate_update


def _rightpad(item, desired_length):
    """
    Given a list, pad to the desired_length with Nones
    This might be slow but it modifies the list in place

    :param item list:
    :param desired_length int:
    :rtype: None
    """
    pass


def _get_datastructure_from_doc(doc, key):
    """
    Get a pass-by-reference data structure from the document so that we can
    update it in-place. This dives deep into the document with the key
    parameter which uses dot notation.

    e.g.
    doc = {'deep': {'nested': {'list': [1, 2, 3]}}}
    key = 'deep.nested.list.5'
    -> a reference to [1, 2, 3, None, None] and 5

    :param doc dict:
    :param key str:
    :returns: the datastructure and the final accessor
    :rtype: list|dict|None, value
    """
    pass


def _get_item_from_doc(doc, key):
    """
    Get an item from the document given a key which might use dot notation.

    e.g.
    doc = {'deep': {'nested': {'list': ['a', 'b', 'c']}}}
    key = 'deep.nested.list.1'
    -> 'b'

    :param doc dict:
    :param key str:
    :rtype: value
    """
    pass


def _make_idx_key(idx_key):
    """
    MongoDB is very liberal when it comes to what keys it can compare on.
    When we get something weird, it makes sense to just store it as a
    hashable key

    :param idx_key value:
    :rtype: hashable value
    """
    pass


def _update_idx_doc_with_new_documents(documents, idx_doc):
    """
    Update an idx_doc given documents which were just inserted / modified / etc

    :param documents list[dict]:
    :param idx_doc {key_str: str, direction: int idx: SortedDict, ...}:
    :rtype: None
    """
    pass


def _remove_docs_from_idx_doc(doc_ids, idx_doc):
    """
    Update an idx_doc given documents which were just removed

    :param doc_ids set[str]:
    :param idx_doc {key_str: str, direction: int idx: SortedDict, ...}:
    :rtype: None
    """
    pass


def _sort_tup(item):
    """
    Get sort tuple of item type according to mongodb rules

    :param item Value:
    :rtype: (int, Value)
    """
    pass


def _sort_func(doc, sort_key):
    """
    Sorter to sort different types according to MongoDB rules

    :param doc dict:
    :param sort_key str:
    :rtype: tuple
    """
    pass


def _sort_docs(docs, sort_list):
    """
    Given the sort list provided in the .sort() method,
    sort the documents in place.

    from https://docs.python.org/3/howto/sorting.html

    :param docs list[dict]:
    :param sort_list list[(key, direction)]
    :rtype: None
    """
    pass
        # validation on direction happens in cursor


def _split_filter(filter, metadata):
    """
    Split the filter into indx_ops and slow_filters which are later used
    differently

    :param filter {doc_key: query_ops}:
    :param metadata dict:
    :rtype: {doc_key: query_ops}, [(SortedDict idx, dict query_ops), ...]
    """
    pass


def _apply_indx_ops(indx_ops):
    """
    Return all doc_ids that can be found through the index filters

    :param indx_ops {idx_key: query_ops}:
    :param indexes dict:
    :rtype: set
    """
    pass


class Collection():
    UNIMPLEMENTED = ['aggregate', 'aggregate_raw_batches', 'bulk_write', 'codec_options',
                     'create_indexes', 'drop', 'drop_indexes', 'ensure_index',
                     'estimated_document_count', 'find_one_and_delete',
                     'find_one_and_replace', 'find_one_and_update', 'find_raw_batches',
                     'inline_map_reduce', 'list_indexes', 'map_reduce', 'next',
                     'options', 'read_concern', 'read_preference', 'rename', 'watch', ]
    DEPRECATED = ['reindex', 'parallel_scan', 'initialize_unordered_bulk_op',
                  'initialize_ordered_bulk_op', 'group', 'count', 'insert', 'save',
                  'update', 'remove', 'find_and_modify', 'ensure_index']

    def __init__(self, collection_name, database, write_concern=None, read_concern=None):
        self.name = collection_name
        self.database = database
        self._write_concern = write_concern or WriteConcern()
        self._read_concern = read_concern or ReadConcern()
        self._engine = database._engine
        self._existence_verified = False
        self._base_location = f'{database.name}.{collection_name}'

    def __repr__(self):
        return "Collection(%s, %r)" % (repr(self.database), self.name)

    def __getattr__(self, attr):
        """
        First check for deprecated / unimplemented.
        Then, MongoDB has this weird thing where there can be dots in a collection
        name.
        """
        if attr in self.DEPRECATED:
            raise MongitaNotImplementedError.create_depr("Collection", attr)
        if attr in self.UNIMPLEMENTED:
            raise MongitaNotImplementedError.create("Collection", attr)
        return Collection(collection_name=self.name + '.' + attr,
                          database=self.database)

    @property
    def full_name(self):
        pass

    @property
    def write_concern(self):
        pass

    @property
    def read_concern(self):
        pass

    def with_options(self, **kwargs):
        pass

    def __create(self):
        """
        MongoDB doesn't require you to explicitly create collections. They
        are created when first accessed. This creates the collection and is
        called early in modifier methods.
        """
        pass

    def __insert_one(self, document):
        """
        Insert a single document.

        :param document dict:
        :rtype: None
        """
        pass

    @support_alert
    def insert_one(self, document):
        """
        Insert a single document.

        :param document dict:
        :rtype: results.InsertOneResult
        """
        pass

    @support_alert
    def insert_many(self, documents, ordered=True):
        """
        Insert documents. If ordered, stop inserting if there is an error.
        If not ordered, all operations are attempted

        :param list documents:
        :param bool ordered:
        :rtype: results.InsertManyResult
        """
        pass

    @support_alert
    def replace_one(self, filter, replacement, upsert=False):
        """
        Replace one document. If no document was found with the filter,
        and upsert is True, insert the replacement.

        :param filter dict:
        :param replacement dict:
        :param bool upsert:
        :rtype: results.UpdateResult
        """
        pass

    def __find_one_id(self, filter, sort=None, skip=None, upsert=False):
        """
        Given the filter, return a single object_id or None.

        :param filter dict:
        :param sort list[(key, direction)]|None
        :param skip int|None
        :rtype: str|None
        """
        pass

    def __find_one(self, filter, sort, skip):
        """
        Given the filter, return a single doc or None.

        :param filter dict:
        :param sort list[(key, direction)]|None
        :param skip int|None
        :rtype: dict|None
        """
        pass

    def __find_ids(self, filter, sort=None, limit=None, skip=None, metadata=None):
        """
        Given a filter, find all doc_ids that match this filter.
        Be sure to also sort and limit them.
        This method will download documents for non-indexed filters (slow_filters).
        Downloaded docs are cached in the engine layer so performance cost is minimal.
        This method returns a generator

        :param filter dict:
        :param sort list[(key, direction)]|None:
        :param limit int|None:
        :param skip int|None:
        :param metadata dict|None:
        :rtype: Generator(list[str])
        """
        pass

    def __find(self, filter, sort=None, limit=None, skip=None, metadata=None, shallow=False):
        """
        Given a filter, find all docs that match this filter.
        This method returns a generator.

        :param filter dict:
        :param sort list[(key, direction)]|None:
        :param limit int|None:
        :param skip int|None:
        :param metadata dict|None:
        :rtype: Generator(list[dict])
        """
        pass

    @support_alert
    def find_one(self, filter=None, sort=None, skip=None):
        """
        Return the first matching document.

        :param filter dict:
        :param sort list[(key, direction)]|None:
        :param skip int|None:
        :rtype: dict|None
        """
        pass

    @support_alert
    def find(self, filter=None, sort=None, limit=None, skip=None):
        """
        Return a cursor of all matching documents.

        :param filter dict:
        :param sort list[(key, direction)]|None:
        :param limit int|None:
        :param skip int|None:
        :rtype: cursor.Cursor
        """
        pass

    def __update_doc(self, doc_id, update):
        """
        Given a doc_id and an update dict, find the document and safely update it.
        Returns the updated document

        :param doc_id str:
        :param update dict:
        :rtype: dict
        """
        pass

    @support_alert
    def update_one(self, filter, update, upsert=False):
        """
        Find one document matching the filter and update it.
        The 'upsert' parameter is not supported.

        :param filter dict:
        :param update dict:
        :param upsert bool:
        :rtype: results.UpdateResult
        """
        pass

    @support_alert
    def update_many(self, filter, update, upsert=False):
        """
        Update every document matched by the filter.
        The 'upsert' parameter is not supported.

        :param filter dict:
        :param update dict:
        :param upsert bool:
        :rtype: results.UpdateResult
        """
        pass

    @support_alert
    def delete_one(self, filter):
        """
        Delete one document matching the filter.

        :param filter dict:
        :rtype: results.DeleteResult
        """
        pass

    @support_alert
    def delete_many(self, filter):
        """
        Delete all documents matching the filter.

        :param filter dict:
        :rtype: results.DeleteResult
        """
        pass

    @support_alert
    def count_documents(self, filter):
        """
        Returns a count of all documents matching the filter.
        This can be much faster than taking the length of a find query.

        :param filter dict:
        :rtype: int
        """
        pass

    @support_alert
    def distinct(self, key, filter=None):
        """
        Given a key, return all distinct documents matching the key

        :param key str:
        :param filter dict|None:
        :rtype: list[str]
        """
        pass

    def __get_metadata(self):
        """
        Thin wrapper to get metadata.
        Always be sure to lock the engine when modifying metadata

        :rtype: dict
        """
        pass

    def __update_indicies_deletes(self, doc_ids, metadata):
        """
        Given a list of deleted document ids, remove those documents from all indexes.
        Returns the new metadata dictionary.

        :param doc_ids set[str]:
        :param metadata dict:
        :rtype: dict
        """
        pass

    def __update_indicies(self, documents, metadata):
        """
        Given a list of deleted document ids, add those documents to all indexes.
        Returns the new metadata dictionary.

        :param documents list[dict]:
        :param metadata dict:
        :rtype: dict
        """
        pass

    @support_alert
    def create_index(self, keys, background=False):
        """
        Create a new index for the collection.
        Indexes can dramatically speed up queries that use its fields.
        Currently, only single key indicies are supported.
        Returns the name of the new index.

        :param keys str|[(key, direction)]:
        :param background bool:
        :rtype: str
        """
        pass

    @support_alert
    def drop_index(self, index_or_name):
        """
        Drops the index given by the index_or_name parameter. Passing index
        objects is not supported

        :param index_or_name str|(str, int)
        :rtype: None
        """
        pass

    @support_alert
    def index_information(self):
        """
        Returns a list of indexes in the collection

        :rtype: {idx_id: {'key': [(key_str, direction_int)]}}
        """
        pass
