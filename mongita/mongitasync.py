import pymongo
from . import mongita_client


def _resolve_client(connection_type, uri):
    """
    :param str connection_type:
    :param str uri:
    :rtype: mongita.MongitaClientDisk|pymongo.MongoClient
    """
    pass


def _resolve_collections(collections):
    """
    Split a list of raw collections into a list of database/collection tuples

    :param list[str] collections:
    :rtype: list[(str, str|None)]
    """
    pass


def _batch_docs(cursor, cnt=1000):
    """
    Batch a generator of documents into lists of length cnt

    :param generator[dict] cursor:
    :param int cnt:
    :rtype: generator[list[dict]]
    """
    pass


def _confirm_loop(msg, logger):
    """
    Confirm in a loop that the user wants to do the thing.
    Returns a tuple of (yes/no, yesall)

    :param str msg:
    :param Logger logger:
    :rtype: (bool, bool)
    """
    pass


def _replace_collection(source, dest, database, collection, force, logger):
    """
    Replace a single collection at destination with the source's collection.
    Returns whether we want to 'force' going forward

    :param MongoClient|MongitaClientDisk source:
    :param MongoClient|MongitaClientDisk dest:
    :param str database:
    :param str collection:
    :param bool force:
    :param Logger logger:
    :rtype: bool
    """
    pass


class _Logger():
    def __init__(self, quiet):
        self.quiet = quiet

    def log(self, msg, *args):
        pass


def mongitasync(source_type, destination_type, collections, force=False,
                source_uri=None, destination_uri=None, quiet=False):
    """
    Sync a list of collections from the source to the destination.
    Source/destination can be either 'mongita' or 'mongodb'
    Collections can be formatted as either 'db.coll' or plain 'db'

    :param str source_type: mongita|mongodb
    :param str destination_type: mongita|mongodb
    :param list[str]|str collections:
    :param bool force:
    :param str source_uri:
    :param str destination_uri:
    :param bool quiet:
    """
    pass
