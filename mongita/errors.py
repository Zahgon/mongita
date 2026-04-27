class MongitaError(Exception):
    pass


class MongitaNotImplementedError(MongitaError, NotImplementedError):
    @staticmethod
    def create(cls, attr):
        pass

    @staticmethod
    def create_client(cls, attr):
        pass

    @staticmethod
    def create_depr(cls, attr):
        pass


class InvalidName(MongitaError):
    pass


class InvalidOperation(MongitaError):
    pass


class OperationFailure(MongitaError):
    pass


class DuplicateKeyError(MongitaError):
    pass


# For pymongo compatibility - especially in unit tests
PyMongoError = MongitaError
